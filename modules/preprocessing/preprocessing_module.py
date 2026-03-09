import json
import logging
import re
from pathlib import Path
from typing import Any


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def clean_text(text: str) -> str:
    # Repair frequent OCR mistakes for financial docs.
    corrections = {
        "lNVOICE": "INVOICE",
        "lnvoice": "Invoice",
        "T0TAL": "TOTAL",
        "IF5C": "IFSC",
        "G5T": "GST",
    }

    for bad, good in corrections.items():
        text = text.replace(bad, good)

    text = text.replace("\x0c", " ")
    text = re.sub(r"[^\S\r\n]+", " ", text)
    text = re.sub(r"[\t\f\v]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Join line breaks that split words or identifiers.
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)
    text = re.sub(r"(?<=\w)\n(?=\w)", " ", text)

    # Keep only generally safe financial-document punctuation.
    text = re.sub(r"[^\w\s\.,:/\-()\u20B9$\u20AC\u00A3]", " ", text)
    text = re.sub(r"\s{2,}", " ", text)

    return text.strip()


def save_json(data: Any, output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
