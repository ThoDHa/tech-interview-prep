# The Interview Method

The hardest moment in a system design round is the open prompt: "Design Twitter." Forty-five minutes, a whiteboard, and no constraints. This guide replaces that moment with a repeatable 6-step method, the design-round sibling of [How to Approach a Problem](../foundations/how_to_approach.md). None of the steps require brilliance. They are a checklist you run every time, and the interesting design conversation emerges while running it.

## The time budget

For a standard 45-minute round, budget roughly:

| Step | Time | Running total |
|------|------|---------------|
| 1. Clarify requirements | 5 min | 5 |
| 2. Back-of-envelope estimation | 5 min | 10 |
| 3. API and data model sketch | 5 min | 15 |
| 4. High-level architecture | 10 min | 25 |
| 5. Deep dives (interviewer-driven) | 15 min | 40 |
| 6. Wrap-up | 5 min | 45 |

The budget is a guide, not a law. If the interviewer pulls you into a deep dive at minute 12, follow them: the budget's real job is to stop you from spending 25 minutes on step 1 or reaching minute 40 with no architecture on the board.

## The method

### 1. Clarify functional and non-functional requirements

Never start drawing. Start asking. Split your questions into two lists and write both on the board, because everything later refers back to them.

**Functional requirements** are what the system does. For "design a chat app": one-on-one messages? Group chats? Read receipts? Media attachments? Pick the 3 or 4 core features *with the interviewer* and explicitly park the rest: "I'll treat typing indicators as out of scope unless you want them."

**Non-functional requirements** are the qualities that shape the architecture: scale (users, requests), latency targets, availability, consistency needs, durability. These, not the features, determine most of your design.

What to say:

> "Before I design anything, let me pin down scope. For features, I'll focus on X, Y, Z and leave W out unless you disagree. For scale, are we talking about 100 thousand users or 100 million? And is this read-heavy or write-heavy?"

A useful closing move for this step: state the read/write ratio out loud. "So this is roughly 100 reads per write" is one sentence that will justify half your later decisions.

### 2. Back-of-envelope estimation

Turn the agreed scale into numbers: QPS (average and peak), storage growth, and bandwidth. The arithmetic itself is covered in [Back-of-Envelope Estimation](estimation.md); in the interview, the point is to do it *out loud*, rounding aggressively.

What to say:

> "100 million DAU, each reading their feed 5 times a day: that's 500 million reads a day, and a day is about 10^5 seconds, so roughly 5,000 reads per second on average, call it 15,000 at peak. Writes are maybe a hundredth of that. So this is a read-dominated system and caching will matter more than write throughput."

Notice the shape: numbers, then a *conclusion*. Estimation that does not change your design was wasted breath.

### 3. API and data model sketch

Define the system's contract before its internals. A handful of endpoints and the core entities are enough:

```
POST /messages          {to, text}        -> {message_id, timestamp}
GET  /conversations/:id/messages?before=  -> [messages], cursor

Message:  id, conversation_id, sender_id, text, created_at
Conversation:  id, participant_ids, last_message_at
```

Keep it minimal. You are not writing an OpenAPI spec; you are making sure you and the interviewer agree on what goes in and out, and you are surfacing the entities you will later have to store, shard, and cache. This is also the natural place to note the primary access pattern ("messages are always fetched by conversation, newest first"), because that pattern picks your database indexes and partition keys in step 5.

Four API-design practices each deserve one sentence in the sketch, and not more than that: step 3 has five minutes, and the sketch, not a spec, is the deliverable.

- **Versioning.** Put `/v1/` in the paths from the start. Contracts change,
  and a version prefix turns the first breaking change into a new path instead of a coordinated migration.
- **REST vs RPC.** Resource-oriented REST is the shared vocabulary of these
  interviews and fits most systems; move to RPC-style method calls when the operation is an action rather than a thing ("join conversation"), which is why real systems usually mix both.
- **Error contracts.** Return structured errors with status codes the
  client can act on (400 for validation, 401/403 for auth, 429 with `Retry-After` for rate limiting), never a 200 with an error string in the body. The [rate limiter case study](case_studies/rate_limiter.md) works out a full rejection contract.
- **Idempotency keys.** For any write a client might retry, require a
  client-generated key (`client_msg_id` in the [chat case study](case_studies/chat_system.md)) so the retry is a no-op instead of a duplicate. It is the same idempotency contract the message queues section demands of consumers, pushed out to the API edge.

