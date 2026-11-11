"""Automated benchmark for evaluating hallucination rate and citation grounding precision."""
from typing import List, Dict, Any

from backend.app.agents.answer_evaluator import AnswerEvaluator


class HallucinationBenchmark:
    def evaluate_run(self, evaluated_claims: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate precision, recall, and hallucination rate across claims.
        Each item in evaluated_claims contains:
          - claim: str
          - verified: bool
        """
        if not evaluated_claims:
            return {
                "total_claims": 0,
                "verified_count": 0,
                "hallucination_rate": 0.0,
                "grounding_precision": 1.0
            }

        total = len(evaluated_claims)
        verified = sum(1 for c in evaluated_claims if c.get("verified", False))
        unverified = total - verified

        return {
            "total_claims": total,
            "verified_count": verified,
            "hallucination_count": unverified,
            "hallucination_rate": unverified / total,
            "grounding_precision": verified / total
        }

    def evaluate_answer(
        self,
        question: str,
        expected_keywords: List[str],
        actual_answer: str,
        citations: List[str],
        max_valid_page: int = 500
    ) -> Dict[str, Any]:
        """Delegate answer accuracy evaluation to AnswerEvaluator."""
        evaluator = AnswerEvaluator()
        return evaluator.evaluate(
            question=question,
            expected_keywords=expected_keywords,
            actual_answer=actual_answer,
            citations=citations,
            max_valid_page=max_valid_page
        )
