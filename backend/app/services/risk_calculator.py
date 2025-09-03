from typing import List, Tuple


def calculate_risk_score(risk_data: dict) -> Tuple[str, float, List[str]]:
    """Calculate risk score based on input parameters"""
    score = 0.0
    recommendations = []
    
    # Amount-based risk calculation
    amount = risk_data.get('amount', 0)
    if amount > 1000000:
        score += 3.0
        recommendations.append("Large loan amount requires additional collateral")
    elif amount > 500000:
        score += 2.0
        recommendations.append("Moderate loan amount, ensure stable income verification")
    elif amount > 100000:
        score += 1.0
        recommendations.append("Standard verification process recommended")
    else:
        recommendations.append("Low amount loan, expedited processing possible")
    
    # Company size impact
    company_size = risk_data.get('company_size', '')
    if company_size == 'startup':
        score += 2.5
        recommendations.append("Startup requires business plan review and market analysis")
    elif company_size == 'small':
        score += 1.5
        recommendations.append("Small business requires financial history review")
    elif company_size == 'medium':
        score += 1.0
        recommendations.append("Medium business shows good stability")
    elif company_size == 'large':
        score += 0.5
        recommendations.append("Large business shows strong stability")
    else:
        recommendations.append("Enterprise level shows excellent stability")
    
    # Industry risk assessment
    industry = risk_data.get('industry', '')
    high_risk_industries = ['real_estate', 'retail']
    medium_risk_industries = ['technology', 'consulting']
    low_risk_industries = ['healthcare', 'education', 'finance']
    
    if industry in high_risk_industries:
        score += 2.0
        recommendations.append("High-risk industry requires additional documentation")
    elif industry in medium_risk_industries:
        score += 1.0
        recommendations.append("Medium-risk industry, standard review process")
    elif industry in low_risk_industries:
        score += 0.5
        recommendations.append("Low-risk industry, favorable conditions")
    
    # Years in business
    years_in_business = risk_data.get('years_in_business', 0)
    if years_in_business < 1:
        score += 3.0
        recommendations.append("New business requires extensive financial review")
    elif years_in_business < 3:
        score += 2.0
        recommendations.append("Young business requires careful evaluation")
    elif years_in_business < 10:
        score += 1.0
        recommendations.append("Established business with good track record")
    else:
        recommendations.append("Well-established business with strong history")
    
    # Annual revenue assessment
    annual_revenue = risk_data.get('annual_revenue', 0)
    if annual_revenue < 100000:
        score += 2.5
        recommendations.append("Low revenue requires additional income verification")
    elif annual_revenue < 500000:
        score += 1.5
        recommendations.append("Moderate revenue, verify growth trends")
    elif annual_revenue < 1000000:
        score += 1.0
        recommendations.append("Good revenue base, standard process")
    else:
        recommendations.append("Strong revenue base, favorable terms possible")
    
    # Credit history impact
    credit_score = risk_data.get('credit_score', 700)
    if credit_score < 600:
        score += 3.0
        recommendations.append("Poor credit score requires cosigner or additional collateral")
    elif credit_score < 700:
        score += 2.0
        recommendations.append("Fair credit score, standard interest rates apply")
    elif credit_score < 800:
        score += 1.0
        recommendations.append("Good credit score, competitive rates available")
    else:
        recommendations.append("Excellent credit score, best rates available")
    
    # Determine risk level
    if score <= 3.0:
        risk_level = "LOW"
    elif score <= 6.0:
        risk_level = "MEDIUM"
    elif score <= 9.0:
        risk_level = "HIGH"
    else:
        risk_level = "VERY_HIGH"
    
    return risk_level, round(score, 2), recommendations
