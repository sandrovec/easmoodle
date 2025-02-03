from flask import Flask, jsonify, request
from flask_cors import CORS  # Importar CORS
import requests

app = Flask(__name__)

# Configuración de CORS para permitir solicitudes desde tu dominio
CORS(app, origins="https://escueladeartesonoras.com")  # Permite solicitudes desde tu dominio

# Configuración de la API de Moodle
MOODLE_URL = "https://escueladeartesonoras.com/moodle/webservice/rest/server.php"
TOKEN = "2373eab4985d0366690868436e053e1f"

# Función para obtener los cursos del usuario
def get_courses(user_id):
    params = {
        'wstoken': TOKEN,
        'wsfunction': 'core_enrol_get_users_courses',
        'moodlewsrestformat': 'json',
        'userid': user_id
    }

    response = requests.get(MOODLE_URL, params=params)

    if response.status_code == 200:
        return jsonify(response.json())  # Devuelve los cursos del alumno
    else:
        return jsonify({"error": "No se pudo obtener los cursos"}), 500

# Ruta para interactuar con el chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Recibimos la entrada del usuario
    user_input = request.json.get('user_input')
    user_id = request.json.get('user_id')  # ID del usuario desde la solicitud

    if not user_input or not user_id:
        return jsonify({"error": "User input and user ID are required"}), 400

    # Si el usuario pregunta por un curso, mostramos recomendaciones
    if 'curso' in user_input.lower():
        # Obtener los cursos del usuario
        response = get_courses(user_id)

        if response.status_code == 200:
            courses = response.json()
            if courses:  # Si el alumno tiene cursos, recomendar el primero
                recommended_course = courses[0]['fullname']  # Ejemplo de recomendación
                return jsonify({"message": f"Te recomiendo estudiar el curso: {recommended_course}"}), 200
            else:
                return jsonify({"message": "Parece que no estás inscrito en ningún curso aún."}), 200
        else:
            return jsonify({"message": "Lo siento, no pude obtener los cursos en este momento."}), 500

    # Si la entrada no se entiende, una respuesta por defecto
    return jsonify({"message": "Lo siento, no entendí tu mensaje. ¿En qué puedo ayudarte?"}), 200

# Ruta para obtener cursos del usuario directamente
@app.route('/get_courses', methods=['GET'])
def get_courses_endpoint():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    return get_courses(user_id)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

