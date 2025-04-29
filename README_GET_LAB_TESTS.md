# Instructions to Run and Test the /get-lab-tests API

## Setup Environment

1. Create and activate a Python virtual environment (optional but recommended):

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

2. Install required dependencies:

```bash
pip install fastapi uvicorn pillow pytesseract
```

3. Install Tesseract OCR engine on your system:

- For Windows: Download and install from https://github.com/tesseract-ocr/tesseract
- For Linux (Debian/Ubuntu): `sudo apt-get install tesseract-ocr`
- For MacOS: `brew install tesseract`

Make sure the `tesseract` command is available in your system PATH.

## Run the FastAPI App

Run the app using uvicorn:

```bash
uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Test the /get-lab-tests Endpoint

You can test the endpoint using curl or tools like Postman.

Example using curl:

```bash
curl -X POST "http://127.0.0.1:8000/get-lab-tests" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@path_to_your_image_file.png"
```

Replace `path_to_your_image_file.png` with the path to the image file you want to test.

## Response

The API returns a JSON response with the following structure:

```json
{
  "lab_tests": [
    {
      "lab_test_name": "Test Name",
      "lab_test_value": "Value",
      "bio_reference_range": "Reference Range",
      "lab_test_out_of_range": true/false
    },
    ...
  ],
  "is_success": true
}
```

- `lab_test_out_of_range` is a boolean indicating if the test value lies outside the reference range.
- `is_success` indicates if the API call was successful.

## Notes

- The text extraction and parsing logic is basic and may need adjustments for different lab report formats.
- Ensure the uploaded file is an image format supported by PIL and pytesseract.
