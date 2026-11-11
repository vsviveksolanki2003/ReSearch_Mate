"""Dataset preparation for academic instruction fine-tuning."""
import json
from typing import Dict, Any, List

class AcademicDatasetPreparer:
    SYSTEM_PROMPT = (
        "You are ReSearch_Mate, an offline academic AI assistant. "
        "Answer questions rigorously using ONLY the provided research passages. "
        "Every single claim must cite the paper title and page number in brackets."
    )

    def format_chat_sample(self, sample: Dict[str, Any]) -> str:
        """
        Format a training sample into Llama 3.1 instruct prompt format.
        Sample keys:
          - paper_title, section, page, text
          - question, grounded_answer
        """
        context = f"Paper: {sample['paper_title']} (Page {sample['page']}, Section: {sample['section']})\nPassage: {sample['text']}"
        user_message = f"Context:\n{context}\n\nQuestion:\n{sample['question']}"

        template = (
            "<|start_header_id|>system<|end_header_id|>\n\n"
            f"{self.SYSTEM_PROMPT}<|eot_id|>"
            "<|start_header_id|>user<|end_header_id|>\n\n"
            f"{user_message}<|eot_id|>"
            "<|start_header_id|>assistant<|end_header_id|>\n\n"
            f"{sample['grounded_answer']}<|eot_id|>"
        )
        return template

    def build_dataset_from_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Transform document chunks into training instruction pairs."""
        dataset = []
        for c in chunks:
            sample = {
                "paper_title": c.get("paper_title", "Research Paper"),
                "section": c.get("section_title", "Methodology"),
                "page": c.get("page_number", 1),
                "text": c.get("content", ""),
                "question": f"Summarize the findings and methodology reported in section {c.get('section_title', 'Methodology')}.",
                "grounded_answer": f"According to the source text: {c.get('content', '')} [{c.get('paper_title', 'Research Paper')}, p. {c.get('page_number', 1)}]."
            }
            formatted_text = self.format_chat_sample(sample)
            dataset.append({"text": formatted_text})
        return dataset
