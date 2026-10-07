# Gaps filled from the All-in-One Exam Guide

These are things the book flags as exam-critical that the objective list alone does not spell out. Nothing here is deep theory. It is the extra vocabulary and the handful of traps that cost points.

### How CompTIA words things (traps)

| CompTIA says | It means | Why it matters |
| --- | --- | --- |
| Phases | The five PMI process groups: initiating, planning, executing, monitoring and controlling, closing | Questions ask "which phase" for things like stakeholder identification (initiation) or EVM (monitoring and controlling) |
| Waterfall | Predictive, plan-driven | Treat the two words as the same thing |
| Agile / adaptive | Iterative, change-welcoming | Adaptive projects do *not* use a scope statement, WBS, network diagram or formal change control. They use a product backlog, product roadmap and reprioritization instead. |
| Projects vs operations | Temporary and unique vs ongoing and repetitive | Expect at least one question that asks you to tell them apart |

**Question tactics the book stresses:** read for "except" and "not"; when two answers look right, the scenario contains a clue (phase, methodology, who is asking) that picks one; answer every question (blank = wrong); first instinct is usually right; about 72 of 90 correct passes.

### Activities by phase (know what happens where)

| Phase | Core activities |
| --- | --- |
| Initiating | Create the charter, identify stakeholders |
| Planning | Project management plan, scope statement, WBS, activity list and sequence, estimates, schedule, budget, quality plan, resource plan, communications plan, risk plan and register, procurement plan, stakeholder engagement plan |
| Executing | Direct the work, manage quality, acquire and develop the team, manage communications, implement risk responses, conduct procurements, manage stakeholder engagement |
| Monitoring and controlling | Integrated change control, validate scope, control scope/schedule/cost, quality control, EVM, monitor risks, administer procurements |
| Closing | Close the project or phase, formal acceptance, close contracts, release resources, archive, lessons learned |

### Estimating

| Estimate type | When | Accuracy |
| --- | --- | --- |
| Rough order of magnitude (ROM) | Initiating, top-down | Least accurate (about −25% to +75%) |
| Budget estimate | Early planning, scope approved, top-down | Moderate (about −10% to +25%) |
| Definitive estimate | Late planning, built from the WBS, bottom-up | Most accurate (about −5% to +10%), slowest to create |

- **Analogous** needs historical data from a similar project. No history means no analogous estimate.
- **Bottom-up** from the WBS (predictive) or the product backlog (agile) is the most accurate.
- If a question is stuck between options and one of them is the WBS, lean toward the WBS.
- **Effort-driven** activities get faster with more people. **Fixed-duration** activities (software install, curing, a waiting period) do not.

### Cost types

| Type | Definition | Example |
| --- | --- | --- |
| Direct | Charged only to this project | Team travel, equipment leased for this project |
| Indirect | Cost of doing business, shared | Rent, utilities, phone |
| Fixed | Constant regardless of usage | Monthly equipment rental |
| Variable | Changes with quantity | Catering per attendee, licenses per user |
| Cost of conformance | Money spent to get quality right: training, testing, standards | Prevention and appraisal |
| Cost of nonconformance | Cost of failure: rework, downtime, lost sales, waste | Internal and external failure |

### Quality: assurance vs control

- **Quality assurance (QA):** planning to do the work right the first time. Process-focused, done in executing.
- **Quality control (QC):** inspecting the results to confirm they meet requirements. Product-focused, done in monitoring and controlling.
- You cannot inspect quality into a product. The team doing the work has the largest effect on quality.
- Quality = conformance to requirements plus fitness for use. The final test of quality is customer acceptance (validation).
- In agile, QC happens every iteration through the sprint demo.
- Also know: **Kaizen** (continuous small improvements), **just-in-time** (low inventory, needs high quality), and **flowcharts** (process steps).

### People and power

| PM power type | Source |
| --- | --- |
| Formal / legitimate / positional | Assigned by senior management (the charter) |
| Reward | Ability to give bonuses, recognition, good assignments |
| Coercive / penalty | Ability to discipline. Team works out of fear. |
| Expert | The PM's own knowledge of the subject |
| Referent | Team likes the PM, or the PM references someone powerful ("the CEO wants this") |

