from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
from pydantic import BaseModel
import pytesseract
from PIL import Image
import io
import re

app = FastAPI()

class LabTest(BaseModel):
    lab_test_name: str
    lab_test_value: str
    bio_reference_range: str
    lab_test_out_of_range: bool

class LabTestResponse(BaseModel):
    lab_tests: List[LabTest]
    is_success: bool

def parse_lab_tests(text: str) -> List[Dict[str, Any]]:
    """
    Parse the OCR extracted text to find lab test names, values, and reference ranges.
    This is a simplified example and may need to be adapted to the specific format of lab reports.
    """
    lab_tests = []
    # Example regex pattern to capture lab test name, value, and reference range
    # This pattern assumes lines like: TestName  Value  ReferenceRange
    pattern = re.compile(r"([A-Za-z\s]+)\s+([\d\.]+)\s+([\d\.-]+)")
    for match in pattern.finditer(text):
        name = match.group(1).strip()
        value = match.group(2).strip()
        ref_range = match.group(3).strip()
        # Determine if value is out of range (simple numeric comparison)
        try:
            val_num = float(value)
            if '-' in ref_range:
                low, high = ref_range.split('-')
                low = float(low)
                high = float(high)
                out_of_range = val_num < low or val_num > high
            else:
                out_of_range = False
        except:
            out_of_range = False
        lab_tests.append({
            "lab_test_name": name,
            "lab_test_value": value,
            "bio_reference_range": ref_range,
            "lab_test_out_of_range": out_of_range
        })
    return lab_tests

@app.post("/get-lab-tests", response_model=LabTestResponse)
async def get_lab_tests(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image file.")
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        text = pytesseract.image_to_string(image)
        lab_tests = parse_lab_tests(text)
        return LabTestResponse(lab_tests=lab_tests, is_success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
