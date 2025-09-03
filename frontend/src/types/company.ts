export interface Company {
  id: number;
  name: string;
  email: string;
  phone: string;
  industry: string;
  annual_revenue: number;
  company_size: number;
  owner_id: number;
  created_at: string;
}

export interface CreateCompanyData {
  name: string;
  email: string;
  phone: string;
  industry: string;
  annual_revenue: number;
  company_size: number;
}

export interface CompanyFormData extends CreateCompanyData {}
