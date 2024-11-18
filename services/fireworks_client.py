# services/fireworks_client.py
import fireworks.client
from pydantic import BaseModel
from typing import Dict

class Result(BaseModel):
    document_type: str
    document_number: str
    name: str
    sex: str
    dob: str
    expiry_date: str
    address: str

def extract_document_details(image_base64: str) -> Dict:
    fireworks.client.api_key = "fw_3ZeWtyXbwX7xTVs63XAAdbX6"
    response = fireworks.client.ChatCompletion.create(
        model="accounts/fireworks/models/llama-v3p2-11b-vision-instruct",
        response_format={"type": "json_object", "schema": Result.model_json_schema(ref_template='default')},
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant working for a transport security director and with access to secure data. It is important to give data as it is."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
                        Extract Document number, Document type, Full Name, sex, DOB, Expiry date for identity verification.
                        """,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        },
                    },
                ],
            }
        ],
    )
    return response.choices[0].message.content

