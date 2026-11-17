import os
import re
import json
from typing import Dict, Any, List, Optional, Tuple
import httpx
from backend.app.config import settings
from backend.app.schemas.pydantic_schemas import CitationItem, QueryResponse

class QueryRouter:
    """
    Intelligently classifies user queries to route between deterministic financial engine,
    ESG analysis, hybrid document retrieval, or combined synthesis.
    """

    @classmethod
    def classify(cls, query: str) -> str:
        q = query.lower()

        # Company comparison
        if any(term in q for term in ["compare", "versus", " vs ", "better than", "higher than"]):
            return "COMPARISON"

        # ESG indicators or sustainability
        if any(term in q for term in ["esg", "carbon", "emission", "renewable", "water", "waste", "diversity",
                                      "safety", "governance", "independent director", "brsr", "board"]):
            return "ESG"

        # Financial explanation
        if any(term in q for term in ["why did", "explain the", "driver of", "reason for", "cause of", "factors behind"]):
            if any(term in q for term in ["margin", "revenue", "profit", "growth", "cost", "cash flow", "decline", "increase"]):
                return "FINANCIAL_EXPLANATION"

        # Deterministic calculations
        if any(term in q for term in ["calculate", "what is the roe", "what is roa", "current ratio",
                                      "debt to equity", "growth rate", "net profit margin", "operating margin"]):
            return "FINANCIAL_CALCULATION"

        # General Document inquiries
        if any(term in q for term in ["summarize", "management discussion", "auditor", "risk", "annual report", "section"]):
            return "DOCUMENT"

        return "COMBINED"


