import os
import shutil
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.database import get_db
from backend.app.models.schema_models import Company, Document, DocumentChunk
from backend.app.schemas.pydantic_schemas import DocumentResponse, DocumentChunkResponse
from backend.app.rag.document_parser import DocumentParser
from backend.app.rag.chunker import StructureAwareChunker
from backend.app.rag.vector_store import VectorStoreManager

router = APIRouter(prefix="/documents", tags=["Document Management & Ingestion"])

@router.get("", response_model=List[DocumentResponse])
def list_documents(company_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    query = db.query(Document)
    if company_id is not None:
        query = query.filter(Document.company_id == company_id)
    return query.order_by(Document.created_at.desc()).all()

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    company_id: int = Form(...),
    document_type: str = Form("Annual Report"),
    fiscal_year: Optional[int] = Form(None),
    title: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Ingest a corporate report PDF:
    Validates file type/size, detects duplicates via SHA-256,
    extracts text and tables with page preservation, performs structure-aware chunking,
    and indexes dense vectors into Qdrant.
    """
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    filename = file.filename
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF documents are supported for RAG indexing.")

    file_bytes = await file.read()
    file_size = len(file_bytes)
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if file_size > max_bytes:
        raise HTTPException(status_code=400, detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB.")

    # Save to disk
    save_path = settings.UPLOAD_DIR / f"{company_id}_{filename}"
    with open(save_path, "wb") as f:
        f.write(file_bytes)

    # Compute SHA-256 for duplicate detection
    file_hash = DocumentParser.compute_file_hash(str(save_path))
    existing_doc = db.query(Document).filter(Document.file_hash == file_hash).first()
    if existing_doc:
        os.remove(save_path)
        raise HTTPException(
            status_code=400,
            detail=f"Duplicate document detected! This file is already indexed as '{existing_doc.title}' (ID {existing_doc.id})."
        )

    doc_title = title or f"{comp.ticker} {document_type} {f'FY{fiscal_year}' if fiscal_year else ''}".strip()

    # Create Document record
    doc_obj = Document(
        company_id=comp.id,
        title=doc_title,
        file_name=filename,
        file_path=str(save_path),
        file_hash=file_hash,
        file_size_bytes=file_size,
        document_type=document_type,
        fiscal_year=fiscal_year,
        status="PROCESSING"
    )
    db.add(doc_obj)
    db.commit()
    db.refresh(doc_obj)

    # Ingestion Pipeline: Parse -> Chunk -> Index
    try:
        pages_data, metadata = DocumentParser.parse_pdf(str(save_path))
        doc_obj.total_pages = metadata["total_pages"]

        chunks = StructureAwareChunker.chunk_pages(pages_data, {
            "document_id": doc_obj.id,
            "company_id": comp.id,
            "company_name": comp.name,
            "fiscal_year": fiscal_year,
            "title": doc_title,
            "document_type": document_type
        })

        # Save chunks in relational DB
        for chk in chunks:
            chunk_rec = DocumentChunk(
                document_id=doc_obj.id,
                company_id=comp.id,
                fiscal_year=fiscal_year,
                page_number=chk["page_number"],
                section=chk["section"],
                chunk_index=chk["chunk_index"],
                chunk_id=chk["chunk_id"],
                content=chk["content"],
                token_count=chk["token_count"],
                is_table=chk["is_table"]
            )
            db.add(chunk_rec)

        # Index vectors in Qdrant
        VectorStoreManager.upsert_chunks(chunks)

        doc_obj.status = "INDEXED"
        doc_obj.total_chunks = len(chunks)
        db.commit()
        db.refresh(doc_obj)

    except Exception as e:
        db.rollback()
        doc_obj.status = "FAILED"
        doc_obj.error_message = str(e)
        db.commit()
        db.refresh(doc_obj)
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

    return doc_obj

@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    # Remove file from disk
    if os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except Exception:
            pass

    db.delete(doc)
    db.commit()
    return {"message": f"Document '{doc.title}' deleted successfully."}

@router.get("/{document_id}/chunks", response_model=List[DocumentChunkResponse])
def get_document_chunks(document_id: int, db: Session = Depends(get_db)):
    return db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).order_by(DocumentChunk.chunk_index.asc()).all()

@router.get("/{document_id}/download")
def download_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not os.path.exists(doc.file_path):
        raise HTTPException(status_code=404, detail="Document file not found on server.")
    return FileResponse(doc.file_path, filename=doc.file_name, media_type="application/pdf")
