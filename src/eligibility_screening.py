# src/eligibility_screening.py

def screen_client(name, annual_income, household_size, issue_type, county):
    """
    Screen client for Land of Lincoln Legal Aid eligibility.

    Returns eligibility status, priority level, and next steps.
    Uses 125% of Federal Poverty Guidelines (LSC requirement for legal aid).
    """

    # 2025 Federal Poverty Guidelines (single person, rest of US)
    fpl_2025 = {
        1: 15650,
        2: 21150,
        3: 26650,
        4: 32150,
        5: 37650,
        6: 43150,
        7: 48650,
        8: 54150,
    }

    # Legal aid organizations use 125% of FPL (LSC requirement)
    INCOME_MULTIPLIER = 1.25

    # Get income limit for household size
    base_fpl = fpl_2025.get(household_size, 37650)
    income_limit = base_fpl * INCOME_MULTIPLIER

    # Calculate poverty percentage
    poverty_percentage = (annual_income / income_limit) * 100

    # Determine eligibility
    eligible = annual_income <= income_limit

    # Determine priority level (for eviction cases)
    priority_level = None
    priority_description = None

    if issue_type.lower() == 'eviction':
        if poverty_percentage <= 75:
            priority_level = 'HIGH'
            priority_description = 'Immediate assistance recommended - at or below 75% of poverty limit'
        elif poverty_percentage <= 100:
            priority_level = 'MEDIUM'
            priority_description = 'Standard processing - between 75-100% of poverty limit'
        else:
            priority_level = 'LOW'
            priority_description = 'Below priority threshold but may qualify for other services'

    # Build response
    result = {
        'name': name,
        'eligible': eligible,
        'income_limit': income_limit,
        'annual_income': annual_income,
        'household_size': household_size,
        'poverty_percentage': poverty_percentage,
        'priority_level': priority_level,
        'priority_description': priority_description,
        'next_steps': []
    }

    if eligible:
        result['next_steps'] = [
            'Call Eviction Hotline: (855) 601-9474 (Mon-Fri 9am-4pm)',
            'Call LARC for legal advice: (877) 342-7891',
            'Bring proof of income and eviction notice to initial appointment'
        ]
    else:
        result['next_steps'] = [
            'Visit illinoislegalaid.org for self-help resources',
            'Check if you qualify for emergency assistance programs',
            'Contact local bar association for pro bono options'
        ]

    return result


def print_screening_result(result):
    """Print eligibility screening result in a formatted way."""
    print(f"\n{'='*60}")
    print(f"ELIGIBILITY SCREENING RESULT")
    print(f"{'='*60}")
    print(f"Name: {result['name']}")
    print(f"Annual Income: ${result['annual_income']:.2f}")
    print(f"Household Size: {result['household_size']}")
    print(f"Income Limit (125% FPL): ${result['income_limit']:.2f}")
    print(f"Poverty Percentage: {result['poverty_percentage']:.1f}%")
    print(f"\nEligible: {'✅ YES' if result['eligible'] else '❌ NO'}")

    if result.get('priority_level'):
        print(f"Priority Level: {result['priority_level']} - {result['priority_description']}")

    print(f"\nNext Steps:")
    for i, step in result['next_steps']:
        print(f"  {i}. {step}")

    print(f"{'='*60}\n")
