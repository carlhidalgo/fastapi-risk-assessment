import { RiskAssessmentResponse, CreateRiskAssessmentData } from '../types/risk';
import { api } from './authService';

export class RiskService {
  static async assessRisk(assessmentData: CreateRiskAssessmentData): Promise<RiskAssessmentResponse> {
    const response = await api.post<RiskAssessmentResponse>(
      '/risk/assess',
      assessmentData
    );
    return response.data;
  }
}
