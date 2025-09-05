#!/usr/bin/env python3
"""
Script para crear datos de prueba:
- 1 usuario de prueba
- 20 empresas
- 20 evaluaciones de riesgo
"""

import random
import sys
import os
from datetime import datetime, timedelta

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.company import Company
from app.models.request import Request
from app.core.security import get_password_hash

# Datos de empresas ficticias
COMPANIES_DATA = [
    {"name": "TechSolutions S.A.", "email": "contact@techsolutions.com", "phone": "+51-1-234-5678", "industry": "Tecnología", "annual_revenue": 5000000, "company_size": 150},
    {"name": "Constructora Andina Ltda.", "email": "info@constructoraandina.com", "phone": "+51-1-234-5679", "industry": "Construcción", "annual_revenue": 12000000, "company_size": 300},
    {"name": "Comercial del Norte S.A.C.", "email": "ventas@comercialnorte.com", "phone": "+51-1-234-5680", "industry": "Comercio", "annual_revenue": 3500000, "company_size": 80},
    {"name": "Transportes Rápidos E.I.R.L.", "email": "admin@transportesrapidos.com", "phone": "+51-1-234-5681", "industry": "Transporte", "annual_revenue": 2800000, "company_size": 120},
    {"name": "Industrias Metálicas S.A.", "email": "contacto@industriasmetalicas.com", "phone": "+51-1-234-5682", "industry": "Manufactura", "annual_revenue": 8500000, "company_size": 200},
    {"name": "Agropecuaria El Campo S.A.", "email": "info@elcampo.com", "phone": "+51-1-234-5683", "industry": "Agricultura", "annual_revenue": 4200000, "company_size": 90},
    {"name": "Servicios Financieros Plus", "email": "contacto@financierosplus.com", "phone": "+51-1-234-5684", "industry": "Finanzas", "annual_revenue": 15000000, "company_size": 250},
    {"name": "Textiles Modernos S.A.C.", "email": "ventas@textilesmodernos.com", "phone": "+51-1-234-5685", "industry": "Textil", "annual_revenue": 6700000, "company_size": 180},
    {"name": "Minera del Sur S.A.", "email": "info@minerasur.com", "phone": "+51-1-234-5686", "industry": "Minería", "annual_revenue": 25000000, "company_size": 500},
    {"name": "Restaurantes Gourmet S.A.", "email": "contacto@restaurantesgourmet.com", "phone": "+51-1-234-5687", "industry": "Restaurantes", "annual_revenue": 1800000, "company_size": 60},
    {"name": "Laboratorios Médicos S.A.", "email": "info@laboratoriosmedicos.com", "phone": "+51-1-234-5688", "industry": "Salud", "annual_revenue": 7500000, "company_size": 140},
    {"name": "Educación Superior S.A.C.", "email": "admin@educacionsuperior.com", "phone": "+51-1-234-5689", "industry": "Educación", "annual_revenue": 4800000, "company_size": 100},
    {"name": "Energía Renovable S.A.", "email": "contacto@energiarenovable.com", "phone": "+51-1-234-5690", "industry": "Energía", "annual_revenue": 18000000, "company_size": 220},
    {"name": "Inmobiliaria Premium Ltda.", "email": "ventas@inmobiliariapremium.com", "phone": "+51-1-234-5691", "industry": "Inmobiliaria", "annual_revenue": 9200000, "company_size": 75},
    {"name": "Consultora Estratégica S.A.", "email": "info@consultoraestrategy.com", "phone": "+51-1-234-5692", "industry": "Consultoría", "annual_revenue": 3200000, "company_size": 45},
    {"name": "Productos Químicos S.A.C.", "email": "contacto@productosquimicos.com", "phone": "+51-1-234-5693", "industry": "Química", "annual_revenue": 11500000, "company_size": 160},
    {"name": "Turismo Aventura S.A.", "email": "reservas@turismoaventura.com", "phone": "+51-1-234-5694", "industry": "Turismo", "annual_revenue": 2100000, "company_size": 35},
    {"name": "Telecomunicaciones Avanzadas", "email": "info@telecomavanzadas.com", "phone": "+51-1-234-5695", "industry": "Telecomunicaciones", "annual_revenue": 22000000, "company_size": 400},
    {"name": "Distribuidora Nacional S.A.", "email": "ventas@distribuidoranacional.com", "phone": "+51-1-234-5696", "industry": "Distribución", "annual_revenue": 14300000, "company_size": 280},
    {"name": "Servicios Logísticos S.A.C.", "email": "contacto@servicioslogisticos.com", "phone": "+51-1-234-5697", "industry": "Logística", "annual_revenue": 5900000, "company_size": 110}
]

# Propósitos de préstamos
LOAN_PURPOSES = [
    "Expansión de negocio",
    "Compra de maquinaria",
    "Capital de trabajo",
    "Refinanciamiento",
    "Construcción de planta",
    "Modernización tecnológica",
    "Adquisición de vehículos",
    "Inversión en inventario",
    "Desarrollo de productos",
    "Apertura de sucursal"
]

