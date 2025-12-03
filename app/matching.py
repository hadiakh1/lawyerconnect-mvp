"""
Advanced lawyer matching algorithm that considers multiple factors:
- Case type (category match)
- Client profile (budget, urgency, pricing preference)
- Lawyer specialization
- Lawyer success rate
- Availability
- Pricing compatibility
"""
from typing import List, Tuple, Dict
from .models import LawyerProfile, Issue


def calculate_match_score(lawyer: LawyerProfile, issue: Issue) -> Tuple[float, Dict[str, float]]:
    """
    Calculate a match score (0-100) for a lawyer-issue pair.
    Returns: (total_score, breakdown_dict)
    """
    breakdown = {}
    total_score = 0.0
    
    # 1. Case Type Match (30% weight) - Most important
    case_type_score = calculate_case_type_match(lawyer, issue)
    breakdown['case_type'] = case_type_score
    total_score += case_type_score * 0.30
    
    # 2. Lawyer Specialization (20% weight)
    specialization_score = calculate_specialization_score(lawyer, issue)
    breakdown['specialization'] = specialization_score
    total_score += specialization_score * 0.20
    
    # 3. Success Rate (15% weight)
    success_rate_score = lawyer.case_success_rate * 100  # Convert 0-1 to 0-100
    breakdown['success_rate'] = success_rate_score
    total_score += success_rate_score * 0.15
    
    # 4. Availability (15% weight)
    availability_score = calculate_availability_score(lawyer)
    breakdown['availability'] = availability_score
    total_score += availability_score * 0.15
    
    # 5. Pricing Compatibility (15% weight)
    pricing_score = calculate_pricing_compatibility(lawyer, issue)
    breakdown['pricing'] = pricing_score
    total_score += pricing_score * 0.15
    
    # 6. Client Profile Match (5% weight) - Additional factors
    profile_score = calculate_client_profile_match(lawyer, issue)
    breakdown['client_profile'] = profile_score
    total_score += profile_score * 0.05
    
    return round(total_score, 2), breakdown


def calculate_case_type_match(lawyer: LawyerProfile, issue: Issue) -> float:
    """Score based on how well lawyer's expertise matches the case category."""
    lawyer_categories = [c.strip().lower() for c in lawyer.categories_list()]
    issue_category = issue.category.lower()
    
    # Exact match = 100 points
    if issue_category in lawyer_categories:
        return 100.0
    
    # Partial match (category contains issue or vice versa) = 70 points
    for cat in lawyer_categories:
        if issue_category in cat or cat in issue_category:
            return 70.0
    
    # Related categories = 40 points (you can expand this logic)
    related_categories = {
        'harassment': ['workplace discrimination', 'domestic violence'],
        'workplace discrimination': ['harassment'],
        'domestic violence': ['family disputes', 'harassment'],
        'family disputes': ['domestic violence'],
        'property issues': ['fraud'],
        'fraud': ['property issues'],
    }
    
    if issue_category in related_categories:
        for related in related_categories[issue_category]:
            if related in lawyer_categories:
                return 40.0
    
    return 0.0


def calculate_specialization_score(lawyer: LawyerProfile, issue: Issue) -> float:
    """Score based on lawyer's specialization depth and rating."""
    # Base score from rating (0-5 scale converted to 0-100)
    rating_score = (lawyer.rating / 5.0) * 100
    
    # Bonus for having multiple relevant categories
    lawyer_categories = [c.strip().lower() for c in lawyer.categories_list()]
    issue_category = issue.category.lower()
    
    if issue_category in lawyer_categories:
        # If lawyer specializes in this exact category, give full rating score
        return min(rating_score, 100.0)
    else:
        # If not exact match, reduce by 30%
        return rating_score * 0.7


def calculate_availability_score(lawyer: LawyerProfile) -> float:
    """Score based on lawyer's availability."""
    if not lawyer.is_available_for_new_case():
        return 0.0
    
    # Calculate availability percentage
    if lawyer.max_cases == 0:
        return 100.0  # No limit
    
    capacity_used = lawyer.current_cases / lawyer.max_cases
    availability_pct = (1.0 - capacity_used) * 100
    
    # Prefer lawyers with more capacity (but don't penalize too much)
    if capacity_used < 0.5:
        return 100.0  # Less than 50% capacity = full score
    elif capacity_used < 0.8:
        return 80.0  # 50-80% capacity = good score
    else:
        return 60.0  # 80-100% capacity = lower but still available


