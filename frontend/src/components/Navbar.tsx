import React from 'react';
import { Company } from '../types';
import { Building2, Cpu, CheckCircle2, AlertCircle } from 'lucide-react';

interface NavbarProps {
  companies: Company[];
  selectedCompany: Company | null;
  onSelectCompany: (company: Company) => void;
  llmProvider: string;
}

export const Navbar: React.FC<NavbarProps> = ({
  companies,
  selectedCompany,
  onSelectCompany,
  llmProvider
}) => {
  return (
    <header className="h-16 bg-white border-b border-slate-200 px-6 flex items-center justify-between sticky top-0 z-30 shadow-xs">
      {/* Brand & Title */}
      <div className="flex items-center space-x-3">
        <div className="w-10 h-10 rounded-lg bg-blue-900 flex items-center justify-center text-white font-bold text-lg shadow-sm">
          FA
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-base font-bold text-slate-900 tracking-tight">AI Financial Analyst</h1>
            <span className="text-[10px] font-semibold uppercase tracking-wider bg-blue-50 text-blue-800 px-2 py-0.5 rounded border border-blue-200">
              B.Tech RAG Core
            </span>
          </div>
          <p className="text-xs text-slate-500">Hybrid Retrieval • Deterministic Engine • ESG Intelligence</p>
        </div>
      </div>

      {/* Center & Right Controls */}
      <div className="flex items-center space-x-4">
        {/* Company Selector */}
        <div className="flex items-center space-x-2 bg-slate-50 border border-slate-300 rounded-lg px-3 py-1.5 shadow-2xs">
          <Building2 className="w-4 h-4 text-blue-900" />
          <span className="text-xs font-medium text-slate-600">Active Company:</span>
          <select
            value={selectedCompany?.id || ''}
            onChange={(e) => {
              const comp = companies.find(c => c.id === Number(e.target.value));
              if (comp) onSelectCompany(comp);
            }}
            className="bg-transparent text-xs font-semibold text-slate-900 focus:outline-hidden cursor-pointer"
          >
            {companies.map(c => (
              <option key={c.id} value={c.id}>
                {c.name} ({c.ticker})
              </option>
            ))}
          </select>
        </div>

        {/* LLM Engine Status Indicator */}
        <div className="flex items-center space-x-2 bg-slate-100 border border-slate-200 rounded-lg px-2.5 py-1 text-xs">
          <Cpu className="w-3.5 h-3.5 text-slate-600" />
          <span className="text-slate-500">Engine:</span>
          <span className="font-semibold text-blue-950 capitalize">{llmProvider}</span>
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
        </div>
      </div>
    </header>
  );
};
