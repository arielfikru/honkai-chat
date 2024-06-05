from flask import Flask, render_template, request, jsonify
import json
import google.generativeai as genai
import yaml

app = Flask(__name__)

with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

api_key = config['gemini_ai']['api_key']

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

model_name = "gemini-1.5-flash"
model = genai.GenerativeModel(
    model_name=model_name,
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="Kamu hanya boleh memberi output dengan format\n\n```\n      {\n        \"from\": \"char\",\n        \"value\": \"\"\n      }\n```\n\n**Kamu hanya akan menghasilkan output dari char dan tidak akan me-generate bagian sebelumnya dari percakapan. Serta tidak boleh memberikan hasil yang repetitif terhadap outputmu sebelumnya**",
)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    conversation = json.loads(request.form['conversation'])

    new_message = {
        "from": "user",
        "value": message
    }
    conversation.append(new_message)

    herta_typing = {
        "from": "char",
        "value": "Herta is typing..."
    }
    conversation.append(herta_typing)

    chat_history = [{"role": "user", "parts": [json.dumps({"conversations": conversation})]}]

    chat_session = model.start_chat(history=chat_history)

    response = chat_session.send_message(message)

    response_json = json.loads(response.text.strip("```json"))
    conversation.pop()
    conversation.append(response_json)

    return jsonify(conversation)

@app.route('/char_settings')
def char_settings():
    return render_template('char_settings.html')


@app.route('/update_settings', methods=['POST'])
def update_settings():
    global model, generation_config, model_name

    new_settings = request.json

    generation_config.update({
        "temperature": new_settings['temperature'],
        "top_p": new_settings['top_p'],
        "top_k": new_settings['top_k'],
        "max_output_tokens": new_settings['max_output_tokens']
    })

    model_name = new_settings['model_name']

    model = genai.GenerativeModel(
        model_name=model_name,
        safety_settings=safety_settings,
        generation_config=generation_config,
        system_instruction="Kamu hanya boleh memberi output dengan format\n\n```\n      {\n        \"from\": \"char\",\n        \"value\": \"\"\n      }\n```\n\n**Kamu hanya akan menghasilkan output dari char dan tidak akan me-generate bagian sebelumnya dari percakapan. Serta tidak boleh memberikan hasil yang repetitif terhadap outputmu sebelumnya**",
    )

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
