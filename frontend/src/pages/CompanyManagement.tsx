import React, { useState } from 'react';
import { Company } from '../types';
import { api } from '../api/client';
import { Building, Plus, Trash2, Check, ExternalLink, Globe } from 'lucide-react';

interface CompanyManagementProps {
  companies: Company[];
  selectedCompany: Company | null;
  onSelectCompany: (company: Company) => void;
  onRefresh: () => void;
}

export const CompanyManagement: React.FC<CompanyManagementProps> = ({
  companies,
  selectedCompany,
  onSelectCompany,
  onRefresh
}) => {
  const [showAddForm, setShowAddForm] = useState<boolean>(false);
  const [formData, setFormData] = useState({
    ticker: '',
    name: '',
    sector: 'Information Technology',
    industry: 'Software Services',
    exchange: 'NSE',
    currency: 'INR',
    units: 'Crores',
    cik: '',
    isin: '',
    ir_url: '',
    description: ''
  });
  const [errorMsg, setErrorMsg] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    try {
      await api.createCompany(formData);
      setShowAddForm(false);
      onRefresh();
      setFormData({
        ticker: '',
        name: '',
        sector: 'Information Technology',
        industry: 'Software Services',
        exchange: 'NSE',
        currency: 'INR',
        units: 'Crores',
        cik: '',
        isin: '',
        ir_url: '',
        description: ''
      });
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Failed to create company.');
    }
  };

  const handleDelete = async (id: number, name: string) => {
    if (!window.confirm(`Are you sure you want to delete ${name}? All associated financial records and indexed documents will be removed.`)) {
      return;
    }
    try {
      await api.deleteCompany(id);
      onRefresh();
    } catch (err) {
      console.error('Delete company failed:', err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-2xs flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold text-slate-900">Company Management</h1>
          <p className="text-xs text-slate-500 mt-0.5">Manage portfolio companies, exchanges, identifiers, and reporting units.</p>
        </div>
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="flex items-center space-x-1.5 bg-blue-900 hover:bg-blue-800 text-white text-xs font-semibold px-3.5 py-2 rounded-lg transition"
        >
          <Plus className="w-4 h-4" />
          <span>Add Custom Company</span>
        </button>
      </div>

      {/* Add Company Form */}
      {showAddForm && (
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs space-y-4">
          <h2 className="text-sm font-bold text-slate-900">Add New Corporate Entity</h2>
          {errorMsg && <div className="p-3 bg-rose-50 border border-rose-200 text-rose-700 text-xs rounded-lg">{errorMsg}</div>}
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Ticker Symbol *</label>
              <input
                type="text"
                required
                placeholder="e.g. INFY, AAPL, TCS"
                value={formData.ticker}
                onChange={e => setFormData({ ...formData, ticker: e.target.value.toUpperCase() })}
                className="w-full border border-slate-300 rounded-lg p-2 focus:outline-hidden focus:border-blue-900"
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Company Name *</label>
              <input
                type="text"
                required
                placeholder="Full Legal Name"
                value={formData.name}
                onChange={e => setFormData({ ...formData, name: e.target.value })}
                className="w-full border border-slate-300 rounded-lg p-2 focus:outline-hidden focus:border-blue-900"
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Exchange</label>
              <select
                value={formData.exchange}
                onChange={e => setFormData({ ...formData, exchange: e.target.value })}
                className="w-full border border-slate-300 rounded-lg p-2 focus:outline-hidden focus:border-blue-900"
              >
                <option value="NSE">NSE (National Stock Exchange of India)</option>
                <option value="BSE">BSE (Bombay Stock Exchange)</option>
                <option value="NASDAQ">NASDAQ (US)</option>
                <option value="NYSE">NYSE (US)</option>
              </select>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Currency Code</label>
              <input
                type="text"
                required
                placeholder="INR, USD, EUR"
                value={formData.currency}
                onChange={e => setFormData({ ...formData, currency: e.target.value.toUpperCase() })}
                className="w-full border border-slate-300 rounded-lg p-2 focus:outline-hidden focus:border-blue-900"
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Reporting Units</label>
              <input
                type="text"
                required
                placeholder="Crores, Millions, Billions"
                value={formData.units}
                onChange={e => setFormData({ ...formData, units: e.target.value })}
                className="w-full border border-slate-300 rounded-lg p-2 focus:outline-hidden focus:border-blue-900"
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-700 mb-1">SEC CIK (if US-listed)</label>
              <input
                type="text"
                placeholder="e.g. 0000320193"
                value={formData.cik}
                onChange={e => setFormData({ ...formData, cik: e.target.value })}
                className="w-full border border-slate-300 rounded-lg p-2 focus:outline-hidden focus:border-blue-900"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Sector</label>
              <input
                type="text"
                value={formData.sector}
                onChange={e => setFormData({ ...formData, sector: e.target.value })}
                className="w-full border border-slate-300 rounded-lg p-2 focus:outline-hidden focus:border-blue-900"
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Industry</label>
              <input
                type="text"
                value={formData.industry}
                onChange={e => setFormData({ ...formData, industry: e.target.value })}
                className="w-full border border-slate-300 rounded-lg p-2 focus:outline-hidden focus:border-blue-900"
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Investor Relations URL</label>
              <input
                type="url"
                placeholder="https://..."
                value={formData.ir_url}
                onChange={e => setFormData({ ...formData, ir_url: e.target.value })}
                className="w-full border border-slate-300 rounded-lg p-2 focus:outline-hidden focus:border-blue-900"
              />
            </div>
          </div>

          <div>
            <label className="block font-semibold text-slate-700 mb-1 text-xs">Description</label>
            <textarea
              rows={2}
              value={formData.description}
              onChange={e => setFormData({ ...formData, description: e.target.value })}
              className="w-full border border-slate-300 rounded-lg p-2 text-xs focus:outline-hidden focus:border-blue-900"
              placeholder="Corporate operational profile..."
            ></textarea>
          </div>

          <div className="flex justify-end space-x-2 pt-2">
            <button
              type="button"
              onClick={() => setShowAddForm(false)}
              className="px-4 py-2 border border-slate-300 rounded-lg text-xs font-semibold text-slate-700 hover:bg-slate-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-900 text-white rounded-lg text-xs font-semibold hover:bg-blue-800"
            >
              Save Company
            </button>
          </div>
        </form>
      )}

      {/* Companies Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {companies.map((c) => {
          const isSelected = selectedCompany?.id === c.id;
          return (
            <div
              key={c.id}
              className={`bg-white rounded-xl p-5 border transition shadow-2xs relative flex flex-col justify-between ${
                isSelected ? 'border-blue-900 ring-2 ring-blue-900/10' : 'border-slate-200 hover:border-slate-300'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-bold px-2 py-0.5 rounded bg-blue-50 text-blue-900 border border-blue-200">
                    {c.ticker}
                  </span>
                  <span className="text-xs text-slate-500 font-medium">{c.exchange || 'NSE'}</span>
                </div>
                <h3 className="text-sm font-bold text-slate-900 mb-1">{c.name}</h3>
                <p className="text-xs text-slate-500 line-clamp-2 mb-3">
                  {c.description || 'Corporate entity registered in system.'}
                </p>
                <div className="space-y-1 text-xs text-slate-600 bg-slate-50 p-3 rounded-lg border border-slate-200 mb-4">
                  <div>Sector: <span className="font-semibold text-slate-800">{c.sector || 'General'}</span></div>
                  <div>Currency: <span className="font-semibold text-slate-800">{c.currency} ({c.units})</span></div>
                  {c.cik && <div>SEC CIK: <span className="font-mono text-slate-800">{c.cik}</span></div>}
                </div>
              </div>

              <div className="flex items-center justify-between pt-3 border-t border-slate-100">
                <button
                  onClick={() => onSelectCompany(c)}
                  className={`text-xs font-semibold px-3 py-1.5 rounded-lg transition flex items-center space-x-1 ${
                    isSelected
                      ? 'bg-emerald-600 text-white'
                      : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                  }`}
                >
                  {isSelected ? (
                    <>
                      <Check className="w-3.5 h-3.5" />
                      <span>Active</span>
                    </>
                  ) : (
                    <span>Set Active</span>
                  )}
                </button>

                <button
                  onClick={() => handleDelete(c.id, c.name)}
                  className="p-1.5 text-slate-400 hover:text-rose-600 transition rounded"
                  title="Delete company"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
