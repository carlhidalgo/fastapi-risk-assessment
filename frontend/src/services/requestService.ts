import { RiskRequest, CreateRequestData, RequestStatistics, RequestFormData } from '../types/request';
import { api } from './authService';

export class RequestService {
  static async getRequests(params?: {
    page?: number;
    size?: number;
    search?: string;
    status?: string;
    risk_level?: string;
    min_amount?: number;
    max_amount?: number;
  }): Promise<{
    items: RiskRequest[];
    page: number;
    size: number;
    total: number;
    pages: number;
  }> {
    const queryParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          queryParams.append(key, value.toString());
        }
      });
    }
    
    const response = await api.get<{
      items: RiskRequest[];
      page: number;
      size: number;
      total: number;
      pages: number;
    }>(`/requests/?${queryParams.toString()}`);
    return response.data;
  }

  static async createRequest(requestData: CreateRequestData): Promise<RiskRequest> {
    const response = await api.post<RiskRequest>('/requests/', requestData);
    return response.data;
  }

  static async createRequestFromForm(formData: RequestFormData): Promise<RiskRequest> {
    const requestData: CreateRequestData = {
      company_id: formData.company_id,
      amount: formData.amount,
      purpose: formData.purpose,
      risk_inputs: {
        annual_revenue: formData.annual_revenue,
        credit_score: formData.credit_score,
        debt_to_equity_ratio: formData.debt_to_equity_ratio,
        employee_count: formData.employee_count,
        years_in_business: formData.years_in_business,
        cash_flow: formData.cash_flow,
        industry_risk_factor: formData.industry_risk_factor
      }
    };
    return this.createRequest(requestData);
  }

  static async getRequest(id: number): Promise<RiskRequest> {
    const response = await api.get<RiskRequest>(`/requests/${id}`);
    return response.data;
  }

  static async updateRequest(id: number, requestData: CreateRequestData): Promise<RiskRequest> {
    const response = await api.put<RiskRequest>(`/requests/${id}`, requestData);
    return response.data;
  }

  static async updateRequestFromForm(id: number, formData: RequestFormData): Promise<RiskRequest> {
    const requestData: CreateRequestData = {
      company_id: formData.company_id,
      amount: formData.amount,
      purpose: formData.purpose,
      risk_inputs: {
        annual_revenue: formData.annual_revenue,
        credit_score: formData.credit_score,
        debt_to_equity_ratio: formData.debt_to_equity_ratio,
        employee_count: formData.employee_count,
        years_in_business: formData.years_in_business,
        cash_flow: formData.cash_flow,
        industry_risk_factor: formData.industry_risk_factor
      }
    };
    return this.updateRequest(id, requestData);
  }

  static async deleteRequest(id: number): Promise<void> {
    await api.delete(`/requests/${id}`);
  }

  static async getRequestStatistics(): Promise<RequestStatistics> {
    const response = await api.get<RequestStatistics>('/requests/statistics');
    return response.data;
  }
}
