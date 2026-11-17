import React, { useState, useEffect, useRef } from 'react';
import { Company, QueryResponse, CitationItem } from '../types';
import { api } from '../api/client';
import {
  Send, Bot, User, BookOpen, ShieldCheck, CheckCircle2,
  AlertCircle, Sparkles, CornerDownRight, FileText, ChevronRight
} from 'lucide-react';

interface AIAssistantChatProps {
  company: Company | null;
}

interface ChatMessage {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  queryType?: string;
  citations?: CitationItem[];
  grounded?: boolean;
  timestamp: string;
}

export const AIAssistantChat: React.FC<AIAssistantChatProps> = ({ company }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputQuery, setInputQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedCitation, setSelectedCitation] = useState<CitationItem | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const sampleQuestions = [
    "Why did operating margin change in FY2024?",
    "Calculate ROE and Net Margin for FY2024",
    "What are the principal risk factors disclosed in the annual report?",
    "What are the company's Scope 1 and Scope 2 carbon emissions?",
    "Summarize management discussion on revenue growth drivers.",
    "Explain the change in operating cash flows."
  ];

  useEffect(() => {
    if (!company) return;
    // Initial greeting
    setMessages([
      {
        id: 'initial',
        sender: 'assistant',
        text: `Hello! I am your AI Financial Analyst for **${company.name} (${company.ticker})**. ` +
              `I answer questions using **Hybrid RAG** (Dense Qdrant search + BM25 keyword matching + Cross-encoder reranking) ` +
              `and **deterministic Python calculations**. All claims include verifiable source citations with page numbers.`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
    ]);
  }, [company]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (queryText?: string) => {
    const q = (queryText || inputQuery).trim();
    if (!q || !company || loading) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text: q,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages(prev => [...prev, userMsg]);
    setInputQuery('');
    setLoading(true);

    try {
      const resp: QueryResponse = await api.queryChat({
        query: q,
        company_id: company.id,
        top_k: 4,
        enable_reranking: true
      });

      const assistantMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: resp.answer,
        queryType: resp.query_type,
        citations: resp.citations,
        grounded: resp.grounded,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, assistantMsg]);
    } catch (err: any) {
      const errorMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: `Error processing inquiry: ${err.response?.data?.detail || err.message}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  if (!company) {
    return <div className="p-8 text-center text-slate-500">Please select a company to chat with the AI Analyst.</div>;
  }

  return (
    <div className="h-[calc(100vh-8.5rem)] flex flex-col bg-white border border-slate-200 rounded-xl shadow-2xs overflow-hidden">
      {/* Chat Header */}
      <div className="px-6 py-3.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-blue-900 flex items-center justify-center text-white font-bold text-xs">
            RAG
          </div>
          <div>
            <h2 className="text-xs font-bold text-slate-900 flex items-center space-x-2">
              <span>AI Financial Analyst • {company.ticker}</span>
              <span className="text-[10px] font-semibold bg-emerald-100 text-emerald-800 px-2 py-0.2 rounded">
                Grounded Hybrid Retrieval
              </span>
            </h2>
            <p className="text-[11px] text-slate-500">Cross-encoder reranking & verified page citations</p>
          </div>
        </div>
      </div>

      {/* Messages Feed */}
      <div className="flex-1 p-6 overflow-y-auto space-y-5 bg-slate-50/50">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex items-start space-x-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.sender === 'assistant' && (
              <div className="w-7 h-7 rounded-lg bg-blue-950 text-white flex items-center justify-center shrink-0 mt-0.5">
                <Bot className="w-4 h-4" />
              </div>
            )}
            <div
              className={`max-w-3xl rounded-xl p-4 text-xs shadow-2xs leading-relaxed ${
                msg.sender === 'user'
                  ? 'bg-blue-900 text-white font-medium ml-12'
                  : 'bg-white text-slate-800 border border-slate-200 mr-12'
              }`}
            >
              {/* Type Badge */}
              {msg.queryType && (
                <div className="mb-2 flex items-center space-x-2">
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-blue-50 text-blue-900 border border-blue-200">
                    Routing: {msg.queryType}
                  </span>
                  {msg.grounded && (
                    <span className="text-[10px] text-emerald-700 flex items-center space-x-1 font-semibold">
                      <CheckCircle2 className="w-3 h-3" />
                      <span>Zero-Hallucination Grounded</span>
                    </span>
                  )}
                </div>
              )}

              {/* Message Content */}
              <div className="whitespace-pre-wrap font-sans text-xs space-y-1.5">
                {msg.text}
              </div>

              {/* Citations Block */}
              {msg.citations && msg.citations.length > 0 && (
                <div className="mt-4 pt-3 border-t border-slate-200">
                  <div className="text-[11px] font-bold text-slate-700 mb-2 flex items-center space-x-1.5">
                    <BookOpen className="w-3.5 h-3.5 text-blue-900" />
                    <span>Supporting Document Citations ({msg.citations.length}):</span>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    {msg.citations.map((cit, idx) => (
                      <button
                        key={idx}
                        onClick={() => setSelectedCitation(cit)}
                        className="text-left p-2.5 rounded-lg border border-slate-200 bg-slate-50 hover:bg-blue-50 hover:border-blue-300 transition text-[11px] group"
                      >
                        <div className="flex items-center justify-between font-bold text-blue-950 mb-0.5">
                          <span className="truncate max-w-[180px]">[{idx + 1}] {cit.document_title}</span>
                          <span className="bg-blue-100 text-blue-900 px-1.5 py-0.2 rounded text-[10px] shrink-0 font-semibold">
                            P.{cit.page_number}
                          </span>
                        </div>
                        <div className="text-[10px] text-slate-500 mb-1">Section: {cit.section}</div>
                        <p className="text-slate-600 italic line-clamp-2">"{cit.snippet}"</p>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              <div className="mt-1 text-right text-[10px] opacity-60">
                {msg.timestamp}
              </div>
            </div>
            {msg.sender === 'user' && (
              <div className="w-7 h-7 rounded-lg bg-blue-800 text-white flex items-center justify-center shrink-0 mt-0.5">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="flex items-center space-x-2 text-xs text-slate-500 italic pl-10">
            <span className="w-2 h-2 rounded-full bg-blue-900 animate-pulse"></span>
            <span>Synthesizing deterministic metrics and cross-encoder evidence...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Questions */}
      <div className="px-6 py-2.5 bg-slate-50 border-t border-slate-200 flex items-center space-x-2 overflow-x-auto text-xs">
        <span className="text-[11px] font-semibold text-slate-500 shrink-0">Sample Inquiries:</span>
        {sampleQuestions.map((q, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(q)}
            className="shrink-0 bg-white hover:bg-blue-50 hover:border-blue-300 border border-slate-200 text-slate-700 text-[11px] px-2.5 py-1 rounded-full transition"
          >
            {q}
          </button>
        ))}
      </div>

      {/* Input Box */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend();
        }}
        className="p-4 bg-white border-t border-slate-200 flex items-center space-x-3"
      >
        <input
          type="text"
          placeholder={`Ask about ${company.name}'s financial ratios, margins, risk factors, or ESG disclosures...`}
          value={inputQuery}
          onChange={(e) => setInputQuery(e.target.value)}
          className="flex-1 border border-slate-300 rounded-lg px-4 py-2.5 text-xs focus:outline-hidden focus:border-blue-900"
        />
        <button
          type="submit"
          disabled={!inputQuery.trim() || loading}
          className="bg-blue-900 hover:bg-blue-800 disabled:opacity-50 text-white px-4 py-2.5 rounded-lg text-xs font-semibold flex items-center space-x-1.5 transition shadow-2xs"
        >
          <span>Send</span>
          <Send className="w-3.5 h-3.5" />
        </button>
      </form>

      {/* Citation Detail Modal */}
      {selectedCitation && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-xl max-w-xl w-full p-6 border border-slate-200">
            <div className="flex items-center justify-between pb-3 border-b border-slate-200 mb-3">
              <div className="flex items-center space-x-2">
                <FileText className="w-4 h-4 text-blue-900" />
                <h3 className="text-sm font-bold text-slate-900">{selectedCitation.document_title}</h3>
              </div>
              <button
                onClick={() => setSelectedCitation(null)}
                className="text-xs font-bold text-slate-400 hover:text-slate-600"
              >
                ✕
              </button>
            </div>
            <div className="space-y-3 text-xs">
              <div className="flex items-center space-x-4 text-slate-600 bg-slate-50 p-2.5 rounded-lg border border-slate-200">
                <div>Page: <b className="text-slate-900">{selectedCitation.page_number}</b></div>
                <div>Section: <b className="text-slate-900">{selectedCitation.section}</b></div>
                <div>Type: <b className="text-slate-900">{selectedCitation.document_type}</b></div>
                {selectedCitation.relevance_score && (
                  <div>Rerank Score: <b className="text-emerald-700">{selectedCitation.relevance_score.toFixed(3)}</b></div>
                )}
              </div>
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Verbatim Extracted Passage:</label>
                <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 font-mono text-[11px] leading-relaxed max-h-56 overflow-y-auto">
                  "{selectedCitation.snippet}"
                </div>
              </div>
              <div className="text-[10px] text-slate-400 italic">
                *Verified passage preserved during structure-aware PDF chunking with original page index.
              </div>
            </div>
            <div className="mt-4 pt-3 border-t border-slate-200 flex justify-end">
              <button
                onClick={() => setSelectedCitation(null)}
                className="px-4 py-1.5 bg-slate-900 text-white rounded text-xs font-semibold"
              >
                Done
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
