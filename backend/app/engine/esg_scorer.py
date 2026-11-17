from typing import Dict, Any, Optional, Tuple
from backend.app.models.schema_models import ESGData

class TransparentESGScorer:
    """
    Project-Specific ESG Scoring Engine.
    
    DISCLAIMER:
    This is an academic, project-specific ESG estimation methodology.
    It is NOT an official MSCI, Sustainalytics, S&P Global, or CRISIL rating.
    
    Principles:
    1. Undisclosed indicators are explicitly reported as 'MISSING' and not treated as zero/penalty.
    2. Sub-scores are computed by averaging disclosed normalized indicator values within each pillar.
    3. Requires at least 30% data coverage to compute composite score.
    4. Weights: Environmental 30%, Social 30%, Governance 40%.
    """

    WEIGHT_E = 0.30
    WEIGHT_S = 0.30
    WEIGHT_G = 0.40
    MIN_COVERAGE_THRESHOLD = 30.0  # percentage

    @classmethod
    def evaluate_esg(cls, esg: ESGData) -> Dict[str, Any]:
        """
        Evaluate ESG record and return score breakdown, coverage, and formula explanation.
        """
        # ==================== Environmental Pillar ====================
        e_indicators = {}
        
        # Renewable energy % (0 - 100)
        if esg.renewable_energy_pct is not None:
            score = min(max(esg.renewable_energy_pct, 0.0), 100.0)
            e_indicators["renewable_energy"] = {
                "label": "Renewable Energy Share",
                "raw_value": f"{esg.renewable_energy_pct:.1f}%",
                "normalized_score": round(score, 1),
                "weight_in_pillar": 0.25,
                "status": "DISCLOSED"
            }
        else:
            e_indicators["renewable_energy"] = {"label": "Renewable Energy Share", "raw_value": None, "status": "UNDISCLOSED"}

        # Water recycled %
        if esg.water_recycled_pct is not None:
            score = min(max(esg.water_recycled_pct, 0.0), 100.0)
            e_indicators["water_recycled"] = {
                "label": "Water Recycled / Reused",
                "raw_value": f"{esg.water_recycled_pct:.1f}%",
                "normalized_score": round(score, 1),
                "weight_in_pillar": 0.25,
                "status": "DISCLOSED"
            }
        else:
            e_indicators["water_recycled"] = {"label": "Water Recycled / Reused", "raw_value": None, "status": "UNDISCLOSED"}

        # Waste recycled %
        if esg.waste_recycled_pct is not None:
            score = min(max(esg.waste_recycled_pct, 0.0), 100.0)
            e_indicators["waste_recycled"] = {
                "label": "Waste Diverted / Recycled",
                "raw_value": f"{esg.waste_recycled_pct:.1f}%",
                "normalized_score": round(score, 1),
                "weight_in_pillar": 0.25,
                "status": "DISCLOSED"
            }
        else:
            e_indicators["waste_recycled"] = {"label": "Waste Diverted / Recycled", "raw_value": None, "status": "UNDISCLOSED"}

        # GHG Emissions Disclosed (Scope 1 & 2)
        if esg.carbon_emissions_scope1 is not None or esg.carbon_emissions_scope2 is not None:
            # Disclosure and tracking of emissions provides transparent accountability
            score = 80.0
            if esg.carbon_emissions_scope1 is not None and esg.carbon_emissions_scope2 is not None:
                score = 90.0
            if esg.carbon_emissions_scope3 is not None:
                score = 100.0
            e_indicators["ghg_emissions"] = {
                "label": "GHG Scope 1 & 2 Emissions Tracking",
                "raw_value": f"Scope1: {esg.carbon_emissions_scope1 or 0:,.0f} MT, Scope2: {esg.carbon_emissions_scope2 or 0:,.0f} MT",
                "normalized_score": score,
                "weight_in_pillar": 0.25,
                "status": "DISCLOSED"
            }
        else:
            e_indicators["ghg_emissions"] = {"label": "GHG Scope 1 & 2 Emissions Tracking", "raw_value": None, "status": "UNDISCLOSED"}

        # ==================== Social Pillar ====================
        s_indicators = {}

        # Female workforce % (benchmark 10% - 50%)
        if esg.female_workforce_pct is not None:
            score = min((esg.female_workforce_pct / 45.0) * 100.0, 100.0)
            s_indicators["workforce_diversity"] = {
                "label": "Gender Diversity (% Female)",
                "raw_value": f"{esg.female_workforce_pct:.1f}%",
                "normalized_score": round(score, 1),
                "status": "DISCLOSED"
            }
        else:
            s_indicators["workforce_diversity"] = {"label": "Gender Diversity (% Female)", "raw_value": None, "status": "UNDISCLOSED"}

        # Training hours per employee (benchmark: 40 hrs = 100)
        if esg.training_hours_per_employee is not None:
            score = min((esg.training_hours_per_employee / 40.0) * 100.0, 100.0)
            s_indicators["employee_training"] = {
                "label": "Avg Training Hours / Employee",
                "raw_value": f"{esg.training_hours_per_employee:.1f} hrs",
                "normalized_score": round(score, 1),
                "status": "DISCLOSED"
            }
        else:
            s_indicators["employee_training"] = {"label": "Avg Training Hours / Employee", "raw_value": None, "status": "UNDISCLOSED"}

        # Safety / Lost time injury rate (0 -> 100, > 2 -> degrades)
        if esg.lost_time_injury_rate is not None:
            score = max(100.0 - (esg.lost_time_injury_rate * 25.0), 0.0)
            s_indicators["health_safety"] = {
                "label": "Lost Time Injury Rate (LTIR)",
                "raw_value": f"{esg.lost_time_injury_rate:.2f}",
                "normalized_score": round(score, 1),
                "status": "DISCLOSED"
            }
        else:
            s_indicators["health_safety"] = {"label": "Lost Time Injury Rate (LTIR)", "raw_value": None, "status": "UNDISCLOSED"}

        # Human Rights Policy
        if esg.human_rights_policy is not None:
            score = 100.0 if esg.human_rights_policy else 0.0
            s_indicators["human_rights"] = {
                "label": "Formal Human Rights Policy",
                "raw_value": "Adopted" if esg.human_rights_policy else "Not Adopted",
                "normalized_score": score,
                "status": "DISCLOSED"
            }
        else:
            s_indicators["human_rights"] = {"label": "Formal Human Rights Policy", "raw_value": None, "status": "UNDISCLOSED"}

        # CSR Spending
        if esg.csr_spending_amount is not None:
            score = 90.0 if esg.csr_spending_amount > 0 else 20.0
            s_indicators["csr_investment"] = {
                "label": "CSR Expenditure Program",
                "raw_value": f"{esg.csr_spending_amount:,.2f}",
                "normalized_score": score,
                "status": "DISCLOSED"
            }
        else:
            s_indicators["csr_investment"] = {"label": "CSR Expenditure Program", "raw_value": None, "status": "UNDISCLOSED"}

        # ==================== Governance Pillar ====================
        g_indicators = {}

        # Board Independence (benchmark: 50% independent)
        if esg.independent_directors_pct is not None:
            score = min((esg.independent_directors_pct / 50.0) * 100.0, 100.0)
            g_indicators["board_independence"] = {
                "label": "Independent Directors Share",
                "raw_value": f"{esg.independent_directors_pct:.1f}%",
                "normalized_score": round(score, 1),
                "status": "DISCLOSED"
            }
        else:
            g_indicators["board_independence"] = {"label": "Independent Directors Share", "raw_value": None, "status": "UNDISCLOSED"}

        # Women on Board (benchmark: 30%)
        if esg.women_on_board_pct is not None:
            score = min((esg.women_on_board_pct / 30.0) * 100.0, 100.0)
            g_indicators["women_on_board"] = {
                "label": "Women Directors on Board",
                "raw_value": f"{esg.women_on_board_pct:.1f}%",
                "normalized_score": round(score, 1),
                "status": "DISCLOSED"
            }
        else:
            g_indicators["women_on_board"] = {"label": "Women Directors on Board", "raw_value": None, "status": "UNDISCLOSED"}

        # CEO / Chair Separation
        if esg.ceo_chair_separation is not None:
            score = 100.0 if esg.ceo_chair_separation else 50.0
            g_indicators["ceo_chair_separation"] = {
                "label": "CEO & Board Chair Separation",
                "raw_value": "Separated" if esg.ceo_chair_separation else "Combined",
                "normalized_score": score,
                "status": "DISCLOSED"
            }
        else:
            g_indicators["ceo_chair_separation"] = {"label": "CEO & Board Chair Separation", "raw_value": None, "status": "UNDISCLOSED"}

        # Code of Conduct / Ethics
        if esg.ethics_code_established is not None:
            score = 100.0 if esg.ethics_code_established else 0.0
            g_indicators["ethics_code"] = {
                "label": "Code of Business Ethics",
                "raw_value": "Established" if esg.ethics_code_established else "None",
                "normalized_score": score,
                "status": "DISCLOSED"
            }
        else:
            g_indicators["ethics_code"] = {"label": "Code of Business Ethics", "raw_value": None, "status": "UNDISCLOSED"}

        # Whistleblower Mechanism
        if esg.whistleblower_mechanism is not None:
            score = 100.0 if esg.whistleblower_mechanism else 0.0
            g_indicators["whistleblower"] = {
                "label": "Vigil Mechanism / Whistleblower",
                "raw_value": "Operational" if esg.whistleblower_mechanism else "None",
                "normalized_score": score,
                "status": "DISCLOSED"
            }
        else:
            g_indicators["whistleblower"] = {"label": "Vigil Mechanism / Whistleblower", "raw_value": None, "status": "UNDISCLOSED"}

        # Anti-Corruption Policy
        if esg.anti_corruption_policy is not None:
            score = 100.0 if esg.anti_corruption_policy else 0.0
            g_indicators["anti_corruption"] = {
                "label": "Anti-Bribery & Corruption Policy",
                "raw_value": "Active" if esg.anti_corruption_policy else "None",
                "normalized_score": score,
                "status": "DISCLOSED"
            }
        else:
            g_indicators["anti_corruption"] = {"label": "Anti-Bribery & Corruption Policy", "raw_value": None, "status": "UNDISCLOSED"}

        # Data Privacy Policy
        if esg.data_privacy_policy is not None:
            score = 100.0 if esg.data_privacy_policy else 0.0
            g_indicators["data_privacy"] = {
                "label": "Data Privacy & Cybersecurity Policy",
                "raw_value": "Active" if esg.data_privacy_policy else "None",
                "normalized_score": score,
                "status": "DISCLOSED"
            }
        else:
            g_indicators["data_privacy"] = {"label": "Data Privacy & Cybersecurity Policy", "raw_value": None, "status": "UNDISCLOSED"}

        # ==================== Coverage Calculation ====================
        all_indicators = {**e_indicators, **s_indicators, **g_indicators}
        total_indicators_count = len(all_indicators)
        disclosed_count = sum(1 for ind in all_indicators.values() if ind.get("status") == "DISCLOSED")
        coverage_pct = round((disclosed_count / total_indicators_count) * 100.0, 1)

        # Helper to compute pillar score from disclosed items
        def get_pillar_score(pillar_dict: Dict[str, Any]) -> Optional[float]:
            disclosed = [v["normalized_score"] for v in pillar_dict.values() if v.get("status") == "DISCLOSED"]
            if not disclosed:
                return None
            return round(sum(disclosed) / len(disclosed), 1)

        e_score = get_pillar_score(e_indicators)
        s_score = get_pillar_score(s_indicators)
        g_score = get_pillar_score(g_indicators)

        # Check sufficiency: minimum 30% coverage required
        is_sufficient = coverage_pct >= cls.MIN_COVERAGE_THRESHOLD
        overall_score = None

        if is_sufficient:
            # Weighted average of available pillars normalized by their active weights
            active_weights = 0.0
            weighted_sum = 0.0
            if e_score is not None:
                weighted_sum += e_score * cls.WEIGHT_E
                active_weights += cls.WEIGHT_E
            if s_score is not None:
                weighted_sum += s_score * cls.WEIGHT_S
                active_weights += cls.WEIGHT_S
            if g_score is not None:
                weighted_sum += g_score * cls.WEIGHT_G
                active_weights += cls.WEIGHT_G
                
            if active_weights > 0:
                overall_score = round(weighted_sum / active_weights, 1)

        formula_explanation = (
            f"Overall ESG Score = ({cls.WEIGHT_E*100:.0f}% × Environmental) + "
            f"({cls.WEIGHT_S*100:.0f}% × Social) + ({cls.WEIGHT_G*100:.0f}% × Governance). "
            f"Sub-pillar scores are computed strictly from disclosed indicators without penalizing unrecorded metrics."
        )

        limitations = [
            "Academic / Project-Specific Rating: This score represents an internal model and is NOT an official MSCI, Sustainalytics, or regulatory ESG rating.",
            f"Data Coverage: {coverage_pct}% of core indicators disclosed ({disclosed_count}/{total_indicators_count}).",
            "Non-disclosure is not treated as negative performance; unrecorded indicators are omitted from pillar averages.",
            "Requires verifiable sustainability reports (BRSR/GRI/TCFD) for institutional audit grade verification."
        ]

        if not is_sufficient:
            limitations.append(
                f"Insufficient data coverage ({coverage_pct}% < {cls.MIN_COVERAGE_THRESHOLD}%). "
                "Overall score withheld to prevent misleading evaluations."
            )

        return {
            "environmental_score": e_score,
            "social_score": s_score,
            "governance_score": g_score,
            "overall_esg_score": overall_score,
            "data_coverage_pct": coverage_pct,
            "is_sufficient_data": is_sufficient,
            "weights": {
                "environmental": cls.WEIGHT_E,
                "social": cls.WEIGHT_S,
                "governance": cls.WEIGHT_G
            },
            "indicator_scores": {
                "environmental": e_indicators,
                "social": s_indicators,
                "governance": g_indicators
            },
            "formula_explanation": formula_explanation,
            "methodology_limitations": limitations
        }
