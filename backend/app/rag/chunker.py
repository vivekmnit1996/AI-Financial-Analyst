import re
from typing import List, Dict, Any

class StructureAwareChunker:
    """
    Chunks document pages into retrieval-optimized segments with strict metadata preservation.
    """

    DEFAULT_CHUNK_SIZE = 350  # target words per chunk
    CHUNK_OVERLAP = 50        # words overlap

    @classmethod
    def chunk_pages(
        cls,
        pages_data: List[Dict[str, Any]],
        document_meta: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Takes pages extracted from a document and creates structure-aware chunks.
        
        document_meta must include:
            document_id, company_id, company_name, fiscal_year, title, document_type
        """
        all_chunks = []
        global_chunk_idx = 0

        for page in pages_data:
            page_num = page["page_number"]
            section = page["section"]
            text = page["text"]
            is_table = page["is_table"]

            # If the entire page text is compact, treat it as a single chunk
            words = text.split()
            if len(words) <= cls.DEFAULT_CHUNK_SIZE + 50:
                chunk_id = f"doc_{document_meta['document_id']}_p{page_num}_c0"
                all_chunks.append({
                    "chunk_id": chunk_id,
                    "chunk_index": global_chunk_idx,
                    "document_id": document_meta["document_id"],
                    "company_id": document_meta["company_id"],
                    "company_name": document_meta.get("company_name", "Unknown"),
                    "fiscal_year": document_meta.get("fiscal_year"),
                    "document_title": document_meta.get("title", ""),
                    "document_type": document_meta.get("document_type", "Annual Report"),
                    "page_number": page_num,
                    "section": section,
                    "content": text,
                    "token_count": len(words),
                    "is_table": is_table
                })
                global_chunk_idx += 1
                continue

            # Otherwise, split by paragraphs first to preserve structure
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
            
            # If paragraphs are too few or long, chunk by sliding word window
            current_words = []
            sub_chunk_idx = 0

            for para in paragraphs:
                para_words = para.split()
                if len(current_words) + len(para_words) <= cls.DEFAULT_CHUNK_SIZE:
                    current_words.extend(para_words)
                else:
                    if current_words:
                        chunk_text = " ".join(current_words)
                        chunk_id = f"doc_{document_meta['document_id']}_p{page_num}_c{sub_chunk_idx}"
                        all_chunks.append({
                            "chunk_id": chunk_id,
                            "chunk_index": global_chunk_idx,
                            "document_id": document_meta["document_id"],
                            "company_id": document_meta["company_id"],
                            "company_name": document_meta.get("company_name", "Unknown"),
                            "fiscal_year": document_meta.get("fiscal_year"),
                            "document_title": document_meta.get("title", ""),
                            "document_type": document_meta.get("document_type", "Annual Report"),
                            "page_number": page_num,
                            "section": section,
                            "content": chunk_text,
                            "token_count": len(current_words),
                            "is_table": is_table
                        })
                        global_chunk_idx += 1
                        sub_chunk_idx += 1
                        
                        # Retain overlap
                        overlap_words = current_words[-cls.CHUNK_OVERLAP:] if len(current_words) > cls.CHUNK_OVERLAP else []
                        current_words = overlap_words + para_words
                    else:
                        current_words = para_words

            # Add remaining words
            if current_words:
                chunk_text = " ".join(current_words)
                chunk_id = f"doc_{document_meta['document_id']}_p{page_num}_c{sub_chunk_idx}"
                all_chunks.append({
                    "chunk_id": chunk_id,
                    "chunk_index": global_chunk_idx,
                    "document_id": document_meta["document_id"],
                    "company_id": document_meta["company_id"],
                    "company_name": document_meta.get("company_name", "Unknown"),
                    "fiscal_year": document_meta.get("fiscal_year"),
                    "document_title": document_meta.get("title", ""),
                    "document_type": document_meta.get("document_type", "Annual Report"),
                    "page_number": page_num,
                    "section": section,
                    "content": chunk_text,
                    "token_count": len(current_words),
                    "is_table": is_table
                })
                global_chunk_idx += 1

        return all_chunks