def calculate_pricing_compatibility(lawyer: LawyerProfile, issue: Issue) -> float:
    """Score based on pricing compatibility between lawyer and client budget."""
    client_budget_min = issue.budget_min
    client_budget_max = issue.budget_max
    preferred_pricing = issue.preferred_pricing.lower()
    
    score = 0.0
    
    # Check if pricing models match
    if preferred_pricing == "hourly":
        if lawyer.hourly_rate > 0:
            # Estimate: assume 10-40 hours for typical case
            estimated_min = lawyer.hourly_rate * 10
            estimated_max = lawyer.hourly_rate * 40
            
            if estimated_min <= client_budget_max and estimated_max >= client_budget_min:
                # Budget overlaps
                overlap = min(estimated_max, client_budget_max) - max(estimated_min, client_budget_min)
                total_range = max(estimated_max, client_budget_max) - min(estimated_min, client_budget_min)
                score = (overlap / total_range) * 100 if total_range > 0 else 50.0
            else:
                # Budget doesn't overlap - calculate distance
                if estimated_min > client_budget_max:
                    diff = estimated_min - client_budget_max
                    score = max(0, 50 - (diff / client_budget_max) * 50) if client_budget_max > 0 else 0
                else:
                    diff = client_budget_min - estimated_max
                    score = max(0, 50 - (diff / client_budget_min) * 50) if client_budget_min > 0 else 0
    
    elif preferred_pricing == "fixed":
        if lawyer.fixed_rate_min > 0 or lawyer.fixed_rate_max > 0:
            lawyer_min = lawyer.fixed_rate_min if lawyer.fixed_rate_min > 0 else lawyer.fixed_rate_max * 0.5
            lawyer_max = lawyer.fixed_rate_max if lawyer.fixed_rate_max > 0 else lawyer.fixed_rate_min * 2
            
            if lawyer_min <= client_budget_max and lawyer_max >= client_budget_min:
                overlap = min(lawyer_max, client_budget_max) - max(lawyer_min, client_budget_min)
                total_range = max(lawyer_max, client_budget_max) - min(lawyer_min, client_budget_min)
                score = (overlap / total_range) * 100 if total_range > 0 else 50.0
            else:
                score = 30.0  # Partial match
    
    elif preferred_pricing == "contingency":
        if lawyer.accepts_contingency:
            score = 100.0  # Perfect match
        else:
            score = 20.0  # Lawyer doesn't accept contingency
    
    # If no pricing preference or lawyer doesn't offer preferred model, give neutral score
    if score == 0.0:
        score = 50.0  # Neutral score
    
    return min(score, 100.0)


def calculate_client_profile_match(lawyer: LawyerProfile, issue: Issue) -> float:
    """Score based on client profile factors (urgency, location, etc.)."""
    score = 50.0  # Base score
    
    # Urgency matching (lawyers with higher success rates might handle urgent cases better)
    if issue.urgency in ["high", "urgent"]:
        if lawyer.case_success_rate >= 0.85:
            score += 30.0  # High success rate lawyers for urgent cases
        elif lawyer.case_success_rate >= 0.75:
            score += 15.0
    
    # Location matching (if same city, bonus)
    # This is a placeholder - you can add user location to Issue model if needed
    # if lawyer.city and issue.user.city and lawyer.city == issue.user.city:
    #     score += 20.0
    
    return min(score, 100.0)


def match_lawyers_to_issue(issue: Issue, all_lawyers: List[LawyerProfile]) -> List[Tuple[LawyerProfile, float, Dict[str, float]]]:
    """
    Match lawyers to an issue and return sorted list of (lawyer, score, breakdown).
    Returns top matches sorted by score (highest first).
    """
    matches = []
    
    for lawyer in all_lawyers:
        if not lawyer.user or not lawyer.user.is_lawyer:
            continue
        
        score, breakdown = calculate_match_score(lawyer, issue)
        matches.append((lawyer, score, breakdown))
    
    # Sort by score (highest first)
    matches.sort(key=lambda x: x[1], reverse=True)
    
    return matches

