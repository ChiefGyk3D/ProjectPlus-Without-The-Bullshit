# 1.0 Project Management Concepts (33%)

The largest domain. It covers how projects are run (methodologies), controlled (change, risk, issues, schedule, quality), and staffed (communication, meetings, teams, procurement).

### 1.1 Characteristics of a project, methodologies and frameworks

**A project is** a temporary effort that creates a unique product, service or result. It differs from operations, which are ongoing and repetitive.

| Characteristic | Meaning | Example |
| --- | --- | --- |
| Start and finish | Defined beginning and end, with dates and deliverables | Migrate email to the cloud by 30 June |
| Unique | Each project differs in objectives, constraints and requirements | A one-off ERP rollout for a single client |
| Reason / purpose | Exists to meet a business need or goal | Reduce help-desk calls by 20% |
| Part of a program | A program groups related projects managed together for combined benefit | Data center move: network, servers and apps projects |
| Part of a portfolio | A portfolio is all programs and projects an organization funds, aligned to strategy | Everything IT is funding this year |

**Project vs program vs portfolio:** a project delivers an output, a program coordinates related projects for a shared benefit, and a portfolio selects and prioritizes work to match strategy.

**Predictive vs adaptive:** predictive (plan-driven, such as Waterfall and PRINCE2) fixes scope early. Adaptive (Agile) lets scope evolve while time and cost stay fixed.

| Methodology / framework | Core idea | Terms to know |
| --- | --- | --- |
| Waterfall | Linear and sequential. Each phase finishes before the next starts. Changes late in the project are costly. | Requirements, design, implementation, testing, deployment, maintenance. Predictive. Heavy documentation. |
| Agile | Iterative and incremental delivery of working product, with customer feedback every cycle. | Sprint/iteration, backlog, self-organizing team, adaptive planning, continuous improvement, deliver value early. |
| Scrum | Agile framework using time-boxed sprints (commonly 2 to 4 weeks, never longer than 1 month in the Scrum Guide). | Roles: Product Owner (maximizes value, owns product backlog), Scrum Master (facilitator, removes impediments), Development Team (builds the increment). Events: sprint planning, daily scrum/stand-up, sprint review, sprint retrospective. Artifacts: product backlog, sprint backlog, increment. |
| Kanban | Visual pull system. Cards move across columns on a board. | Visualize work, limit work in progress (WIP), manage flow, cycle time, throughput, continuous delivery with no fixed iterations. |
| Extreme Programming (XP) | Agile engineering practices for high-quality code. | Pair programming (driver and observer), test-driven development (TDD), continuous integration, simple design, refactoring, small releases, collective code ownership, on-site customer. |
| Scaled Agile Framework (SAFe) | Applies Agile and Lean at enterprise scale. | Agile Release Train (ART, 50 to 125 people), Program Increment (PI, about 8 to 12 weeks), Lean Portfolio Management, Portfolio Kanban. |
| DevOps | Joins development and operations to shorten delivery with automation and shared ownership. | Continuous integration (CI), continuous delivery/deployment (CD), infrastructure as code (IaC), monitoring and feedback, breaking down silos. |
| DevSecOps | DevOps with security built into every stage. | Shift left (test security early), security as code, automated security testing, threat modeling, continuous monitoring. |
| PRINCE2 (PRojects IN Controlled Environments) | Process-based, stage-by-stage method with strong governance. | 7 principles (continued business justification, learn from experience, defined roles, manage by stages, manage by exception, focus on products, tailor to suit). 7 themes (business case, organization, quality, plans, risk, change, progress). 7 processes (starting up, initiating, directing, controlling a stage, managing product delivery, managing stage boundaries, closing). Project Board, product-based planning. |
| Software Development Life Cycle (SDLC) | The phases software goes through, regardless of method. | Planning, analysis, design, implementation/coding, testing, deployment, maintenance and support. |

