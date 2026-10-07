# 4.0 Basics of IT and Governance (18%)

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

!!! tip "Exam tip"
    at project close, remove access promptly. At project start, define access requirements and classify data first.


### 4.3 Compliance and privacy

| Term | Definition |
| --- | --- |
| Data confidentiality | Protecting sensitive data from unauthorized disclosure |
| Personally identifiable information (PII) | Data that identifies a person: name, address, SSN, email, IP address |
| Personal health information (PHI) | Health data linked to a person. Protected in the US by HIPAA. |
| Legal and regulatory impacts | Laws that affect how the project handles data and operates |
| Country, state and province privacy rules | Examples: GDPR (EU), CCPA/CPRA (California), PIPEDA (Canada). Rules depend on where the data subject lives, not just where the company sits. |
| Industry or organization compliance | Examples: HIPAA (health), PCI DSS (payment cards), SOX (financial reporting), FERPA (education records) |

!!! tip "Exam tip"
    if a project handles data from a region with strict rules (for example EU residents), the PM must account for those rules even if the team is elsewhere.


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

!!! tip "Exam tip"
    never deploy untested changes to production. A change goes through test or staging, gets approval, runs in a maintenance window with a rollback plan, then is validated.
