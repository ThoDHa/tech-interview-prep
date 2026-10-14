# System Design: Start Here

The coding rounds test whether you can solve a well-defined problem. The system design round tests something different: whether you can take a vague, open-ended prompt ("design a chat app") and turn it into a concrete architecture through a series of *reasoned tradeoffs*. There is no single correct answer, and the interviewer is not checking whether you know a specific technology. They are watching how you think when nothing is given.

This section is a **scaffold, not a finished course**. It gives you a repeatable method, the arithmetic to size a system out loud, the vocabulary of standard components, and guided case studies with deliberate gaps for you to fill. Expect it to grow: the case study roadmap lists designs that are planned but not yet written.

## What the round actually tests

- **Tradeoff reasoning, not trivia.** "SQL or NoSQL?" is never the question.
  "What does this workload need, and what are you willing to give up to get it?" always is. Saying "Cassandra" earns nothing; explaining *why* write-heavy, partition-friendly data tolerates eventual consistency earns a lot.
- **Structured thinking under ambiguity.** The prompt is vague on purpose.
  Strong candidates narrow it with questions before drawing anything.
- **Quantitative sanity.** You will be expected to estimate load and storage
  with rough numbers and to notice when a design cannot possibly handle the math you just did.
- **Communication.** The round is a conversation. Interviewers steer, and
  following their steering is graded.

## Which of the four design interviews this trains

"System design" names four different interview formats, and preparing for the wrong one is the quietest way to waste a prep weekend:

- **Back end / distributed system design.** Architecture across servers and
  datacenters: databases, caching, queues, replication, consistency, fault tolerance. This is the format everything in this section trains: the method, the estimation material, the building blocks, and the case studies are all aimed at it.
- **API design.** The system's contracts: endpoints, versioning, error
  handling, idempotency. Our coverage is the transferable core, collected in [step 3 of the method](method.md#3-api-and-data-model-sketch) rather than as its own track.
- **Object-oriented design.** Classes, relationships, interfaces, and
  patterns in the small: parking lots, elevators, chess. Different canon, different prep; NeetCode's free [OOD course](https://neetcode.io/courses) is the starting point, not this section.
- **Front end system design.** Client application and UI component
  architecture, out of scope for a LeetCode-based repo; [GreatFrontEnd's Front End System Design Playbook](https://www.greatfrontend.com/front-end-system-design-playbook) covers it properly.

If your loop is the OOD or front end format instead, treat this section as background vocabulary and prepare from the pointers above.

## How this section is organized

| Guide | What it gives you | Read it when |
|-------|-------------------|--------------|
| [The Interview Method](method.md) | A repeatable 6-step framework with a time budget for a 45-minute round | First: everything else plugs into it |
| [Back-of-Envelope Estimation](estimation.md) | Latency numbers, powers of two, QPS and storage arithmetic, worked examples | Second: step 2 of the method depends on it |
| [Building Blocks](building_blocks.md) | The component vocabulary: load balancers, caches, databases, queues, and the rest | Third, or as a reference while doing case studies |
| [Case Studies](case_studies/index.md) | Five guided workthroughs (URL shortener, rate limiter, news feed, chat, web crawler) with answers hidden behind collapsible blocks | Last: this is where the method becomes muscle memory |

## A suggested study path

1. Read [The Interview Method](method.md) and internalize the 6 steps
   (about 1 hour).
2. Work through [Back-of-Envelope Estimation](estimation.md) with a pen.
   Redo the worked examples yourself before opening the traces (2 to 3 hours, mostly practice).
3. Read [Building Blocks](building_blocks.md) once end to end, then treat it
   as a reference (2 to 3 hours).
4. Do the five [case studies](case_studies/index.md) *actively*: attempt each
   prompt yourself before opening the collapsed answers, and finish the "extend this scaffold" checklist for at least one of them (2 to 3 hours each, so 10 to 15 hours total).
5. Repeat a case study cold a week later, out loud, with a 45-minute timer.
   Talking through a design is a different skill from reading one.

That is roughly 15 to 22 hours for a solid baseline. Senior-level depth comes from extending the scaffolds and from reading about real systems, not from rereading these pages.

## How this complements the DSA sections

The [How to Approach a Problem](../foundations/how_to_approach.md) guide is this section's sibling: both replace blank-page panic with a checklist. The mindset transfers directly. In a coding round you restate the problem, walk examples, write the brute force, then optimize. In a design round you clarify requirements, estimate, sketch the simple architecture, then deepen it where the numbers or the interviewer demand. In both cases the first version is deliberately simple, and the improvement is justified by identified cost, not by reflex.

The DSA knowledge also shows up directly: hash-based sharding is [hashing](../patterns/hashing/intuition.md) at datacenter scale, an LRU cache is a Grind75 problem *and* a production component, and rate limiters are sliding windows over time instead of arrays.

## Seniority expectations, honestly

Interviewers calibrate the same prompt differently by level. Knowing the bar keeps you from over- or under-preparing.

| Level | What passes | What is not yet expected |
|-------|-------------|--------------------------|
| Junior / new grad | A reasonable set of components wired together sensibly: a load balancer, app servers, a database, a cache, with correct data flow and honest estimation | Deep failure analysis, exotic components, defending consistency choices under fire |
| Mid-level | All of the above, plus correct choices *with reasons*: why this partition key, why a queue here, what breaks first under 10x load | Designing for problems the interviewer has not raised |
| Senior / staff | Deep tradeoffs and failure handling: what happens when the cache dies, how the system degrades, migration paths, consistency guarantees stated precisely, and pushing back on requirements when they conflict | Nothing is off the table; the interviewer will probe until they find the edge of your knowledge, which is normal |

At every level, the fastest way to fail is the same: silence, hand-waved numbers, or ignoring the interviewer's steering. The method exists to prevent all three.

## This section is growing

The five case studies are scaffolded workthroughs with intentional gaps, and the [roadmap](case_studies/index.md#roadmap-case-studies-not-yet-written) lists classics that are not yet written. If a topic you need is missing, the building blocks page plus the method are usually enough to attempt it yourself, which is better practice anyway.

## Further resources

This scaffold covers the method and the core vocabulary; when you want more depth, a second explanation, or a last-minute revision pass, these are the sources worth your time:

- [System Design in a Hurry](https://www.hellointerview.com/learn/system-design/in-a-hurry/introduction)
  (Hello Interview): the strongest free primer, covering delivery, high-level concepts, and core technologies, with worked versions of the classic questions. Use it to check our case studies against another treatment of the same problem.
- [System Design Primer](https://github.com/donnemartin/system-design-primer):
  the most comprehensive free reference. Too long to read linearly under time pressure; treat it as an encyclopedia.
- *System Design Interview: An Insider's Guide, Second Edition* by Alex Xu
  ([Amazon](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)): the standard book, beginner friendly, with step-by-step deep dives of famous systems.
- [System Design Cheatsheet](https://gist.github.com/vasanthk/485d1c25737e8e72759f)
  (vasanthk's gist): brief and dense, positioned exactly where this section has a gap: the revision pass the day before the interview.
- [System Design Roadmap](https://roadmap.sh/system-design): a step-by-step
  topic checklist with links, useful for auditing what you have and have not covered.

---

*The interview-type taxonomy and the canonical question framing follow the [Tech Interview Handbook's system design guide](https://www.techinterviewhandbook.org/system-design/); all explanations, the method, the estimation material, and the case studies are original to this project.*
