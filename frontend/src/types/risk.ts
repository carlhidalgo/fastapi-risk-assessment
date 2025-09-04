export interface RiskAssessmentRequest {
  company_id: string;
  amount: number;
  purpose: string;
  annual_revenue?: number;
  employee_count?: number;
  years_in_business?: number;
  debt_to_equity_ratio?: number;
  credit_score?: number;
}

export interface RiskAssessmentResponse {
  risk_level: string;
  risk_score: number;
  recommendations: string[];
  approved: boolean;
}

export interface CreateRiskAssessmentData extends RiskAssessmentRequest {}
