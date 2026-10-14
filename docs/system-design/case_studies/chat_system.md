# Case Study: Chat System

"Design WhatsApp" introduces everything the first three studies could avoid: long-lived stateful connections, real-time delivery, ordering, offline devices, and presence. It is the study where "the server calls the client" for the first time, and that inversion drives most of the design. A scaffolded workthrough of the [6-step method](../method.md); attempt each collapsed answer first.

## Step 1: Requirements

**Functional:**

- One-on-one messaging, delivered in near real time when both users are
  online.
- Delivery states: sent, delivered, read.
- Offline delivery: messages wait, and a push notification goes out.
- Message history: a device can fetch older messages; a new device can
  sync a conversation.
- Online presence (online / last seen). Group chat: agree to defer it
  (extension checklist); small groups change less than you'd think, huge groups change everything.

**Non-functional:**

- Scale: 50 million DAU, ~10 million concurrently connected at peak.
- Latency: message delivery should feel instant when online: a few
  hundred ms end to end.
- Ordering: within one conversation, both participants see the same order.
  No global cross-conversation ordering is needed (say this; it is a huge relaxation).
- Durability: an acknowledged message is never lost. Availability: per
  CAP, during trouble prefer accepting messages over rejecting them.

## Step 2: Estimation

**Prompt A: Message write QPS, assuming each DAU sends 40 messages/day.**

??? note "Answer"
    50M × 40 = 2 × 10^9 messages/day ≈ 24,000/s average, ~60,000/s peak.

    Each message also triggers a delivery to (usually) one recipient plus receipts flowing back, so total event throughput is a small multiple of that: order 10^5/s at peak.

    Conclusion: comfortably beyond one database primary; the message store is sharded from day one, and the natural key is conversation_id (deep dive 2 depends on this).

**Prompt B: What does holding 10 million concurrent WebSocket connections cost, and how many gateway servers is that?**

??? note "Answer"
    A mostly-idle connection costs kernel + userspace state on the order of 10 KB: 10^7 × 10 KB ≈ 100 GB of memory fleet-wide, which is nothing. Connections are cheap to *hold*; the limits are file descriptors, event-loop wakeups, and blast radius per node.

    At a conservative ~100,000 connections per node, 10M concurrent needs ~100 gateway nodes (plus headroom, so ~150).

    Conclusion: the connection layer is its own horizontally-scaled tier, and "which gateway is user X connected to right now?" becomes a first-class routing problem (deep dive 1).

**Prompt C: Message storage per year, text only.**

??? note "Answer"
    ~100 B of text + ~100 B of ids, timestamps, and state flags ≈ 200 B per message.

    2 × 10^9/day × 200 B = 400 GB/day × 365 ≈ 150 TB/year before replication, ~450 TB with 3x.

    Conclusion: modest per-message, huge in aggregate, append-only, always queried by conversation and recency: a textbook fit for a wide-column store partitioned by conversation_id and clustered by message id descending.

## Step 3: API and data model

```
Over the WebSocket (both directions):
  client -> server:  send    {conv_id, client_msg_id, text}
  server -> client:  deliver {conv_id, msg_id, seq, sender, text}
                     receipt {conv_id, msg_id, state: delivered|read}

HTTP (non-realtime):
  GET /conversations/:id/messages?before_seq=...   history & sync

Message:      conv_id (partition), seq, msg_id, sender_id, text,
              created_at, state
Conversation: id, participant_ids, last_seq, last_activity
Session:      user_id -> {gateway_id, device_ids}    (the routing table)
Inbox/undelivered: user_id -> [msg refs]             (offline queue)
```

`client_msg_id` is generated on the phone and makes sends idempotent: the client retries over flaky mobile networks, and the server dedupes. Chat is the one prompt where idempotency appears in the *API*, not just inside the backend, because the client is a participant in the reliability story.

## Step 4: High-level architecture

```
 sender's phone                              recipient's phone
      │  websocket                                ▲  websocket
      ▼                                           │
 ┌──────────┐    ┌─────────────┐    ┌──────────┐
 │ gateway A │──▶│ chat service │──▶│ gateway B │   (session registry
 └──────────┘    │              │    └──────────┘    says B holds the
                 │  1 persist   │                    recipient)
                 │  2 assign seq│    ┌─────────────┐
                 │  3 route     │──▶│ push service │  (recipient offline:
                 └──────┬──────┘    │ (APNs/FCM)   │   notify instead)
                        ▼           └─────────────┘
              ┌──────────────────┐
              │ message store    │   ┌──────────────────┐
              │ (sharded by      │   │ session registry │
              │  conversation)   │   │ user -> gateway  │
              └──────────────────┘   └──────────────────┘
```

