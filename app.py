from flask import Flask, request, jsonify
from helper.openai_api import text_complition
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)


@app.route('/')
def home():
    return 'All is well...'


@app.route('/dialogflow/cx/receiveMessage', methods=['POST'])
def cxReceiveMessage():
    try:
        data = request.get_json()
        # Use this tag peoperty to choose the action
        # tag = data['fulfillmentInfo']['tag']
        query_text = data['text']

        result = text_complition(query_text)

        if result['status'] == 1:
            logger.info(f{finish_reason}: {tokens_total})

			return jsonify(
                {
                    'fulfillment_response': {
                        'messages': [
                            {
                                'text': {
                                    'text': [result['response']],
                                    'redactedText': [result['response']]
                                },
                                'responseType': 'HANDLER_PROMPT',
                                'source': 'VIRTUAL_AGENT'
                            }
                        ]
                    }
                }
            )
    except:
        pass
    return jsonify(
        {
            'fulfillment_response': {
                'messages': [
                    {
                        'text': {
                            'text': ['Something went wrong.'],
                            'redactedText': ['Something went wrong.']
                        },
                        'responseType': 'HANDLER_PROMPT',
                        'source': 'VIRTUAL_AGENT'
                    }
                ]
            }
        }
    )
