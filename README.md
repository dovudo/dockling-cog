# Dockling Replica

Docling model for the Replicate platform, based on [docling-serve](https://github.com/docling-ai/docling-serve).

## Description

This project provides an API for converting documents of various formats (PDF, DOCX, PPTX, XLSX, HTML, Markdown, etc.) into structured formats (JSON, Markdown, CSV) with OCR support and table extraction.

## Features

- 📄 **Multiple formats**: PDF, DOCX, PPTX, XLSX, HTML, Markdown, CSV, AsciiDoc
- 🔍 **OCR support**: EasyOCR, Tesseract, RapidOCR, OCRMac
- 📊 **Table extraction**: Fast and accurate modes
- 🖼️ **Image processing**: Embedded, referenced, or placeholder modes
- 🌐 **REST API**: Full API for integration
- 📁 **File upload**: Support for direct file upload and URL

## Usage

### Via Web Interface

Visit: https://replicate.com/dovudo/dockling

**Two ways to upload files:**
1. **Direct upload** - drag and drop file into the interface
2. **File URL** - specify a link to a file on the internet

### Via Replicate API

```bash
# Upload file by URL
curl -X POST \
  -H "Authorization: Token YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "version": "a0f739f66d05c2f822a01360283619c2ea72ffffd94a322261d8554496b2f67b",
    "input": {
      "file_url": "https://example.com/document.pdf",
      "from_formats": ["pdf"],
      "to_formats": ["json"],
      "do_ocr": true,
      "ocr_engine": "easyocr"
    }
  }' \
  https://api.replicate.com/v1/predictions
```

### Via Python Client

```python
import replicate

# Upload by URL
output = replicate.run(
    "dovudo/dockling:a0f739f66d05c2f822a01360283619c2ea72ffffd94a322261d8554496b2f67b",
    input={
        "file_url": "https://example.com/document.pdf",
        "to_formats": ["json"],
        "do_ocr": True
    }
)

# Upload local file
with open("document.pdf", "rb") as f:
    output = replicate.run(
        "dovudo/dockling:a0f739f66d05c2f822a01360283619c2ea72ffffd94a322261d8554496b2f67b",
        input={
            "file": f,
            "to_formats": ["json"],
            "do_ocr": True
        }
    )
```

## Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `file` | File | File to convert (upload directly) | None |
| `file_url` | str | URL of file to convert | None |
| `from_formats` | List[str] | Input formats | - |
| `to_formats` | List[str] | Output formats | - |
| `do_ocr` | bool | Enable OCR | true |
| `force_ocr` | bool | Force OCR | false |
| `ocr_engine` | str | OCR engine | easyocr |
| `ocr_lang` | List[str] | OCR languages | - |
| `pdf_backend` | str | PDF backend | dlparse_v4 |
| `table_mode` | str | Table mode | fast |
| `image_export_mode` | str | Image export mode | embedded |
| `page_range` | List[List[int]] | Page ranges | - |
| `document_timeout` | float | Processing timeout (seconds) | - |
| `abort_on_error` | bool | Abort on error | false |

**Note:** Specify either `file` (for direct upload) or `file_url` (for URL), but not both.

## Supported Formats

### Input Formats
- PDF (pypdfium2, dlparse_v1, dlparse_v2, dlparse_v4)
- Microsoft Office (DOCX, PPTX, XLSX)
- HTML
- Markdown
- CSV
- AsciiDoc
- JATS XML
- USPTO XML

### Output Formats
- JSON
- Markdown
- CSV
- HTML
- XML

## OCR Engines

- **easyocr**: Universal OCR with support for multiple languages
- **tesseract**: Classic OCR engine
- **rapidocr**: Fast OCR
- **ocrmac**: macOS optimized OCR
- **tesserocr**: Python wrapper for Tesseract

## Architecture

The project uses [Cog](https://github.com/replicate/cog) to package the model and [docling-serve](https://github.com/docling-ai/docling-serve) as the main processing engine.

### File Structure

```
dockling-replica/
├── cog.yaml          # Cog configuration
├── predict.py        # Main model code
├── Dockerfile        # Docker image
└── README.md         # Documentation
```

## Development

### Local Development

1. Install Cog:
```bash
pip install cog
```

2. Run locally:
```bash
# With URL
cog predict -i file_url="https://example.com/document.pdf"

# With local file
cog predict -i file=@document.pdf
```

3. Build and push:
```bash
cog build
cog push r8.im/dovudo/dockling
```

### Dependencies

Main dependencies are automatically installed via `cog.yaml`:
- docling-serve
- requests
- python-multipart

## License

The project is based on [Docling](https://github.com/docling-ai/docling) and [docling-serve](https://github.com/docling-ai/docling-serve).

## Links

- [Replicate model](https://replicate.com/dovudo/dockling)
- [Docling documentation](https://docling.ai)
- [docling-serve](https://github.com/docling-ai/docling-serve)
- [Cog documentation](https://github.com/replicate/cog) 