!!! tip "Exam tips"
    - Kanban is the only one listed that has no sprints and uses WIP limits. It is a *pull* system.
    - SAFe means *scaling* Agile. If the scenario has many teams and a large enterprise, think SAFe.
    - "Security built in early" points to DevSecOps. "Developers and operations collaborate" points to DevOps.
    - PRINCE2 questions use words like *stages*, *Project Board* or *business case*.


### 1.2 Agile vs Waterfall

| Criterion | Agile | Waterfall |
| --- | --- | --- |
| Tolerance for change (requirements, budget, schedule) | High. Requirements change between sprints. | Low. Changes are costly and may restart earlier phases. |
| Approach | Adaptive, iterative | Predictive, sequential |
| Best when | Requirements are unclear or evolving | Requirements are stable and well understood |
| Culture | Collaborative, transparent, empowered teams | Hierarchical, clear role boundaries |
| Industry fit | Software, product development, fast-moving markets | Construction, aerospace, defense, heavily regulated work |
| Product ownership | Dedicated Product Owner prioritizes the backlog | Sponsor and stakeholders define scope up front |
| Roles | Cross-functional, self-organizing (Scrum Master, Product Owner, Developers) | Specialized, separate teams (design, dev, test) with a PM directing |
| Team size | Small (often 5 to 9) | Often larger, specialists per phase |
| Resource commitment | Ongoing, near full-time during sprints | Heavy at the phase where the skill is needed |
| Communication | Frequent and informal: daily stand-up, planning, review, retrospective | Formal documentation and milestone meetings |
| Delivery | Working increments every sprint | One main delivery at the end |
| Budget and schedule | Time and cost fixed, scope flexible | Scope fixed, time and cost estimated |

!!! tip "Exam tip"
    a hybrid approach mixes both (for example, Waterfall for hardware procurement and Agile for software). Pick it when the scenario has a regulated or fixed-date portion plus a changing portion.


### 1.3 Change control process

A **change** is any alteration to the approved scope, schedule, cost, quality or baseline. Changes must be controlled so the project does not drift. The standard process, in order:

1. Create or receive a change request (CR). It must be formally documented.
2. Document the request in the change control log.
3. Conduct a preliminary review (is it valid, complete and feasible?).
4. Conduct an impact assessment (scope, schedule, cost, quality, resources, risk).
5. Document change recommendations (approve, reject or defer, with reasons).
6. Determine the decision makers.
7. Escalate to the change control board (CCB), if applicable.
8. Document the approval status in the change control log.
9. Communicate the change status to stakeholders.
10. Update the project plan (and baselines if approved).
11. Implement the change.
12. Validate the change implementation.
13. Communicate that the change has been deployed.

| Term | Definition |
| --- | --- |
| Change request | Formal proposal to alter scope, schedule, budget or deliverables |
| Change control log | Register of all CRs with requester, date, status and decision |
| Change control board (CCB) | Group with authority to approve or reject significant changes |
| Impact assessment | Analysis of what a change affects across the project constraints |
| Product change vs project change | Product change alters what is delivered (a feature). Project change alters how it is delivered (schedule, budget, resources, plan). |
| Scope creep | Uncontrolled growth in scope with no change control and no matching time or budget |
| Gold plating | Adding extras the customer did not ask for |
| Baseline | Approved version of scope, schedule or cost used as the comparison point |

!!! tip "Exam tips"
    - The impact assessment always comes *before* a decision. Never implement first.
    - When a stakeholder asks for "one small addition", the correct reply is to submit a change request, not to just do it.
    - Only approved changes update the plan and baseline.


### 1.4 Risk management

A **risk** is an uncertain event that, if it happens, affects an objective. It has not happened yet. Risks can be negative (threats) or positive (opportunities).

**General sources of risk** (events that make an organization "unsettled"): new projects, new management, regulatory environment changes, digital transformation, infrastructure end-of-life, mergers and acquisitions, reorganization, and a major cybersecurity event.

