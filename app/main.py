import argparse
import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from nlp_module import FinancialEntityExtractor
from ocr_module import OCRProcessor
from utils import clean_text, save_json, setup_logging


def process_document(file_path: str, ocr: OCRProcessor, nlp: FinancialEntityExtractor) -> Dict[str, Any]:
    logger = logging.getLogger("pipeline")
    logger.info("Processing document: %s", file_path)

    ocr_output = ocr.extract_text(file_path)
    raw_text = ocr_output["raw_text"]
    cleaned_text = clean_text(raw_text)
    entities = nlp.extract_entities(cleaned_text)

    result = {
        "file_path": str(Path(file_path).resolve()),
        "file_type": ocr_output["file_type"],
        "raw_text": raw_text,
        "clean_text": cleaned_text,
        "entities": entities,
    }
    return result


def process_batch(batch_dir: str, ocr: OCRProcessor, nlp: FinancialEntityExtractor) -> List[Dict[str, Any]]:
    logger = logging.getLogger("pipeline")
    root = Path(batch_dir)
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Invalid batch directory: {batch_dir}")

    supported = {".pdf", ".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
    files = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in supported]

    logger.info("Found %s supported document(s) in %s", len(files), batch_dir)

    results: List[Dict[str, Any]] = []
    for path in files:
        try:
            results.append(process_document(str(path), ocr, nlp))
        except Exception as exc:
            logger.exception("Failed to process file: %s", path)
            results.append(
                {
                    "file_path": str(path.resolve()),
                    "error": str(exc),
                }
            )

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="FinTech Intelligent Document Parser")
    parser.add_argument("--input", type=str, help="Input document path (PDF/JPG/PNG)")
    parser.add_argument("--batch-dir", type=str, help="Batch directory containing documents")
    parser.add_argument("--output", type=str, help="Optional output JSON file path")
    parser.add_argument("--log-level", type=str, default="INFO", help="Logging level")
    parser.add_argument(
        "--tesseract-cmd",
        type=str,
        default=None,
        help="Optional absolute path to tesseract executable",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    setup_logging(args.log_level)
    logger = logging.getLogger("main")

    if not args.input and not args.batch_dir:
        raise ValueError("Provide either --input or --batch-dir")

    ocr = OCRProcessor(tesseract_cmd=args.tesseract_cmd)
    nlp = FinancialEntityExtractor()

    try:
        if args.batch_dir:
            result: Any = process_batch(args.batch_dir, ocr, nlp)
        else:
            result = process_document(args.input, ocr, nlp)

        output_text = json.dumps(result, indent=2, ensure_ascii=False)
        print(output_text)

        if args.output:
            save_json(result, args.output)
            logger.info("Saved structured output to %s", args.output)

    except Exception as exc:
        logger.exception("Pipeline failed")
        raise SystemExit(f"Error: {exc}") from exc


if __name__ == "__main__":
    main()