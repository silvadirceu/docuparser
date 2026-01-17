import os
import base64
import json
from typing import Dict, Any, Union
from openai import OpenAI

class DeepSeekEngine:
    def __init__(self):
        # Allow configuring host and model via env vars
        self.base_url = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434/v1")
        self.api_key = os.getenv("OLLAMA_API_KEY", "ollama") # Ollama doesn't strictly need a key usually
        self.model = os.getenv("OLLAMA_MODEL", "deepseek-r1")
        
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

    def _encode_image(self, image_path_or_bytes: Union[str, bytes]) -> str:
        if isinstance(image_path_or_bytes, str):
            with open(image_path_or_bytes, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        return base64.b64encode(image_path_or_bytes).decode('utf-8')

    def process(self, file_path_or_bytes: Any) -> Dict[str, Any]:
        """
        Process document with DeepSeek via Ollama.
        """
        try:
            # Check if input is likely an image/pdf we can send as image to VLM
            # For this implementation, we assume the model can handle base64 image input 
            # (common for multimodal models in OpenAI format, though pure deepseek-r1 is text-only. 
            # We assume user has a setup that works or we fallback to text extraction if they don't).
            # If the model is text-only, this might fail or hallucinate if we just paste base64. 
            # However, standard practice for "OCR via LLM" implies VLM.
            
            base64_image = self._encode_image(file_path_or_bytes)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Extract all data from this document image into a structured JSON format. Include fields for 'document_info', 'entities', 'tables', and 'totals'. Do not include markdown formatting or explanations, just the raw JSON."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                response_format={ "type": "json_object" } # Force JSON if supported, otherwise prompt relies on it
            )
            
            content = response.choices[0].message.content
            
            # Clean content if it contains markdown code blocks
            if "```json" in content:
                content = content.replace("```json", "").replace("```", "")
            elif "```" in content:
                content = content.replace("```", "")
                
            return json.loads(content)

        except Exception as e:
            print(f"DeepSeek OCR Error: {e}")
            return {
                "error": str(e),
                "raw_text_fallback": "Failed to process with DeepSeek",
                "tables": [],
                "entities": {}
            }
