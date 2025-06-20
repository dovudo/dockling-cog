from cog import BasePredictor, Input, File, Path
import requests
import os
import time
import subprocess
import tempfile
import shutil
from typing import List, Optional, Tuple, Union

class Predictor(BasePredictor):
    def setup(self):
        # Environment for the service (can be extended as needed)
        env = {
            **os.environ,
            "DOCLING_SERVE_PORT": "5001",
            "DOCLING_SERVE_MAX_SYNC_WAIT": "600",
            "DOCLING_SERVE_ENG_KIND": "local",
            "DOCLING_SERVE_ENG_LOC_NUM_WORKERS": "2",
            "CUDA_VISIBLE_DEVICES": "0",
        }
        self.proc = subprocess.Popen(
            ["docling-serve", "run"],
            env=env,
        )
        # Wait for the service to start
        for _ in range(30):
            try:
                requests.get("http://localhost:5001/docs")
                break
            except Exception:
                time.sleep(1)

    def predict(
        self,
        file: Optional[File] = Input(description="File to convert (upload file directly)", default=None),
        file_url: Optional[str] = Input(description="URL of file to convert (alternative to file upload)", default=None),
        from_formats: Optional[List[str]] = Input(description="Input format(s) to convert from", default=None),
        to_formats: Optional[List[str]] = Input(description="Output format(s) to convert to", default=None),
        image_export_mode: str = Input(description="Image export mode", default="embedded", choices=["placeholder", "embedded", "referenced"]),
        do_ocr: bool = Input(description="Enable OCR", default=True),
        force_ocr: bool = Input(description="Force OCR", default=False),
        ocr_engine: str = Input(description="OCR engine", default="easyocr", choices=["easyocr", "ocrmac", "rapidocr", "tesserocr", "tesseract"]),
        ocr_lang: Optional[List[str]] = Input(description="OCR languages", default=None),
        pdf_backend: str = Input(description="PDF backend", default="dlparse_v4", choices=["pypdfium2", "dlparse_v1", "dlparse_v2", "dlparse_v4"]),
        table_mode: str = Input(description="Table mode", default="fast", choices=["fast", "accurate"]),
        page_range: Optional[List[List[int]]] = Input(description="Page ranges to convert (list of [start, end])", default=None),
        document_timeout: Optional[float] = Input(description="Timeout for processing each document (seconds)", default=None),
        abort_on_error: bool = Input(description="Abort on error", default=False),
    ) -> dict:
        # Determine files to process
        files_to_process = []
        
        if file is not None:
            # If file is uploaded directly, save it to a temporary directory
            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, file.name)
            
            # Copy the uploaded file
            with open(file_path, 'wb') as f:
                shutil.copyfileobj(file, f)
            
            files_to_process.append(file_path)
            print(f"📁 File uploaded: {file.name} -> {file_path}")
            
        elif file_url is not None:
            # If URL is specified
            files_to_process.append(file_url)
            print(f"🌐 Using URL: {file_url}")
        else:
            return {"error": "Either file upload or file URL must be specified"}
        
        payload = {
            "files": files_to_process,
            "image_export_mode": image_export_mode,
            "do_ocr": do_ocr,
            "force_ocr": force_ocr,
            "table_mode": table_mode,
            "abort_on_error": abort_on_error,
            "ocr_engine": ocr_engine,
            "pdf_backend": pdf_backend,
        }
        if from_formats:
            payload["from_formats"] = from_formats
        if to_formats:
            payload["to_formats"] = to_formats
        if ocr_lang:
            payload["ocr_lang"] = ocr_lang
        if page_range:
            payload["page_range"] = page_range
        if document_timeout:
            payload["document_timeout"] = document_timeout

        try:
            print(f"🚀 Sending request to docling-serve with {len(files_to_process)} file(s)")
            response = requests.post(
                "http://localhost:5001/v1alpha/convert/source",
                json=payload,
                headers={"accept": "application/json"}
            )
            response.raise_for_status()
            result = response.json()
            
            # Clean up temporary files
            if file is not None:
                try:
                    shutil.rmtree(temp_dir)
                    print(f"🗑️ Temporary files cleaned: {temp_dir}")
                except Exception as e:
                    print(f"⚠️ Failed to clean temporary files: {e}")
            
            return result
            
        except Exception as e:
            # Clean up temporary files in case of error
            if file is not None:
                try:
                    shutil.rmtree(temp_dir)
                except:
                    pass
            return {"error": str(e)}

    def teardown(self):
        if hasattr(self, "proc"):
            self.proc.terminate() 