| Term | Definition |
| --- | --- |
| Known risk | Identified and analyzed, so it can be planned for |
| Unknown risk | Not yet identified. Covered by management reserve, not by a specific plan. |
| Risk register | Central log of risks: description, probability, impact, owner, response, status |
| Risk owner | Person accountable for monitoring a risk and carrying out its response |
| Risk trigger | Warning sign that a risk is about to occur |
| Contingency plan | Planned response that runs *if* the risk occurs |
| Fallback plan | Backup used if the first response does not work |
| Residual risk | Risk left after a response |
| Secondary risk | New risk created by the response itself |
| Risk appetite / tolerance | How much risk the organization accepts |

**Risk responses**

| Response | Negative risk (threat) | Positive risk (opportunity) |
| --- | --- | --- |
| Accept | Acknowledge and monitor, maybe set aside reserve | Take the benefit if it comes, no effort to chase it |
| Avoid | Change the plan to remove the threat | n/a |
| Mitigate | Reduce probability or impact | n/a |
| Transfer | Shift the impact to a third party (insurance, outsourcing, warranty) | n/a |
| Enhance | n/a | Raise probability or impact of the opportunity |
| Exploit | n/a | Make sure the opportunity definitely happens |
| Share | n/a | Partner with another party who can capture it better |

!!! note "Memory aid"
    negative = *A*ccept, *A*void, *M*itigate, *T*ransfer. Positive = *A*ccept, *E*nhance, *E*xploit, *S*hare.


**Risk analysis**

- **Qualitative:** rates risks by judgment using a probability and impact matrix. Also considers interconnectivity (how risks affect each other) and detectability (how easily a risk is noticed).
- **Quantitative:** uses numbers and models. Simulation (such as Monte Carlo) estimates the chance of finishing on time or on budget.
- **Impact analysis:** probability vs impact. High probability and high impact risks get attention first.
- **Situational/scenario analysis:** asks "what if" for specific situations.

Expected monetary value is the simplest quantitative measure:

```text
EMV = Probability × Impact
```

**Connections:** an unmanaged risk that occurs becomes an **issue**. Risk responses often cause **changes** (so run them through change control). **Roles:** every risk has an owner and a defined point of escalation.

!!! tip "Exam tips"
    - Buying insurance or hiring a contractor to take the risk = transfer. Choosing a different supplier to eliminate the risk = avoid.
    - A risk is in the *future*. If it has already happened, it is an issue.


### 1.5 Issue management

An **issue** is a problem that is happening now and may affect the project. It needs action, not just monitoring.

| Term | Definition |
| --- | --- |
| Issue log | Tracker of issues: description, status, priority, owner, due date, resolution |
| Escalation path | The defined chain of people to contact when the team cannot resolve an issue |
| Ownership | Each issue is assigned to a named person who is accountable |
| Root cause analysis (RCA) | Finding the underlying reason, not the symptom (5 Whys, fishbone diagram) |
| Work-around | Temporary fix that keeps work moving but does not remove the cause |
| Contingency plan | Predefined response executed when a known risk becomes an issue |
| Resolution plan | Steps, owner and date to fix the issue |

**Prioritizing issues** by: severity, impact to the project, urgency, and scope of impact to the organization. Escalate when it exceeds the owner's authority.

**Process:** identify and log, assign owner, prioritize, analyze root cause, execute contingency plan or work-around, fix and track, escalate if needed, document the outcome and lessons learned.

**Connections:** issues may require changes (through change control), and changes can cause new issues.

**Risk vs issue:** risk = might happen (future, probability). Issue = is happening (present, certain).

### 1.6 Schedule development and management

**Sequencing and dependencies**

| Dependency type | Meaning | Example |
| --- | --- | --- |
| Hard logic / mandatory | Physically or contractually required order | Build the server before installing software on it |
| Soft logic / discretionary | Preferred order by best practice | Do UI design before database tuning |
| External | Depends on something outside the project | Vendor delivers hardware |
| Internal | Depends on another project task or team | Testing waits for development |

