import axios from 'axios';
import { Company, CreateCompanyData } from '../types/company';
import { API_CONFIG } from '../constants/config';

export class CompanyService {
  private static baseURL = API_CONFIG.BASE_URL;

  static async getCompanies(): Promise<Company[]> {
    const response = await axios.get<Company[]>(`${this.baseURL}/companies/`);
    return response.data;
  }

  static async createCompany(companyData: CreateCompanyData): Promise<Company> {
    const response = await axios.post<Company>(`${this.baseURL}/companies/`, companyData);
    return response.data;
  }

  static async getCompany(id: number): Promise<Company> {
    const response = await axios.get<Company>(`${this.baseURL}/companies/${id}`);
    return response.data;
  }
}
