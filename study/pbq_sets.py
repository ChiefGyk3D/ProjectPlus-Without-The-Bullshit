"""Fixed sets for the ordering and matching sheets, taken from this guide's own lists and tables.

ORDERINGS: title -> steps in the correct order. A sheet asks for a random run of them.
MATCHINGS: title -> {term: description}. Every description in a set is unique, so a
match is never ambiguous. Nothing here comes from the book.
"""

ORDERINGS = {
    "Project phases": ["Discovery", "Initiation", "Planning", "Execution", "Closing"],
    "Tuckman's team stages": ["Forming", "Storming", "Norming", "Performing", "Adjourning"],
    "Change control process": [
        "Create or receive a change request",
        "Document the request in the change control log",
        "Conduct a preliminary review",
        "Conduct an impact assessment",
        "Document change recommendations",
        "Determine the decision makers",
        "Escalate to the change control board",
        "Document the approval status in the log",
        "Communicate the change status to stakeholders",
        "Update the project plan",
    ],
    "Sprint events": ["Sprint planning", "Daily scrum", "Sprint review", "Sprint retrospective"],
    "Estimates, least to most accurate": ["Rough order of magnitude", "Budget estimate", "Definitive estimate"],
}

MATCHINGS = {
    "Conflict styles": {
        "Collaborate": "Work together to meet everyone's needs",
        "Compromise": "Each side gives something up",
        "Smoothing": "Emphasize agreement and downplay differences",
        "Forcing": "One side imposes a decision with authority",
        "Avoiding": "Ignore or postpone the conflict",
    },
    "Methodologies": {
        "Waterfall": "Linear, each phase finishes before the next starts",
        "Kanban": "Visual pull system with work-in-progress limits",
        "Scrum": "Time-boxed sprints with defined roles and events",
        "Extreme Programming": "Pair programming and test-driven development",
        "DevSecOps": "Security built into every stage of delivery",
        "SAFe": "Agile and Lean applied at enterprise scale",
    },
    "Easily confused pairs": {
        "Risk": "Might happen",
        "Issue": "Is happening now",
        "Contingency reserve": "Set aside for known risks",
        "Management reserve": "Set aside for unknown unknowns",
        "Crashing": "Add resources, which costs money",
        "Fast tracking": "Overlap tasks, which adds risk",
        "Verification": "Did we build it right",
        "Validation": "Did we build the right thing",
    },
    "Cost types": {
        "Direct cost": "Charged only to this project",
        "Indirect cost": "Shared cost of doing business",
        "Fixed cost": "Constant regardless of usage",
        "Variable cost": "Changes with quantity",
        "Cost of conformance": "Money spent to get quality right",
        "Cost of nonconformance": "The cost of failure, such as rework",
    },
    "Phase activities": {
        "Initiating": "Create the charter and identify stakeholders",
        "Planning": "Build the WBS and the schedule",
        "Executing": "Direct the work and acquire the team",
        "Monitoring and controlling": "Run integrated change control",
        "Closing": "Archive records and capture lessons learned",
    },
    "Estimate types": {
        "Rough order of magnitude": "Made while initiating, top-down, least accurate",
        "Budget estimate": "Made early in planning once scope is approved",
        "Definitive estimate": "Built bottom-up from the WBS, most accurate",
    },
    "Earned value formulas": {
        "CPI": "EV / AC",
        "SPI": "EV / PV",
        "CV": "EV - AC",
        "SV": "EV - PV",
        "EAC (current rate continues)": "BAC / CPI",
        "VAC": "BAC - EAC",
    },
}
