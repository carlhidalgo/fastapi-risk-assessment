export interface RiskInputs {
  annual_revenue: number;
  credit_score: number;
  debt_to_equity_ratio: number;
  employee_count: number;
  years_in_business: number;
  cash_flow: number;
  industry_risk_factor: number;
}

export interface RiskRequest {
  id: string;
  company_id: string;
  amount: number;
  purpose: string;
  risk_inputs: RiskInputs;
  risk_score: number;
  status: 'pending' | 'approved' | 'rejected';
  risk_level: string;
  recommendations?: string;
  approved?: boolean;
  created_at: string;
  updated_at?: string;
}

export interface CreateRequestData {
  company_id: string;
  amount: number;
  purpose: string;
  risk_inputs: RiskInputs;
}

export interface RequestStatistics {
  total_requests: number;
  approved_requests: number;
  rejected_requests: number;
  pending_requests: number;
  total_amount_requested: number;
  approval_rate: number;
}

export interface RequestFormData {
  company_id: string;
  amount: number;
  purpose: string;
  annual_revenue: number;
  credit_score: number;
  debt_to_equity_ratio: number;
  employee_count: number;
  years_in_business: number;
  cash_flow: number;
  industry_risk_factor: number;
}