No power type is "best". Pick the one that fits the situation.

| Motivation theory | One-line version |
| --- | --- |
| Maslow's hierarchy | Physiological, safety, social, esteem, self-actualization, in that order |
| Herzberg | Hygiene factors (pay, safety, job security) only prevent dissatisfaction. Motivators (recognition, responsibility, growth) drive performance. |
| McGregor X and Y | Theory X: people are lazy and need micromanagement. Theory Y: people are self-motivated. |
| Ouchi Theory Z | Participative management, commitment and long-term opportunity motivate |
| McClelland | Needs for achievement, affiliation and power, shaped by experience |
| Vroom expectancy | People work in proportion to the reward they expect |

Other team terms: **virtual / non-collocated teams** (remote, need extra communication effort), **emotional intelligence** (self-awareness and self-control), **project champion** (informal cheerleader, may or may not be the sponsor), **huddle** (quick daily team meeting), **information radiator** (agile status posted publicly), **war room / project information center**.

### Scope, requirements and selection

- **Product scope** = features of the deliverable. **Project scope** = the work to produce it.
- **Scope verification / validate scope** = formal customer acceptance of deliverables at the end of each phase or project.
- **MoSCoW** prioritization: Must have, Should have, Could have, Would be nice (won't this time). Used for backlog requirements.
- **Constraints** limit options: time, cost, scope, plus quality, security rules, resource availability.
- Projects are selected by **benefit measurement** methods (scoring models, cost-benefit ratio, economic models). Constrained optimization (math models) is rarely the answer.
- **Delphi technique:** rounds of anonymous surveys to reach consensus, used for risk identification and estimates.

### Schedule and risk extras

- **GERT** (Graphical Evaluation and Review Technique) is a network diagram with branches and loops. Agile projects use a **product roadmap** instead of a network diagram.
- **Resource leveling** can push the finish date. **Resource smoothing** keeps the date and works within float.
- **Schedule baseline:** when events change the schedule, version the baseline so you keep the history of why the project ran long.
- **Business risk** has upside and downside (time and money). **Pure risk** has only downside (injury, theft, loss of life).
- **Utility function:** a person's or organization's willingness to accept risk.
- Risk goes in the **risk register**. Issues go in the **issue log**. An issue is a risk that happened.
- **Burn rate:** in a predictive project, how fast money is spent. In agile, how fast stories are completed. Read the context.

### Change and release extras

- **Integrated change control:** examining how a change affects *every* part of the project (scope, time, cost, quality, risk, resources).
- **Regression plan** = **fallback plan** = **rollback plan**: steps to return to the last known good state. Staging is where you prove the change before production.
- Adaptive projects welcome change and reprioritize the backlog instead of running a change control process.
- Never bring management a problem without a proposed solution.

### Procurement extras

- Normal order: write the **SOW**, then issue an **RFQ, RFP or invitation to bid**. A quote and a bid give a price. A proposal gives ideas plus a price.
- A **bidders' conference** lets all sellers ask questions fairly.
- A **purchase order** is a unilateral contract. A **letter of intent** is not a contract.
- Procurement questions are almost always from the **buyer's** point of view.
- Cost-reimbursable (cost plus) and T&M put overrun risk on the buyer. Fixed price puts it on the seller.

### Closing extras

- Formal acceptance and sign-off come from the **customer**, not the PM.
- Archive everything even if nobody requires it. Archived records are called **historical information** and feed future analogous estimates.
- Third-party reviews or audits may be required by regulators (banking, health care).

### Communication arithmetic trap

Questions often ask how many *additional* channels you get when people join. Calculate before and after, then subtract.

```text
30(29)/2 − 25(24)/2 = 435 − 300 = 135
```

Also from the book: about 55% of communication is nonverbal. **Active listening** means giving feedback, repeating the message back and asking clarifying questions. **Noise**, jargon, hostility and cultural differences are barriers.
