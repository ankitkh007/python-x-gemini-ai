from core.gemini_client import client
from google.genai import types
import httpx
import pathlib
import io

# doc_url = (
#     "https://discovery.ucl.ac.uk/id/eprint/10089234/1/343019_3_art_0_py4t4l_convrt.pdf"
# )

# # Retrieve and encode the PDF byte
# doc_data = httpx.get(doc_url).content
# pdf = types.Part.from_bytes(data=doc_data, mime_type="application/pdf")

## Loacally stored files are processed in this manner
# file_path = pathlib.Path("projects\pdfs\mamta_report.pdf")
# pdf = types.Part.from_bytes(data=file_path.read_bytes(), mime_type="application/pdf")

file_path = pathlib.Path("projects\pdfs\Report.pdf")
file_data = io.BytesIO(file_path.read_bytes())

## Using Upload files API from Gemini
pdf = client.files.upload(file=file_data, config={"mime_type": "application/pdf"})

prompt = "Summarize this report and generate a conclusion along with suggestion required if any."

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=[pdf, prompt],
    config=types.GenerateContentConfig(
        system_instruction="Be concise and precise, use bullets for better ouput."
    ),
)

print(response.text)
