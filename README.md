# SOLID-AI-Manager
Interface to work with AI models using **SOLID** principles

This interface presents service to work with various AI models: from gemini to chatGPT.
This service is following the **five SOLID principles**. It has secondary services:
- Request Maker - builds and sends request
- Extractor - extracts response data data

The main service **not** depend on a specific services/AI models implementation.

# Usage
### 1. Clone repository
```bash
git clone https://github.com/yeghor/SOLID-AI-Manager.git
```
### 2. Set up credentials
Create `.env` file and fill with your API keys:
```
# API_KEY_{MODELTYPE}
API_KEY_GEMINI = "YourAPIKey"
API_KEY_DEEPSEEK = "YourAPIKey"
```
### Run the program
Open `main_service.py`, create `MainAiService` instance passing model type as a first argument.

And call `query(query_text: str, json=True)` method
Example:
```Python
if __name__ == "__main__":
    service = MainAiService("gemini")
    print(service.query("How much os 2 times 2?", json=True))
```
