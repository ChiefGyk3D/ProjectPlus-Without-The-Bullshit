# Project+ Without The Bullshit


A CompTIA Project+ PK0-005 study guide for people who already know how to run projects and just need the cert.
Last updated 2026-10-06. Maintained by [ChiefGyk3D](https://github.com/ChiefGyk3D). Licensed MIT.

## How to use this guide

This guide covers every PK0-005 exam objective (1.1 through 4.5) in the official objective order, with a definition and an exam tip for each term. Learn the terms in order, then use the "Gaps filled" section and the formulas and acronym tables at the end for last-minute review. The gaps section was cross-checked against the CompTIA Project+ All-in-One Exam Guide (PK0-005), including its exam tips and its Critical Exam Information appendix.

| Domain | Weight | What it tests |
| --- | --- | --- |
| 1.0 Project Management Concepts | 33% | Methodologies, change, risk, issues, schedule, quality, communication, meetings, teams, procurement |
| 2.0 Project Life Cycle Phases | 30% | Discovery, initiation, planning, execution, closing |
| 3.0 Tools and Documentation | 19% | Charts, logs, productivity tools, quality charts |
| 4.0 Basics of IT and Governance | 18% | ESG, security, compliance, IT infrastructure, operational change control |

Exam format (confirmed against the CompTIA Project+ All-in-One Exam Guide): up to 90 questions in 90 minutes, multiple choice, multiple response and performance-based items, passing score 710 on a 100 to 900 scale. CompTIA recommends 6 to 12 months of project management experience. The domain weights above come from memory, because the book prints them as an image.

### Study tips

- Most questions are scenarios. For each term, ask "when would a project manager choose this over the alternatives?"
- Learn lists in their groups (for example the four negative risk responses, the five conflict styles). Questions often give three right answers and one that belongs to a different group.
- Pay attention to words like *first*, *best*, *next* and *most likely*. They signal which step in a process the question wants.
- Memorize the formulas in the last section. A few questions need arithmetic, and all of them are quick.

**Memory aids used below:** PM = project manager, PMO = project management office, SOW = statement of work, WBS = work breakdown structure.

## 1.0 Project Management Concepts (33%)

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

**Exam tips for 1.1**

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

**Exam tip:** a hybrid approach mixes both (for example, Waterfall for hardware procurement and Agile for software). Pick it when the scenario has a regulated or fixed-date portion plus a changing portion.

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

**Exam tips for 1.3**

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

**Memory aid:** negative = *A*ccept, *A*void, *M*itigate, *T*ransfer. Positive = *A*ccept, *E*nhance, *E*xploit, *S*hare.

**Risk analysis**

- **Qualitative:** rates risks by judgment using a probability and impact matrix. Also considers interconnectivity (how risks affect each other) and detectability (how easily a risk is noticed).
- **Quantitative:** uses numbers and models. Simulation (such as Monte Carlo) estimates the chance of finishing on time or on budget.
- **Impact analysis:** probability vs impact. High probability and high impact risks get attention first.
- **Situational/scenario analysis:** asks "what if" for specific situations.

Expected monetary value is the simplest quantitative measure:

$$
EMV = Probability \times Impact
$$

**Connections:** an unmanaged risk that occurs becomes an **issue**. Risk responses often cause **changes** (so run them through change control). **Roles:** every risk has an owner and a defined point of escalation.

**Exam tips for 1.4**

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

$$
PERT = \frac{O + 4M + P}{6}
$$

**Schedule maintenance:** use the critical path to track delays, watch buffer use, check the impact on cadence, forecast the finish date, publish and share the updated schedule, and run sprint planning and backlog grooming.

**Exam tips for 1.6**

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

$$
CV = EV - AC \qquad SV = EV - PV \qquad CPI = \frac{EV}{AC} \qquad SPI = \frac{EV}{PV}
$$

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

$$
Channels = \frac{n(n-1)}{2}
$$

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

**Exam tip:** unclear scope favors T&M or cost plus. Clear scope favors fixed price. An MSA is signed once, then SOWs and POs cover each piece of work.

## 2.0 Project Life Cycle Phases (30%)

The phases in order: **discovery/concept preparation, initiation, planning, execution, closing**. Monitoring and controlling runs alongside them. Know what is produced in each phase and what comes first.

### 2.1 Discovery / concept preparation artifacts

These artifacts exist *before* the project is formally approved. They justify it.

| Artifact | Definition |
| --- | --- |
| Business case | Documents why the project should happen: problem or opportunity, options, costs, benefits, risks |
| Business objective | The measurable business outcome the project supports |
| Return on investment (ROI) analysis | Compares expected benefit with cost |
| Current state vs future state | Today's process or system compared with the desired outcome. The gap is the work. |
| Prequalified vendor | Supplier already vetted, so selection is faster |
| Predetermined client | Customer already identified before the project starts (common in service contracts) |
| Preexisting contracts | Agreements already in place that shape scope: client SOW, client TOR |
| Capital expense (CapEx) | One-time spend on assets that last (servers, licenses bought outright). Depreciated over time. |
| Operational expense (OpEx) | Ongoing day-to-day cost (subscriptions, support, cloud usage). Expensed when incurred. |
| Feasibility study | Checks if the project is technically, financially and operationally possible |
| Cost-benefit analysis | Compares total cost with total benefit. Benefit-cost ratio above 1 is favorable. |
| Payback period | Time to recover the initial investment |

$$
ROI = \frac{Net\ Benefit}{Cost} \times 100\%
$$

**Exam tip:** moving from on-premises hardware (CapEx) to cloud subscriptions shifts spend to OpEx.

### 2.2 Initiation phase

Goal: authorize the project and define who and what it involves at a high level.

| Activity / artifact | Definition |
| --- | --- |
| Project charter | Document that formally authorizes the project and the PM. Contains objectives, success criteria and a preliminary scope statement. Signed by the sponsor. |
| Project objectives | What the project will achieve (SMART: specific, measurable, achievable, relevant, time-bound) |
| Success criteria | Measurable conditions that show the project succeeded |
| Preliminary scope statement | High-level description of what is in and out of scope |
| Stakeholder identification and assessment | Find stakeholders, record them in the **stakeholder register**, and analyze influence and interest (power/interest grid) |
| Responsibility assignment matrix (RAM) | Shows who does what on each deliverable |
| RACI | **R**esponsible (does the work), **A**ccountable (one person, final sign-off), **C**onsulted (two-way input), **I**nformed (one-way updates) |
| Communication channels | Agreed ways the team will communicate |
| Records management plan | How data and documents are stored, retained, secured and disposed of |
| Access requirements | Which people need which systems, folders and tools, on a need-to-know basis |
| Review existing artifacts | Reuse prior documents, lessons learned and templates |
| Solution design | High-level approach to meet the need |
| Kickoff meeting | First meeting with team and stakeholders to align on goals, roles, scope and plan |

**Exam tips for 2.2**

- The charter comes first. Nothing else is baselined until the project is authorized.
- Every RACI row needs exactly one **A**.
- The PM is named in the charter, which gives authority to use organizational resources.

### 2.3 Planning phase

Goal: define how the work will be done and set the baselines.

| Activity / artifact | Definition |
| --- | --- |
| Assess the resource pool | Check who and what is available, plus a preliminary procurement needs assessment |
| Assign project resources | Match people and equipment to tasks |
| Train project team members | Fill skill gaps |
| Communication plan | Audience, content, method, frequency, owner. Includes meeting cadence. |
| Detailed scope statement | Deliverables, boundaries, assumptions, constraints, acceptance criteria |
| Work breakdown structure (WBS) | Hierarchical breakdown of all project work into deliverable-based work packages (the 100% rule: includes all work and only the work) |
| WBS dictionary | Describes each WBS element in detail |
| Backlog | Prioritized list of remaining work (Agile) |
| Project schedule | Sequenced tasks with durations, resources and dates. Establish cadences. |
| Budget | Cost estimates, aggregated into the cost baseline, with contingency reserve |
| Quality assurance (QA) plan | Standards, metrics and reviews that prevent defects |
| Initial risk assessment | Identify and analyze risks, build the risk register |
| Transition / release plan | Plans how the product moves to operations: operational training, go-live, operational handoff, and internal and external audiences |
| Project management plan | Master document that combines all subsidiary plans (scope, schedule, cost, quality, resource, communication, risk, procurement, stakeholder) |
| Baselines | Approved scope, schedule and cost baselines for measuring performance |
| Milestones | Key checkpoints |
| Minimum viable product (MVP) | Smallest version that delivers value and allows feedback |

**Exam tip:** the WBS divides *deliverables*, not activities. The project management plan is approved by the sponsor and becomes the benchmark for change control.

### 2.4 Execution phase

Goal: do the work in the plan, manage people and vendors, and report progress.

| Activity | Definition |
| --- | --- |
| Execute tasks per the plan | Produce deliverables as planned |
| Organizational change management (OCM) | Helps people adopt the change: impacts and responses, training, communication, documentation, new knowledge bases and processes, ensuring adoption and reinforcing it over time |
| Manage vendors | Enforce rules of engagement, monitor performance, approve deliverables |
| Project meetings and updates | Regular touch points |
| Tracking and reporting | Team touch points, risk reporting, external status reporting, overall progress reporting, gap analysis, ad hoc reporting |
| Update budget and timeline | Reflect actuals and approved changes |
| Manage conflict | Choose a resolution style (below) |
| Phase gate review | Checkpoint where stakeholders decide to proceed, change or stop |

| Conflict style | How it works | Outcome |
| --- | --- | --- |
| Collaborate / problem solve | Work together to find a solution that meets everyone's needs | Win-win, best long term |
| Compromise | Each side gives something up | Both partly satisfied (lose-lose) |
| Smoothing / accommodate | Emphasize agreement, downplay differences | Short-term peace, problem remains |
| Forcing / direct | One side imposes a decision with authority | Win-lose, damages relationships |
| Avoiding / withdraw | Ignore or postpone the conflict | Problem remains, only good to cool down |

**Exam tip:** collaboration is usually the best answer unless the scenario describes an emergency (forcing) or a minor issue with emotions running high (avoiding or smoothing).

### 2.5 Closing phase

Goal: formally finish the work and capture what was learned.

| Activity | Definition |
| --- | --- |
| Project evaluation | Compare results with success criteria and the plan |
| Validation of deliverables | Customer formally accepts deliverables |
| Closing contracts | Complete and close vendor contracts, resolve claims, make final payment |
| Removing access | Disable accounts, badges and permissions for the team and vendors |
| Releasing resources | Return people, equipment and facilities |
| Project closure meeting | Final meeting to review outcome and next steps |
| Closeout report | Summary of performance, variances, deliverables and lessons |
| Collecting stakeholder feedback | Surveys or interviews on satisfaction |
| Archiving documentation | Store records per the records plan |
| Budget reconciliation | Compare final costs with budget and close accounts |
| Rewards and celebration | Recognize the team |
| Project sign-off | Sponsor or customer formally accepts closure |

**Exam tip:** the order that usually matters: validate deliverables, close contracts, remove access and release resources, then hold the closure meeting, archive records and obtain sign-off.

## 3.0 Tools and Documentation (19%)

### 3.1 Tools used throughout the project life cycle

**Tracking charts**

| Chart | What it shows | Best used to |
| --- | --- | --- |
| Gantt chart | Tasks as horizontal bars on a timeline, with durations, dependencies and progress | Show and track the schedule |
| Milestone chart | Key events and dates, without task detail | Brief executives |
| Project network diagram | Tasks as boxes joined by arrows showing dependencies | Find the critical path |
| PERT chart | Network diagram with three-point duration estimates | Estimate uncertain durations |
| Budget burndown chart | Budget remaining (or spent) over time | Track spending against plan |
| Project organizational chart | Team structure and reporting lines | Show who reports to whom |

**Logs, registers and reports**

| Tool | Definition |
| --- | --- |
| Issue log | Tracks current issues, owners, status and resolution |
| Defect log | Records defects found in testing: severity, steps to reproduce, status |
| Change log | Records all change requests and decisions |
| Risk register | Full catalog of risks with probability, impact, owner and response |
| Risk report | Summary of overall risk exposure and top risks for stakeholders |
| Project dashboard | Visual display of key metrics (KPIs) at a glance, often live |
| Project status report | Periodic update on progress, accomplishments, risks, issues and next steps |
| Version control tools | Track revisions of documents and code, support collaboration and rollback |
| Time-tracking tools | Record time spent per task for billing, utilization and estimates |
| Task board | Visual board (To do, In progress, Done), used in Agile and Kanban |
| Requirements traceability matrix (RTM) | Links each requirement to its source, design, test and deliverable, so nothing is missed |
| Stakeholder register | List of stakeholders with interest, influence and engagement strategy |
| Lessons learned register | Captures what worked and what did not |

**Exam tips for 3.1**

- Critical path is found on a network diagram. Schedule progress is shown on a Gantt chart.
- The risk **register** is the detailed log. The risk **report** is the summary for others.
- The RTM proves requirements are all covered and tested.

### 3.2 Project management productivity tools

| Category | Examples and use |
| --- | --- |
| Communication tools | Email (formal, asynchronous), messaging (SMS, chat for quick questions), telephone, face-to-face meetings, video, enterprise social media |
| Collaboration tools | Real-time multi-author editing, file sharing platforms, workflow and e-signature platforms, whiteboards, wiki knowledge bases |
| Meeting tools | Real-time surveys and polling, calendaring, print media, conferencing platforms |
| Documentation and office tools | Word processing, spreadsheets, presentations, charting and diagramming |
| Project scheduling tools | Cloud-based (browser access, vendor maintained, subscription) vs on-premises (local installation, you manage servers and updates, more control) |
| Ticketing / case management | Logs requests and incidents, assigns owners, tracks them to resolution, common in IT support |

| Cloud-based tool | On-premises / local installation |
| --- | --- |
| Accessible anywhere, easy collaboration | Data stays inside your network |
| Vendor handles updates and backup | You handle updates, backup and hardware |
| Subscription (OpEx) | License and hardware purchase (CapEx) |
| Depends on internet and vendor security | Better for strict security or offline needs |

### 3.3 Quality and performance charts

| Chart | What it shows | Use to decide |
| --- | --- | --- |
| Histogram | Bar chart of how often values fall into ranges (distribution) | See the spread of data (for example defect counts) |
| Pareto chart | Bars sorted from largest to smallest with a cumulative line (80/20 rule) | Focus on the "vital few" causes |
| Run chart | Data points in time order | See trends, shifts and patterns over time |
| Scatter diagram | Two variables plotted as points | Test for correlation (positive, negative, none) |
| Fishbone / Ishikawa diagram | Cause-and-effect branches (people, process, equipment, materials, environment, methods) | Find root causes |
| Control chart | Data over time with mean and upper and lower control limits | Tell normal variation from special causes. Out of control if points go outside limits or show a run of 7 on one side. |
| Burnup chart | Work completed against total scope over time | Track progress and scope changes |
| Burndown chart | Work remaining over time | See if the sprint or release will finish on time |
| Velocity chart | Story points completed per sprint | Forecast capacity |
| Decision tree | Branches of choices with probabilities and outcomes | Pick the option with best expected value |

**Exam tips for 3.3**

- Pareto = prioritize problems. Fishbone = find causes. Control chart = is the process stable? Scatter = relationship between two things.
- A burnup chart shows scope changes. A burndown chart does not.

## 4.0 Basics of IT and Governance (18%)

### 4.1 Environmental, social and governance (ESG)

**ESG** factors measure a project's wider responsibility beyond cost and schedule.

| Factor | Project considerations |
| --- | --- |
| Environmental | Impact on the local and global environment: energy use, e-waste, carbon footprint, sustainable sourcing |
| Social | Impact on people and communities: working conditions, diversity, accessibility, local effects |
| Governance | Following applicable regulations and standards, ethics, transparency, oversight |
| Company vision, mission and values | Project work should align with them |
| Brand value | Poor ESG behavior can damage reputation and brand |

### 4.2 Information security concepts

| Area | Concepts |
| --- | --- |
| Physical security | Facility access (badges, locks, visitor logs), mobile device considerations (loss, theft, encryption), removable media (USB drives can leak or spread malware) |
| Operational security | Background screening, security clearance requirements |
| Digital security | Resource access and permissions (least privilege), remote access restrictions (VPN), multifactor authentication (MFA: something you know, have, or are) |
| Data security | Data classification by sensitivity (public, internal, confidential, restricted), intellectual property, trade secrets, national security information, access on a need-to-know basis |
| Corporate IT security policies | Acceptable use, password rules, branding restrictions on what may be shared publicly |

**Confidentiality, integrity, availability (CIA triad):** keep data private, accurate and accessible. **Least privilege:** give only the access needed for the role.

**Exam tip:** at project close, remove access promptly. At project start, define access requirements and classify data first.

### 4.3 Compliance and privacy

| Term | Definition |
| --- | --- |
| Data confidentiality | Protecting sensitive data from unauthorized disclosure |
| Personally identifiable information (PII) | Data that identifies a person: name, address, SSN, email, IP address |
| Personal health information (PHI) | Health data linked to a person. Protected in the US by HIPAA. |
| Legal and regulatory impacts | Laws that affect how the project handles data and operates |
| Country, state and province privacy rules | Examples: GDPR (EU), CCPA/CPRA (California), PIPEDA (Canada). Rules depend on where the data subject lives, not just where the company sits. |
| Industry or organization compliance | Examples: HIPAA (health), PCI DSS (payment cards), SOX (financial reporting), FERPA (education records) |

**Exam tip:** if a project handles data from a region with strict rules (for example EU residents), the PM must account for those rules even if the team is elsewhere.

### 4.4 Basic IT concepts

| Concept | Definition |
| --- | --- |
| Infrastructure | Computing services, networking and connectivity, storage, and supporting documentation |
| Multitiered architecture | Presentation tier (user interface), application tier (business logic), data tier (database) |
| Data warehouse | Central store of integrated historical data for reporting and analysis |
| Platform as a service (PaaS) | Provider supplies platform and runtime. You deploy apps. |
| Infrastructure as a service (IaaS) | Provider supplies virtual servers, storage and networking. You manage OS and apps. |
| Software as a service (SaaS) | Provider supplies finished software over the internet, usually by subscription |
| Anything as a service (XaaS) | Any capability delivered as a service (security, analytics, desktops) |
| Enterprise resource planning (ERP) | Integrated suite for core business processes (finance, HR, supply chain) |
| Customer relationship management (CRM) | Manages customer data, sales and service interactions |
| Database | Organized storage of structured data |
| Electronic document and record management system (EDRMS) | Stores, controls and retains documents and records |
| Content management system (CMS) | Creates and manages web or digital content |
| Financial systems | Accounting, billing, payroll and budgeting software |

**Cloud responsibility:** the user controls the most in IaaS, less in PaaS, and least in SaaS. Remember it as *I* = infrastructure only is given to you, *P* = platform given, *S* = software given.

### 4.5 Operational change control during an IT project

| Area | Key steps |
| --- | --- |
| IT infrastructure change control | Schedule downtime or maintenance windows, send customer notifications, prepare a rollback plan, run validation checks after the change |
| Software change control | Define requirements, assess risk, test (automated and manual), obtain approval, notify customers, release |
| Cloud vs on-premises change control | Cloud: provider controls some changes, so follow provider notice and shared-responsibility terms. On-premises: you control the whole stack and the change window. |
| CI/CD | Continuous integration merges and tests code often. Continuous delivery keeps code always releasable. Continuous deployment releases automatically to production. |
| Production vs beta / staging | Staging or beta mirrors production so changes can be tested safely before release. Production is the live environment. |
| Tiered environments | Development, test, staging/beta and production, with promotion between them after approval |

**Rollback plan:** documented steps to return to the last known good state if the change fails. **Maintenance window:** agreed time when planned downtime has least impact.

**Exam tip:** never deploy untested changes to production. A change goes through test or staging, gets approval, runs in a maintenance window with a rollback plan, then is validated.

## Gaps filled from the All-in-One Exam Guide

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

$$
\frac{30(29)}{2} - \frac{25(24)}{2} = 435 - 300 = 135
$$

Also from the book: about 55% of communication is nonverbal. **Active listening** means giving feedback, repeating the message back and asking clarifying questions. **Noise**, jargon, hostility and cultural differences are barriers.

## Formulas and acronym quick reference

### Formulas

$$
\begin{aligned}
EMV &= P \times I \\
PERT &= \frac{O + 4M + P}{6} \\
Channels &= \frac{n(n-1)}{2} \\
ROI &= \frac{Net\ Benefit}{Cost} \times 100\% \\
CV &= EV - AC \qquad SV = EV - PV \\
CPI &= \frac{EV}{AC} \qquad SPI = \frac{EV}{PV} \\
EAC &= \frac{BAC}{CPI} \qquad ETC = EAC - AC \qquad VAC = BAC - EAC
\end{aligned}
$$

| Earned value term | Meaning |
| --- | --- |
| PV (planned value) | Budgeted cost of work scheduled |
| EV (earned value) | Budgeted cost of work actually completed |
| AC (actual cost) | Real money spent |
| BAC | Budget at completion (total budget) |
| EAC | Estimate at completion (forecast total cost) |
| ETC | Estimate to complete (remaining cost) |

Read the result: variance above 0 or index above 1 is *good*. Below 0 or below 1 is *bad*.

### Acronyms

| Acronym | Meaning |
| --- | --- |
| ART | Agile Release Train |
| BA | Business analyst |
| CCB | Change control board |
| CI/CD | Continuous integration / continuous delivery or deployment |
| CMS | Content management system |
| CPI / SPI | Cost / schedule performance index |
| CRM | Customer relationship management |
| EDRMS | Electronic document and record management system |
| ERP | Enterprise resource planning |
| ESG | Environmental, social and governance |
| IaaS / PaaS / SaaS / XaaS | Infrastructure / platform / software / anything as a service |
| IaC | Infrastructure as code |
| JAD / JAR | Joint application development / review |
| KPI | Key performance indicator |
| MFA | Multifactor authentication |
| MSA | Master service agreement |
| MVP | Minimum viable product |
| NDA | Non-disclosure agreement |
| OCM | Organizational change management |
| OKR | Objectives and key results |
| PERT | Program evaluation review technique |
| PHI / PII | Personal health information / personally identifiable information |
| PMO | Project management office |
| PO | Purchase order |
| PRINCE2 | PRojects IN Controlled Environments |
| QA | Quality assurance |
| RACI | Responsible, accountable, consulted, informed |
| RAM | Responsibility assignment matrix |
| RCA | Root cause analysis |
| RFB / RFI / RFP / RFQ | Request for bid / information / proposal / quote |
| ROI | Return on investment |
| RTM | Requirements traceability matrix |
| SAFe | Scaled Agile Framework |
| SDLC | Software development life cycle |
| SLA | Service-level agreement |
| SME | Subject matter expert |
| SOW | Statement of work |
| T&M | Time and material |
| TDD | Test-driven development |
| TOR | Terms of reference |
| UAT | User acceptance testing |
| WBS | Work breakdown structure |
| WIP | Work in progress |
| XP | Extreme Programming |

### Easily confused pairs

| Pair | Difference |
| --- | --- |
| Risk vs issue | Risk might happen. Issue is happening now. |
| Contingency vs management reserve | Known risks vs unknown-unknowns |
| Crashing vs fast tracking | Add resources (cost) vs overlap tasks (risk) |
| Verification vs validation | Built it right vs built the right thing |
| Program vs portfolio | Related projects vs all work aligned to strategy |
| Product owner vs product manager | Agile backlog owner vs strategic product lead |
| RFI vs RFP vs RFQ | Learn vs detailed proposal vs price only |
| Fixed price vs T&M | Seller bears cost risk vs buyer bears cost risk |
| Burnup vs burndown | Work done with scope line vs work remaining |
| Gantt vs network diagram | Schedule bars vs dependency logic |
| CapEx vs OpEx | One-time asset vs ongoing running cost |
| Revise baseline vs rebaseline | Update for approved change vs full reset |
