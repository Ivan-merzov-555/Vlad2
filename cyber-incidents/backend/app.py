from flask import Flask, request, jsonify, make_response
import csv
import os
from functools import wraps

app = Flask(__name__)

# Файлы для хранения данных
USERS_FILE = 'users.csv'
INCIDENTS_FILE = 'incidents.csv'

# Инициализация файлов, если они не существуют
def init_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'password'])
    
    if not os.path.exists(INCIDENTS_FILE):
        with open(INCIDENTS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'title', 'description', 'severity', 'status', 'reporter', 'created_at'])

init_files()

# Простая проверка авторизации
def check_auth(username, password):
    with open(USERS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False

# Декоратор для проверки авторизации
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated

# Регистрация нового пользователя
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Проверяем существование пользователя
        with open(USERS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['username'] == username:
                    return jsonify({'error': 'Username already exists'}), 400
        
        # Добавляем пользователя
        with open(USERS_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, password])
        
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Работа с инцидентами
@app.route('/incidents', methods=['GET'])
@login_required
def get_incidents():
    incidents = []
    with open(INCIDENTS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            incidents.append(row)
    return jsonify(incidents)

@app.route('/incidents', methods=['POST'])
@login_required
def add_incident():
    data = request.get_json()
    auth = request.authorization
    
    # Генерируем ID (просто увеличиваем максимальный существующий)
    incident_id = 1
    with open(INCIDENTS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row['id']) >= incident_id:
                incident_id = int(row['id']) + 1
    
    new_incident = {
        'id': incident_id,
        'title': data.get('title'),
        'description': data.get('description'),
        'severity': data.get('severity', 'medium'),
        'status': data.get('status', 'open'),
        'reporter': auth.username,
        'created_at': data.get('created_at', '')  # В реальном приложении нужно использовать datetime
    }
    
    with open(INCIDENTS_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            new_incident['id'],
            new_incident['title'],
            new_incident['description'],
            new_incident['severity'],
            new_incident['status'],
            new_incident['reporter'],
            new_incident['created_at']
        ])
    
    return jsonify(new_incident), 201

@app.route('/incidents/<int:incident_id>', methods=['PUT'])
@login_required
def update_incident(incident_id):
    data = request.get_json()
    
    # Читаем все инциденты
    incidents = []
    with open(INCIDENTS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            incidents.append(row)
    
    # Находим и обновляем инцидент
    updated = False
    for incident in incidents:
        if int(incident['id']) == incident_id:
            incident['title'] = data.get('title', incident['title'])
            incident['description'] = data.get('description', incident['description'])
            incident['severity'] = data.get('severity', incident['severity'])
            incident['status'] = data.get('status', incident['status'])
            updated = True
            break
    
    if not updated:
        return jsonify({'error': 'Incident not found'}), 404
    
    # Перезаписываем файл
    with open(INCIDENTS_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'title', 'description', 'severity', 'status', 'reporter', 'created_at'])
        for incident in incidents:
            writer.writerow([
                incident['id'],
                incident['title'],
                incident['description'],
                incident['severity'],
                incident['status'],
                incident['reporter'],
                incident['created_at']
            ])
    
    return jsonify({'message': 'Incident updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)