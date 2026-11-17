import React, { useEffect, useState } from 'react';
import { Company, FinancialAnalysis, ESGScoreBreakdown, DocumentItem } from '../types';
import { api } from '../api/client';
import {
  TrendingUp,
  ShieldCheck,
  FileText,
  DollarSign,
  Percent,
  Activity,
  ArrowUpRight,
  ArrowDownRight,
  Building,
  RefreshCw,
  ExternalLink
} from 'lucide-react';
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from 'recharts';

interface OverviewDashboardProps {
  company: Company | null;
  onNavigate: (tab: any) => void;
}

export const OverviewDashboard: React.FC<OverviewDashboardProps> = ({ company, onNavigate }) => {
  const [analysis, setAnalysis] = useState<FinancialAnalysis | null>(null);
  const [esgBreakdown, setEsgBreakdown] = useState<ESGScoreBreakdown | null>(null);
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    if (!company) return;
    loadDashboardData(company.id);
  }, [company]);

  const loadDashboardData = async (companyId: number) => {
    setLoading(true);
    try {
      const [anData, docData] = await Promise.all([
        api.getFinancialAnalysis(companyId),
        api.getDocuments(companyId),
      ]);
      setAnalysis(anData);
      setDocuments(docData);

      try {
        const esgData = await api.getESGScoreBreakdown(companyId);
        setEsgBreakdown(esgData);
      } catch {
        setEsgBreakdown(null);
      }
    } catch (err) {
      console.error('Error loading overview data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!company) {
    return (
      <div className="p-8 text-center text-slate-500">
        Please select or create a company to view the overview dashboard.
      </div>
    );
  }

  const latestRatio = analysis?.ratios && analysis.ratios.length > 0
    ? analysis.ratios[analysis.ratios.length - 1]
    : null;

  const chartData = analysis?.ratios?.map(r => ({
    year: `FY${r.fiscal_year}`,
    Revenue: r.revenue || 0,
    OperatingProfit: r.operating_profit || 0,
    NetProfit: r.net_profit || 0,
    OperatingMargin: r.operating_profit_margin_pct || 0,
  })) || [];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-2xs flex flex-col md:flex-row items-start md:items-center justify-between">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-900 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
              {company.exchange || 'Public Company'}
            </span>
            <span className="text-xs text-slate-400">•</span>
            <span className="text-xs text-slate-500">{company.sector || 'Commercial Enterprise'}</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mt-1">{company.name} ({company.ticker})</h1>
          <p className="text-xs text-slate-600 max-w-2xl mt-1">
            {company.description || 'Enterprise corporate reporting and financial analytics.'}
          </p>
        </div>
        <div className="mt-4 md:mt-0 flex items-center space-x-3">
          <button
            onClick={() => onNavigate('collection')}
            className="flex items-center space-x-1.5 bg-blue-900 hover:bg-blue-800 text-white text-xs font-semibold px-3.5 py-2 rounded-lg transition shadow-2xs"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Automated Collection</span>
          </button>
          <button
            onClick={() => onNavigate('reports')}
            className="flex items-center space-x-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold px-3.5 py-2 rounded-lg border border-slate-300 transition"
          >
            <FileText className="w-3.5 h-3.5 text-slate-500" />
            <span>Reports</span>
          </button>
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Revenue */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between text-slate-500 text-xs mb-1">
            <span>Latest Revenue (FY{latestRatio?.fiscal_year || 'N/A'})</span>
            <DollarSign className="w-4 h-4 text-blue-900" />
          </div>
          <div className="text-xl font-bold text-slate-900">
            {company.currency} {latestRatio?.revenue?.toLocaleString() || '-'} <span className="text-xs font-normal text-slate-500">{company.units}</span>
          </div>
          <div className="mt-2 flex items-center text-xs">
            {latestRatio?.revenue_growth_pct !== undefined && latestRatio?.revenue_growth_pct !== null ? (
              <span className={`flex items-center font-semibold ${latestRatio.revenue_growth_pct >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                {latestRatio.revenue_growth_pct >= 0 ? <ArrowUpRight className="w-3.5 h-3.5 mr-0.5" /> : <ArrowDownRight className="w-3.5 h-3.5 mr-0.5" />}
                {latestRatio.revenue_growth_pct > 0 ? `+${latestRatio.revenue_growth_pct}%` : `${latestRatio.revenue_growth_pct}%`} YoY
              </span>
            ) : (
              <span className="text-slate-400">Base period / Single year</span>
            )}
          </div>
        </div>

        {/* Operating Margin */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between text-slate-500 text-xs mb-1">
            <span>Operating Profit Margin</span>
            <Percent className="w-4 h-4 text-emerald-700" />
          </div>
          <div className="text-xl font-bold text-slate-900">
            {latestRatio?.operating_profit_margin_pct !== undefined && latestRatio?.operating_profit_margin_pct !== null
              ? `${latestRatio.operating_profit_margin_pct}%`
              : '-'}
          </div>
          <div className="mt-2 text-xs text-slate-500">
            Operating EBIT: {company.currency} {latestRatio?.operating_profit?.toLocaleString() || '-'} {company.units}
          </div>
        </div>

        {/* Return on Equity (ROE) */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between text-slate-500 text-xs mb-1">
            <span>Return on Equity (ROE)</span>
            <Activity className="w-4 h-4 text-blue-800" />
          </div>
          <div className="text-xl font-bold text-slate-900">
            {latestRatio?.return_on_equity_pct !== undefined && latestRatio?.return_on_equity_pct !== null
              ? `${latestRatio.return_on_equity_pct}%`
              : '-'}
          </div>
          <div className="mt-2 text-xs text-slate-500">
            Debt-to-Equity: {latestRatio?.debt_to_equity !== undefined && latestRatio?.debt_to_equity !== null ? latestRatio.debt_to_equity : '0.00'}
          </div>
        </div>

        {/* ESG Composite Score */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between text-slate-500 text-xs mb-1">
            <span>Project ESG Score</span>
            <ShieldCheck className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-xl font-bold text-emerald-700">
            {esgBreakdown?.overall_esg_score !== undefined && esgBreakdown?.overall_esg_score !== null
              ? `${esgBreakdown.overall_esg_score} / 100`
              : 'N/A'}
          </div>
          <div className="mt-2 text-xs text-slate-500 flex justify-between">
            <span>E: {esgBreakdown?.environmental_score || '-'}</span>
            <span>S: {esgBreakdown?.social_score || '-'}</span>
            <span>G: {esgBreakdown?.governance_score || '-'}</span>
          </div>
        </div>
      </div>

      {/* Main Charts & Analytics Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Financial Trends Chart */}
        <div className="lg:col-span-2 bg-white p-6 rounded-xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-base font-bold text-slate-900">Historical Financial Performance</h2>
              <p className="text-xs text-slate-500">Audited Revenue & Profitability in {company.currency} ({company.units})</p>
            </div>
            <span className="text-xs font-medium text-blue-900 bg-blue-50 px-2 py-1 rounded">
              Deterministic Python Engine
            </span>
          </div>
          <div className="h-72 w-full">
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                  <XAxis dataKey="year" tick={{ fontSize: 11, fill: '#64748B' }} />
                  <YAxis tick={{ fontSize: 11, fill: '#64748B' }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0F172A', color: '#F8FAFC', borderRadius: '8px', fontSize: '12px' }}
                    formatter={(val: any) => [`${company.currency} ${Number(val).toLocaleString()} ${company.units}`, '']}
                  />
                  <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                  <Bar dataKey="Revenue" fill="#1E3A8A" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="OperatingProfit" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="NetProfit" fill="#10B981" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-xs text-slate-400">
                No financial history available for this company. Use Data Collection or CSV upload.
              </div>
            )}
          </div>
        </div>

        {/* Analytical Insights & Summary */}
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-base font-bold text-slate-900">Analytical Insights</h2>
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
            </div>
            <div className="space-y-2.5 text-xs text-slate-700">
              {analysis?.summary_insights && analysis.summary_insights.length > 0 ? (
                analysis.summary_insights.map((insight, idx) => (
                  <div key={idx} className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg">
                    • {insight}
                  </div>
                ))
              ) : (
                <p className="text-slate-400 italic">No calculated insights available.</p>
              )}
            </div>
          </div>

          <div className="mt-5 pt-4 border-t border-slate-200">
            <button
              onClick={() => onNavigate('chat')}
              className="w-full flex items-center justify-center space-x-2 bg-blue-900 hover:bg-blue-800 text-white text-xs font-semibold py-2.5 rounded-lg transition"
            >
              <span>Ask AI Analyst About {company.ticker}</span>
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Lower Row: Documents & Data Coverage */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Uploaded Documents */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-bold text-slate-900">Indexed Corporate Reports</h3>
            <button onClick={() => onNavigate('documents')} className="text-xs text-blue-900 font-semibold hover:underline">
              View All ({documents.length})
            </button>
          </div>
          <div className="space-y-2">
            {documents.slice(0, 3).map(doc => (
              <div key={doc.id} className="flex items-center justify-between p-2.5 bg-slate-50 rounded-lg border border-slate-200 text-xs">
                <div className="flex items-center space-x-2.5">
                  <FileText className="w-4 h-4 text-blue-900 shrink-0" />
                  <div>
                    <div className="font-semibold text-slate-900">{doc.title}</div>
                    <div className="text-[11px] text-slate-500">
                      {doc.document_type} • {doc.total_pages} pages • {doc.total_chunks} chunks
                    </div>
                  </div>
                </div>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800">
                  {doc.status}
                </span>
              </div>
            ))}
            {documents.length === 0 && (
              <p className="text-xs text-slate-400 py-3 text-center">No reports indexed yet. Use Data Collection.</p>
            )}
          </div>
        </div>

        {/* ESG Coverage Card */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-bold text-slate-900">ESG Disclosures & Transparency</h3>
            <button onClick={() => onNavigate('esg')} className="text-xs text-blue-900 font-semibold hover:underline">
              Detailed Breakdown
            </button>
          </div>
          {esgBreakdown ? (
            <div>
              <div className="flex items-center justify-between text-xs mb-1">
                <span className="text-slate-600">Core Indicator Disclosure Coverage:</span>
                <span className="font-bold text-slate-900">{esgBreakdown.data_coverage_pct}%</span>
              </div>
              <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden mb-3">
                <div
                  className="bg-emerald-600 h-full rounded-full transition-all"
                  style={{ width: `${Math.min(esgBreakdown.data_coverage_pct, 100)}%` }}
                ></div>
              </div>
              <p className="text-[11px] text-slate-500 mb-2">
                <b>Formula:</b> {esgBreakdown.formula_explanation}
              </p>
              <div className="p-2.5 bg-slate-50 border border-slate-200 rounded text-[11px] text-slate-600 italic">
                {esgBreakdown.methodology_limitations[0]}
              </div>
            </div>
          ) : (
            <p className="text-xs text-slate-400 py-3 text-center">No ESG data recorded for this company yet.</p>
          )}
        </div>
      </div>
    </div>
  );
};
