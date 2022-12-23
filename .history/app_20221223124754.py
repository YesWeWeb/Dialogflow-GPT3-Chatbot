# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
# from cgitb import text
from flask import Flask, request, make_response, jsonify
# from datetime import date
import os
import openai
# import json
# import requests
# import time
key = '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'
openai.api_key = key
import hashlib



def leave_last_lines_from_file(filename,lines_count):
	with open(filename) as f:
		lines = f.readlines()
		return ''.join(lines[-lines_count:])


 
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
 




  

def results():
	if request.method == "POST":

		# build a request object 
		req = request.get_json(force=True) 

		# fetch action from json 
		prompt = req.get('queryResult').get('queryText') 


		dialogflow_session_id = req.get('session')


		encoded = dialogflow_session_id.encode()
		md5_hash = hashlib.md5(encoded).hexdigest()
		context_file = f"./talk_sessions/{md5_hash}.txt"


		if not os.path.isfile(context_file):
			f = open(context_file, 'w')
			f.close()




		f = open(context_file, "a")
		f.write(f"{prompt}\n")
		f.close()

		#open and read the file after the appending:
		f = open(context_file, "r")
		finalPrompt =  f.read()
		f.close()


		gptResponseText = get_gpt3_response(finalPrompt)





		f = open(context_file, "a")

		if gptResponseText in f.read():
			gptResponseText = get_gpt3_response(finalPrompt)

		f.write(f"{gptResponseText}\n\n\n")
		f.close()


		last_lines_of_memory = leave_last_lines_from_file(context_file, 20)
		#write in file
		f = open(context_file, "w")
		f.write(f"{last_lines_of_memory}")
		f.close()




		#if trimmed gptResponseText was empty, then return "sorry, I couldn't understant that"  as fullfillmenttext else return gptResponseText 

		if gptResponseText == "":
			return {'fulfillmentText': "Sorry, I couldn't understand that"} 
		else:
			return {'fulfillmentText': gptResponseText} 

def get_gpt3_response(finalPrompt):
	response = openai.Completion.create(
		engine="text-davinci-001",
		prompt=f"{finalPrompt}\n",
		temperature=0.5,
		max_tokens=100,
		top_p=1,
		frequency_penalty=0,
		presence_penalty=0)
		
	gptResponseText = response.choices[0].text
	return gptResponseText


# create a route for webhook 
@app.route('/webhook', methods=['GET', 'POST']) 
def webhook(): 
	# return response 
	return make_response(jsonify(results())) 





# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
	return 'hello world!'
 
# main driver function
if __name__ == '__main__':
 
	# run() method of Flask class runs the application
	# on the local development server.
	app.run()







