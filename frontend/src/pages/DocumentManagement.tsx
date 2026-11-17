import React, { useState, useEffect } from 'react';
import { Company, DocumentItem } from '../types';
import { api } from '../api/client';
import {
  FileText, Upload, Trash2, Download, CheckCircle2,
  Clock, AlertTriangle, Eye, Layers, FileDown
} from 'lucide-react';

interface DocumentManagementProps {
  company: Company | null;
}

export const DocumentManagement: React.FC<DocumentManagementProps> = ({ company }) => {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [showUploadModal, setShowUploadModal] = useState<boolean>(false);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [documentType, setDocumentType] = useState<string>('Annual Report');
  const [fiscalYear, setFiscalYear] = useState<number>(2024);
  const [uploadProgress, setUploadProgress] = useState<string>('');
  const [selectedDocChunks, setSelectedDocChunks] = useState<any[]>([]);
  const [viewingDocTitle, setViewingDocTitle] = useState<string>('');

  useEffect(() => {
    if (!company) return;
    loadDocuments(company.id);
  }, [company]);

  const loadDocuments = async (companyId: number) => {
    setLoading(true);
    try {
      const docs = await api.getDocuments(companyId);
      setDocuments(docs);
    } catch (err) {
      console.error('Failed to load documents:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFile || !company) return;
    setUploadProgress('Extracting text & tables, building structure-aware chunks, and indexing Qdrant vectors...');
    try {
      await api.uploadDocument(company.id, uploadFile, documentType, fiscalYear);
      setUploadProgress('Document successfully indexed into Qdrant vector database!');
      setTimeout(() => {
        setShowUploadModal(false);
        setUploadProgress('');
        loadDocuments(company.id);
      }, 1500);
    } catch (err: any) {
      setUploadProgress(`Error: ${err.response?.data?.detail || 'Upload failed'}`);
    }
  };

  const handleDelete = async (id: number, title: string) => {
    if (!window.confirm(`Delete document "${title}" and remove its chunks from the vector database?`)) return;
    try {
      await api.deleteDocument(id);
      if (company) loadDocuments(company.id);
    } catch (err) {
      console.error('Delete failed:', err);
    }
  };

  const handleViewChunks = async (doc: DocumentItem) => {
    try {
      const res = await fetch(`/api/v1/documents/${doc.id}/chunks`);
      const chunks = await res.json();
      setSelectedDocChunks(chunks);
      setViewingDocTitle(doc.title);
    } catch (err) {
      console.error('Failed to fetch chunks:', err);
    }
  };

  if (!company) {
    return <div className="p-8 text-center text-slate-500">Please select a company first.</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-2xs flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-900 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
              Qdrant Vector Intelligence
            </span>
            <span className="text-xs text-slate-500">Structure-Aware Chunking</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 mt-1">Corporate Report Document Library</h1>
          <p className="text-xs text-slate-600 mt-0.5">
            Preserves original page numbers, table geometries, and section boundaries for zero-hallucination citations.
          </p>
        </div>
        <button
          onClick={() => setShowUploadModal(true)}
          className="mt-4 md:mt-0 flex items-center space-x-1.5 bg-blue-900 hover:bg-blue-800 text-white text-xs font-semibold px-4 py-2 rounded-lg transition shadow-2xs"
        >
          <Upload className="w-3.5 h-3.5" />
          <span>Upload PDF Report</span>
        </button>
      </div>

      {/* Documents Table */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
        <h2 className="text-sm font-bold text-slate-900 mb-3">Indexed Corporate Reports ({documents.length})</h2>
        <div className="overflow-x-auto rounded-lg border border-slate-200">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-900 text-white font-semibold">
              <tr>
                <th className="px-4 py-2.5">Document Title</th>
                <th className="px-4 py-2.5">Type</th>
                <th className="px-4 py-2.5">Year</th>
                <th className="px-4 py-2.5">Pages</th>
                <th className="px-4 py-2.5">Vector Chunks</th>
                <th className="px-4 py-2.5">Status</th>
                <th className="px-4 py-2.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {documents.map((doc) => (
                <tr key={doc.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-semibold text-slate-900 flex items-center space-x-2">
                    <FileText className="w-4 h-4 text-blue-900 shrink-0" />
                    <span>{doc.title}</span>
                  </td>
                  <td className="px-4 py-3 text-slate-600">{doc.document_type}</td>
                  <td className="px-4 py-3 font-medium">{doc.fiscal_year ? `FY${doc.fiscal_year}` : '-'}</td>
                  <td className="px-4 py-3">{doc.total_pages} pgs</td>
                  <td className="px-4 py-3">
                    <span className="font-semibold text-blue-900">{doc.total_chunks}</span> chunks
                  </td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      doc.status === 'INDEXED' ? 'bg-emerald-100 text-emerald-800' :
                      doc.status === 'PROCESSING' ? 'bg-amber-100 text-amber-800' : 'bg-rose-100 text-rose-800'
                    }`}>
                      {doc.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right space-x-2">
                    <button
                      onClick={() => handleViewChunks(doc)}
                      className="p-1.5 text-blue-900 hover:bg-blue-50 rounded"
                      title="Inspect extracted chunks & page numbers"
                    >
                      <Eye className="w-3.5 h-3.5 inline" />
                    </button>
                    <a
                      href={`/api/v1/documents/${doc.id}/download`}
                      download
                      className="p-1.5 text-slate-600 hover:bg-slate-100 rounded inline-block"
                      title="Download PDF"
                    >
                      <Download className="w-3.5 h-3.5" />
                    </a>
                    <button
                      onClick={() => handleDelete(doc.id, doc.title)}
                      className="p-1.5 text-rose-600 hover:bg-rose-50 rounded"
                      title="Delete"
                    >
                      <Trash2 className="w-3.5 h-3.5 inline" />
                    </button>
                  </td>
                </tr>
              ))}
              {documents.length === 0 && (
                <tr>
                  <td colSpan={7} className="text-center py-8 text-slate-400">
                    No corporate documents indexed yet. Upload a PDF or use Data Collection.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Chunk Inspector Modal / Panel */}
      {selectedDocChunks.length > 0 && (
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs space-y-3">
          <div className="flex items-center justify-between pb-3 border-b border-slate-200">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Extracted Chunks & Page Metadata</h3>
              <p className="text-xs text-slate-500">Document: <b>{viewingDocTitle}</b> ({selectedDocChunks.length} chunks indexed in Qdrant)</p>
            </div>
            <button
              onClick={() => setSelectedDocChunks([])}
              className="text-xs font-semibold text-slate-400 hover:text-slate-600"
            >
              Close Inspector ✕
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-96 overflow-y-auto">
            {selectedDocChunks.map((chk, idx) => (
              <div key={idx} className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs">
                <div className="flex items-center justify-between font-semibold text-slate-700 mb-1.5">
                  <span className="bg-blue-100 text-blue-900 px-2 py-0.5 rounded text-[10px]">
                    Page {chk.page_number} • {chk.section}
                  </span>
                  <span className="text-[10px] text-slate-400">
                    Chunk #{chk.chunk_index} ({chk.token_count} words)
                  </span>
                </div>
                <p className="text-slate-600 text-[11px] leading-relaxed line-clamp-4">
                  "{chk.content}"
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Upload PDF Modal */}
      {showUploadModal && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-xl max-w-md w-full p-6 border border-slate-200">
            <h3 className="text-sm font-bold text-slate-900 mb-2">Upload Corporate Report PDF</h3>
            <p className="text-xs text-slate-500 mb-4">
              Upload Annual Reports, Sustainability Reports (BRSR), or Quarterly Results.
            </p>
            <form onSubmit={handleUpload} className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold text-slate-700 mb-1">Document Type</label>
                <select
                  value={documentType}
                  onChange={e => setDocumentType(e.target.value)}
                  className="w-full border border-slate-300 rounded p-1.5"
                >
                  <option value="Annual Report">Annual Report</option>
                  <option value="Quarterly Report">Quarterly Report</option>
                  <option value="Sustainability Report / BRSR">Sustainability Report / BRSR</option>
                  <option value="Investor Presentation">Investor Presentation</option>
                </select>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Fiscal Year</label>
                <input
                  type="number"
                  value={fiscalYear}
                  onChange={e => setFiscalYear(Number(e.target.value))}
                  className="w-full border border-slate-300 rounded p-1.5"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">Select PDF File</label>
                <input
                  type="file"
                  accept=".pdf"
                  required
                  onChange={e => setUploadFile(e.target.files ? e.target.files[0] : null)}
                  className="w-full text-slate-500 file:mr-4 file:py-2 file:px-3 file:rounded file:border-0 file:text-xs file:font-semibold file:bg-blue-50 file:text-blue-900 hover:file:bg-blue-100 cursor-pointer"
                />
              </div>

              {uploadProgress && (
                <div className="p-2.5 rounded bg-blue-50 text-blue-900 border border-blue-200 text-xs">
                  {uploadProgress}
                </div>
              )}

              <div className="flex justify-end space-x-2 pt-3">
                <button
                  type="button"
                  onClick={() => setShowUploadModal(false)}
                  className="px-3 py-1.5 border border-slate-300 rounded font-semibold text-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!uploadFile}
                  className="px-4 py-1.5 bg-blue-900 text-white rounded font-semibold hover:bg-blue-800 disabled:opacity-50"
                >
                  Upload & Index
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
