from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import random
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
socketio = SocketIO(app)

sensor_progress_1 = 50
sensor_progress_2 = 50
notifications_1 = []
notifications_2 = []

# Define notifications in the global scope
notifications = {'notifications_1': notifications_1, 'notifications_2': notifications_2}

# Function to check notifications based on sensor progress
def check_notifications(progress_1, progress_2):
    global notifications_1, notifications_2
    threshold = 10

    if progress_1 < threshold:
        notifications_1.insert(0, 'Food served')
    if progress_2 < threshold:
        notifications_2.insert(0, 'Water served')

    # Keep only the latest 8 notifications
    notifications_1 = notifications_1[:8]
    notifications_2 = notifications_2[:8]

    # Emit a WebSocket event to update clients
    socketio.emit('update_notifications', {'notifications_1': notifications_1, 'notifications_2': notifications_2})

@app.route('/')
def Index():
    return render_template('Index.html')

@app.route('/Horarios', methods=['GET', 'POST'])
def Horarios():
    if request.method == 'POST':
        # Handle form submission
        session['numberOfElements'] = session.get('numberOfElements', 1)
        session['selectedTimes'] = request.form.getlist('selectedTimes')
    else:
        # Default values or values from session
        numberOfElements = session.get('numberOfElements', 1)
        selectedTimes = session.get('selectedTimes', [''])

    return render_template('Horarios.html', numberOfElements=numberOfElements, selectedTimes=selectedTimes)

@app.route('/Niveles', methods=['GET', 'POST'])
def Niveles():
    if request.method == 'POST':
        # Handle form submission
        progress_1 = int(request.form.get('progress_1'))
        progress_2 = int(request.form.get('progress_2'))
        session['progress_1'] = progress_1
        session['progress_2'] = progress_2

        # Check for notifications
        check_notifications(progress_1, progress_2)
    else:
        # Default value or value from session
        progress_1 = session.get('progress_1', 0)
        progress_2 = session.get('progress_2', 0)

    # Pass notifications to the template
    return render_template('Niveles.html', progress_1=progress_1, progress_2=progress_2, notifications=notifications)

@app.route('/Datos')
def Datos():
    return render_template('Datos.html')

@app.route('/Notificaciones')
def Notificaciones():
    numberOfElements = session.get('numberOfElements', 1)

    # Display the selected number in another HTML page
    return render_template('Notificaciones.html', numberOfElements=numberOfElements, notifications=notifications)

@app.route('/update_session', methods=['POST'])
def update_session():
    try:
        data = request.get_json()
        session['numberOfElements'] = int(data.get('numberOfElements', 1))
        session['selectedTimes'] = data.get('selectedTimes', [])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': f'Invalid request - {str(e)}'})

@app.route('/update_progress', methods=['POST'])
def update_progress():
    try:
        data = request.get_json()
        session['progress_1'] = int(data.get('progress_1', 0))
        session['progress_2'] = int(data.get('progress_2', 0))

        # Check for notifications
        check_notifications(session['progress_1'], session['progress_2'])

        # Emit a WebSocket event to update clients
        socketio.emit('update_progress', {'progress_1': session['progress_1'], 'progress_2': session['progress_2']})

        return jsonify({'success': True, 'progress_1': session['progress_1'], 'progress_2': session['progress_2']})
    except Exception as e:
        return jsonify({'error': f'Invalid request - {str(e)}'})

def simulate_sensor_reading():
    # Simulate reading the sensor value (replace this with actual sensor reading logic)
    return random.randint(0, 100)

def send_sensor_updates():
    while True:
        # Simulate reading the sensor values and send updates every 5 seconds
        sensor_progress_1 = simulate_sensor_reading()
        sensor_progress_2 = simulate_sensor_reading()

        # Check for notifications
        check_notifications(sensor_progress_1, sensor_progress_2)

        # Emit WebSocket event to update clients
        socketio.emit('update_progress', {
            'progress_1': sensor_progress_1,
            'progress_2': sensor_progress_2,
            'notifications_1': notifications_1,
            'notifications_2': notifications_2
        })

        # Sleep for 5 seconds before sending the next update
        time.sleep(5)

# Start a separate thread to send periodic updates
update_thread = threading.Thread(target=send_sensor_updates)
update_thread.daemon = True  # Exit the thread when the main thread exits
update_thread.start()

@app.route('/get_sensor_values')
def get_sensor_values():
    global sensor_progress_1, sensor_progress_2
    # Simulate reading the sensor values (replace this with actual sensor reading)
    sensor_progress_1 = simulate_sensor_reading()
    sensor_progress_2 = simulate_sensor_reading()

    # Check for notifications
    check_notifications(sensor_progress_1, sensor_progress_2)

    # Emit a WebSocket event to update clients
    socketio.emit('update_progress', {'progress_1': sensor_progress_1, 'progress_2': sensor_progress_2, 'notifications_1': notifications_1, 'notifications_2': notifications_2})

    return jsonify({'progress_1': sensor_progress_1, 'progress_2': sensor_progress_2, 'notifications_1': notifications_1, 'notifications_2': notifications_2})

# Add a new WebSocket event to handle sensor value requests
@socketio.on('request_sensor_values')
def handle_sensor_value_request():
    global sensor_progress_1, sensor_progress_2
    emit('update_progress', {'progress_1': sensor_progress_1, 'progress_2': sensor_progress_2, 'notifications_1': notifications_1, 'notifications_2': notifications_2})

@app.route('/get_notifications')
def get_notifications():
    global notifications
    return jsonify(notifications)

if __name__ == '__main__':
    socketio.run(app, debug=True)