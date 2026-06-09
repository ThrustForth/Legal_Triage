"""
Process guide templates for common legal situations in Illinois.

Each template contains structured information about the legal process including
steps, deadlines, forms, and important notes.
"""

from typing import Dict, List, Any

# Process guide templates
PROCESS_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "eviction": {
        "title": "Eviction Process in Illinois",
        "steps": [
            {
                "number": 1,
                "title": "Receive Notice",
                "description": "Landlord must provide written notice of eviction. Notice period depends on reason for eviction.",
                "deadline": "3-30 days depending on reason",
                "details": [
                    "For non-payment: 30-day notice required",
                    "For lease violation: 10-day notice may be used",
                    "For ending tenancy: 30-day notice required"
                ]
            },
            {
                "number": 2,
                "title": "Respond to Notice",
                "description": "Tenant can respond to the eviction notice by paying rent, fixing violation, or filing answer.",
                "deadline": "Before the deadline on the notice",
                "details": [
                    "Pay outstanding rent if that's the reason",
                    "Fix lease violation if possible",
                    "File written response with court"
                ]
            },
            {
                "number": 3,
                "title": "Landlord Files Court Case",
                "description": "If tenant doesn't resolve the issue, landlord files eviction lawsuit in circuit court.",
                "deadline": "After notice period expires",
                "details": [
                    "File complaint with circuit court",
                    "Pay filing fees (ask for waiver if low income)",
                    "Serve tenant with court documents"
                ]
            },
            {
                "number": 4,
                "title": "Court Hearing",
                "description": "Both parties appear before judge to present their case.",
                "deadline": "Typically 7-14 days after filing",
                "details": [
                    "Tenant should attend unless waiving right",
                    "Bring all documents and evidence",
                    "Judge will make decision that day"
                ]
            },
            {
                "number": 5,
                "title": "Judgment & Sheriff Eviction",
                "description": "If judgment is for landlord, sheriff enforces the eviction.",
                "deadline": "Usually 7-10 days after judgment",
                "details": [
                    "Tenant must move out by specified date",
                    "Landlord can change locks after sheriff leaves",
                    "Personal property left behind may be disposed"
                ]
            }
        ],
        "forms": [
            "Notice to Quit",
            "Summons",
            "Complaint for Possession",
            "Answer to Eviction"
        ],
        "timeline": "30-90 days typical",
        "important_notes": [
            "Contact legal aid immediately - free assistance available",
            "Keep all notices and court documents",
            "Follow all deadlines strictly",
            "You have constitutional rights as a tenant"
        ],
        "contact_info": {
            "eviction_hotline": "855-601-9474",
            "hours": "Monday-Friday 9am-4pm"
        }
    },
    
    "divorce": {
        "title": "Divorce Process in Illinois",
        "steps": [
            {
                "number": 1,
                "title": "File Petition for Dissolution",
                "description": "Complete and file the divorce petition with the circuit court in your county.",
                "deadline": "Once filed, serve spouse within 120 days",
                "details": [
                    "Complete online Easy Form or paper forms",
                    "Provide marriage date and location",
                    "List property and debt information"
                ]
            },
            {
                "number": 2,
                "title": "Serve Spouse",
                "description": "Legal documents must be delivered to your spouse.",
                "deadline": "Within 120 days of filing",
                "details": [
                    "Use sheriff or process server",
                    "Or have spouse sign waiver of service",
                    "File proof of service with court"
                ]
            },
            {
                "number": 3,
                "title": "Wait for Response",
                "description": "Spouse has time to file an answer or counter-petition.",
                "deadline": "Typically 30 days after service",
                "details": [
                    "If no response, proceed to default judgment",
                    "If response filed, case continues",
                    "Consider mediation for uncontested divorce"
                ]
            },
            {
                "number": 4,
                "title": "Financial Disclosure",
                "description": "Both parties exchange financial information.",
                "deadline": "As set by court order",
                "details": [
                    "Income and expense information",
                    "Asset and liability listings",
                    "Tax returns and pay stubs"
                ]
            },
            {
                "number": 5,
                "title": "Final Hearing",
                "description": "Judge approves settlement and signs judgment.",
                "deadline": "Date set by court",
                "details": [
                    "Attend final hearing if required",
                    "Judge reviews agreement terms",
                    "Sign final judgment for dissolution"
                ]
            }
        ],
        "forms": [
            "Petition for Dissolution of Marriage",
            "Summons",
            "Appearance and Resistance (if contesting)",
            "Marital Settlement Agreement",
            "Judgment for Dissolution of Marriage"
        ],
        "timeline": "4-12 months typical",
        "important_notes": [
            "Uncontested divorces go faster",
            "Residency requirement: lived in Illinois 90+ days",
            "Grounds not required - can divorce 'without cause'",
            "Child support calculated using state guidelines"
        ],
        "contact_info": {
            "legal_aid": "Check local legal aid organization",
            "forms_website": "Illinois Courts Standardized Forms website"
        }
    },
    
    "custody": {
        "title": "Child Custody Process in Illinois",
        "steps": [
            {
                "number": 1,
                "title": "File Custody Petition",
                "description": "File petition with circuit court in county where child lives.",
                "deadline": "Immediately when custody issue arises",
                "details": [
                    "Establish legal custody arrangement",
                    "Request physical custody (where child lives)",
                    "Request legal custody (decision-making)"
                ]
            },
            {
                "number": 2,
                "title": "Court Evaluation (if contested)",
                "description": "Court may order professional custody evaluation.",
                "deadline": "Weeks to months, depending on court schedule",
                "details": [
                    "Evaluator interviews parents and child",
                    "Reviews home environments",
                    "Writes detailed custody recommendation"
                ]
            },
            {
                "number": 3,
                "title": "Parenting Plan",
                "description": "Develop detailed plan for child's care and schedule.",
                "deadline": "Before final order",
                "details": [
                    "Regular parenting time schedule",
                    "Decision-making responsibilities",
                    "Holiday and vacation schedules"
                ]
            },
            {
                "number": 4,
                "title": "Court Decision",
                "description": "Judge determines custody based on child's best interests.",
                "deadline": "As set by court",
                "details": [
                    "Primary residential parent",
                    "Allocated decision-making responsibility",
                    "Any restrictions on relocation"
                ]
            },
            {
                "number": 5,
                "title": "Ongoing Modifications",
                "description": "Either parent can request changes if circumstances change.",
                "deadline": "Show substantial change in circumstances",
                "details": [
                    "File motion to modify custody",
                    "Court must find change is in child's best interest",
                    "Current custody not automatically changed"
                ]
            }
        ],
        "forms": [
            "Petition for Allocation of Parental Responsibilities",
            "Summons",
            "Parenting Plan",
            "Custody Evaluation Request",
            "Motion for Temporary Order"
        ],
        "timeline": "2-18 months depending on complexity",
        "important_notes": [
            "Best interests of child is the standard",
            "Both parents have right to know about child",
            "Grandparents may have visitation rights",
            "Relocation requires court approval"
        ],
        "contact_info": {
            "family_legal_aid": "Check local family law legal aid",
            "mediation_services": "Available in most counties"
        }
    },
    
    "debt_collection": {
        "title": "Debt Collection Defense Process",
        "steps": [
            {
                "number": 1,
                "title": "Verify the Debt",
                "description": "Confirm you owe the debt and the amount claimed.",
                "deadline": "Within 30 days of first contact",
                "details": [
                    "Request validation in writing",
                    "Check credit reports",
                    "Don't acknowledge debt as yours yet"
                ]
            },
            {
                "number": 2,
                "title": "Dispute if Necessary",
                "description": "Send dispute letter if you think debt is wrong.",
                "deadline": "Within 30 days of validation request",
                "details": [
                    "Send certified mail with return receipt",
                    "State reasons for dispute",
                    "Collector must verify before continuing"
                ]
            },
            {
                "number": 3,
                "title": "Respond to Lawsuit",
                "description": "If sued, file written answer with the court.",
                "deadline": "Before date listed in summons (usually 7-30 days)",
                "details": [
                    "File answer denying allegations",
                    "Assert any defenses",
                    "Counter-claim if appropriate"
                ]
            },
            {
                "number": 4,
                "title": "Negotiate Settlement",
                "description": "Try to negotiate payment arrangement.",
                "deadline": "Before judgment entered",
                "details": [
                    "Offer lump sum settlement",
                    "Propose payment plan",
                    "Get agreement in writing"
                ]
            },
            {
                "number": 5,
                "title": "Defend at Trial",
                "description": "If no settlement, prepare for court appearance.",
                "deadline": "As scheduled by court",
                "details": [
                    "Gather all documents",
                    "Prepare witnesses if needed",
                    "Present your defense"
                ]
            }
        ],
        "forms": [
            "Debt Validation Letter",
            "Answer to Complaint",
            "Settlement Agreement",
            "Financial Statement"
        ],
        "timeline": "30 days to several months",
        "important_notes": [
            "Statute of limitations varies by debt type",
            "Collection cannot continue after statute expires",
            "Medical debts have special protections",
            "Credit reporting limited to 7 years"
        ],
        "contact_info": {
            "consumer_legal_aid": "Check local consumer law legal aid",
            "credit_bureaus": "Equifax, Experian, TransUnion"
        }
    },
    
    "identity_theft": {
        "title": "Identity Theft Response Process",
        "steps": [
            {
                "number": 1,
                "title": "Report the Crime",
                "description": "File report with FTC and local police.",
                "deadline": "Immediately when discovered",
                "details": [
                    "File online at IdentityTheft.gov",
                    "File police report in your area",
                    "Get Identity Theft Affidavit"
                ]
            },
            {
                "number": 2,
                "title": "Place Fraud Alerts",
                "description": "Contact credit bureaus to place alerts on accounts.",
                "deadline": "Within 24 hours of discovery",
                "details": [
                    "Call one bureau - they all notify others",
                    "Alerts last 1 year initially",
                    "Free credit monitoring provided"
                ]
            },
            {
                "number": 3,
                "title": "Close Compromised Accounts",
                "description": "Close bank accounts and credit cards that were accessed.",
                "deadline": "As soon as possible",
                "details": [
                    "Get new account numbers",
                    "Update automatic payments",
                    "Monitor new accounts closely"
                ]
            },
            {
                "number": 4,
                "title": "Dispute Fraudulent Charges",
                "description": "Report fraudulent transactions on credit reports.",
                "deadline": "Within 30 days of discovery",
                "details": [
                    "Send disputes in writing",
                    "Include Identity Theft Affidavit",
                    "Follow up on dispute results"
                ]
            },
            {
                "number": 5,
                "title": "Monitor and Recover",
                "description": "Continuously monitor accounts and credit reports.",
                "deadline": "Ongoing for months or years",
                "details": [
                    "Check credit reports quarterly",
                    "Review bank and credit card statements",
                    "Keep detailed records of all actions"
                ]
            }
        ],
        "forms": [
            "FTC Identity Theft Report",
            "Police Report",
            "Credit Bureaus Fraud Alerts",
            "Dispute Letters",
            "Identity Theft Affidavit"
        ],
        "timeline": "Ongoing - months to years",
        "important_notes": [
            "Time is critical - act immediately",
            "Keep detailed records of all actions",
            "Credit bureaus must investigate disputes",
            "Consider credit freeze for extra protection"
        ],
        "contact_info": {
            "ftc_complaint": "1-877-FTC-HELP",
            "identity_theft_hotline": "1-877-ID-THEFT"
        }
    }
}


def get_template(topic: str) -> Dict[str, Any]:
    """Get a process guide template by topic.
    
    Args:
        topic: The legal topic (e.g., 'eviction', 'divorce')
        
    Returns:
        Process guide template dictionary
    """
    return PROCESS_TEMPLATES.get(topic.lower(), {})


def list_topics() -> List[str]:
    """List all available process guide topics.
    
    Returns:
        List of topic strings
    """
    return list(PROCESS_TEMPLATES.keys())