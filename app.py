import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Configuración de la API de Moodle
MOODLE_URL = "https://escueladeartesonoras.com/moodle/webservice/rest/server.php"
TOKEN = os.getenv("MOODLE_TOKEN")  # Asegúrate de establecer esta variable de entorno

@app.route('/get_courses', methods=['GET'])
def get_courses():
    # Recibimos el ID del alumno desde la URL de la solicitud
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # Parámetros para obtener los cursos del alumno
    params = {
        'wstoken': TOKEN,
        'wsfunction': 'core_enrol_get_users_courses',
        'moodlewsrestformat': 'json',
        'userid': user_id
    }

    # Realiza la solicitud a la API de Moodle
    response = requests.get(MOODLE_URL, params=params)

    if response.status_code == 200:
        try:
            return jsonify(response.json())  # Devuelve los cursos del alumno
        except ValueError:
            return jsonify({"error": "Error al procesar la respuesta de la API"}), 500
    else:
        return jsonify({"error": "No se pudo obtener los cursos"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Usa el puerto proporcionado por Render
    app.run(debug=True, host='0.0.0.0', port=port)
