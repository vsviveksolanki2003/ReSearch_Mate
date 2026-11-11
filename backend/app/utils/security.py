"""Security utilities for input validation, file signatures, and path sanitization."""
import re
from pathlib import Path

MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB

def validate_pdf_content(file_bytes: bytes) -> bool:
    """Validate that file begins with standard PDF magic bytes '%PDF-'."""
    if len(file_bytes) < 5:
        return False
    # PDF magic signature is %PDF- (hex: 25 50 44 46 2D)
    return file_bytes.startswith(b"%PDF-")

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal and script injections."""
    # Extract only the base name (prevents ../ and / traversal)
    base_name = Path(filename).name
    # Strip dangerous characters
    cleaned = re.sub(r"[^\w\.\-\_]", "", base_name)
    # Ensure it ends with .pdf
    if not cleaned.lower().endswith(".pdf"):
        cleaned = f"{cleaned}.pdf"
    return cleaned

def check_file_size(file_bytes: bytes, max_bytes: int = MAX_FILE_SIZE_BYTES) -> bool:
    """Verify that file size does not exceed threshold."""
    return len(file_bytes) <= max_bytes
