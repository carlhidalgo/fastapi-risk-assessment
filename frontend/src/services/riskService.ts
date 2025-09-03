import axios from 'axios';
import { RiskAssessmentResponse, CreateRiskAssessmentData } from '../types/risk';
import { API_CONFIG } from '../constants/config';

export class RiskService {
  private static baseURL = API_CONFIG.BASE_URL;

  static async assessRisk(assessmentData: CreateRiskAssessmentData): Promise<RiskAssessmentResponse> {
    const response = await axios.post<RiskAssessmentResponse>(
      `${this.baseURL}/risk/assess`,
      assessmentData
    );
    return response.data;
  }
}
