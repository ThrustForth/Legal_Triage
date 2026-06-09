#!/usr/bin/env python3
"""
Eligibility screening for legal aid clients.

This module provides functions to screen clients for legal aid eligibility
based on income, issue type, and geographic location.
"""

# 2024 Poverty Guidelines (annual income)
POVERTY_GUIDELINES = {
    1: 15060,
    2: 20440,
    3: 25820,
    4: 31200,
    5: 36580,
    6: 41960,
    7: 47340,
    8: 52720,
}

# For households larger than 8, add $5,380 for each additional person
ADDITIONAL_PERSON_AMOUNT = 5380

# Maximum income multiplier (125% of poverty line)
MAX_INCOME_MULTIPLIER = 1.25

# Services offered by the organization
SERVICES = {
    'eviction': True,
    'divorce': True,
    'custody': True,
    'debt collection': True,
    'identity theft': True,
    'housing': True,
    'consumer': True,
}

# Urgent issues (higher priority)
URGENT_ISSUES = {'eviction', 'custody'}

# Service areas
SERVICE_AREAS = {
    'cook county',
    'dupage county', 
    'lake county'
}


def get_poverty_line(household_size):
    """
    Get the poverty line for a given household size.
    
    Args:
        household_size (int): Number of people in household
        
    Returns:
        int: Annual poverty line amount
    """
    if household_size <= 8:
        return POVERTY_GUIDELINES.get(household_size, 0)
    else:
        # For households larger than 8
        base = POVERTY_GUIDELINES[8]
        additional = (household_size - 8) * ADDITIONAL_PERSON_AMOUNT
        return base + additional


def get_max_income(household_size):
    """
    Calculate maximum income for eligibility (125% of poverty line).
    
    Args:
        household_size (int): Number of people in household
        
    Returns:
        float: Maximum annual income for eligibility
    """
    poverty_line = get_poverty_line(household_size)
    return poverty_line * MAX_INCOME_MULTIPLIER


def screen_income(income, household_size):
    """
    Screen client based on income eligibility.
    
    Args:
        income (float): Client's annual income
        household_size (int): Number of people in household
        
    Returns:
        tuple: (eligible_bool, max_income_amount)
    """
    max_income = get_max_income(household_size)
    return income <= max_income, max_income


def screen_issue(issue):
    """
    Screen client based on whether organization handles the issue.
    
    Args:
        issue (str): Legal issue type
        
    Returns:
        bool: True if organization handles this issue
    """
    # Normalize issue for comparison
    issue_normalized = issue.lower().strip()
    return SERVICES.get(issue_normalized, False)


def screen_geographic(county):
    """
    Screen client based on geographic location.
    
    Args:
        county (str): Client's county
        
    Returns:
        bool: True if county is in service area
    """
    # Normalize county for comparison
    county_normalized = county.lower().strip()
    return county_normalized in SERVICE_AREAS


def determine_priority(issue, income_eligible, issue_eligible, geographic_eligible):
    """
    Determine priority level for eligible clients.
    
    Args:
        issue (str): Legal issue type
        income_eligible (bool): Whether client passes income screening
        issue_eligible (bool): Whether client passes issue screening
        geographic_eligible (bool): Whether client passes geographic screening
        
    Returns:
        int or None: Priority level (1=critical, 2=high, 3=normal) or None if ineligible
    """
    # If any screening failed, client is not eligible
    if not (income_eligible and issue_eligible and geographic_eligible):
        return None
    
    # Determine priority based on issue type
    issue_normalized = issue.lower().strip()
    if issue_normalized in URGENT_ISSUES:
        return 1  # Critical priority
    else:
        return 2  # High priority for non-urgent but eligible issues


def screen_client(name, income, household_size, issue, county):
    """
    Main function to screen a client for legal aid eligibility.
    
    Args:
        name (str): Client's name
        income (float): Client's annual income
        household_size (int): Number of people in household
        issue (str): Legal issue type
        county (str): Client's county
        
    Returns:
        dict: Screening results with eligibility status and details
    """
    # Screen each criterion
    income_eligible, max_income = screen_income(income, household_size)
    issue_eligible = screen_issue(issue)
    geographic_eligible = screen_geographic(county)
    
    # Determine overall eligibility
    eligible = income_eligible and issue_eligible and geographic_eligible
    
    # Determine priority (None if ineligible)
    priority = determine_priority(issue, income_eligible, issue_eligible, geographic_eligible)
    
    # Prepare result dictionary
    result = {
        'name': name,
        'eligible': eligible,
        'income_eligible': income_eligible,
        'max_income': round(max_income, 2),
        'issue_eligible': issue_eligible,
        'geographic_eligible': geographic_eligible,
        'priority': priority
    }
    
    return result


def print_screening_result(result):
    """
    Print a formatted version of the screening result.
    
    Args:
        result (dict): Result from screen_client function
    """
    print(f"Eligibility Screening Results for {result['name']}")
    print("=" * 50)
    print(f"Eligible: {'YES' if result['eligible'] else 'NO'}")
    print()
    
    if result['eligible']:
        print(" PASSED ALL CRITERIA")
        print(f"Priority Level: {result['priority']}")
        priority_names = {1: "Critical", 2: "High", 3: "Normal"}
        print(f"Priority Description: {priority_names.get(result['priority'], 'Unknown')}")
    else:
        print(" DID NOT MEET ALL REQUIREMENTS")
        print()
        print("Criteria Breakdown:")
        print(f"  Income Eligible: {'' if result['income_eligible'] else ''} "
              f"(Max: ${result['max_income']:,.2f})")
        print(f"  Issue Eligible:  {'' if result['issue_eligible'] else ''}")
        print(f"  Geographic Eligible: {'' if result['geographic_eligible'] else ''}")
        print()
        if not result['eligible']:
            print("Referral Information:")
            print("  Client may need to be referred to other legal services")
            print("  that specialize in their specific needs.")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Screen client for legal aid eligibility")
    parser.add_argument("--name", required=True, help="Client's name")
    parser.add_argument("--income", type=float, required=True, help="Client's annual income")
    parser.add_argument("--household", type=int, required=True, help="Number of people in household")
    parser.add_argument("--issue", required=True, help="Legal issue type")
    parser.add_argument("--county", required=True, help="Client's county")
    
    args = parser.parse_args()
    
    result = screen_client(
        name=args.name,
        income=args.income,
        household_size=args.household,
        issue=args.issue,
        county=args.county
    )
    
    print_screening_result(result)