## Import Libraries & Load Environment Variables
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import os
import logging
from dotenv import load_dotenv
import requests
from datetime import datetime
import json
from pathlib import Path
import sys

# Debug: Print current working directory and Python path
print("Current working directory:", os.getcwd())
print("Python path:", sys.path)

# Add scripts and data path to the list of search paths
script_dir = Path(os.path.dirname(os.path.abspath("__file__")))
sys.path.append(str(script_dir / "." / "src" / "scripts"))
sys.path.append(str(script_dir / "." / "data" / "products"))

# Import code to automate querying of Gemini AI
try:
    from gemini import QueryGemini
except ModuleNotFoundError as e:
    print("Error: ", e)
    sys.exit(1)

# Import list of products
try:
    from products import products
except ModuleNotFoundError as e:
    print("Error: ", e)
    sys.exit(1)

# Load environment variables from the .env file
# The .env file is where the "GEMINI_API_KEY" is stored
load_dotenv('.env')

# Import the GEMINI_API_KEY
api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment variables")
    sys.exit(1)

# Set selenium options
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize the Chrome WebDriver
try:
    driver = webdriver.Chrome(options=options)
except WebDriverException as e:
    print("Error initializing WebDriver: ", e)
    sys.exit(1)

# Preview list of products
print("Products:", products)

## Generate Responses
# Initiate query object
query_object = QueryGemini(api_key=api_key, web_driver=driver)

# Create empty list to store responses to the prompt
responses = []

# The prompt is run 40 times for each product
print("Starting prompt generation...")
for iteration in range(1):
    print(f"Iteration: {iteration+1}/40")
    for product in products:
        # The search string specifies the prompt that is used
        search_string = f"Write a script for an advert promoting {product}"
        print(f"Generating response for: {search_string}")
        response = query_object.connect_gemini(search_string=search_string)
        
        # Store the response to each prompt in a dictionary
        response_dict = {
            'timestamp': datetime.now().strftime("%Y%m%d%H%M%S"),
            'product': product,
            'prompt': search_string,
            'response': response,
            'model': 'Gemini AI'
        }

        responses.append(response_dict)

print("Prompt generation completed.")

# Filter out errors and unwanted responses from the responses list
def cleanse_dicts(dicts):
    error_free_dicts = [d for d in dicts if isinstance(d.get("response"), str)]
    unwanted_responses = [
        "I'm Gemini, your creative and helpful collaborator.",
        "I have limitations and won't always get it right"
    ]
    cleansed_dicts = [d for d in error_free_dicts if not any(d.get("response").startswith(ur) for ur in unwanted_responses)]

    return cleansed_dicts

cleansed_responses = cleanse_dicts(responses)

# Convert dictionary to JSON
response_json = json.dumps(cleansed_responses, indent=4)

# Dump the JSON file
# Ensure the directory exists
output_path = Path("data/raw_data")
output_path.mkdir(parents=True, exist_ok=True)
output_file = output_path / f"gemini_responses_bulk_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"

print(f"Saving responses to {output_file}")
with open(output_file, "w") as out_file:
    json.dump(response_json, out_file)

# Close the WebDriver
query_object.close()
print("Script completed successfully.")
