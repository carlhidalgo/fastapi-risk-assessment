import { Company, CreateCompanyData } from '../types/company';
import { api } from './authService';

export class CompanyService {
  static async getCompanies(): Promise<Company[]> {
    const response = await api.get<Company[]>('/companies/');
    return response.data;
  }

  static async createCompany(companyData: CreateCompanyData): Promise<Company> {
    const response = await api.post<Company>('/companies/', companyData);
    return response.data;
  }

  static async getCompany(id: number): Promise<Company> {
    const response = await api.get<Company>(`/companies/${id}`);
    return response.data;
  }

  static async updateCompany(id: number, companyData: Partial<CreateCompanyData>): Promise<Company> {
    const response = await api.put<Company>(`/companies/${id}`, companyData);
    return response.data;
  }

  static async deleteCompany(id: number): Promise<void> {
    await api.delete(`/companies/${id}`);
  }
}
