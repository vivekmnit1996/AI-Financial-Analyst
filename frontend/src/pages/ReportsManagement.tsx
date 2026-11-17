import React, { useState, useEffect } from 'react';
import { Company, GeneratedReport } from '../types';
import { api } from '../api/client';
import {
  FileText, Download, ExternalLink, Trash2, Plus, Sparkles, CheckCircle2
} from 'lucide-react';

interface ReportsManagementProps {
  company: Company | null;
}

export const ReportsManagement: React.FC<ReportsManagementProps> = ({ company }) => {
  const [reports, setReports] = useState<GeneratedReport[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [fiscalYear, setFiscalYear] = useState<number>(2024);
  const [reportType, setReportType] = useState<string>('Comprehensive Financial & ESG');
  const [customTitle, setCustomTitle] = useState<string>('');

  useEffect(() => {
    loadReports();
  }, [company]);

  const loadReports = async () => {
    setLoading(true);
    try {
      const data = await api.getReports(company?.id);
      setReports(data);
    } catch (err) {
      console.error('Failed to load reports:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!company) return;
    setIsGenerating(true);
    try {
      await api.generateReport({
        company_id: company.id,
        fiscal_year: fiscalYear,
        report_type: reportType,
        title: customTitle || undefined
      });
      setIsGenerating(false);
      setCustomTitle('');
      loadReports();
    } catch (err: any) {
      alert(`Report generation failed: ${err.response?.data?.detail || err.message}`);
      setIsGenerating(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this generated report?')) return;
    try {
      await api.deleteReport(id);
      loadReports();
    } catch (err) {
      console.error('Failed to delete report:', err);
    }
  };

  if (!company) {
    return <div className="p-8 text-center text-slate-500">Please select a company first.</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-2xs">
        <div className="flex items-center space-x-2">
          <span className="text-xs font-bold uppercase tracking-wider text-blue-900 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
            Export Engine
          </span>
          <span className="text-xs text-slate-500">PDF & HTML Dossiers</span>
        </div>
        <h1 className="text-2xl font-bold text-slate-900 mt-1">Institutional Financial & ESG Reports</h1>
        <p className="text-xs text-slate-600 mt-0.5">
          Generate downloadable PDF reports (ReportLab) and responsive HTML dossiers with audited financial tables, ESG scoring breakdown, and page citations.
        </p>
      </div>

      {/* Generation Form */}
      <form onSubmit={handleGenerate} className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs space-y-4">
        <h2 className="text-sm font-bold text-slate-900 flex items-center space-x-2">
          <Sparkles className="w-4 h-4 text-blue-900" />
          <span>Generate New Dossier for {company.name}</span>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div>
            <label className="block font-semibold text-slate-700 mb-1">Fiscal Year</label>
            <input
              type="number"
              value={fiscalYear}
              onChange={e => setFiscalYear(Number(e.target.value))}
              className="w-full border border-slate-300 rounded-lg p-2 focus:outline-hidden focus:border-blue-900"
            />
          </div>
          <div>
            <label className="block font-semibold text-slate-700 mb-1">Report Type</label>
            <select
              value={reportType}
              onChange={e => setReportType(e.target.value)}
              className="w-full border border-slate-300 rounded-lg p-2 focus:outline-hidden focus:border-blue-900"
            >
              <option value="Comprehensive Financial & ESG">Comprehensive Financial & ESG</option>
              <option value="Financial Deep-Dive">Financial Deep-Dive</option>
              <option value="ESG Evaluation">ESG Evaluation</option>
            </select>
          </div>
          <div>
            <label className="block font-semibold text-slate-700 mb-1">Custom Title (Optional)</label>
            <input
              type="text"
              placeholder={`e.g. ${company.ticker} Annual Performance Review FY${fiscalYear}`}
              value={customTitle}
              onChange={e => setCustomTitle(e.target.value)}
              className="w-full border border-slate-300 rounded-lg p-2 focus:outline-hidden focus:border-blue-900"
            />
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button
            type="submit"
            disabled={isGenerating}
            className={`flex items-center space-x-1.5 text-white text-xs font-semibold px-4 py-2 rounded-lg transition shadow-2xs ${
              isGenerating ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-900 hover:bg-blue-800'
            }`}
          >
            <FileText className="w-4 h-4" />
            <span>{isGenerating ? 'Synthesizing & Generating...' : 'Generate PDF & HTML Report'}</span>
          </button>
        </div>
      </form>

      {/* Generated Reports Table */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
        <h2 className="text-sm font-bold text-slate-900 mb-3">Available Reports Library ({reports.length})</h2>
        <div className="overflow-x-auto rounded-lg border border-slate-200">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-900 text-white font-semibold">
              <tr>
                <th className="px-4 py-2.5">Title</th>
                <th className="px-4 py-2.5">Company</th>
                <th className="px-4 py-2.5">Year</th>
                <th className="px-4 py-2.5">Report Type</th>
                <th className="px-4 py-2.5">Generated Date</th>
                <th className="px-4 py-2.5 text-right">Downloads & Formats</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {reports.map((rep) => (
                <tr key={rep.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-semibold text-slate-900 flex items-center space-x-2">
                    <FileText className="w-4 h-4 text-blue-900 shrink-0" />
                    <span>{rep.title}</span>
                  </td>
                  <td className="px-4 py-3">{rep.company_name}</td>
                  <td className="px-4 py-3 font-medium">FY{rep.fiscal_year}</td>
                  <td className="px-4 py-3 text-slate-600">{rep.report_type}</td>
                  <td className="px-4 py-3 text-slate-500">{new Date(rep.created_at).toLocaleDateString()}</td>
                  <td className="px-4 py-3 text-right space-x-2">
                    <a
                      href={rep.pdf_url}
                      download
                      className="inline-flex items-center space-x-1 px-2.5 py-1 rounded bg-blue-50 text-blue-900 hover:bg-blue-100 font-semibold border border-blue-200"
                    >
                      <Download className="w-3 h-3" />
                      <span>PDF</span>
                    </a>
                    <a
                      href={rep.html_url}
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center space-x-1 px-2.5 py-1 rounded bg-slate-100 text-slate-700 hover:bg-slate-200 font-semibold border border-slate-300"
                    >
                      <ExternalLink className="w-3 h-3" />
                      <span>HTML</span>
                    </a>
                    <button
                      onClick={() => handleDelete(rep.id)}
                      className="p-1 text-slate-400 hover:text-rose-600 transition"
                      title="Delete report"
                    >
                      <Trash2 className="w-3.5 h-3.5 inline" />
                    </button>
                  </td>
                </tr>
              ))}
              {reports.length === 0 && (
                <tr>
                  <td colSpan={6} className="text-center py-8 text-slate-400">
                    No reports generated yet. Click "Generate PDF & HTML Report" above to build your first dossier.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
