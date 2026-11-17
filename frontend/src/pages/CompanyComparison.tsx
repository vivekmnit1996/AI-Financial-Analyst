import React, { useState, useEffect } from 'react';
import { Company } from '../types';
import { api } from '../api/client';
import { Scale, Check, DollarSign, Activity } from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

interface CompanyComparisonProps {
  companies: Company[];
}

export const CompanyComparison: React.FC<CompanyComparisonProps> = ({ companies }) => {
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [comparisonData, setComparisonData] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    // Default to first 2-3 companies
    if (companies.length > 0 && selectedIds.length === 0) {
      setSelectedIds(companies.slice(0, 3).map(c => c.id));
    }
  }, [companies]);

  useEffect(() => {
    if (selectedIds.length > 0) {
      loadComparison();
    }
  }, [selectedIds]);

  const loadComparison = async () => {
    setLoading(true);
    try {
      const data = await api.compareCompanies(selectedIds);
      setComparisonData(data);
    } catch (err) {
      console.error('Failed to compare companies:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleCompany = (id: number) => {
    if (selectedIds.includes(id)) {
      if (selectedIds.length > 1) {
        setSelectedIds(selectedIds.filter(x => x !== id));
      }
    } else {
      setSelectedIds([...selectedIds, id]);
    }
  };

  const chartData = comparisonData.map(c => ({
    name: c.ticker,
    OperatingMargin: c.operating_profit_margin_pct || 0,
    NetMargin: c.net_profit_margin_pct || 0,
    ROE: c.return_on_equity_pct || 0,
  }));

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-2xs">
        <h1 className="text-xl font-bold text-slate-900">Multi-Company Peer Comparison</h1>
        <p className="text-xs text-slate-500 mt-0.5">
          Benchmark operating margins, capital efficiency, profitability, and leverage across public corporations.
        </p>

        {/* Company Selection Pills */}
        <div className="mt-4 flex flex-wrap gap-2">
          {companies.map(c => {
            const isChecked = selectedIds.includes(c.id);
            return (
              <button
                key={c.id}
                onClick={() => toggleCompany(c.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center space-x-1.5 border transition ${
                  isChecked
                    ? 'bg-blue-900 text-white border-blue-900 shadow-2xs'
                    : 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100'
                }`}
              >
                <span>{c.name} ({c.ticker})</span>
                {isChecked && <Check className="w-3.5 h-3.5" />}
              </button>
            );
          })}
        </div>
      </div>

      {/* Comparative Charts */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs">
        <h2 className="text-sm font-bold text-slate-900 mb-1">Comparative Margin & Capital Efficiency (%)</h2>
        <p className="text-xs text-slate-500 mb-4">Direct comparison of latest operating margins, net margins, and ROE.</p>
        <div className="h-64 w-full">
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#64748B' }} />
                <YAxis tick={{ fontSize: 11, fill: '#64748B' }} unit="%" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0F172A', color: '#F8FAFC', borderRadius: '8px', fontSize: '12px' }}
                  formatter={(val: any) => [`${Number(val).toFixed(2)}%`, '']}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Bar dataKey="OperatingMargin" fill="#1E3A8A" radius={[4, 4, 0, 0]} name="Operating Margin %" />
                <Bar dataKey="NetMargin" fill="#10B981" radius={[4, 4, 0, 0]} name="Net Margin %" />
                <Bar dataKey="ROE" fill="#F59E0B" radius={[4, 4, 0, 0]} name="ROE %" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-full flex items-center justify-center text-xs text-slate-400">
              Select at least one company to view comparative charts.
            </div>
          )}
        </div>
      </div>

      {/* Comparative Metrics Table */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
        <h2 className="text-sm font-bold text-slate-900 mb-3">Key Financial Benchmarking Metrics</h2>
        <div className="overflow-x-auto rounded-lg border border-slate-200">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-900 text-white font-semibold">
              <tr>
                <th className="px-4 py-2.5">Company</th>
                <th className="px-4 py-2.5">Sector</th>
                <th className="px-4 py-2.5">Latest Year</th>
                <th className="px-4 py-2.5">Revenue</th>
                <th className="px-4 py-2.5">Revenue Growth</th>
                <th className="px-4 py-2.5">Operating Margin</th>
                <th className="px-4 py-2.5">Net Margin</th>
                <th className="px-4 py-2.5">ROE</th>
                <th className="px-4 py-2.5">Debt / Equity</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {comparisonData.map(c => (
                <tr key={c.company_id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-bold text-slate-900">
                    {c.company_name} <span className="text-slate-500 font-normal">({c.ticker})</span>
                  </td>
                  <td className="px-4 py-3 text-slate-600">{c.sector || 'General'}</td>
                  <td className="px-4 py-3 font-semibold">{c.latest_fiscal_year ? `FY${c.latest_fiscal_year}` : '-'}</td>
                  <td className="px-4 py-3 font-medium">
                    {c.revenue ? `${c.currency} ${c.revenue.toLocaleString()} ${c.units}` : '-'}
                  </td>
                  <td className="px-4 py-3">
                    {c.revenue_growth_pct !== null && c.revenue_growth_pct !== undefined
                      ? <span className={`font-semibold ${c.revenue_growth_pct >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>{c.revenue_growth_pct > 0 ? '+' : ''}{c.revenue_growth_pct}%</span>
                      : '-'}
                  </td>
                  <td className="px-4 py-3 font-bold text-blue-900">
                    {c.operating_profit_margin_pct ? `${c.operating_profit_margin_pct}%` : '-'}
                  </td>
                  <td className="px-4 py-3">{c.net_profit_margin_pct ? `${c.net_profit_margin_pct}%` : '-'}</td>
                  <td className="px-4 py-3 font-semibold">{c.return_on_equity_pct ? `${c.return_on_equity_pct}%` : '-'}</td>
                  <td className="px-4 py-3">{c.debt_to_equity !== null && c.debt_to_equity !== undefined ? c.debt_to_equity : '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