def generate_risk_inputs():
    """Genera inputs de riesgo aleatorios pero realistas"""
    credit_score = random.randint(300, 850)
    debt_to_income = round(random.uniform(0.1, 0.8), 2)
    collateral_value = random.randint(50000, 5000000)
    employment_length = random.randint(1, 25)
    
    return {
        "credit_score": credit_score,
        "debt_to_income": debt_to_income,
        "collateral_value": collateral_value,
        "employment_length": employment_length
    }

def calculate_risk_score(risk_inputs):
    """Calcula el puntaje de riesgo basado en los inputs"""
    score = 50  # Base score
    
    # Credit score impact (30% weight)
    if risk_inputs["credit_score"] >= 750:
        score -= 20
    elif risk_inputs["credit_score"] >= 650:
        score -= 10
    elif risk_inputs["credit_score"] >= 550:
        score += 10
    else:
        score += 25
    
    # Debt to income ratio impact (25% weight)
    if risk_inputs["debt_to_income"] <= 0.3:
        score -= 15
    elif risk_inputs["debt_to_income"] <= 0.5:
        score -= 5
    else:
        score += 20
    
    # Collateral value impact (20% weight)
    if risk_inputs["collateral_value"] >= 1000000:
        score -= 10
    elif risk_inputs["collateral_value"] >= 500000:
        score -= 5
    else:
        score += 10
    
    # Employment length impact (25% weight)
    if risk_inputs["employment_length"] >= 10:
        score -= 10
    elif risk_inputs["employment_length"] >= 5:
        score -= 5
    else:
        score += 15
    
    # Ensure score is within bounds
    return max(0, min(100, score))

def get_risk_level(risk_score):
    """Determina el nivel de riesgo basado en el puntaje"""
    if risk_score <= 30:
        return "BAJO"
    elif risk_score <= 70:
        return "MEDIO"
    else:
        return "ALTO"

def create_test_data():
    """Crea todos los datos de prueba"""
    print("🚀 Iniciando creación de datos de prueba...")
    
    # Recrear las tablas
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Crear sesión de base de datos
    db = SessionLocal()
    
    try:
        # 1. Crear o usar usuario de prueba existente
        print("👤 Verificando usuario de prueba...")
        test_user = db.query(User).filter(User.email == "admin@test.com").first()
        
        if test_user:
            print(f"✅ Usuario existente encontrado: {test_user.email}")
        else:
            test_user = User(
                email="admin@test.com",
                hashed_password=get_password_hash("admin123"),
                is_active=True
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            print(f"✅ Usuario creado: {test_user.email}")
        
        # 2. Crear 20 empresas
        print("🏢 Creando 20 empresas...")
        companies = []
        for i, company_data in enumerate(COMPANIES_DATA):
            company = Company(
                name=company_data["name"],
                email=company_data["email"],
                phone=company_data["phone"],
                industry=company_data["industry"],
                annual_revenue=company_data["annual_revenue"],
                company_size=company_data["company_size"],
                user_id=test_user.id
            )
            db.add(company)
            companies.append(company)
            print(f"  📝 {i+1}/20: {company.name}")
        
        db.commit()
        
        # Refresh companies to get their IDs
        for company in companies:
            db.refresh(company)
        
        print("✅ 20 empresas creadas exitosamente")
        
        # 3. Crear 20 evaluaciones de riesgo
        print("📊 Creando 20 evaluaciones de riesgo...")
        
        for i in range(20):
            # Seleccionar empresa aleatoria
            company = random.choice(companies)
            
            # Generar datos aleatorios
            risk_inputs = generate_risk_inputs()
            risk_score = calculate_risk_score(risk_inputs)
            risk_level = get_risk_level(risk_score)
            amount = random.randint(50000, 2000000)
            purpose = random.choice(LOAN_PURPOSES)
            approved = risk_score <= 70  # Aprobar si el riesgo es bajo o medio
            
            # Fecha aleatoria en los últimos 6 meses
            created_date = datetime.now() - timedelta(days=random.randint(1, 180))
            
            request = Request(
                company_id=str(company.id),
                amount=amount,
                purpose=purpose,
                risk_inputs=risk_inputs,
                risk_score=risk_score,
                risk_level=risk_level,
                approved=approved,
                created_at=created_date,
                user_id=test_user.id
            )
            
            db.add(request)
            
            status = "✅ APROBADO" if approved else "❌ RECHAZADO"
            print(f"  📈 {i+1}/20: {company.name} - ${amount:,} - Riesgo: {risk_score} ({risk_level}) - {status}")
        
        db.commit()
        print("✅ 20 evaluaciones de riesgo creadas exitosamente")
        
        # Resumen final
        print("\n🎉 ¡DATOS DE PRUEBA CREADOS EXITOSAMENTE!")
        print("=" * 50)
        print(f"👤 Usuario: admin@test.com")
        print(f"🔑 Contraseña: admin123")
        print(f"🏢 Empresas: 20")
        print(f"📊 Evaluaciones: 20")
        print("=" * 50)
        print("🌐 Puedes iniciar sesión en http://localhost:3000")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()
