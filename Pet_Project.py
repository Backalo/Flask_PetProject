from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = '1234'

sensor_progress = 50

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
        progress = int(request.form.get('progress'))
        session['progress'] = progress
    else:
        # Default value or value from session
        progress = session.get('progress', 0)

    return render_template('Niveles.html', progress=progress)
    
@app.route('/Datos')
def Datos():
    return render_template('Datos.html')

@app.route('/Notificaciones')
def Notificaciones():
    numberOfElements = session.get('numberOfElements', 1)

    # Display the selected number in another HTML page
    return render_template('Notificaciones.html', numberOfElements=numberOfElements)

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
        session['progress'] = int(data.get('progress', 0))
        return jsonify({'success': True, 'progress': session['progress']})
    except Exception as e:
        return jsonify({'error': f'Invalid request - {str(e)}'})

@app.route('/get_sensor_value')
def get_sensor_value():
    global sensor_progress
    # Simulate reading the sensor value (replace this with actual sensor reading)
    sensor_progress = simulate_sensor_reading()
    return jsonify({'progress': sensor_progress})

def simulate_sensor_reading():
    # Simulate reading the sensor value (replace this with actual sensor reading logic)
    import random
    return random.randint(0, 100)


if __name__ == '__main__':
    app.run(debug=True)