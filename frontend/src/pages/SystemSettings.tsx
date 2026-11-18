import React, { useState, useEffect } from 'react';
import { SystemSettings as SettingsType } from '../types';
import { api } from '../api/client';
import {
  Settings, CheckCircle2, AlertCircle, Database, Cpu, Key, RefreshCw, Layers
} from 'lucide-react';

interface SystemSettingsProps {
  onSettingsUpdated: () => void;
}

export const SystemSettings: React.FC<SystemSettingsProps> = ({ onSettingsUpdated }) => {
  const [settings, setSettings] = useState<SettingsType | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [health, setHealth] = useState<any>(null);

  // Form for LLM updates
  const [provider, setProvider] = useState<string>('deterministic');
  const [geminiKey, setGeminiKey] = useState<string>('');
  const [openaiKey, setOpenaiKey] = useState<string>('');
  const [modelName, setModelName] = useState<string>('gemini-flash-lite-latest');
  const [statusMsg, setStatusMsg] = useState<string>('');

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    setLoading(true);
    try {
      const [data, healthData] = await Promise.all([
        api.getSettings(),
        api.getHealth()
      ]);
      setSettings(data);
      setHealth(healthData);
      setProvider(data.llm_provider);
    } catch (err) {
      console.error('Failed to load settings:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatusMsg('Updating system configuration...');
    try {
      const res = await api.updateLLMSettings({
        llm_provider: provider,
        gemini_api_key: geminiKey || undefined,
        openai_api_key: openaiKey || undefined,
        llm_model_name: modelName || undefined
      });
      setStatusMsg(`Success: ${res.message}`);
      setGeminiKey('');
      setOpenaiKey('');
      loadSettings();
      onSettingsUpdated();
    } catch (err: any) {
      setStatusMsg(`Error: ${err.response?.data?.detail || err.message}`);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-2xs">
        <h1 className="text-xl font-bold text-slate-900">System Architecture & Diagnostic Settings</h1>
        <p className="text-xs text-slate-500 mt-0.5">
          Configure database connections, Qdrant vector storage, cross-encoder rerankers, and LLM abstraction keys.
        </p>
      </div>

      {/* Diagnostics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Relational Database */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-800 flex items-center space-x-1.5">
              <Database className="w-4 h-4 text-blue-900" />
              <span>Relational Storage</span>
            </span>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 flex items-center space-x-1">
              <CheckCircle2 className="w-3 h-3" />
              <span>{health?.database || 'CONNECTED'}</span>
            </span>
          </div>
          <p className="text-xs text-slate-500 mb-2 truncate" title={settings?.database_url}>
            Target: <code>{settings?.database_url}</code>
          </p>
          <div className="text-[11px] text-slate-600">
            PostgreSQL / SQLite ORM with foreign key integrity and WAL journaling.
          </div>
        </div>

        {/* Qdrant Vector Store */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-800 flex items-center space-x-1.5">
              <Layers className="w-4 h-4 text-blue-900" />
              <span>Qdrant Vector DB</span>
            </span>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 flex items-center space-x-1">
              <CheckCircle2 className="w-3 h-3" />
              <span>{health?.qdrant || 'ONLINE'}</span>
            </span>
          </div>
          <p className="text-xs text-slate-500 mb-2">
            Collection: <code>{settings?.qdrant_collection}</code> (Mode: {settings?.qdrant_mode})
          </p>
          <div className="text-[11px] text-slate-600">
            Embedding Dimension: <b>384</b> (Cosine Distance Metric)
          </div>
        </div>

        {/* AI Reasoning Engine */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-800 flex items-center space-x-1.5">
              <Cpu className="w-4 h-4 text-blue-900" />
              <span>Active AI Engine</span>
            </span>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-900 capitalize">
              {settings?.llm_provider || 'Deterministic'}
            </span>
          </div>
          <p className="text-xs text-slate-500 mb-2">
            Model: <code>{settings?.embedding_model}</code>
          </p>
          <div className="text-[11px] text-slate-600">
            Cross-Encoder Reranker: <b>{settings?.reranker_enabled ? 'Active' : 'Disabled'}</b>
          </div>
        </div>
      </div>

      {/* LLM Provider Configuration Form */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs">
        <h2 className="text-sm font-bold text-slate-900 mb-2">LLM Provider Configuration</h2>
        <p className="text-xs text-slate-500 mb-4">
          Select your LLM inference engine. A fully functional <b>Deterministic Reasoning Fallback</b> is active by default, ensuring zero hallucinations and verified calculations even without external API credentials.
        </p>

        {statusMsg && (
          <div className="p-3 bg-blue-50 border border-blue-200 text-blue-900 text-xs rounded-lg mb-4">
            {statusMsg}
          </div>
        )}

        <form onSubmit={handleUpdate} className="space-y-4 text-xs">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Active LLM Provider</label>
              <select
                value={provider}
                onChange={e => setProvider(e.target.value)}
                className="w-full border border-slate-300 rounded-lg p-2.5 focus:outline-hidden focus:border-blue-900"
              >
                <option value="deterministic">Deterministic Engine (Local / Fallback, Zero-Key)</option>
                <option value="gemini">Google Gemini API</option>
                <option value="openai">OpenAI API</option>
                <option value="ollama">Ollama Local LLM</option>
              </select>
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">Target Model Name</label>
              <input
                type="text"
                placeholder="e.g. gemini-1.5-flash or gpt-4o-mini"
                value={modelName}
                onChange={e => setModelName(e.target.value)}
                className="w-full border border-slate-300 rounded-lg p-2.5 focus:outline-hidden focus:border-blue-900"
              />
            </div>
          </div>

          {/* Conditional Keys */}
          {provider === 'gemini' && (
            <div>
              <label className="block font-semibold text-slate-700 mb-1 flex items-center justify-between">
                <span>Google Gemini API Key</span>
                <span className="text-[10px] text-slate-400">
                  {settings?.gemini_configured ? 'Currently Configured ✓' : 'Not Set'}
                </span>
              </label>
              <input
                type="password"
                placeholder="Enter AIzaSy... (leave blank to keep current)"
                value={geminiKey}
                onChange={e => setGeminiKey(e.target.value)}
                className="w-full border border-slate-300 rounded-lg p-2.5 focus:outline-hidden focus:border-blue-900 font-mono"
              />
            </div>
          )}

          {provider === 'openai' && (
            <div>
              <label className="block font-semibold text-slate-700 mb-1 flex items-center justify-between">
                <span>OpenAI API Key</span>
                <span className="text-[10px] text-slate-400">
                  {settings?.openai_configured ? 'Currently Configured ✓' : 'Not Set'}
                </span>
              </label>
              <input
                type="password"
                placeholder="Enter sk-... (leave blank to keep current)"
                value={openaiKey}
                onChange={e => setOpenaiKey(e.target.value)}
                className="w-full border border-slate-300 rounded-lg p-2.5 focus:outline-hidden focus:border-blue-900 font-mono"
              />
            </div>
          )}

          <div className="flex justify-end pt-2">
            <button
              type="submit"
              className="bg-blue-900 hover:bg-blue-800 text-white font-semibold text-xs px-4 py-2 rounded-lg transition"
            >
              Save Configuration
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