Life of a message: sender's gateway forwards to the chat service, which (1) persists the message, (2) assigns it the next sequence number in the conversation, (3) acks "sent" back to the sender, then looks up the recipient in the session registry and pushes via their gateway (online) or hands off to the push-notification service (offline). Receipts travel the same pipes in reverse.

Persist *before* delivering: durability first means a crash after the ack can delay a message but never lose one. State that ordering explicitly; interviewers listen for it.

## Step 5: Deep dives

### 1. The connection layer and message routing

- Gateways hold WebSockets and do nothing else: no business logic, just
  auth, heartbeats, and pipes. Keeping them dumb makes the stateful tier the *simplest* tier, which is the only way running 150 of them is sane.
- The session registry (Redis: `user_id -> gateway_id`, TTL refreshed by
  heartbeat) is how anyone finds anyone. Sending a message is: look up recipient's gateway, RPC to it, it writes to the socket.
- Gateway death drops ~100k connections at once: clients reconnect with
  jittered backoff (a reconnect stampede is a self-inflicted [thundering herd](../building_blocks.md#caching)), land on other gateways, re-register, and run sync (deep dive 3) to fill any gap. Design the failure path as the normal path: phones roam and drop connections constantly anyway.

### 2. Ordering: who assigns the sequence?

- Requirement was per-conversation ordering only, so the answer is a
  per-conversation sequence number, assigned at persist time by the shard that owns the conversation. Sharding by conversation_id means one owner per conversation: no coordination, no consensus, just an atomic increment on the owning shard.
- Why not client timestamps? Phone clocks skew by minutes. Why not server
  arrival time? Two gateways racing can interleave differently than either participant observed. A single authoritative sequencer per conversation is the cheapest thing that makes both phones agree.
- Devices render by `seq`, and a gap in `seq` is a *detectable* signal
  that a fetch is needed: ordering and reliability come from the same mechanism, which is what makes this design elegant enough to say out loud.

### 3. Delivery states, offline devices, and sync

- State machine per message: **sent** (persisted, acked to sender),
  **delivered** (recipient device acked receipt), **read** (recipient opened the conversation). Each transition is itself a tiny message flowing back through the same pipeline; nothing new is needed.
- Offline recipients: the message sits in the store; an undelivered
  marker goes to their inbox; the push service sends a notification. On reconnect, the device says "conversation X, I have up to seq 41" and the server returns 42 onward: **cursor-based sync, per device**, because a user's phone and laptop have different cursors.
- At-least-once everywhere, so duplicates happen (retries, reconnects):
  `client_msg_id` dedupes on the write side, `(conv_id, seq)` dedupes on the read side. Idempotency is not a patch here; it is the design.

### 4. Presence without melting

- Naive presence is a fan-out bomb: every connect/disconnect broadcast to
  every contact is (events × contacts) traffic, and flaky mobile radios generate events constantly.
- Standard mitigations, in order: heartbeat with a lazy timeout (offline
  means "no heartbeat for 30s", so brief blips never publish), debounce transitions (only publish a state stable for ~10s), and prefer *pull* ("fetch presence for the 20 conversations on screen") over push for everyone but the currently-open conversation.
- Presence is also the one part of the system where data *loss* is
  totally fine: it is rebuilt by the next heartbeat. Saying "this table can live in Redis with TTLs and no durability, unlike messages" shows you are matching guarantees to data, which is the round's core skill.

## Step 6: Wrap-up

- **Bottleneck:** the chat service's persist-and-route path at 10^5
  events/s; it scales horizontally because conversations are independent, but the session registry is a shared dependency to watch.
- **Failure modes:** gateway loss (reconnect + sync, rehearsed above),
  session registry staleness (message routed to a gateway the user left: fall back to offline delivery, which is why offline is the *default* path, not the exception), push provider outage (messages still sync; only the nudge is lost).
- **Evolution:** v1 is long-polling against one database and it works for
  a small user base; WebSockets, sharding, and the registry arrive with scale. E2E encryption is the deepest change: the server loses the ability to read what it stores, which touches search, spam filtering, and multi-device sync all at once.

## Extend this scaffold

- [ ] **Group chat**: at 3 participants nothing changes; at 500, sending
  becomes a small [fan-out](news_feed.md) problem: where does the per-recipient work happen, and does `seq` survive?
- [ ] **End-to-end encryption**: key exchange, multi-device key
  distribution, and which server features (search, previews) you must give up.
- [ ] **Media messages**: presigned upload to
  [object storage](../building_blocks.md#object-storage), thumbnails in the message payload, CDN delivery.
- [ ] **Typing indicators**: ephemeral, loss-tolerant, high-frequency:
  design the cheapest possible path and defend never persisting it.
- [ ] **Multi-region**: users in Europe and Asia sharing a conversation;
  where does the conversation's sequencer live, and what latency does physics impose?
- [ ] **Message search**: an index over 150 TB/year that respects
  conversation privacy boundaries.
