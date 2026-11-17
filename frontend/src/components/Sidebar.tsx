import React from 'react';
import {
  LayoutDashboard,
  CloudDownload,
  Building,
  TrendingUp,
  FileText,
  MessageSquareCode,
  ShieldCheck,
  Scale,
  FileBarChart,
  Settings
} from 'lucide-react';

export type NavTab =
  | 'overview'
  | 'collection'
  | 'companies'
  | 'financials'
  | 'documents'
  | 'chat'
  | 'esg'
  | 'comparison'
  | 'reports'
  | 'settings';

interface SidebarProps {
  activeTab: NavTab;
  onTabChange: (tab: NavTab) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, onTabChange }) => {
  const menuItems = [
    { id: 'overview', label: 'Overview Dashboard', icon: LayoutDashboard },
    { id: 'collection', label: 'Data Collection', icon: CloudDownload, badge: 'Auto' },
    { id: 'companies', label: 'Companies', icon: Building },
    { id: 'financials', label: 'Financial Analysis', icon: TrendingUp },
    { id: 'documents', label: 'Document Library', icon: FileText },
    { id: 'chat', label: 'AI Analyst Chat', icon: MessageSquareCode, badge: 'RAG' },
    { id: 'esg', label: 'ESG Evaluation', icon: ShieldCheck },
    { id: 'comparison', label: 'Company Comparison', icon: Scale },
    { id: 'reports', label: 'Generated Reports', icon: FileBarChart },
    { id: 'settings', label: 'System Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col shrink-0 min-h-[calc(100vh-4rem)] border-r border-slate-800">
      <div className="p-4 border-b border-slate-800">
        <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
          Navigation Modules
        </span>
      </div>
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id as NavTab)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                isActive
                  ? 'bg-blue-800 text-white shadow-xs'
                  : 'text-slate-300 hover:bg-slate-800 hover:text-white'
              }`}
            >
              <div className="flex items-center space-x-3">
                <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span
                  className={`text-[9px] font-bold px-1.5 py-0.5 rounded ${
                    isActive
                      ? 'bg-blue-900 text-blue-200'
                      : 'bg-slate-800 text-slate-300 border border-slate-700'
                  }`}
                >
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Footer Info */}
      <div className="p-4 border-t border-slate-800 text-[11px] text-slate-400">
        <div className="flex items-center justify-between">
          <span>Qdrant Local Vector DB</span>
          <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
        </div>
        <div className="mt-1 text-[10px] text-slate-400">
          Deterministic Numerical Engine
        </div>
      </div>
    </aside>
  );
};
