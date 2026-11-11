"""Answer accuracy evaluator for ReSearch_Mate."""
import re
from typing import List, Dict, Any, Optional


class AnswerEvaluator:
    MIN_DETAIL_WORDS = 50  # answers shorter than this get low detail score

    def evaluate(
        self,
        question: str,
        expected_keywords: List[str],
        actual_answer: str,
        citations: List[str],
        max_valid_page: int = 500
    ) -> Dict[str, Any]:
        keyword_coverage = self._keyword_coverage(expected_keywords, actual_answer)
        citation_precision = self._citation_precision(citations, actual_answer)
        detail_score = self._detail_score(actual_answer, question)
        hallucination_flag = self._check_hallucination(citations, max_valid_page)

        # Weighted accuracy: keyword_coverage (40%) + citation_precision (40%) + detail_score (20%)
        # But if hallucination_flag is True, cap at 0.4
        accuracy_score = (keyword_coverage * 0.4 + citation_precision * 0.4 + detail_score * 0.2)
        if hallucination_flag:
            accuracy_score = min(accuracy_score, 0.4)

        return {
            "accuracy_score": round(accuracy_score, 3),
            "keyword_coverage": round(keyword_coverage, 3),
            "citation_precision": round(citation_precision, 3),
            "detail_score": round(detail_score, 3),
            "hallucination_flag": hallucination_flag
        }

    def _keyword_coverage(self, expected: List[str], answer: str) -> float:
        if not expected:
            return 1.0
        answer_lower = answer.lower()
        found = sum(1 for kw in expected if kw.lower() in answer_lower)
        return found / len(expected)

    def _citation_precision(self, citations: List[str], answer: str) -> float:
        if not citations:
            return 0.0
        # Check if any citation-like pattern exists in the answer
        pattern = r'\[.+?,\s*p\.?\s*\d+\]'
        matches = re.findall(pattern, answer)
        return 1.0 if matches else 0.0

    def _detail_score(self, answer: str, question: str) -> float:
        words = answer.split()
        word_count = len(words)
        # Score: 0 for <10 words, scales to 1.0 at MIN_DETAIL_WORDS
        score = min(word_count / self.MIN_DETAIL_WORDS, 1.0)
        return score

    def _check_hallucination(self, citations: List[str], max_valid_page: int) -> bool:
        for cit in citations:
            match = re.search(r'p\.?\s*(\d+)', cit)
            if match:
                page_num = int(match.group(1))
                if page_num > max_valid_page:
                    return True
        return False