| Relationship | Rule | Frequency |
| --- | --- | --- |
| Finish-to-start (FS) | B cannot start until A finishes | Most common |
| Start-to-start (SS) | B cannot start until A starts | Parallel work |
| Finish-to-finish (FF) | B cannot finish until A finishes | Documentation ends with the build |
| Start-to-finish (SF) | B cannot finish until A starts | Rare (shift handover) |

The task that must come first is the **predecessor**. The task that follows is the **successor**. **Lead** is overlap (successor starts early). **Lag** is a delay (waiting time, such as concrete curing).

| Term | Definition |
| --- | --- |
| Milestone | Zero-duration marker of an important event or deliverable |
| Estimating techniques | Analogous (from similar past projects), parametric (unit rate, such as hours per line of code), bottom-up (sum of work packages), three-point, expert judgment |
| Three-point / PERT estimate | Weighted average of optimistic (O), most likely (M) and pessimistic (P) |
| Story points | Relative size estimate for agile work (Fibonacci scale, planning poker) |
| Epic > story > task | Epic is a large body of work. A story is a user-facing slice. A task is a unit of work to finish a story. |
| Sprint goal | Short statement of what the sprint will achieve |
| Velocity | Story points a team completes per sprint, used to forecast |
| Backlog prioritization | Ordering backlog items by value, risk and dependency |
| Critical path | Longest sequence of dependent tasks. It sets the minimum project duration. Zero total float. |
| Float / slack | How long a task can slip without delaying the next task (free float) or the end date (total float) |
| Crashing | Add resources to critical path tasks to shorten the schedule (raises cost) |
| Fast tracking | Run tasks in parallel that were planned in sequence (raises risk) |
| Resource loading | Amount of a resource assigned over time. Overallocation means more than 100% capacity. |
| Resource leveling | Adjust the schedule to remove overallocation (may extend the finish date) |
| Contingency reserve / buffer | Time or money for *known* risks, owned by the PM |
| Management reserve | Money or time for *unknown-unknowns*, released by senior management |
| Cadence | Regular rhythm of delivery, such as two-week sprints or monthly releases |
| Baseline | Approved original plan used as a benchmark |
| Revise baseline vs rebaseline | Revising updates part of the plan for approved changes. Rebaselining resets the whole baseline after major change, which loses the original variance history. |

```text
PERT = (O + 4M + P) / 6
```

**Schedule maintenance:** use the critical path to track delays, watch buffer use, check the impact on cadence, forecast the finish date, publish and share the updated schedule, and run sprint planning and backlog grooming.

!!! tip "Exam tips"
    - Delays on the critical path delay the project. Delays on non-critical tasks (with float) do not, until float is used up.
    - Crashing costs money. Fast tracking adds risk. Know which is which.
    - Contingency reserve is for known risks. Management reserve is for unknown-unknowns.


### 1.7 Quality management vs performance management

**Quality management** asks "does the deliverable meet requirements?" **Performance management** asks "is the project on track for cost, schedule and goals?"

| Term | Definition |
| --- | --- |
| Retrospective / lessons learned | Team reflects on what went well and what to improve (end of sprint or phase) |
| Sprint review | End-of-sprint demo to stakeholders to get feedback on the increment |
| Service-level agreement (SLA) | Contract that sets measurable service levels (uptime, response time) and penalties |
| Key performance indicator (KPI) | Measurable value showing progress toward an objective |
| Objectives and key results (OKRs) | Goal-setting: an objective plus measurable key results |
| Cost variance (CV) | Earned value minus actual cost. Negative = over budget. |
| Schedule variance (SV) | Earned value minus planned value. Negative = behind schedule. |
| Audit | Formal independent review of compliance with processes or standards |
| Inspection | Examination of a product or work to see if it meets requirements |
| Verification | "Did we build it *right*?" Checks against specifications, usually internal |
| Validation | "Did we build the *right thing*?" Customer or user confirms it meets needs |
| Post-implementation support / warranty period | Time after go-live in which defects are fixed at no extra charge |

