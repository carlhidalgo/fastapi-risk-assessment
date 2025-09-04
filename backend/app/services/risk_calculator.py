from typing import List, Tuple
from app.schemas.schemas import RiskRequest, RiskResponse


def safe_get_numeric(data: dict, key: str, default: float = 0) -> float:
    """Safely get numeric value from dict, handling None values"""
    value = data.get(key, default)
    return default if value is None else float(value)


def calculate_risk_score(data: RiskRequest) -> RiskResponse:
    """
    Calculate risk score based on business metrics
    Returns a score from 0-100 and risk assessment
    """
    score = 0
    recommendations = []
    
    # 1. FACTOR INGRESOS (30 puntos máximo)
    if data.annual_revenue and data.amount:
        ratio = data.amount / data.annual_revenue
        if ratio <= 0.3:  # Excelente
            score += 30
            recommendations.append("Excelente ratio préstamo/ingresos, procesamiento expedito posible")
        elif ratio <= 0.5:  # Bueno
            score += 25
            recommendations.append("Ratio de préstamo aceptable para sus ingresos")
        elif ratio <= 0.7:  # Regular
            score += 15
            recommendations.append("La cantidad solicitada es alta en relación a sus ingresos")
        else:  # Pobre
            score += 5
            recommendations.append("Alto riesgo: cantidad del préstamo muy alta para sus ingresos")
    
    # 2. FACTOR EMPLEADOS (20 puntos máximo)
    if data.employee_count:
        if data.employee_count >= 50:
            score += 20
            recommendations.append("Empresa grande muestra excelente estabilidad")
        elif data.employee_count >= 11:
            score += 15
            recommendations.append("Empresa mediana muestra buena estabilidad")
        elif data.employee_count >= 5:
            score += 10
            recommendations.append("Empresa pequeña, considere mostrar planes de crecimiento")
        else:
            score += 5
            recommendations.append("Empresa muy pequeña, perfil de mayor riesgo")
    
    # 3. FACTOR AÑOS EN NEGOCIO (20 puntos máximo)
    if data.years_in_business:
        if data.years_in_business >= 10:
            score += 20
            recommendations.append("Empresa bien establecida con sólida trayectoria")
        elif data.years_in_business >= 5:
            score += 15
            recommendations.append("Empresa establecida con buen historial")
        elif data.years_in_business >= 2:
            score += 10
            recommendations.append("Empresa moderadamente establecida")
        else:
            score += 5
            recommendations.append("Empresa nueva, considere plan de negocio detallado")
    
    # 4. FACTOR SALUD FINANCIERA (15 puntos máximo)
    if data.debt_to_equity_ratio is not None:
        if data.debt_to_equity_ratio <= 0.5:
            score += 15
            recommendations.append("Excelente salud financiera")
        elif data.debt_to_equity_ratio <= 1.0:
            score += 10
            recommendations.append("Salud financiera moderada, verificar tendencias")
        else:
            score += 5
            recommendations.append("Alto ratio de deuda, considere reducción de deudas")
    
    # 5. FACTOR PUNTUACIÓN CREDITICIA (15 puntos máximo)
    if data.credit_score:
        if data.credit_score >= 750:
            score += 15
            recommendations.append("Excelente puntuación crediticia, tarifas competitivas disponibles")
        elif data.credit_score >= 650:
            score += 10
            recommendations.append("Buena puntuación crediticia, tarifas competitivas disponibles")
        else:
            score += 5
            recommendations.append("Puntuación crediticia regular, trabaje en mejorarla")
    
    # Determinar nivel de riesgo y aprobación
    if score >= 70:
        risk_level = "Bajo"
        approved = True
    elif score >= 50:
        risk_level = "Medio" 
        approved = True
    else:
        risk_level = "Alto"
        approved = False
    
    return RiskResponse(
        risk_score=score,
        risk_level=risk_level,
        approved=approved,
        recommendations=recommendations
    )


# Función legacy para compatibilidad hacia atrás
def calculate_risk_score_legacy(risk_data: dict) -> Tuple[str, float, List[str]]:
    """Legacy function for backward compatibility"""
    score = 0.0
    recommendations = []
    
    # Amount-based risk calculation
    amount = safe_get_numeric(risk_data, 'amount', 0)
    if amount > 1000000:
        score += 3.0
        recommendations.append("Cantidad de préstamo grande requiere garantías adicionales")
    elif amount > 500000:
        score += 2.0
        recommendations.append("Cantidad moderada, asegurar verificación de ingresos estables")
    elif amount > 100000:
        score += 1.0
        recommendations.append("Proceso de verificación estándar recomendado")
    else:
        recommendations.append("Préstamo de cantidad baja, procesamiento expedito posible")
    
    # Company size impact
    size_category = risk_data.get('size_category', 'medium')
    if size_category == 'startup':
        score += 2.5
        recommendations.append("Startup requiere revisión de plan de negocio")
    elif size_category == 'small':
        score += 1.5
        recommendations.append("Empresa pequeña requiere revisión de historial financiero")
    elif size_category == 'medium':
        score += 1.0
        recommendations.append("Empresa mediana muestra buena estabilidad")
    elif size_category == 'large':
        score += 0.5
        recommendations.append("Empresa grande muestra fuerte estabilidad")
    else:  # enterprise
        recommendations.append("Nivel empresarial muestra excelente estabilidad")
    
    # Determine risk level
    if score <= 3.0:
        risk_level = "BAJO"
    elif score <= 6.0:
        risk_level = "MEDIO"
    elif score <= 9.0:
        risk_level = "ALTO"
    else:
        risk_level = "MUY_ALTO"
    
    return risk_level, round(score, 2), recommendations
