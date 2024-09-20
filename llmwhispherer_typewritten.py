from unstract.llmwhisperer.client import LLMWhispererClient

# Initialize the client with your API key
client = LLMWhispererClient(base_url="https://llmwhisperer-api.unstract.com/v1",
                            api_key='a8e0698063a64fe9a7f9848b1f62e660',
                            api_timeout=300)

# Extract tables from the PDF
result = client.whisper(file_path="Dirac-language-manual-for-tesseract-feature-analysis.pdf", output_mode='line-printer')
extracted_text = result["extracted_text"]
print(extracted_text)
