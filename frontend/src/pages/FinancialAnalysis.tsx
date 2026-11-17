import React, { useState, useEffect } from 'react';
import { Company, FinancialRecord, FinancialAnalysis as AnalysisType } from '../types';
import { api } from '../api/client';
import {
  TrendingUp, Upload, Plus, AlertCircle, CheckCircle2,
  Table as TableIcon, Activity, Percent, DollarSign, FileSpreadsheet
} from 'lucide-react';
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from 'recharts';

interface FinancialAnalysisProps {
  company: Company | null;
}

export const FinancialAnalysis: React.FC<FinancialAnalysisProps> = ({ company }) => {
  const [financials, setFinancials] = useState<FinancialRecord[]>([]);
  const [analysis, setAnalysis] = useState<AnalysisType | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [showUploadModal, setShowUploadModal] = useState<boolean>(false);
  const [showAddModal, setShowAddModal] = useState<boolean>(false);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>('');

  // Form for manual entry
  const [manualForm, setManualForm] = useState({
    fiscal_year: 2025,
    period: 'FY',
    revenue: '',
    cost_of_revenue: '',
    operating_profit: '',
    net_profit: '',
    total_assets: '',
    total_liabilities: '',
    shareholders_equity: '',
    debt: '',
    cash: '',
    operating_cash_flow: '',
    eps: '',
    source: 'Manual Data Entry'
  });

  useEffect(() => {
    if (!company) return;
    loadFinancials(company.id);
  }, [company]);

  const loadFinancials = async (companyId: number) => {
    setLoading(true);
    try {
      const [records, analysisData] = await Promise.all([
        api.getCompanyFinancials(companyId),
        api.getFinancialAnalysis(companyId)
      ]);
      setFinancials(records);
      setAnalysis(analysisData);
    } catch (err) {
      console.error('Error fetching financials:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCsvUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFile || !company) return;
    setUploadStatus('Uploading & validating financial data...');
    try {
      const res = await api.uploadFinancialCsv(company.id, uploadFile);
      setUploadStatus(`Success! Imported ${res.imported_records} records.`);
      setTimeout(() => {
        setShowUploadModal(false);
        setUploadStatus('');
        loadFinancials(company.id);
      }, 1500);
    } catch (err: any) {
      setUploadStatus(`Error: ${err.response?.data?.detail || 'Upload failed'}`);
    }
  };

  const handleManualSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!company) return;
    try {
      const parseN = (v: string) => (v.trim() === '' ? null : parseFloat(v));
      await api.createFinancialRecord({
        company_id: company.id,
        fiscal_year: Number(manualForm.fiscal_year),
        period: manualForm.period,
        currency: company.currency,
        units: company.units,
        source: manualForm.source,
        revenue: parseN(manualForm.revenue),
        cost_of_revenue: parseN(manualForm.cost_of_revenue),
        operating_profit: parseN(manualForm.operating_profit),
        net_profit: parseN(manualForm.net_profit),
        total_assets: parseN(manualForm.total_assets),
        total_liabilities: parseN(manualForm.total_liabilities),
        shareholders_equity: parseN(manualForm.shareholders_equity),
        debt: parseN(manualForm.debt),
        cash: parseN(manualForm.cash),
        operating_cash_flow: parseN(manualForm.operating_cash_flow),
        eps: parseN(manualForm.eps)
      });
      setShowAddModal(false);
      loadFinancials(company.id);
    } catch (err: any) {
      alert(`Error saving record: ${err.response?.data?.detail || 'Failed'}`);
    }
  };

  if (!company) {
    return <div className="p-8 text-center text-slate-500">Please select a company first.</div>;
  }

  const marginChartData = analysis?.ratios?.map(r => ({
    year: `FY${r.fiscal_year}`,
    GrossMargin: r.gross_profit_margin_pct || 0,
    OperatingMargin: r.operating_profit_margin_pct || 0,
    NetMargin: r.net_profit_margin_pct || 0,
    ROE: r.return_on_equity_pct || 0
  })) || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-2xs flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-900 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
              Deterministic Analytics Engine
            </span>
            <span className="text-xs text-slate-500">Currency: {company.currency} ({company.units})</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mt-1">Structured Financial Data & Ratio Analysis</h1>
          <p className="text-xs text-slate-600 mt-0.5">
            Deterministic ratio computations, historical margins, growth rates, and balance sheet reconciliation.
          </p>
        </div>
        <div className="mt-4 md:mt-0 flex items-center space-x-2">
          <button
            onClick={() => setShowUploadModal(true)}
            className="flex items-center space-x-1.5 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold px-3 py-2 rounded-lg border border-slate-300 transition"
          >
            <Upload className="w-3.5 h-3.5" />
            <span>Upload CSV/Excel</span>
          </button>
          <button
            onClick={() => setShowAddModal(true)}
            className="flex items-center space-x-1.5 bg-blue-900 hover:bg-blue-800 text-white text-xs font-semibold px-3.5 py-2 rounded-lg transition"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Add Year Manually</span>
          </button>
        </div>
      </div>

      {/* Warnings & Inconsistencies */}
      {analysis?.missing_data_warnings && analysis.missing_data_warnings.length > 0 && (
        <div className="bg-amber-50 border border-amber-200 p-4 rounded-xl text-xs text-amber-900 space-y-1">
          <div className="flex items-center space-x-2 font-bold text-amber-800">
            <AlertCircle className="w-4 h-4" />
            <span>Data Validation & Completeness Warnings:</span>
          </div>
          {analysis.missing_data_warnings.map((w, idx) => (
            <div key={idx} className="pl-6">• {w}</div>
          ))}
        </div>
      )}

      {/* Margins & ROE Trend Chart */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs">
        <h2 className="text-sm font-bold text-slate-900 mb-1">Profitability & Capital Efficiency Trends (%)</h2>
        <p className="text-xs text-slate-500 mb-4">Historical Operating Margin, Net Margin, and Return on Equity (ROE).</p>
        <div className="h-64 w-full">
          {marginChartData.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={marginChartData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                <XAxis dataKey="year" tick={{ fontSize: 11, fill: '#64748B' }} />
                <YAxis tick={{ fontSize: 11, fill: '#64748B' }} unit="%" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0F172A', color: '#F8FAFC', borderRadius: '8px', fontSize: '12px' }}
                  formatter={(val: any) => [`${Number(val).toFixed(2)}%`, '']}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Line type="monotone" dataKey="OperatingMargin" stroke="#1E3A8A" strokeWidth={2.5} name="Operating Margin %" />
                <Line type="monotone" dataKey="NetMargin" stroke="#10B981" strokeWidth={2} name="Net Margin %" />
                <Line type="monotone" dataKey="ROE" stroke="#F59E0B" strokeWidth={2} name="ROE %" strokeDasharray="4 4" />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-full flex items-center justify-center text-xs text-slate-400">
              No financial records to display chart.
            </div>
          )}
        </div>
      </div>

      {/* Financial Ratios Table */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
        <h2 className="text-sm font-bold text-slate-900 mb-1">Computed Financial Ratios (Python/Pandas)</h2>
        <p className="text-xs text-slate-500 mb-3">All ratios computed deterministically with zero LLM rounding error.</p>
        <div className="overflow-x-auto rounded-lg border border-slate-200">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-900 text-white font-semibold">
              <tr>
                <th className="px-4 py-2.5">Year</th>
                <th className="px-4 py-2.5">Revenue Growth</th>
                <th className="px-4 py-2.5">Gross Margin</th>
                <th className="px-4 py-2.5">Operating Margin</th>
                <th className="px-4 py-2.5">Net Margin</th>
                <th className="px-4 py-2.5">ROE</th>
                <th className="px-4 py-2.5">ROA</th>
                <th className="px-4 py-2.5">Debt / Equity</th>
                <th className="px-4 py-2.5">Current Ratio</th>
                <th className="px-4 py-2.5">OCF / Net Income</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {analysis?.ratios?.map(r => (
                <tr key={`${r.fiscal_year}-${r.period}`} className="hover:bg-slate-50">
                  <td className="px-4 py-2.5 font-bold">FY{r.fiscal_year}</td>
                  <td className={`px-4 py-2.5 font-medium ${r.revenue_growth_pct !== null && r.revenue_growth_pct !== undefined ? (r.revenue_growth_pct >= 0 ? 'text-emerald-600' : 'text-rose-600') : 'text-slate-400'}`}>
                    {r.revenue_growth_pct !== null && r.revenue_growth_pct !== undefined ? `${r.revenue_growth_pct > 0 ? '+' : ''}${r.revenue_growth_pct}%` : '-'}
                  </td>
                  <td className="px-4 py-2.5">{r.gross_profit_margin_pct ? `${r.gross_profit_margin_pct}%` : '-'}</td>
                  <td className="px-4 py-2.5 font-semibold text-blue-900">{r.operating_profit_margin_pct ? `${r.operating_profit_margin_pct}%` : '-'}</td>
                  <td className="px-4 py-2.5">{r.net_profit_margin_pct ? `${r.net_profit_margin_pct}%` : '-'}</td>
                  <td className="px-4 py-2.5 font-semibold">{r.return_on_equity_pct ? `${r.return_on_equity_pct}%` : '-'}</td>
                  <td className="px-4 py-2.5">{r.return_on_assets_pct ? `${r.return_on_assets_pct}%` : '-'}</td>
                  <td className="px-4 py-2.5">{r.debt_to_equity !== null && r.debt_to_equity !== undefined ? r.debt_to_equity : '-'}</td>
                  <td className="px-4 py-2.5">{r.current_ratio !== null && r.current_ratio !== undefined ? r.current_ratio : '-'}</td>
                  <td className="px-4 py-2.5">{r.ocf_to_net_income ? `${r.ocf_to_net_income}x` : '-'}</td>
                </tr>
              ))}
              {(!analysis?.ratios || analysis.ratios.length === 0) && (
                <tr><td colSpan={10} className="text-center py-6 text-slate-400">No ratio calculations available.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Raw Financial Statements Table */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
        <h2 className="text-sm font-bold text-slate-900 mb-1">Audited Financial Statements Data ({company.currency} {company.units})</h2>
        <p className="text-xs text-slate-500 mb-3">Structured values extracted from filings and uploaded reports.</p>
        <div className="overflow-x-auto rounded-lg border border-slate-200">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-100 text-slate-700 font-semibold border-b border-slate-200">
              <tr>
                <th className="px-3 py-2">Year</th>
                <th className="px-3 py-2">Basis</th>
                <th className="px-3 py-2">Revenue</th>
                <th className="px-3 py-2">Op. Profit</th>
                <th className="px-3 py-2">Net Profit</th>
                <th className="px-3 py-2">Total Assets</th>
                <th className="px-3 py-2">Liabilities</th>
                <th className="px-3 py-2">Equity</th>
                <th className="px-3 py-2">Debt</th>
                <th className="px-3 py-2">Cash</th>
                <th className="px-3 py-2">OCF</th>
                <th className="px-3 py-2">Source</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {financials.map(rec => (
                <tr key={rec.id} className="hover:bg-slate-50">
                  <td className="px-3 py-2 font-bold">FY{rec.fiscal_year}</td>
                  <td className="px-3 py-2 text-slate-500">{rec.reporting_basis || 'Consolidated'}</td>
                  <td className="px-3 py-2 font-medium">{rec.revenue?.toLocaleString() || '-'}</td>
                  <td className="px-3 py-2">{rec.operating_profit?.toLocaleString() || '-'}</td>
                  <td className="px-3 py-2 font-medium">{rec.net_profit?.toLocaleString() || '-'}</td>
                  <td className="px-3 py-2">{rec.total_assets?.toLocaleString() || '-'}</td>
                  <td className="px-3 py-2">{rec.total_liabilities?.toLocaleString() || '-'}</td>
                  <td className="px-3 py-2">{rec.shareholders_equity?.toLocaleString() || '-'}</td>
                  <td className="px-3 py-2">{rec.debt?.toLocaleString() || '-'}</td>
                  <td className="px-3 py-2">{rec.cash?.toLocaleString() || '-'}</td>
                  <td className="px-3 py-2">{rec.operating_cash_flow?.toLocaleString() || '-'}</td>
                  <td className="px-3 py-2 text-[10px] text-slate-500 max-w-xs truncate" title={rec.source}>
                    {rec.source}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Upload CSV Modal */}
      {showUploadModal && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-xl max-w-md w-full p-6 border border-slate-200">
            <h3 className="text-sm font-bold text-slate-900 mb-2">Upload Financial Dataset (CSV / XLSX)</h3>
            <p className="text-xs text-slate-500 mb-4">
              Columns supported: <code>fiscal_year, revenue, cost_of_revenue, operating_profit, net_profit, total_assets, total_liabilities, shareholders_equity, debt, cash, operating_cash_flow</code>.
            </p>
            <form onSubmit={handleCsvUpload} className="space-y-4">
              <input
                type="file"
                accept=".csv, .xlsx, .xls"
                onChange={e => setUploadFile(e.target.files ? e.target.files[0] : null)}
                className="w-full text-xs text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-blue-50 file:text-blue-900 hover:file:bg-blue-100 cursor-pointer"
              />
              {uploadStatus && (
                <div className="text-xs p-2.5 rounded bg-slate-100 text-slate-800 font-medium">
                  {uploadStatus}
                </div>
              )}
              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowUploadModal(false)}
                  className="px-3 py-1.5 border border-slate-300 rounded text-xs font-semibold text-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!uploadFile}
                  className="px-4 py-1.5 bg-blue-900 text-white rounded text-xs font-semibold hover:bg-blue-800 disabled:opacity-50"
                >
                  Upload & Validate
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Manual Entry Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-xl max-w-lg w-full p-6 border border-slate-200">
            <h3 className="text-sm font-bold text-slate-900 mb-3">Add Financial Year Record ({company.currency} {company.units})</h3>
            <form onSubmit={handleManualSubmit} className="space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Fiscal Year</label>
                  <input
                    type="number"
                    value={manualForm.fiscal_year}
                    onChange={e => setManualForm({ ...manualForm, fiscal_year: Number(e.target.value) })}
                    className="w-full border border-slate-300 rounded p-1.5"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Revenue</label>
                  <input
                    type="number"
                    step="any"
                    value={manualForm.revenue}
                    onChange={e => setManualForm({ ...manualForm, revenue: e.target.value })}
                    className="w-full border border-slate-300 rounded p-1.5"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Operating Profit (EBIT)</label>
                  <input
                    type="number"
                    step="any"
                    value={manualForm.operating_profit}
                    onChange={e => setManualForm({ ...manualForm, operating_profit: e.target.value })}
                    className="w-full border border-slate-300 rounded p-1.5"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Net Profit After Tax</label>
                  <input
                    type="number"
                    step="any"
                    value={manualForm.net_profit}
                    onChange={e => setManualForm({ ...manualForm, net_profit: e.target.value })}
                    className="w-full border border-slate-300 rounded p-1.5"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Total Assets</label>
                  <input
                    type="number"
                    step="any"
                    value={manualForm.total_assets}
                    onChange={e => setManualForm({ ...manualForm, total_assets: e.target.value })}
                    className="w-full border border-slate-300 rounded p-1.5"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Shareholders' Equity</label>
                  <input
                    type="number"
                    step="any"
                    value={manualForm.shareholders_equity}
                    onChange={e => setManualForm({ ...manualForm, shareholders_equity: e.target.value })}
                    className="w-full border border-slate-300 rounded p-1.5"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Total Debt</label>
                  <input
                    type="number"
                    step="any"
                    value={manualForm.debt}
                    onChange={e => setManualForm({ ...manualForm, debt: e.target.value })}
                    className="w-full border border-slate-300 rounded p-1.5"
                  />
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Operating Cash Flow</label>
                  <input
                    type="number"
                    step="any"
                    value={manualForm.operating_cash_flow}
                    onChange={e => setManualForm({ ...manualForm, operating_cash_flow: e.target.value })}
                    className="w-full border border-slate-300 rounded p-1.5"
                  />
                </div>
              </div>
              <div className="flex justify-end space-x-2 pt-3">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-3 py-1.5 border border-slate-300 rounded font-semibold text-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 bg-blue-900 text-white rounded font-semibold hover:bg-blue-800"
                >
                  Save Record
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
