"""Literature review synthesis and structured export to Markdown and LaTeX formats."""
import re
from typing import List, Optional
from backend.app.schemas.citation import Citation
from backend.app.schemas.analysis import ComparisonMatrix, ResearchGap

class LiteratureReviewExporter:
    @staticmethod
    def _escape_latex(text: str) -> str:
        """Escape special LaTeX characters to prevent compile errors and macro injection."""
        conv = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
            '\\': r'\textbackslash{}',
        }
        regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key=lambda item: -len(item))))
        return regex.sub(lambda match: conv[match.group()], text)

    def export_markdown(
        self,
        topic: str,
        comparison_matrix: Optional[ComparisonMatrix],
        citations: List[Citation],
        research_gaps: List[ResearchGap]
    ) -> str:
        """Generate structured academic literature review in Markdown format."""
        lines = [
            f"# Literature Review: {topic}",
            "",
            "## 1. Introduction & Research Scope",
            f"This review examines and synthesizes recent academic literature regarding **{topic}**.",
            "All claims are grounded in extracted source text passages with verified page-level citations.",
            "",
            "## 2. Comparative Matrix"
        ]

        if comparison_matrix and comparison_matrix.papers:
            headers = ["Research Aspect"] + [p.paper_title for p in comparison_matrix.papers]
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

            for aspect in comparison_matrix.aspects:
                row = [aspect]
                for p in comparison_matrix.papers:
                    val = getattr(p, aspect.lower().replace(" ", "_"), "Extracted from source")
                    row.append(str(val))
                lines.append("| " + " | ".join(row) + " |")
            lines.append("")
        else:
            lines.append("*No comparative papers were selected for matrix view.*")
            lines.append("")

        lines.extend([
            "## 3. Critical Research Gaps",
            "Based on the cross-paper evaluation, the following unresolved limitations were identified:"
        ])
        for idx, gap in enumerate(research_gaps, start=1):
            lines.append(f"### 3.{idx}. {gap.area}")
            lines.append(f"- **Limitation:** {gap.description}")
            lines.append(f"- **Proposed Future Direction:** {gap.potential_direction}")
            lines.append("")

        lines.extend([
            "## 4. Grounded References & Citations",
            ""
        ])
        for idx, c in enumerate(citations, start=1):
            lines.append(f"{idx}. **[{c.paper_title}, p. {c.page_number}]** &mdash; *\"{c.quote}\"*")

        return "\n".join(lines)

    def export_latex(
        self,
        topic: str,
        comparison_matrix: Optional[ComparisonMatrix],
        citations: List[Citation],
        research_gaps: List[ResearchGap]
    ) -> str:
        """Generate structured LaTeX document conforming to academic article templates."""
        esc_topic = self._escape_latex(topic)
        lines = [
            r"\documentclass{article}",
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage{booktabs}",
            r"\usepackage{hyperref}",
            rf"\title{{Literature Review: {esc_topic}}}",
            r"\author{ReSearch\_Mate Automated Academic Reviewer}",
            r"\date{\today}",
            r"\begin{document}",
            r"\maketitle",
            r"\section{Introduction}",
            rf"This document synthesizes findings across reviewed literature concerning {esc_topic}.",
            r"\section{Comparative Analysis}"
        ]

        if comparison_matrix and comparison_matrix.papers:
            num_cols = len(comparison_matrix.papers) + 1
            col_spec = "l" + "p{3.5cm}" * len(comparison_matrix.papers)
            lines.append(rf"\begin{{tabular}}{{{col_spec}}}")
            lines.append(r"\toprule")
            headers = [r"\textbf{Aspect}"] + [rf"\textbf{{{self._escape_latex(p.paper_title)}}}" for p in comparison_matrix.papers]
            lines.append(" & ".join(headers) + r" \\")
            lines.append(r"\midrule")

            for aspect in comparison_matrix.aspects:
                row = [self._escape_latex(aspect)]
                for p in comparison_matrix.papers:
                    val = getattr(p, aspect.lower().replace(" ", "_"), "Extracted from source")
                    row.append(self._escape_latex(str(val)))
                lines.append(" & ".join(row) + r" \\")

            lines.append(r"\bottomrule")
            lines.append(r"\end{tabular}")
        else:
            lines.append(r"No comparison papers were specified.")

        lines.extend([
            r"\section{Identified Research Gaps}"
        ])
        for idx, gap in enumerate(research_gaps, start=1):
            lines.append(rf"\subsection{{{self._escape_latex(gap.area)}}}")
            lines.append(rf"\textbf{{Limitation:}} {self._escape_latex(gap.description)}\\")
            lines.append(rf"\textbf{{Suggested Direction:}} {self._escape_latex(gap.potential_direction)}")

        lines.extend([
            r"\section{Grounded Citations}",
            r"\begin{enumerate}"
        ])
        for c in citations:
            esc_title = self._escape_latex(c.paper_title)
            esc_quote = self._escape_latex(c.quote)
            lines.append(rf"\item \textbf{{{esc_title}, p.~{c.page_number}}}: ``{esc_quote}''")

        lines.extend([
            r"\end{enumerate}",
            r"\end{document}"
        ])
        return "\n".join(lines)
