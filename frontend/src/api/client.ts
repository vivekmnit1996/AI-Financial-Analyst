import axios from 'axios';
import {
  Company, CompanyCatalogItem, FinancialRecord, FinancialAnalysis,
  ESGRecord, ESGScoreBreakdown, DocumentItem, QueryResponse,
  GeneratedReport, CollectionJob, DiscoveredDocument, SystemSettings
} from '../types';

const API_BASE = '/api/v1';

export const api = {
  // Companies
  getCompanies: async (): Promise<Company[]> => {
    const res = await axios.get(`${API_BASE}/companies`);
    return res.data;
  },
  createCompany: async (data: Partial<Company>): Promise<Company> => {
    const res = await axios.post(`${API_BASE}/companies`, data);
    return res.data;
  },
  deleteCompany: async (id: number): Promise<void> => {
    await axios.delete(`${API_BASE}/companies/${id}`);
  },
  searchCatalog: async (query: string = '', exchange?: string): Promise<CompanyCatalogItem[]> => {
    const res = await axios.get(`${API_BASE}/companies/discover/search`, {
      params: { query, exchange }
    });
    return res.data;
  },
  importCatalogCompany: async (ticker: string): Promise<Company> => {
    const res = await axios.post(`${API_BASE}/companies/discover/import`, null, {
      params: { ticker }
    });
    return res.data;
  },

  // Financial Data & Analysis
  getCompanyFinancials: async (companyId: number): Promise<FinancialRecord[]> => {
    const res = await axios.get(`${API_BASE}/financials/company/${companyId}`);
    return res.data;
  },
  getFinancialAnalysis: async (companyId: number): Promise<FinancialAnalysis> => {
    const res = await axios.get(`${API_BASE}/financials/analysis/${companyId}`);
    return res.data;
  },
  createFinancialRecord: async (data: Partial<FinancialRecord>): Promise<FinancialRecord> => {
    const res = await axios.post(`${API_BASE}/financials`, data);
    return res.data;
  },
  deleteFinancialRecord: async (id: number): Promise<void> => {
    await axios.delete(`${API_BASE}/financials/${id}`);
  },
  uploadFinancialCsv: async (companyId: number, file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('company_id', companyId.toString());
    formData.append('file', file);
    const res = await axios.post(`${API_BASE}/financials/upload-csv`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return res.data;
  },
  compareCompanies: async (companyIds: number[]): Promise<any[]> => {
    const res = await axios.get(`${API_BASE}/financials/comparison`, {
      params: { company_ids: companyIds.join(',') }
    });
    return res.data;
  },

  // Documents
  getDocuments: async (companyId?: number): Promise<DocumentItem[]> => {
    const res = await axios.get(`${API_BASE}/documents`, {
      params: companyId ? { company_id: companyId } : {}
    });
    return res.data;
  },
  uploadDocument: async (companyId: number, file: File, documentType: string, fiscalYear?: number): Promise<DocumentItem> => {
    const formData = new FormData();
    formData.append('company_id', companyId.toString());
    formData.append('document_type', documentType);
    if (fiscalYear) formData.append('fiscal_year', fiscalYear.toString());
    formData.append('file', file);

    const res = await axios.post(`${API_BASE}/documents/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return res.data;
  },
  deleteDocument: async (id: number): Promise<void> => {
    await axios.delete(`${API_BASE}/documents/${id}`);
  },

  // ESG
  getESGRecords: async (companyId: number): Promise<ESGRecord[]> => {
    const res = await axios.get(`${API_BASE}/esg/company/${companyId}`);
    return res.data;
  },
  getESGScoreBreakdown: async (companyId: number, fiscalYear?: number): Promise<ESGScoreBreakdown> => {
    const res = await axios.get(`${API_BASE}/esg/score/${companyId}`, {
      params: fiscalYear ? { fiscal_year: fiscalYear } : {}
    });
    return res.data;
  },
  createESGRecord: async (data: Partial<ESGRecord>): Promise<ESGRecord> => {
    const res = await axios.post(`${API_BASE}/esg`, data);
    return res.data;
  },

  // Automated Data Collection
  triggerCollection: async (payload: { company_id: number; sources: string[]; fiscal_years: number[]; document_categories: string[] }): Promise<CollectionJob> => {
    const res = await axios.post(`${API_BASE}/collection/trigger`, payload);
    return res.data;
  },
  getCollectionJobs: async (companyId?: number): Promise<CollectionJob[]> => {
    const res = await axios.get(`${API_BASE}/collection/jobs`, {
      params: companyId ? { company_id: companyId } : {}
    });
    return res.data;
  },
  getDiscoveredDocuments: async (companyId?: number): Promise<DiscoveredDocument[]> => {
    const res = await axios.get(`${API_BASE}/collection/discovered-docs`, {
      params: companyId ? { company_id: companyId } : {}
    });
    return res.data;
  },
  retryCollectionJob: async (jobId: number): Promise<CollectionJob> => {
    const res = await axios.post(`${API_BASE}/collection/retry/${jobId}`);
    return res.data;
  },

  // Chat & Query
  queryChat: async (payload: { query: string; company_id?: number; fiscal_year?: number; top_k?: number; enable_reranking?: boolean }): Promise<QueryResponse> => {
    const res = await axios.post(`${API_BASE}/chat/query`, payload);
    return res.data;
  },
  getChatHistory: async (companyId?: number): Promise<any[]> => {
    const res = await axios.get(`${API_BASE}/chat/history`, {
      params: companyId ? { company_id: companyId } : {}
    });
    return res.data;
  },

  // Reports
  generateReport: async (payload: { company_id: number; fiscal_year: number; report_type?: string; title?: string }): Promise<GeneratedReport> => {
    const res = await axios.post(`${API_BASE}/reports/generate`, payload);
    return res.data;
  },
  getReports: async (companyId?: number): Promise<GeneratedReport[]> => {
    const res = await axios.get(`${API_BASE}/reports`, {
      params: companyId ? { company_id: companyId } : {}
    });
    return res.data;
  },
  deleteReport: async (id: number): Promise<void> => {
    await axios.delete(`${API_BASE}/reports/${id}`);
  },

  // Settings & System
  getSettings: async (): Promise<SystemSettings> => {
    const res = await axios.get(`${API_BASE}/settings`);
    return res.data;
  },
  updateLLMSettings: async (payload: { llm_provider: string; gemini_api_key?: string; openai_api_key?: string; llm_model_name?: string }): Promise<any> => {
    const res = await axios.post(`${API_BASE}/settings/update-llm`, payload);
    return res.data;
  },
  getHealth: async (): Promise<any> => {
    const res = await axios.get(`${API_BASE}/settings/health`);
    return res.data;
  }
};
