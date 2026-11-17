import os
import hashlib
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
import fitz  # PyMuPDF

class DocumentParser:
    """
    Extracts text, structured sections, and tables from PDFs with page number preservation.
    """

    # Common financial report section header patterns
    SECTION_PATTERNS = [
        (r"(?i)management\s+discussion\s+and\s+analysis", "Management Discussion & Analysis"),
        (r"(?i)director[s']?\s+report", "Directors' Report"),
        (r"(?i)balance\s+sheet", "Balance Sheet"),
        (r"(?i)statement\s+of\s+profit\s+and\s+loss|income\s+statement", "Profit & Loss Statement"),
        (r"(?i)cash\s+flow\s+statement", "Cash Flow Statement"),
        (r"(?i)auditor[s']?\s+report", "Auditor's Report"),
        (r"(?i)corporate\s+governance", "Corporate Governance"),
        (r"(?i)business\s+responsibility\s+and\s+sustainability|brsr|sustainability\s+report", "ESG & Sustainability"),
        (r"(?i)risk\s+management|principal\s+risks", "Risk Management"),
        (r"(?i)financial\s+highlights|performance\s+overview", "Financial Highlights"),
        (r"(?i)notes\s+to\s+(the\s+)?financial\s+statements", "Notes to Financial Statements"),
    ]

    @classmethod
    def compute_file_hash(cls, file_path: str) -> str:
        """Compute SHA-256 hash of a file for duplicate detection."""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()

    @classmethod
    def identify_section(cls, text: str, current_section: str = "General") -> str:
        """Identify if a page or text block contains a known section heading."""
        first_few_lines = "\n".join(text.split("\n")[:8])
        for pattern, section_name in cls.SECTION_PATTERNS:
            if re.search(pattern, first_few_lines):
                return section_name
        return current_section

    @classmethod
    def is_likely_table(cls, text: str) -> bool:
        """Check if text looks like a financial table based on digit density and column patterns."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        if not lines:
            return False
        
        table_like_lines = 0
        for line in lines:
            # Lines with multiple numeric cells separated by whitespace or tabs
            nums = re.findall(r"\b\d+(?:[.,]\d+)?%?\b", line)
            if len(nums) >= 2:
                table_like_lines += 1
                
        return (table_like_lines / max(len(lines), 1)) > 0.35

    @classmethod
    def parse_pdf(cls, file_path: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Parses a PDF file into per-page content structures.
        Returns:
            pages: list of dicts with page_number, text, section, is_table
            summary_meta: total_pages, file_hash, file_size
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_hash = cls.compute_file_hash(file_path)
        file_size = os.path.getsize(file_path)

        doc = fitz.open(file_path)
        total_pages = len(doc)
        pages_data = []
        current_section = "General"

        for page_idx in range(total_pages):
            page = doc[page_idx]
            page_num = page_idx + 1
            raw_text = page.get_text("text").strip()

            if not raw_text:
                continue

            current_section = cls.identify_section(raw_text, current_section)
            is_table = cls.is_likely_table(raw_text)

            pages_data.append({
                "page_number": page_num,
                "text": raw_text,
                "section": current_section,
                "is_table": is_table
            })

        doc.close()

        metadata = {
            "total_pages": total_pages,
            "file_hash": file_hash,
            "file_size_bytes": file_size,
        }

        return pages_data, metadata
