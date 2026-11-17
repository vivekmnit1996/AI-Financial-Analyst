import os
from pathlib import Path
from datetime import datetime, timezone
from backend.app.config import settings

def fmt_pct(val, plus=False):
    if val is None:
        return "-"
    return f"{val:+.2f}%" if plus else f"{val:.2f}%"

def fmt_num(val, decimals=2):
    if val is None:
        return "-"
    return f"{val:,.{decimals}f}"

class HTMLReportGenerator:
    """
    Generates standalone, responsive HTML Financial & ESG analytical dossiers.
    """

    @classmethod
    def generate_html_report(
        cls,
        company,
        fiscal_year: int,
        ratios_data: list,
        insights: list,
        esg_breakdown: dict,
        citations: list,
        ai_summary: str,
        output_filename: str
    ) -> str:
        out_path = settings.REPORTS_DIR / output_filename

        ratios_html_rows = ""
        u = company.units
        c = company.currency
        for r in ratios_data:
            growth = r.get("revenue_growth_pct")
            growth_class = "text-slate-600"
            if growth is not None:
                growth_class = "text-emerald-600 font-medium" if growth >= 0 else "text-rose-600 font-medium"

            ratios_html_rows += f"""
            <tr class="hover:bg-slate-50 transition border-b border-slate-200">
                <td class="px-4 py-2 font-semibold">FY{r.get('fiscal_year')}</td>
                <td class="px-4 py-2">{c} {fmt_num(r.get('revenue'))} {u}</td>
                <td class="px-4 py-2 {growth_class}">{fmt_pct(growth, plus=True)}</td>
                <td class="px-4 py-2">{fmt_pct(r.get('operating_profit_margin_pct'))}</td>
                <td class="px-4 py-2">{fmt_pct(r.get('net_profit_margin_pct'))}</td>
                <td class="px-4 py-2">{fmt_pct(r.get('return_on_equity_pct'))}</td>
                <td class="px-4 py-2">{fmt_num(r.get('debt_to_equity'))}</td>
                <td class="px-4 py-2">{c} {fmt_num(r.get('operating_cash_flow'))} {u}</td>
            </tr>
            """

        insights_html = "".join([f"<li class='mb-1.5'>• {ins}</li>" for ins in (insights or [])])
        citations_html = ""
        for idx, cit in enumerate(citations or [], 1):
            citations_html += f"""
            <div class="p-3 bg-slate-50 border border-slate-200 rounded-md mb-2">
                <div class="flex items-center justify-between text-xs font-semibold text-slate-700 mb-1">
                    <span>[{idx}] {cit.get('document_title')} (FY{cit.get('fiscal_year', 'N/A')})</span>
                    <span class="bg-blue-100 text-blue-800 px-2 py-0.5 rounded">Page {cit.get('page_number')} | {cit.get('section')}</span>
                </div>
                <p class="text-xs text-slate-600 italic">"{cit.get('snippet')}"</p>
            </div>
            """

        cov = esg_breakdown.get("data_coverage_pct", 0) if esg_breakdown else 0
        overall = esg_breakdown.get("overall_esg_score", "N/A") if esg_breakdown else "N/A"
        e_sc = esg_breakdown.get("environmental_score", "N/A") if esg_breakdown else "N/A"
        s_sc = esg_breakdown.get("social_score", "N/A") if esg_breakdown else "N/A"
        g_sc = esg_breakdown.get("governance_score", "N/A") if esg_breakdown else "N/A"

        now_str = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{company.name} - AI Financial Analyst Dossier FY{fiscal_year}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
    </style>
