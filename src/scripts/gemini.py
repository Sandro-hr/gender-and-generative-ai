# src/scripts/gemini.py

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class QueryGemini:
    def __init__(self, api_key, web_driver=None, options=None):
        self.api_key = api_key
        self.web_driver = web_driver or webdriver.Chrome(options=options)
    
    def connect_gemini(self, search_string):
        # Correct URL for Google Generative Language API
        url = f"https://generativelanguage.googleapis.com/v1beta2/models/gemini-1.5-flash-latest:generateText?key={self.api_key}"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "prompt": {
                "text": search_string
            },
            "temperature": 0.7,
            "maxOutputTokens": 256
        }
        try:
            print(f"Making request to URL: {url} with headers: {headers} and data: {data}")
            response = requests.post(url, headers=headers, json=data)
            print(f"Response status code: {response.status_code}")
            response.raise_for_status()
            return response.json().get("results")[0]["output"] if response.json().get("results") else None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return str(e)

    def close(self):
        self.web_driver.quit()
