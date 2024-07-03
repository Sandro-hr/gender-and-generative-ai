import openai
from openai import OpenAI
import logging
import os
from datetime import datetime
import time

class QueryGPT():

    def __init__(self, open_ai_api_key, model) -> None:
        
        self.__open_ai_api_key = open_ai_api_key
        self.__model = model

    def query_gpt(self, search_string):
        
        OpenAI.api_key = self.__open_ai_api_key
        
        # Create log file
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(filename=f'logs/{datetime.now().strftime("%Y%m%d%H%M%S")}_chatgpt.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')

        try:
            client = OpenAI(
                api_key=os.environ.get("OPEN_AI_API_KEY"),
            )

            response = client.chat.completions.create(model="gpt-3.5-turbo",
                messages=[{"role": "user","content": search_string}], temperature = 0.7)
            
            logging.info(f"Request successful") 
            return response

        except openai.RateLimitError as e:
            
            retry_time = e.retry_after if hasattr(e, 'retry_after') else 30
            logging.info(f"Rate limit exceeded. Retrying in {retry_time} seconds...")
            print(f"Rate limit exceeded. Retrying in {retry_time} seconds...")
            time.sleep(retry_time)
            return

        except openai.APIError as e:
            retry_time = e.retry_after if hasattr(e, 'retry_after') else 30
            logging.info(f"API error occurred. Retrying in {retry_time} seconds...")
            print(f"API error occurred. Retrying in {retry_time} seconds...")
            time.sleep(retry_time)
            return

        except OSError as e:
            retry_time = 5  # Adjust the retry time as needed
            logging.info(f"Connection error occurred: {e}. Retrying in {retry_time} seconds...")
            print(f"Connection error occurred: {e}. Retrying in {retry_time} seconds...")      
            time.sleep(retry_time)
            return