```text
CV = EV − AC       SV = EV − PV       CPI = EV / AC       SPI = EV / PV
```

CPI or SPI **below 1** is bad (over budget or behind). **Above 1** is good.

**Testing types**

| Test | Purpose |
| --- | --- |
| Unit | Individual functions or components in isolation, usually automated |
| Integration | Combined components work together |
| System | Complete system against requirements |
| Smoke (build verification) | Quick high-level check that a build is stable enough to test further |
| Regression | Re-test after a change to confirm nothing else broke |
| Performance | Speed, response time and throughput under expected load |
| Stress | Push beyond normal limits to find the breaking point |
| User acceptance (UAT) | Final test by real users or the customer to accept the product |

A **test plan** describes scope, approach, resources, schedule, entry/exit criteria and test cases. A **testing cycle** is one round of test, fix and retest.

### 1.8 Communication management

| Concept | Definition and examples |
| --- | --- |
| Synchronous | Real time, everyone present at once: phone call, video meeting, live chat |
| Asynchronous | Not real time, read when convenient: email, recorded video, notifications, wiki |
| Written vs verbal | Written gives a record and precision. Verbal is faster and conveys tone. |
| Formal vs informal | Formal: status reports, contracts, official notices. Informal: hallway chat, instant messages. |
| Internal vs external | Internal: team, sponsor. External: customers, vendors, regulators. |
| Communication platform / modality | The channel chosen for the audience and message (email, chat, portal, conference) |
| Communication plan | Who gets what information, when, how often, in what format, and from whom |

**Communication challenges:** language barriers, time zones and geography, technology factors (access, tools), and cultural differences. Solve with plain language, overlapping hours, recorded updates and agreed norms.

**Maintaining records:** communication **security** (confidentiality), **integrity** (accuracy, not altered) and **archiving** (stored per the records policy).

**Controlling communication:** escalate communication problems and revise the communication plan when stakeholders or conditions change.

**Communication channels formula:** with *n* people, the number of channels is:

```text
Channels = n(n − 1) / 2
```

For example, 10 people = 45 channels. Adding people increases complexity fast.

### 1.9 Meeting management

| Category | Meeting type | Purpose |
| --- | --- | --- |
| Collaborative | Workshop | Hands-on session to build something together |
| Collaborative | Focus group | Gather opinions from a selected group of users |
| Collaborative | Joint application development / review (JAD/JAR) | Users and developers define or review requirements together |
| Collaborative | Brainstorming | Generate many ideas without judging them |
| Informative | Demonstration / presentation | Show or explain a product or topic |
| Informative | Stand-up | Short (about 15 minute) daily team sync: done, doing, blocked |
| Informative | Status | Share progress, risks and issues |
| Decisive | Refinement | Clarify and size backlog items |
| Decisive | Task setting | Assign and agree on work |
| Decisive | Project steering committee | Senior stakeholders decide direction, funding and escalations |

| Element | Definition |
| --- | --- |
| Agenda | Topics, order and time, sent before the meeting |
| Facilitator | Runs the meeting, keeps it on track |
| Scribe | Records notes and decisions |
| Attendees / target audience | Only the people needed for the topic |
| Timeboxing | Fixed time limit per topic or meeting |
| Action items | Tasks from the meeting with an owner and due date |
| Meeting minutes | Record of attendance, decisions and action items |
| Follow-ups | Distribute minutes and track action items to closure |

### 1.10 Team and resource management

**Organizational structures**

