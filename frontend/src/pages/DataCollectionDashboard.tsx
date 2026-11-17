import React, { useState, useEffect } from 'react';
import { Company, CollectionJob, DiscoveredDocument, CompanyCatalogItem } from '../types';
import { api } from '../api/client';
import {
  CloudDownload, RefreshCw, Search, CheckCircle2, AlertTriangle,
  XCircle, Clock, ExternalLink, ShieldAlert, FileText, Database, ArrowRight
} from 'lucide-react';

interface DataCollectionDashboardProps {
  company: Company | null;
  onRefreshCompanyData: () => void;
}

export const DataCollectionDashboard: React.FC<DataCollectionDashboardProps> = ({
  company,
  onRefreshCompanyData
}) => {
  const [jobs, setJobs] = useState<CollectionJob[]>([]);
  const [discoveredDocs, setDiscoveredDocs] = useState<DiscoveredDocument[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [isCollecting, setIsCollecting] = useState<boolean>(false);

  // Configuration options
  const [selectedSources, setSelectedSources] = useState<string[]>([
    'SEC EDGAR', 'NSE/BSE Filings', 'Company IR'
  ]);
  const [selectedYears, setSelectedYears] = useState<number[]>([2023, 2024, 2025]);
  const [selectedCategories, setSelectedCategories] = useState<string[]>([
    'Annual Report', 'Quarterly Report', 'Sustainability Report / BRSR'
  ]);

  // Catalog Search Modal
  const [catalogQuery, setCatalogQuery] = useState<string>('');
  const [catalogResults, setCatalogResults] = useState<CompanyCatalogItem[]>([]);
  const [showCatalog, setShowCatalog] = useState<boolean>(false);

  useEffect(() => {
    if (!company) return;
    loadCollectionData(company.id);
  }, [company]);

  const loadCollectionData = async (companyId: number) => {
    setLoading(true);
    try {
      const [jobList, docList] = await Promise.all([
        api.getCollectionJobs(companyId),
        api.getDiscoveredDocuments(companyId)
      ]);
      setJobs(jobList);
      setDiscoveredDocs(docList);
    } catch (err) {
      console.error('Failed to load collection data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTriggerCollection = async () => {
    if (!company) return;
    setIsCollecting(true);
    try {
      await api.triggerCollection({
        company_id: company.id,
        sources: selectedSources,
        fiscal_years: selectedYears,
        document_categories: selectedCategories
      });
      // Poll after 2 seconds
      setTimeout(() => {
        loadCollectionData(company.id);
        onRefreshCompanyData();
        setIsCollecting(false);
      }, 2500);
    } catch (err) {
      console.error('Collection trigger failed:', err);
      setIsCollecting(false);
    }
  };

  const handleRetryJob = async (jobId: number) => {
    try {
      await api.retryCollectionJob(jobId);
      if (company) loadCollectionData(company.id);
    } catch (err) {
      console.error('Retry failed:', err);
    }
  };

  const handleSearchCatalog = async () => {
    try {
      const results = await api.searchCatalog(catalogQuery);
      setCatalogResults(results);
    } catch (err) {
      console.error('Catalog search failed:', err);
    }
  };

  const handleImportCompany = async (ticker: string) => {
    try {
      await api.importCatalogCompany(ticker);
      onRefreshCompanyData();
      setShowCatalog(false);
    } catch (err) {
      console.error('Import failed:', err);
    }
  };

  if (!company) {
    return <div className="p-8 text-center text-slate-500">Please select a company first.</div>;
  }

  const latestJob = jobs.length > 0 ? jobs[0] : null;
  const warnings: string[] = latestJob && latestJob.validation_warnings_json
    ? JSON.parse(latestJob.validation_warnings_json)
    : [];

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-2xs flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-900 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
              Automated Data Pipeline
            </span>
            <span className="text-xs text-slate-400">•</span>
            <span className="text-xs text-slate-500">SEC EDGAR • NSE • BSE • Official IR</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mt-1">Automated Data Collection & Acquisition</h1>
          <p className="text-xs text-slate-600 max-w-2xl mt-1">
            Collect real audited financials, XBRL facts, sustainability reports (BRSR), and corporate disclosures directly from verified sources.
          </p>
        </div>
        <div className="mt-4 md:mt-0 flex items-center space-x-3">
          <button
            onClick={() => {
              setShowCatalog(true);
              handleSearchCatalog();
            }}
            className="flex items-center space-x-1.5 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold px-3 py-2 rounded-lg border border-slate-300 transition"
          >
            <Search className="w-3.5 h-3.5" />
            <span>Discover Public Companies</span>
          </button>
          <button
            onClick={handleTriggerCollection}
            disabled={isCollecting}
            className={`flex items-center space-x-1.5 text-white text-xs font-semibold px-4 py-2 rounded-lg shadow-2xs transition ${
              isCollecting ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-900 hover:bg-blue-800'
            }`}
          >
            <CloudDownload className={`w-3.5 h-3.5 ${isCollecting ? 'animate-bounce' : ''}`} />
            <span>{isCollecting ? 'Collecting Data...' : 'Collect Data'}</span>
          </button>
        </div>
      </div>

      {/* Pipeline Execution Controls */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
        <h2 className="text-sm font-bold text-slate-900 mb-3">Collection Target Parameters: {company.name}</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
          {/* Sources */}
          <div>
            <label className="block font-semibold text-slate-700 mb-2">Sources to Query:</label>
            <div className="space-y-1.5">
              {['SEC EDGAR', 'NSE/BSE Filings', 'Company IR'].map(s => (
                <label key={s} className="flex items-center space-x-2 text-slate-700 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedSources.includes(s)}
                    onChange={(e) => {
                      if (e.target.checked) setSelectedSources([...selectedSources, s]);
                      else setSelectedSources(selectedSources.filter(x => x !== s));
                    }}
                    className="rounded text-blue-900 focus:ring-0"
                  />
                  <span>{s}</span>
                </label>
              ))}
            </div>
            {company.cik && (
              <span className="inline-block mt-2 text-[10px] bg-slate-100 px-2 py-0.5 rounded text-slate-600">
                Registered SEC CIK: <b>{company.cik}</b>
              </span>
            )}
          </div>

          {/* Fiscal Years */}
          <div>
            <label className="block font-semibold text-slate-700 mb-2">Fiscal Years:</label>
            <div className="flex flex-wrap gap-2">
              {[2022, 2023, 2024, 2025, 2026].map(y => (
                <button
                  key={y}
                  type="button"
                  onClick={() => {
                    if (selectedYears.includes(y)) setSelectedYears(selectedYears.filter(x => x !== y));
                    else setSelectedYears([...selectedYears, y]);
                  }}
                  className={`px-3 py-1 rounded-md text-xs font-semibold border transition ${
                    selectedYears.includes(y)
                      ? 'bg-blue-900 text-white border-blue-900'
                      : 'bg-slate-50 text-slate-600 border-slate-300 hover:bg-slate-100'
                  }`}
                >
                  FY{y}
                </button>
              ))}
            </div>
          </div>

          {/* Document Types */}
          <div>
            <label className="block font-semibold text-slate-700 mb-2">Document Types:</label>
            <div className="space-y-1.5">
              {['Annual Report', 'Quarterly Report', 'Sustainability Report / BRSR'].map(cat => (
                <label key={cat} className="flex items-center space-x-2 text-slate-700 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={selectedCategories.includes(cat)}
                    onChange={(e) => {
                      if (e.target.checked) setSelectedCategories([...selectedCategories, cat]);
                      else setSelectedCategories(selectedCategories.filter(x => x !== cat));
                    }}
                    className="rounded text-blue-900 focus:ring-0"
                  />
                  <span>{cat}</span>
                </label>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Latest Execution Summary Cards */}
      {latestJob && (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <div className="bg-white p-3.5 rounded-xl border border-slate-200">
            <span className="text-[11px] text-slate-500 block">Job Status</span>
            <div className="flex items-center space-x-1.5 mt-1">
              {latestJob.status === 'COMPLETED' && <CheckCircle2 className="w-4 h-4 text-emerald-600" />}
              {latestJob.status === 'RUNNING' && <Clock className="w-4 h-4 text-amber-500 animate-spin" />}
              {latestJob.status === 'FAILED' && <XCircle className="w-4 h-4 text-rose-600" />}
              <span className="text-xs font-bold text-slate-900">{latestJob.status}</span>
            </div>
          </div>

          <div className="bg-white p-3.5 rounded-xl border border-slate-200">
            <span className="text-[11px] text-slate-500 block">Financial Records</span>
            <span className="text-lg font-bold text-slate-900">{latestJob.financial_records_extracted}</span>
          </div>

          <div className="bg-white p-3.5 rounded-xl border border-slate-200">
            <span className="text-[11px] text-slate-500 block">ESG Records</span>
            <span className="text-lg font-bold text-slate-900">{latestJob.esg_records_extracted}</span>
          </div>

          <div className="bg-white p-3.5 rounded-xl border border-slate-200">
            <span className="text-[11px] text-slate-500 block">Docs Discovered</span>
            <span className="text-lg font-bold text-slate-900">{latestJob.documents_discovered}</span>
          </div>

          <div className="bg-white p-3.5 rounded-xl border border-slate-200">
            <span className="text-[11px] text-slate-500 block">Docs Indexed</span>
            <span className="text-lg font-bold text-emerald-700">{latestJob.documents_downloaded}</span>
          </div>

          <div className="bg-white p-3.5 rounded-xl border border-slate-200">
            <span className="text-[11px] text-slate-500 block">Operations</span>
            <div className="text-xs font-semibold text-slate-900 mt-1">
              <span className="text-emerald-600">{latestJob.successful_operations} succ</span> /{' '}
              <span className="text-rose-600">{latestJob.failed_operations} fail</span>
            </div>
          </div>
        </div>
      )}

      {/* Validation Warnings & Reconciliation */}
      {warnings.length > 0 && (
        <div className="bg-amber-50 border border-amber-200 p-4 rounded-xl">
          <div className="flex items-center space-x-2 text-amber-800 font-bold text-xs mb-2">
            <AlertTriangle className="w-4 h-4" />
            <span>Data Validation & Reconciliation Warnings ({warnings.length}):</span>
          </div>
          <div className="space-y-1 text-xs text-amber-900">
            {warnings.map((w, idx) => (
              <div key={idx} className="flex items-start space-x-1.5">
                <span>•</span>
                <span>{w}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Discovered Corporate Documents Table */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-bold text-slate-900">Discovered Corporate Documents</h3>
            <p className="text-xs text-slate-500">Public filings discovered from SEC EDGAR, Stock Exchanges, and IR portals.</p>
          </div>
          <span className="text-xs font-medium text-slate-500">Total: {discoveredDocs.length}</span>
        </div>

        <div className="overflow-x-auto rounded-lg border border-slate-200">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-900 text-white font-semibold">
              <tr>
                <th className="px-4 py-2.5">Title</th>
                <th className="px-4 py-2.5">Type</th>
                <th className="px-4 py-2.5">Year</th>
                <th className="px-4 py-2.5">Source</th>
                <th className="px-4 py-2.5">Status</th>
                <th className="px-4 py-2.5">Source URL</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {discoveredDocs.map((doc) => (
                <tr key={doc.id} className="hover:bg-slate-50">
                  <td className="px-4 py-2.5 font-semibold text-slate-900">{doc.title}</td>
                  <td className="px-4 py-2.5 text-slate-600">{doc.document_type}</td>
                  <td className="px-4 py-2.5">{doc.fiscal_year ? `FY${doc.fiscal_year}` : '-'}</td>
                  <td className="px-4 py-2.5 text-slate-600">{doc.source_name}</td>
                  <td className="px-4 py-2.5">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-50 text-blue-800">
                      {doc.download_status}
                    </span>
                  </td>
                  <td className="px-4 py-2.5 text-blue-900 hover:underline max-w-xs truncate">
                    <a href={doc.source_url} target="_blank" rel="noreferrer" className="flex items-center space-x-1">
                      <span className="truncate">{doc.source_url}</span>
                      <ExternalLink className="w-3 h-3 shrink-0" />
                    </a>
                  </td>
                </tr>
              ))}
              {discoveredDocs.length === 0 && (
                <tr>
                  <td colSpan={6} className="text-center py-6 text-slate-400">
                    No documents discovered yet. Click "Collect Data" above to initiate source discovery.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Execution Logs Terminal */}
      {latestJob && latestJob.logs && (
        <div className="bg-slate-950 text-slate-200 p-4 rounded-xl border border-slate-800 font-mono text-[11px] leading-relaxed">
          <div className="flex items-center justify-between pb-2 mb-2 border-b border-slate-800 text-slate-400">
            <span>Execution Pipeline Terminal Logs (Job ID: #{latestJob.id})</span>
            <span className="text-emerald-400 font-semibold">{latestJob.status}</span>
          </div>
          <pre className="whitespace-pre-wrap overflow-x-auto max-h-48">{latestJob.logs}</pre>
        </div>
      )}

      {/* Catalog Search Modal */}
      {showCatalog && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-xl max-w-2xl w-full p-6 border border-slate-200">
            <div className="flex items-center justify-between pb-3 border-b border-slate-200 mb-4">
              <h3 className="text-base font-bold text-slate-900">Discover Public Companies</h3>
              <button onClick={() => setShowCatalog(false)} className="text-slate-400 hover:text-slate-600 text-sm font-bold">✕</button>
            </div>
            <div className="flex space-x-2 mb-4">
              <input
                type="text"
                placeholder="Search by ticker (e.g. AAPL, INFY, TCS, MSFT) or company name..."
                value={catalogQuery}
                onChange={(e) => setCatalogQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearchCatalog()}
                className="flex-1 border border-slate-300 rounded-lg px-3 py-2 text-xs focus:outline-hidden focus:border-blue-900"
              />
              <button
                onClick={handleSearchCatalog}
                className="bg-blue-900 hover:bg-blue-800 text-white text-xs font-semibold px-4 py-2 rounded-lg"
              >
                Search
              </button>
            </div>
            <div className="max-h-72 overflow-y-auto divide-y divide-slate-100 text-xs">
              {catalogResults.map((item) => (
                <div key={item.ticker} className="py-2.5 flex items-center justify-between">
                  <div>
                    <span className="font-bold text-slate-900">{item.name}</span>{' '}
                    <span className="text-slate-500">({item.ticker})</span>
                    <div className="text-[11px] text-slate-500">
                      Exchange: <b>{item.exchange}</b> • Sector: {item.sector} {item.cik ? `• CIK: ${item.cik}` : ''}
                    </div>
                  </div>
                  <button
                    onClick={() => handleImportCompany(item.ticker)}
                    className="bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-1 rounded text-xs font-semibold"
                  >
                    Import & Select
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