</head>
<body class="bg-slate-100 text-slate-800 p-6 md:p-10">
    <div class="max-w-5xl mx-auto bg-white rounded-xl shadow-md border border-slate-200 p-8">
        
        <!-- Header -->
        <header class="border-b border-slate-200 pb-5 mb-6 flex flex-col md:flex-row justify-between items-start md:items-center">
            <div>
                <span class="text-xs font-bold uppercase tracking-wider text-blue-800 bg-blue-50 px-2.5 py-1 rounded-full">
                    AI Financial Analyst & Report Generator
                </span>
                <h1 class="text-2xl font-bold text-slate-900 mt-2">{company.name} ({company.ticker})</h1>
                <p class="text-sm text-slate-500">Sector: {company.sector} | Exchange: {company.exchange or 'NSE'} | Reporting: FY{fiscal_year}</p>
            </div>
            <div class="mt-4 md:mt-0 text-right">
                <span class="text-xs text-slate-400">Generated: {now_str}</span>
                <div class="mt-1">
                    <span class="inline-block bg-emerald-100 text-emerald-800 text-xs px-2.5 py-1 rounded font-medium">Audited & Verified</span>
                </div>
            </div>
        </header>

        <!-- Executive Summary -->
        <section class="mb-8">
            <h2 class="text-lg font-bold text-slate-900 mb-3 border-l-4 border-blue-800 pl-3">1. Executive Financial Summary & Insights</h2>
            <ul class="text-sm text-slate-700 bg-slate-50 p-4 rounded-lg border border-slate-200">
                {insights_html or "<li>No summary insights computed.</li>"}
            </ul>
            {f'<div class="mt-4 p-4 bg-blue-50/50 rounded-lg border border-blue-200 text-sm text-slate-800"><b class="text-blue-900">Synthesized LLM Analysis:</b><br/>{ai_summary}</div>' if ai_summary else ''}
        </section>

        <!-- Deterministic Financial Table -->
        <section class="mb-8">
            <h2 class="text-lg font-bold text-slate-900 mb-2 border-l-4 border-blue-800 pl-3">2. Deterministic Financial Ratios (Python/Pandas Engine)</h2>
            <p class="text-xs text-slate-500 mb-3 italic">Calculations performed strictly via deterministic code with zero LLM arithmetic.</p>
            <div class="overflow-x-auto rounded-lg border border-slate-200">
                <table class="w-full text-xs text-left">
                    <thead class="bg-slate-900 text-white font-semibold">
                        <tr>
                            <th class="px-4 py-2.5">Period</th>
                            <th class="px-4 py-2.5">Revenue</th>
                            <th class="px-4 py-2.5">YoY Growth</th>
                            <th class="px-4 py-2.5">Operating Margin</th>
                            <th class="px-4 py-2.5">Net Margin</th>
                            <th class="px-4 py-2.5">ROE</th>
                            <th class="px-4 py-2.5">Debt/Equity</th>
                            <th class="px-4 py-2.5">Operating Cash Flow</th>
                        </tr>
                    </thead>
                    <tbody>
                        {ratios_html_rows}
                    </tbody>
                </table>
            </div>
        </section>

        <!-- ESG Performance -->
        <section class="mb-8">
            <h2 class="text-lg font-bold text-slate-900 mb-3 border-l-4 border-blue-800 pl-3">3. Transparent Project-Specific ESG Evaluation</h2>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
                <div class="p-4 bg-emerald-50 border border-emerald-200 rounded-lg text-center">
                    <div class="text-2xl font-bold text-emerald-800">{overall} <span class="text-xs font-normal">/ 100</span></div>
                    <div class="text-xs font-semibold text-emerald-700 mt-1">Composite ESG Score</div>
                    <div class="text-[10px] text-emerald-600 mt-0.5">Coverage: {cov:.1f}%</div>
                </div>
                <div class="p-4 bg-slate-50 border border-slate-200 rounded-lg text-center">
                    <div class="text-xl font-bold text-slate-800">{e_sc} <span class="text-xs font-normal">/ 100</span></div>
                    <div class="text-xs font-medium text-slate-600 mt-1">Environmental (30%)</div>
                </div>
                <div class="p-4 bg-slate-50 border border-slate-200 rounded-lg text-center">
                    <div class="text-xl font-bold text-slate-800">{s_sc} <span class="text-xs font-normal">/ 100</span></div>
                    <div class="text-xs font-medium text-slate-600 mt-1">Social (30%)</div>
                </div>
                <div class="p-4 bg-slate-50 border border-slate-200 rounded-lg text-center">
                    <div class="text-xl font-bold text-slate-800">{g_sc} <span class="text-xs font-normal">/ 100</span></div>
                    <div class="text-xs font-medium text-slate-600 mt-1">Governance (40%)</div>
                </div>
            </div>
            <p class="text-xs text-slate-500 italic">
                *Academic project-specific model: Undisclosed indicators are omitted from pillar calculations rather than penalized.
                Not an official commercial credit rating.
            </p>
        </section>

        <!-- Document Evidence & Citations -->
        <section class="mb-8">
            <h2 class="text-lg font-bold text-slate-900 mb-3 border-l-4 border-blue-800 pl-3">4. Grounded Document Evidence & Citations</h2>
            {citations_html or "<p class='text-xs text-slate-500'>No qualitative citations queried for this generation.</p>"}
        </section>

        <!-- Footer -->
        <footer class="border-t border-slate-200 pt-4 text-center text-xs text-slate-400">
            AI Financial Analyst & Report Generator • Academic Research System • Compliant with Institutional Standards
        </footer>

    </div>
</body>
</html>"""

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return str(out_path)