class LLMService:
    """
    Multi-provider LLM abstraction layer with strict evidence grounding
    and zero-hallucination deterministic fallback engine.
    """

    @classmethod
    def _build_grounded_prompt(
        cls,
        query: str,
        query_type: str,
        metrics: Optional[Dict[str, Any]],
        esg: Optional[Dict[str, Any]],
        evidence: List[Dict[str, Any]]
    ) -> str:
        prompt_parts = [
            "You are an expert AI Financial Analyst and corporate report evaluation system.",
            "STRICT RULES:",
            "1. Answer the user query using ONLY the verified financial metrics and retrieved document evidence provided below.",
            "2. Distinguish clearly between deterministically calculated financial facts and qualitative explanations inferred from documents.",
            "3. If the retrieved evidence does not contain the answer, explicitly state: 'The provided reports do not contain sufficient evidence to confirm this.' DO NOT speculate or hallucinate reasons.",
            "4. For every claim based on a document, include an inline citation in the exact format: [Document Title, Page X, Section].",
            "\n--- VERIFIED FINANCIAL ENGINE DATA ---"
        ]

        if metrics:
            prompt_parts.append(f"Company: {metrics.get('company_name')} ({metrics.get('ticker')})")
            prompt_parts.append(f"Currency: {metrics.get('currency')} | Units: {metrics.get('units')}")
            if "ratios" in metrics:
                for r in metrics["ratios"][-3:]:
                    prompt_parts.append(
                        f"FY{r.get('fiscal_year')}: Revenue={r.get('revenue')}, Net Profit={r.get('net_profit')}, "
                        f"Operating Margin={r.get('operating_profit_margin_pct')}%, Net Margin={r.get('net_profit_margin_pct')}%, "
                        f"Revenue Growth={r.get('revenue_growth_pct')}%, ROE={r.get('return_on_equity_pct')}%, "
                        f"Debt-to-Equity={r.get('debt_to_equity')}, OCF={r.get('operating_cash_flow')}"
                    )
            if "summary_insights" in metrics:
                prompt_parts.append("Calculated Trends: " + " ".join(metrics["summary_insights"]))
        else:
            prompt_parts.append("No structured financial data available.")

        prompt_parts.append("\n--- ESG DISCLOSURES & SCORE ---")
        if esg:
            prompt_parts.append(
                f"ESG Overall Score: {esg.get('overall_esg_score')} / 100 (Coverage: {esg.get('data_coverage_pct')}%) | "
                f"E: {esg.get('environmental_score')}, S: {esg.get('social_score')}, G: {esg.get('governance_score')}. "
                "Notice: Project-specific methodology, not commercial rating."
            )
        else:
            prompt_parts.append("No ESG data available.")

        prompt_parts.append("\n--- RETRIEVED DOCUMENT EVIDENCE ---")
        if evidence:
            for idx, item in enumerate(evidence, 1):
                prompt_parts.append(
                    f"Evidence [{idx}] | Document: {item.get('document_title')} | Type: {item.get('document_type')} | "
                    f"Year: {item.get('fiscal_year')} | Page: {item.get('page_number')} | Section: {item.get('section')}\n"
                    f"Content: \"{item.get('content')}\"\n"
                )
        else:
            prompt_parts.append("No document passages retrieved for this query.")

        prompt_parts.append(f"\nUSER QUESTION: {query}")
        prompt_parts.append("\nANSWER (Professional, structured, grounded with citations):")
        return "\n".join(prompt_parts)

    @classmethod
    def _call_gemini(cls, prompt: str) -> str:
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY not configured.")
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.LLM_MODEL_NAME}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.1, "maxOutputTokens": 1024}
        }
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

    @classmethod
    def _call_openai(cls, prompt: str) -> str:
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY not configured.")
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 1024
        }
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

    @classmethod
    def _call_ollama(cls, prompt: str) -> str:
        url = f"{settings.OLLAMA_BASE_URL}/api/generate"
        payload = {"model": "llama3.2", "prompt": prompt, "stream": False}
        with httpx.Client(timeout=45.0) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["response"]

    @classmethod
    def _deterministic_synthesis(
        cls,
        query: str,
        query_type: str,
        metrics: Optional[Dict[str, Any]],
        esg: Optional[Dict[str, Any]],
        evidence: List[Dict[str, Any]]
    ) -> str:
        """
        High-integrity deterministic analysis generator when external LLM is not active.
        Zero hallucinations: strictly synthesizes verified financial numbers and exact retrieved passages.
        """
        lines = []

        # 1. Financial calculations block
        if metrics and "ratios" in metrics and metrics["ratios"]:
            latest = metrics["ratios"][-1]
            prev = metrics["ratios"][-2] if len(metrics["ratios"]) > 1 else None
            u = metrics.get("units", "units")
            c = metrics.get("currency", "")

            lines.append(f"### Deterministic Financial Analysis: {metrics.get('company_name')} ({metrics.get('ticker')})")
            lines.append(f"**Reporting Period:** FY{latest.get('fiscal_year')} | **Currency:** {c} ({u})")
            
            # Key ratios table
            lines.append("\n**Verified Core Financial Metrics:**")
            if latest.get("revenue") is not None:
                rev_line = f"- **Revenue:** {c} {latest['revenue']:,.2f} {u}"
                if latest.get("revenue_growth_pct") is not None:
                    rev_line += f" (YoY Growth: **{latest['revenue_growth_pct']:+.2f}%**)"
                lines.append(rev_line)
            if latest.get("operating_profit_margin_pct") is not None:
                op_line = f"- **Operating Profit Margin:** **{latest['operating_profit_margin_pct']:.2f}%**"
                if prev and prev.get("operating_profit_margin_pct") is not None:
                    delta = latest['operating_profit_margin_pct'] - prev['operating_profit_margin_pct']
                    op_line += f" (YoY Change: **{delta:+.2f}% pts** compared to FY{prev['fiscal_year']} {prev['operating_profit_margin_pct']:.2f}%)"
                lines.append(op_line)
            if latest.get("net_profit_margin_pct") is not None:
                lines.append(f"- **Net Profit Margin:** **{latest['net_profit_margin_pct']:.2f}%** (Net Profit: {c} {latest.get('net_profit', 0):,.2f} {u})")
            if latest.get("return_on_equity_pct") is not None:
                lines.append(f"- **Return on Equity (ROE):** **{latest['return_on_equity_pct']:.2f}%**")
            if latest.get("debt_to_equity") is not None:
                lines.append(f"- **Debt-to-Equity Ratio:** **{latest['debt_to_equity']:.2f}**")
            if latest.get("operating_cash_flow") is not None:
                lines.append(f"- **Operating Cash Flow:** {c} {latest['operating_cash_flow']:,.2f} {u}")

        # 2. ESG Block if query is ESG related
        if query_type in ["ESG", "COMBINED"] and esg:
            lines.append("\n### Verified ESG Performance (Project-Specific Model)")
            if esg.get("overall_esg_score") is not None:
                lines.append(f"- **Overall ESG Score:** **{esg['overall_esg_score']} / 100** (Data Coverage: {esg.get('data_coverage_pct', 0):.1f}%)")
            lines.append(f"- **Environmental Pillar:** {esg.get('environmental_score', 'N/A')} / 100")
            lines.append(f"- **Social Pillar:** {esg.get('social_score', 'N/A')} / 100")
            lines.append(f"- **Governance Pillar:** {esg.get('governance_score', 'N/A')} / 100")
            lines.append("*(Note: Academic internal methodology; not an official commercial credit or ESG rating)*")

        # 3. Qualitative Evidence & Explanations from Documents
        lines.append("\n### Supporting Document Evidence & Citations")
        if evidence:
            lines.append(f"Retrieved **{len(evidence)} verified passages** from uploaded corporate reports:")
            for idx, item in enumerate(evidence, 1):
                citation_ref = f"[{item.get('document_title', 'Report')}, Page {item.get('page_number', 'N/A')}, Section: {item.get('section', 'General')}]"
                snippet = item.get("content", "").strip()
                if len(snippet) > 300:
                    snippet = snippet[:300] + "..."
                lines.append(f"\n**{idx}. Citation: {citation_ref}** (Relevance: {item.get('rerank_score', item.get('rrf_score', 0)):.3f})")
                lines.append(f"> \"{snippet}\"")
        else:
            lines.append(
                "> **Notice:** No relevant document passages were retrieved for this specific qualitative inquiry. "
                "Per anti-hallucination protocols, no speculative root causes are asserted."
            )

        return "\n".join(lines)

    @classmethod
    def answer_query(
        cls,
        query: str,
        company_id: Optional[int],
        fiscal_year: Optional[int],
        metrics: Optional[Dict[str, Any]],
        esg: Optional[Dict[str, Any]],
        evidence: List[Dict[str, Any]]
    ) -> QueryResponse:
        """
        Executes query routing, calls the appropriate LLM provider or deterministic engine,
        and packages the grounded response with citations.
        """
        query_type = QueryRouter.classify(query)
        warnings = []

        # Convert evidence hits to CitationItem objects
        citations: List[CitationItem] = []
        for item in evidence:
            citations.append(
                CitationItem(
                    document_title=item.get("document_title", "Document"),
                    document_type=item.get("document_type", "Report"),
                    fiscal_year=item.get("fiscal_year"),
                    page_number=item.get("page_number", 1),
                    section=item.get("section", "General"),
                    chunk_id=item.get("chunk_id", ""),
                    relevance_score=item.get("rerank_score") or item.get("rrf_score"),
                    snippet=item.get("content", "")[:300]
                )
            )

        prompt = cls._build_grounded_prompt(query, query_type, metrics, esg, evidence)
        provider_used = "deterministic"
        answer = ""

        # Attempt configured LLM provider
        target_provider = settings.LLM_PROVIDER.lower()
        if target_provider == "gemini" and settings.GEMINI_API_KEY:
            try:
                answer = cls._call_gemini(prompt)
                provider_used = "gemini"
            except Exception as e:
                warnings.append(f"Gemini API request failed ({str(e)}). Switched to deterministic analysis.")
        elif target_provider == "openai" and settings.OPENAI_API_KEY:
            try:
                answer = cls._call_openai(prompt)
                provider_used = "openai"
            except Exception as e:
                warnings.append(f"OpenAI API request failed ({str(e)}). Switched to deterministic analysis.")
        elif target_provider == "ollama":
            try:
                answer = cls._call_ollama(prompt)
                provider_used = "ollama"
            except Exception as e:
                warnings.append(f"Ollama request failed ({str(e)}). Switched to deterministic analysis.")

        # Fallback to deterministic synthesis if provider didn't produce an answer
        if not answer:
            answer = cls._deterministic_synthesis(query, query_type, metrics, esg, evidence)
            provider_used = "deterministic_synthesis"

        return QueryResponse(
            query=query,
            query_type=query_type,
            answer=answer,
            citations=citations,
            deterministic_metrics=metrics,
            esg_summary=esg,
            llm_provider=provider_used,
            grounded=True,
            warnings=warnings
        )
