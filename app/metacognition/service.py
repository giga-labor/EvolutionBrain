class MetacognitionService:
    def evaluate_output(self, output: dict) -> dict:
        used_sources = output.get("used_sources", [])
        answer = output.get("answer", "") or ""
        confidence = float(output.get("confidence", 0.0))

        warnings: list[str] = []
        quality_score = 1.0

        # 1. Context sufficiency
        if len(used_sources) == 0:
            context_sufficiency = "none"
            quality_score -= 0.4
            warnings.append("no_sources_found")
        elif len(used_sources) < 2:
            context_sufficiency = "insufficient"
            quality_score -= 0.2
            warnings.append("low_source_count")
        else:
            context_sufficiency = "sufficient"

        # 2. Source type diversity
        source_types = {s.get("type") for s in used_sources if isinstance(s, dict)}
        if len(source_types) >= 2:
            quality_score += 0.10

        # 3. Overconfidence risk
        if confidence > 0.8 and len(used_sources) < 2:
            overconfidence_risk = "high"
            warnings.append("overconfidence_low_evidence")
            quality_score -= 0.25
        elif confidence > 0.6 and len(used_sources) == 0:
            overconfidence_risk = "medium"
            warnings.append("moderate_confidence_no_sources")
            quality_score -= 0.15
        else:
            overconfidence_risk = "low"

        # 4. Verbose answer with few sources
        if len(answer) > 500 and len(used_sources) < 2:
            warnings.append("verbose_answer_low_evidence")
            quality_score -= 0.10

        quality_score = round(max(0.0, min(1.0, quality_score)), 4)

        return {
            "quality_score": quality_score,
            "context_sufficiency": context_sufficiency,
            "overconfidence_risk": overconfidence_risk,
            "warnings": warnings,
            "source_count": len(used_sources),
            "source_diversity": len(source_types),
        }
