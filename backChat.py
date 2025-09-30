from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Servidor Flask funcionando correctamente"


# Configurar tu API Key de OpenAI
# Es más seguro usar variable de entorno:
# export OPENAI_API_KEY="TU_API_KEY" (Linux/Mac)
# setx OPENAI_API_KEY "TU_API_KEY" (Windows)
openai.api_key = os.getenv("OPENAI_API_KEY")
# O poner directamente (no recomendado para producción):
# openai.api_key = "TU_API_KEY"

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    if not user_msg:
        return jsonify({"reply": "No se recibió ningún mensaje"}), 400

    # Llamada al modelo GPT
    respuesta = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Podés usar gpt-4o, gpt-4.1-mini, etc.
        messages=[
            {"role": "system", "content": "Sos el asistente virtual de la página web de MiEmpresa. Respondé en español usando información oficial de la web si es posible."},
            {"role": "user", "content": user_msg}
        ]
    )

    reply_text = respuesta["choices"][0]["message"]["content"]
    return jsonify({"reply": reply_text})

if __name__ == "__main__":
    app.run(debug=True)