For list endpoints, prefer cursor pagination over page numbers; the `?before=` cursor in the sketch above is its minimal form, and the [news feed case study](case_studies/news_feed.md) explains why cursors beat offsets.

### 4. High-level architecture

Now draw. Start with the simplest thing that satisfies the requirements and the numbers from step 2, and narrate the life of a request through it:

```
client -> load balancer -> app servers -> cache
                                       -> database
                                       -> queue -> async workers
```

Rules for this step:

- **Boxes earn their place.** Every component you draw, you should be able
  to justify with a requirement or a number. A queue because writes spike; a cache because the read ratio is 100:1. Never add a box because "real systems have one."
- **Trace one read and one write end to end.** This catches missing pieces
  faster than staring at the diagram.
- **Say what you are deferring.** "I'm drawing the database as one box for
  now; sharding it is a deep dive if you want to go there." This shows control, and it hands the interviewer a menu for step 5.

### 5. Targeted deep dives, driven by the interviewer

This is the highest-signal part of the round, and the part you control least. The interviewer picks a box and pushes: "What happens when this database can't handle the writes?" "How do two devices see the same conversation state?"

How to handle it:

- **Follow their lead.** If they ask about the cache, do not detour into
  your prepared sharding speech. Steering candidates back is tiring, and it is graded.
- **Offer a menu if they don't steer.** "The interesting problems here are
  feed fan-out, storage sharding, and the online-presence system. Which would you like to dig into?" This is far better than picking silently.
- **Go tradeoff-first.** The pattern for any deep dive answer: state the
  problem, give 2 options, name what each costs, pick one *for this workload*, and say what breaks it. The [Building Blocks](building_blocks.md) page exists to make those options available on demand.
- **Use your numbers.** "At 5,000 QPS a single Postgres primary is fine; at
  500,000 it is not, so I'd shard by conversation_id" is the sound of steps 2 and 5 connecting.

### 6. Wrap-up: bottlenecks, failure modes, evolution

With five minutes left, zoom back out and volunteer the weaknesses before being asked:

- **Bottlenecks:** "The first thing to fall over under 10x load is the
  fan-out workers; I'd move celebrity accounts to fan-out-on-read."
- **Failure modes:** "If the cache cluster dies, the database takes the full
  read load and will not survive it; I'd want request coalescing and load shedding in front."
- **Evolution:** "V1 ships without the queue; when write volume justifies
  it, the API layer already isolates the change."

Criticizing your own design is not weakness. It signals you know the difference between a whiteboard and production, and it usually earns the best minute of the interview.

## Pitfalls

### Diving into detail too early

The classic failure: the candidate hears "chat app" and is drawing WebSocket connection pools by minute three, having never asked how many users there are. Detail before requirements is detail about the wrong system. If you notice yourself designing before step 1 is done, stop and ask a question.

### Ignoring the interviewer's steering

Interviewers redirect for a reason: either the topic is on their rubric or you are stuck in a rut. Treat every interruption as a gift, not an obstacle. The candidate who says "good question, let's follow that" and pivots cleanly outperforms the one who says "I'll get to that" and returns to their script.

### Hand-waving the numbers

"We'll cache it, so it'll be fast" and "we'll shard the database" are empty without magnitudes. If you claim a cache helps, say what the hit rate would need to be and roughly how much memory the hot set takes. Wrong-but-reasoned numbers score better than none: the estimation page exists so that your numbers are at least the right order of magnitude.

### Designing for scale nobody asked for

If the interviewer agreed on 50,000 users, a multi-region active-active deployment with a consensus layer is not impressive, it is a red flag: you are showing you cannot match the solution to the problem. Build the simple version, then say what you would change at 100x. Premature scale is the design-round version of optimizing before profiling.

## When you are stuck

- Return to the requirements list on the board. Unhandled requirements are
  a to-do list in disguise.
- Trace a single request end to end and narrate it. Gaps announce
  themselves.
- Say what you are unsure about, out loud, and reason from first
  principles: "I don't remember Kafka's exact guarantees, but what I need here is at-least-once delivery with ordering per conversation, so let me design to that." Honest reasoning beats confident trivia.

The goal of practice is not to memorize four architectures. It is to make these six steps automatic, so an unfamiliar prompt becomes a familiar process.
