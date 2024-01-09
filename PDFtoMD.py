#!/usr/bin/env python
import time
import requests
import json
from api_keys import MathPic_KEY

APP_KEY = MathPic_KEY

def convert(file):
    # REQUEST PDF ID
    # =============================================================================
    # send PDF via local file
    options = {
        "conversion_formats": {"md": True},
        "math_inline_delimiters": ["$", "$"],
        "rm_spaces": True,
        "enable_spell_check": False
    }
    r = requests.post("https://api.mathpix.com/v3/pdf",
        headers={
            "app_id": "APP_ID",
            "app_key": APP_KEY
        },
        data={
            "options_json": json.dumps(options)
        },
        files={
            "file": open(file,"rb")
        }
    )
    PDF_ID = r.json()["pdf_id"]
    print(PDF_ID)

    # =============================================================================
    # REQUEST STATUS
    processing = True
    while processing:
        # every 5 seconds, check the status of the PDF
        # if the status is "completed", then request the conversion to MD
        time.sleep(10)  # pause for 5 seconds
        # Perform a GET request
        r = requests.get("https://api.mathpix.com/v3/pdf/" + str(PDF_ID),
                        headers={
                            "app_id": PDF_ID,
                            "app_key": APP_KEY,
                            "Content-type": "application/json"
                            }  
        )
        STATUS = r.json()
        print(STATUS)
        if STATUS["status"] == "completed":
            processing = False


    # REQUEST PDF CONVERSION TO MD
    # =============================================================================
    headers = {
    "app_key": APP_KEY,
    "app_id": PDF_ID
    }
    url = "https://api.mathpix.com/v3/pdf/" + PDF_ID + ".md"
    response = requests.get(url, headers=headers)
    print(response.text)
    with open("PDFasMD.md", "w", encoding='utf-8') as f:
        f.write(response.text)
    print("PDFasMD.md created!!!")