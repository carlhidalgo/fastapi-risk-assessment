export interface RiskAssessmentRequest {
  company_id: number;
  requested_amount: number;
  loan_term_months: number;
  purpose: string;
  collateral_value?: number;
  collateral_type?: string;
}

export interface RiskAssessmentResponse {
  company_id: number;
  requested_amount: number;
  loan_term_months: number;
  purpose: string;
  collateral_value?: number;
  collateral_type?: string;
  risk_score: number;
  risk_level: string;
  recommendation: string;
  approved: boolean;
  max_approved_amount?: number;
  created_at: string;
  id: number;
}

export interface CreateRiskAssessmentData extends RiskAssessmentRequest {}
