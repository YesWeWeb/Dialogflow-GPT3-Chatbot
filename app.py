import os
import hashlib
from flask import Flask, request
import openai
import time

openai.api_key = os.getenv("OPENAI_KEY")

initial_prompt = "Tu es mon assistant qui se nomme Nova qui est serviable, drôle, empathique et amical. Ton objectif est de faire en sorte que je me se sente mieux en me sentant écouté. Tu ne sais pas répondre aux questions relatives à la date du jour, à l'heure actuelle, ni aux nouvelles après 2021 car tu n'es pas relié à Internet et tu réponds de façon énigmatique à ce genre de question. L'année en cours est 2023. Pour les questions relatives à la météo, tu imagines une façon amusante de me dire d'aller dehors pour le savoir et sans jamais me donner d'indications sur le temps actuel. Nova est une IA générative conçue pour interagir avec les utilisateurs sur WhatsApp et leur offrir une expérience conversationnelle agréable et enrichissante. En tant qu'assistant personnel, tu es capable de m'aider dans une variété de tâches, telles que la recherche d'informations, la rédaction de contenu, la création d'histoires amusantes, donner des idées de recettes de cuisine. Tu peux aussi discuter de musique, de films, de livres, de voyages, ou de tout ce qui pourrait me passionner. Quand je te demande une explication, tu réponds comme si tu t'adressais à un enfant, en utilisant des analogies ou des métaphores. Avec un ton empathique et engageant, tu m'invitesite à poursuivre la conversation de manière naturelle, en me posant des questions après m'avoir donner des suggestions pertinentes et créatives. Grâce à ton intelligence artificielle avancée, tu es en mesure de comprendre le contexte de la conversation et d'adapter ton discours.\n\nUtilisateur: Bonjour\nNova: Bonjour ! Comment puis-je vous aider ?\n\nUtilisateur: Quelle année sommes nous ? Nous sommes en 2023 !",


def leave_last_lines_from_file(filename,lines_count):
	with open(filename, encoding='utf-8') as file:
		lines = file.readlines()
		return ''.join(lines[-lines_count:])


app = Flask(__name__)

@app.route('/dialogflowES', methods=['POST'])
def ESmain():

	delete_outdated_interactions()
	
	req = request.get_json(force=True)

	prompt = req.get('queryResult').get('queryText')

	dialogflow_session_id = req.get('session')


	encoded = dialogflow_session_id.encode()
	md5_hash = hashlib.md5(encoded).hexdigest()
	context_file = f"./talk_sessions/{md5_hash}.txt"


	if not os.path.isfile(context_file):
		file = open(context_file, 'w', encoding='utf-8')
		file.write(f"{initial_prompt}\n")
		file.close()


	file = open(context_file, "a", encoding='utf-8')
	file.write(f"{prompt}\n")
	file.close()


	file = open(context_file, "r", encoding='utf-8')
	final_prompt =  file.read()
	file.close()

	gpt_response_text = get_gpt3_response(final_prompt)
	gpt_response_text = gpt_response_text.strip()



	file = open(context_file, "r", encoding='utf-8')

	if gpt_response_text in file.read():
		print("same answer was detected")
		gpt_response_text = get_gpt3_response(final_prompt)
		gpt_response_text = gpt_response_text.strip()



	file = open(context_file, "a", encoding='utf-8')
	file.write(f"{gpt_response_text}\n\n\n")
	file.close()


	last_lines_of_memory = leave_last_lines_from_file(context_file, 20)

	file = open(context_file, "w",  encoding='utf-8')
	file.write(f"{last_lines_of_memory}")
	file.close()


	if gpt_response_text == "":
		return {'fulfillmentText': "Sorry, I couldn't understand that"}
	else:
		return {'fulfillmentText': gpt_response_text}


@app.route('/dialogflowCX', methods=['POST'])
def CXmain():

	delete_outdated_interactions()
	
	req = request.get_json(force=True)

	prompt = req.get('text')

	dialogflow_session_id = req.get('sessionInfo').get('session')


	encoded = dialogflow_session_id.encode()
	md5_hash = hashlib.md5(encoded).hexdigest()
	context_file = f"./talk_sessions/{md5_hash}.txt"


	if not os.path.isfile(context_file):
		file = open(context_file, 'w', encoding='utf-8')
		file.write(f"{initial_prompt}\n")
		file.close()


	file = open(context_file, "a", encoding='utf-8')
	file.write(f"{prompt}\n")
	file.close()


	file = open(context_file, "r", encoding='utf-8')
	final_prompt =  file.read()
	file.close()
	print(final_prompt)

	gpt_response_text = get_gpt3_response(final_prompt)
	gpt_response_text = gpt_response_text.strip()



	file = open(context_file, "r", encoding='utf-8')

	if gpt_response_text in file.read():
		print("same answer was detected")
		gpt_response_text = get_gpt3_response(final_prompt)
		gpt_response_text = gpt_response_text.strip()



	file = open(context_file, "a", encoding='utf-8')
	file.write(f"{gpt_response_text}\n\n\n")
	file.close()


	last_lines_of_memory = leave_last_lines_from_file(context_file, 20)

	file = open(context_file, "w",  encoding='utf-8')
	file.write(f"{last_lines_of_memory}")
	file.close()


	if gpt_response_text == "":
		return {"fulfillment_response":{"messages":[{"text":{"text": "Sorry, I couldn't understand that","redactedText": "Sorry, I couldn't understand that"},"responseType":"HANDLER_PROMPT","source":"VIRTUAL_AGENT"}]}}
	else:
		return {"fulfillment_response":{"messages":[{"text":{"text": gpt_response_text,"redactedText": gpt_response_text},"responseType":"HANDLER_PROMPT","source":"VIRTUAL_AGENT"}]}}


	



def delete_outdated_interactions():
	three_minutes_ago = time.time() - 180
	folder = './talk_sessions/'

	for file in os.listdir(folder):
		print(file)
		t = os.stat(folder+file).st_mtime
		if t < three_minutes_ago:
			os.remove(folder+file)



def get_gpt3_response(final_prompt):
	response = openai.Completion.create(
		engine="text-davinci-003",
		prompt=f"{final_prompt}\n",
		temperature=0.4,
      	max_tokens=256,
      	top_p=1,
      	frequency_penalty=0.18,
      	presence_penalty=0,
      	stop=["/nUtilisateur:", "/nNova:"],
    )

	gpt_response_text = response.choices[0].text
	return gpt_response_text



if __name__ == '__main__':
	app.run(port=5000)
