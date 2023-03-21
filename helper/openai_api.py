import os
from dotenv import load_dotenv
import openai
import datetime
import logging

current_date = datetime.date.today()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
openai.api_key = os.environ.get('OPENAI_KEY')

def text_complition(prompt: str) -> dict:
    '''
    Call Openai API for text completion

    Parameters:
        - prompt: user query (str)

    Returns:
        - dict
    '''
    try:

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Bonjour"},
                {"role": "assistant", "content": "Bonjour !/nJe suis Nova, votre assistant personnel./nQue puis-je faire pour vous aujourd'hui ?"}
            ]
        )


        return {
            'status': 1,
            'response': response['choices'][0]['message']['content']
        }
    except:
        return {
            'status': 0,
            'response': ''
        }
        