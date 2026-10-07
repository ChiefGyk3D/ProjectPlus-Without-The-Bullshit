# 3.0 Tools and Documentation (19%)

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

!!! tip "Exam tips"
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

!!! tip "Exam tips"
    - Pareto = prioritize problems. Fishbone = find causes. Control chart = is the process stable? Scatter = relationship between two things.
    - A burnup chart shows scope changes. A burndown chart does not.
