from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = '1234'

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
    try:
        data = request.get_json()
        progress1 = data.get('progress1', 50)
        progress2 = data.get('progress2', 30)
        return jsonify({'progress1': progress1, 'progress2': progress2})
    except Exception as e:
        return jsonify({'error': f'Invalid request - {str(e)}'})
    
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

if __name__ == '__main__':
    app.run(debug=True)