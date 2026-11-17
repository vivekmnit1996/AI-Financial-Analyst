import React, { useState, useEffect } from 'react';
import { Company } from './types';
import { api } from './api/client';
import { Navbar } from './components/Navbar';
import { Sidebar, NavTab } from './components/Sidebar';
import { OverviewDashboard } from './pages/OverviewDashboard';
import { DataCollectionDashboard } from './pages/DataCollectionDashboard';
import { CompanyManagement } from './pages/CompanyManagement';
import { FinancialAnalysis } from './pages/FinancialAnalysis';
import { DocumentManagement } from './pages/DocumentManagement';
import { AIAssistantChat } from './pages/AIAssistantChat';
import { ESGAnalysis } from './pages/ESGAnalysis';
import { CompanyComparison } from './pages/CompanyComparison';
import { ReportsManagement } from './pages/ReportsManagement';
import { SystemSettings } from './pages/SystemSettings';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<NavTab>('overview');
  const [companies, setCompanies] = useState<Company[]>([]);
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);
  const [llmProvider, setLlmProvider] = useState<string>('deterministic');
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    setLoading(true);
    try {
      const [compList, settingsData] = await Promise.all([
        api.getCompanies(),
        api.getSettings()
      ]);
      setCompanies(compList);
      setLlmProvider(settingsData.llm_provider);

      if (compList.length > 0) {
        // Default to TCS or first available
        const defaultComp = compList.find(c => c.ticker === 'TCS') || compList[0];
        setSelectedCompany(defaultComp);
      }
    } catch (err) {
      console.error('Initial data load failed:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectCompany = (comp: Company) => {
    setSelectedCompany(comp);
  };

  const handleRefreshCompanies = async () => {
    try {
      const compList = await api.getCompanies();
      setCompanies(compList);
      if (selectedCompany) {
        const updated = compList.find(c => c.id === selectedCompany.id);
        if (updated) setSelectedCompany(updated);
      }
    } catch (err) {
      console.error('Refresh companies failed:', err);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col font-sans">
      {/* Top Navigation */}
      <Navbar
        companies={companies}
        selectedCompany={selectedCompany}
        onSelectCompany={handleSelectCompany}
        llmProvider={llmProvider}
      />

      {/* Main Container */}
      <div className="flex-1 flex overflow-hidden">
        {/* Navigation Sidebar */}
        <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />

        {/* Content Body */}
        <main className="flex-1 overflow-y-auto p-6 md:p-8 max-w-7xl mx-auto w-full">
          {loading ? (
            <div className="flex items-center justify-center h-64 text-slate-400 text-xs">
              <span className="w-2.5 h-2.5 rounded-full bg-blue-900 animate-pulse mr-2"></span>
              Initializing AI Financial Analyst System...
            </div>
          ) : (
            <>
              {activeTab === 'overview' && (
                <OverviewDashboard company={selectedCompany} onNavigate={setActiveTab} />
              )}
              {activeTab === 'collection' && (
                <DataCollectionDashboard
                  company={selectedCompany}
                  onRefreshCompanyData={handleRefreshCompanies}
                />
              )}
              {activeTab === 'companies' && (
                <CompanyManagement
                  companies={companies}
                  selectedCompany={selectedCompany}
                  onSelectCompany={handleSelectCompany}
                  onRefresh={handleRefreshCompanies}
                />
              )}
              {activeTab === 'financials' && (
                <FinancialAnalysis company={selectedCompany} />
              )}
              {activeTab === 'documents' && (
                <DocumentManagement company={selectedCompany} />
              )}
              {activeTab === 'chat' && (
                <AIAssistantChat company={selectedCompany} />
              )}
              {activeTab === 'esg' && (
                <ESGAnalysis company={selectedCompany} />
              )}
              {activeTab === 'comparison' && (
                <CompanyComparison companies={companies} />
              )}
              {activeTab === 'reports' && (
                <ReportsManagement company={selectedCompany} />
              )}
              {activeTab === 'settings' && (
                <SystemSettings onSettingsUpdated={loadInitialData} />
              )}
            </>
          )}
        </main>
      </div>
    </div>
  );
};
