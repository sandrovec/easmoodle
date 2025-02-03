from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

# Configuración de la API de Moodle
MOODLE_URL = "https://escueladeartesonoras.com/moodle/webservice/rest/server.php"
TOKEN = os.getenv("MOODLE_TOKEN")  # El token se obtiene de una variable de entorno

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
        return jsonify(response.json())  # Devuelve los cursos del alumno
    else:
        return jsonify({"error": "No se pudo obtener los cursos"}), 500

if __name__ == '__main__':
    # Inicia la aplicación en el puerto 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
