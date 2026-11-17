import React, { useState, useEffect } from 'react';
import { Company, ESGRecord, ESGScoreBreakdown } from '../types';
import { api } from '../api/client';
import {
  ShieldCheck, Leaf, Users, Award, AlertTriangle, CheckCircle2,
  HelpCircle, Info, ExternalLink, Plus
} from 'lucide-react';

interface ESGAnalysisProps {
  company: Company | null;
}

export const ESGAnalysis: React.FC<ESGAnalysisProps> = ({ company }) => {
  const [esgRecords, setEsgRecords] = useState<ESGRecord[]>([]);
  const [breakdown, setBreakdown] = useState<ESGScoreBreakdown | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [activePillar, setActivePillar] = useState<'all' | 'environmental' | 'social' | 'governance'>('all');

  useEffect(() => {
    if (!company) return;
    loadESG(company.id);
  }, [company]);

  const loadESG = async (companyId: number) => {
    setLoading(true);
    try {
      const records = await api.getESGRecords(companyId);
      setEsgRecords(records);
      const scoreData = await api.getESGScoreBreakdown(companyId);
      setBreakdown(scoreData);
    } catch (err) {
      console.error('Failed to load ESG data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!company) {
    return <div className="p-8 text-center text-slate-500">Please select a company to view ESG evaluation.</div>;
  }

  const renderIndicatorRow = (key: string, ind: any) => {
    const isDisclosed = ind.status === 'DISCLOSED';
    return (
      <tr key={key} className="hover:bg-slate-50 text-xs border-b border-slate-100">
        <td className="px-4 py-2.5 font-medium text-slate-900">{ind.label}</td>
        <td className="px-4 py-2.5 text-slate-600">{ind.raw_value || <span className="text-slate-400 italic">Not Disclosed</span>}</td>
        <td className="px-4 py-2.5">
          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
            isDisclosed ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-500'
          }`}>
            {ind.status}
          </span>
        </td>
        <td className="px-4 py-2.5 font-bold text-blue-900">
          {isDisclosed ? `${ind.normalized_score} / 100` : '-'}
        </td>
      </tr>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-2xs">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs font-bold uppercase tracking-wider text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                Transparent ESG Methodology
              </span>
              <span className="text-xs text-slate-400">•</span>
              <span className="text-xs text-slate-500">{company.name} ({company.ticker})</span>
            </div>
            <h1 className="text-2xl font-bold text-slate-900 mt-1">ESG Performance & Disclosure Evaluation</h1>
            <p className="text-xs text-slate-600 mt-0.5 max-w-2xl">
              Internal, project-specific ESG scoring model. Non-disclosure is never treated as a penalty;
              sub-pillar scores are computed strictly across verified disclosures.
            </p>
          </div>
          {breakdown && (
            <div className="mt-4 md:mt-0 p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-center min-w-[160px]">
              <span className="text-xs font-semibold text-emerald-800 block">Composite ESG Score</span>
              <span className="text-3xl font-extrabold text-emerald-900 block my-1">
                {breakdown.overall_esg_score !== null ? breakdown.overall_esg_score : 'N/A'}
              </span>
              <span className="text-[10px] text-emerald-700 block">
                Coverage: <b>{breakdown.data_coverage_pct}%</b>
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Mandatory Disclaimer Alert */}
      <div className="bg-blue-50/70 border border-blue-200 p-4 rounded-xl text-xs text-blue-950 flex items-start space-x-3">
        <Info className="w-5 h-5 text-blue-900 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <div className="font-bold">Academic & Project-Specific Rating Notice:</div>
          <p>
            This evaluation reflects our transparent academic algorithm with conceptual weightings:
            <b> Environmental = 30%, Social = 30%, Governance = 40%</b>.
            It is <b>NOT</b> an official rating from MSCI, Sustainalytics, S&P Global, or CRISIL.
            To avoid penalizing companies with partial disclosures, unrecorded indicators are omitted from pillar calculations rather than scored as zero.
          </p>
        </div>
      </div>

      {/* Pillar Cards */}
      {breakdown && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Environmental */}
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-emerald-800 flex items-center space-x-1.5">
                <Leaf className="w-4 h-4 text-emerald-600" />
                <span>Environmental Pillar</span>
              </span>
              <span className="text-xs font-semibold bg-emerald-50 text-emerald-800 px-2 py-0.5 rounded">
                Weight: 30%
              </span>
            </div>
            <div className="text-2xl font-bold text-slate-900 mb-1">
              {breakdown.environmental_score !== null ? `${breakdown.environmental_score} / 100` : 'N/A'}
            </div>
            <p className="text-[11px] text-slate-500">
              Assesses Scope 1 & 2 carbon tracking, renewable energy share, water recycling, and waste diversion.
            </p>
          </div>

          {/* Social */}
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-blue-900 flex items-center space-x-1.5">
                <Users className="w-4 h-4 text-blue-800" />
                <span>Social Pillar</span>
              </span>
              <span className="text-xs font-semibold bg-blue-50 text-blue-800 px-2 py-0.5 rounded">
                Weight: 30%
              </span>
            </div>
            <div className="text-2xl font-bold text-slate-900 mb-1">
              {breakdown.social_score !== null ? `${breakdown.social_score} / 100` : 'N/A'}
            </div>
            <p className="text-[11px] text-slate-500">
              Assesses workforce gender diversity, training investment, safety LTIR, CSR commitments, and human rights.
            </p>
          </div>

          {/* Governance */}
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-purple-900 flex items-center space-x-1.5">
                <Award className="w-4 h-4 text-purple-700" />
                <span>Governance Pillar</span>
              </span>
              <span className="text-xs font-semibold bg-purple-50 text-purple-800 px-2 py-0.5 rounded">
                Weight: 40%
              </span>
            </div>
            <div className="text-2xl font-bold text-slate-900 mb-1">
              {breakdown.governance_score !== null ? `${breakdown.governance_score} / 100` : 'N/A'}
            </div>
            <p className="text-[11px] text-slate-500">
              Assesses board independence, women on board, leadership separation, code of ethics, and whistleblower protections.
            </p>
          </div>
        </div>
      )}

      {/* Indicator Breakdown Table */}
      {breakdown && (
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-bold text-slate-900">Disclosed Indicators & Scoring Decomposition</h2>
            <div className="flex space-x-1 text-xs">
              {(['all', 'environmental', 'social', 'governance'] as const).map(tab => (
                <button
                  key={tab}
                  onClick={() => setActivePillar(tab)}
                  className={`px-3 py-1 rounded-md font-semibold capitalize transition ${
                    activePillar === tab
                      ? 'bg-blue-900 text-white'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {tab}
                </button>
              ))}
            </div>
          </div>

          <div className="overflow-x-auto rounded-lg border border-slate-200">
            <table className="w-full text-left">
              <thead className="bg-slate-900 text-white text-xs font-semibold">
                <tr>
                  <th className="px-4 py-2.5">Indicator Name</th>
                  <th className="px-4 py-2.5">Reported Raw Value</th>
                  <th className="px-4 py-2.5">Status</th>
                  <th className="px-4 py-2.5">Normalized Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {(activePillar === 'all' || activePillar === 'environmental') &&
                  Object.entries(breakdown.indicator_scores.environmental).map(([k, v]) => renderIndicatorRow(k, v))}
                {(activePillar === 'all' || activePillar === 'social') &&
                  Object.entries(breakdown.indicator_scores.social).map(([k, v]) => renderIndicatorRow(k, v))}
                {(activePillar === 'all' || activePillar === 'governance') &&
                  Object.entries(breakdown.indicator_scores.governance).map(([k, v]) => renderIndicatorRow(k, v))}
              </tbody>
            </table>
          </div>

          {/* Formula Explanation */}
          <div className="mt-4 p-4 bg-slate-50 rounded-lg border border-slate-200 text-xs text-slate-700">
            <span className="font-bold text-slate-900 block mb-1">Mathematical Formula:</span>
            <code>{breakdown.formula_explanation}</code>
          </div>
        </div>
      )}
    </div>
  );
};
