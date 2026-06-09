"""Process guide templates for common legal procedures.
Each template is a dict with keys:
- steps: list of step strings
- timeline: optional description of typical timeframe
- forms: list of required form names
- notes: optional extra notes
"""

templates = {
    "eviction": {
        "title": "Illinois Eviction Process",
        "steps": [
            "Serve the tenant with a proper notice to quit (usually 5-10 days).",
            "If the tenant does not cure, file a Complaint for Possession in the appropriate circuit court.",
            "Pay the filing fee and request a judgment on the pleadings.",
            "Obtain a sheriff's notice of removal after judgment is entered.",
            "Coordinate with the sheriff to enforce the eviction if the tenant still refuses to vacate."
        ],
        "timeline": "Typically 30‑90 days depending on court schedule and tenant response.",
        "forms": ["Notice to Quit", "Complaint for Possession", "Summons", "Judgment of Possession", "Sheriff's Notice of Removal"],
        "notes": "Ensure the notice complies with local ordinances; improper notice can invalidate the whole process."
    },
    "divorce": {
        "title": "Illinois Divorce Process",
        "steps": [
            "File a Petition for Dissolution of Marriage with the circuit court.",
            "Serve the spouse with the petition and a Summons.",
            "Complete financial disclosures and exchange them with the spouse.",
            "Participate in mediation or settlement conference to resolve issues.",
            "If no settlement, attend trial and obtain a Final Judgment of Dissolution."
        ],
        "timeline": "Average 4‑12 months, depending on complexity and cooperation.",
        "forms": ["Petition for Dissolution", "Summons", "Financial Statement", "Settlement Agreement", "Final Judgment of Dissolution"],
        "notes": "Illinois is a no‑fault divorce state; grounds are not required if both parties agree."
    },
    "custody": {
        "title": "Illinois Child Custody Process",
        "steps": [
            "File a Petition for Allocation of Parental Responsibilities (custody petition).",
            "Serve the other parent with the petition and any related motions.",
            "Complete required parenting classes if ordered by the court.",
            "Participate in mediation or a parenting plan conference.",
            "Attend a hearing; the judge issues an Allocation of Parental Responsibilities order."
        ],
        "timeline": "Typically 2‑18 months, depending on case load and dispute level.",
        "forms": ["Petition for Allocation of Parental Responsibilities", "Parenting Plan", "Child Support Worksheet"],
        "notes": "The best interests of the child standard guides all decisions; documentation of parental involvement helps."
    },
    "debt_collection": {
        "title": "Debt Collection Defense Process",
        "steps": [
            "Review the complaint and verify the debt’s validity and amount.",
            "Send a Debt Validation Letter to the creditor within 30 days of service.",
            "If the creditor fails to validate, file a Motion to Dismiss for Lack of Jurisdiction or Improper Service.",
            "Prepare and submit an Answer to the Complaint, asserting any defenses (e.g., statute of limitations).",
            "If the case proceeds, engage in settlement negotiations or prepare for trial."
        ],
        "timeline": "30 days for validation; overall case may extend several months.",
        "forms": ["Debt Validation Letter", "Answer to Complaint", "Motion to Dismiss"],
        "notes": "Act quickly; many defenses are lost if not raised within statutory periods."
    },
    "identity_theft": {
        "title": "Identity Theft Response Process",
        "steps": [
            "File a report with the Federal Trade Commission (FTC) at identitytheft.gov.",
            "Place a fraud alert on credit reports with the major credit bureaus.",
            "Report the theft to local law enforcement and obtain a police report.",
            "Dispute fraudulent accounts with each creditor using FTC‑provided letters.",
            "Monitor credit reports for 12 months and consider a credit freeze if needed."
        ],
        "timeline": "Immediate for FTC report; monitoring continues for at least a year.",
        "forms": ["FTC Identity Theft Report", "Fraud Alert Request", "Police Report", "Credit Dispute Letter"],
        "notes": "Keep copies of all correspondence; the FTC offers a recovery plan checklist."
    }
}

def get_template(topic: str):
    """Return the template dict for a given topic or None if not found."""
    key = topic.lower().replace(" ", "_")
    return templates.get(key)

TEMPLATE_TOPICS = templates

TEMPLATE_TOPICS = templates