| Structure | Who the team reports to | PM authority |
| --- | --- | --- |
| Functional | Functional (department) manager | Little to none. PM is a coordinator. |
| Weak matrix | Functional manager, with some project work | Low |
| Balanced matrix | Both functional and project manager | Moderate |
| Strong matrix | Mostly the project manager | High |
| Projectized | Project manager, fully dedicated | Highest |

**Matrix** structures have dual reporting. They can cause conflict over priorities and resource sharing.

**Resource life cycle:** acquisition (needs assessment), maintenance, hardware decommissioning, end-of-life software, and successor planning.

| Resource concept | Definition |
| --- | --- |
| Human, physical, capital resources | People, equipment and facilities, money |
| Internal vs external | Employees vs contractors and vendors |
| Shared vs dedicated | Used by several projects vs assigned to one |
| Gap analysis | Compare current state with needed state: feature/functionality, skills, utilization |

**Tuckman's team life cycle:** Forming (polite, unsure) then Storming (conflict, roles tested) then Norming (agreement, trust) then Performing (high productivity) then Adjourning (project ends, team disbands). The PM provides **feedback**, maintains **momentum** and manages the stage the team is in.

| Role | Responsibility |
| --- | --- |
| Project manager (PM) | Plans, executes and closes the project; manages scope, schedule, budget and team |
| Program manager | Coordinates multiple related projects |
| Product manager | Owns product strategy and life cycle, market and launch |
| Product owner | Agile role that prioritizes the backlog and maximizes value |
| Scrum master | Coaches the team on Scrum, removes impediments |
| Sponsor | Provides funding and authority, champions the project |
| Stakeholders | Anyone affected by or able to affect the project |
| Senior management | Executive direction and support |
| Project management office (PMO) | Standardizes methods and supports PMs across the organization |
| Business analyst (BA) | Gathers and defines requirements |
| Subject matter expert (SME) | Deep knowledge in one area |
| Architect | Designs the technical structure |
| Developers / engineers | Build the solution |
| Testers / QA specialists | Verify quality, find defects |
| End users | People who will use the product, key for feedback and adoption |
| Core (operational) team | Work on the project day to day |
| Extended (functional) team | Contribute part-time or on specific tasks |

### 1.11 Procurement and vendor selection

**Resource procurement methods:** **build** (make in house), **buy** (purchase and own), **lease** (rent for a term), **subscription / pay-as-you-go** (ongoing use-based fee).

| Exploratory document | Purpose |
| --- | --- |
| Request for information (RFI) | Learn what vendors offer. Early research, no commitment. |
| Request for proposal (RFP) | Ask for a detailed solution and price when the approach is not fixed |
| Request for bid (RFB) | Ask for a firm price for a clearly defined requirement |
| Request for quote (RFQ) | Ask for a price on specific items or services |

**Vendor evaluation:** best value vs lowest cost, cost-benefit analysis, market research and competitive analysis, qualifications, prequalified vendors, demonstration, technical approach, physical and financial capacity, and references.

| Contract / document | Definition | Who bears cost risk |
| --- | --- | --- |
| Fixed price | Set total price regardless of effort | Seller |
| Time and material (T&M) | Pay hourly rate plus materials | Buyer |
| Cost plus | Pay actual costs plus a fee or percentage | Buyer |
| Unit price | Pay a set price per unit delivered | Shared (depends on quantity) |
| Maintenance agreement | Ongoing support after delivery, may include warranty | n/a |
| Master service agreement (MSA) | Umbrella terms for many future work orders | n/a |
| Purchase order (PO) | Buyer's authorization to purchase | n/a |
| Terms of reference (TOR) | Defines purpose, scope and responsibilities of an engagement | n/a |
| Statement of work (SOW) | Detailed scope, deliverables, tasks, timeline and acceptance for the work | n/a |
| Non-disclosure agreement (NDA) | Legal agreement to keep information confidential | n/a |

!!! tip "Exam tip"
    unclear scope favors T&M or cost plus. Clear scope favors fixed price. An MSA is signed once, then SOWs and POs cover each piece of work.
