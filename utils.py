import requests
import os
from werkzeug.utils import secure_filename

OLLAMA_API_URL = "http://localhost:11434/api/generate"
UPLOAD_FOLDER = 'uploads'

def query_llm(prompt):
    data = {
        "model": "llama2:9b",
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_API_URL, json=data)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    return response.json()['response']

def handle_file_upload(file):
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return file_path
    return None
