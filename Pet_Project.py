from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = '1234'

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = 'flask_session'
app.config['SESSION_PERMANENT'] = True

Session(app)

@app.route('/')
def Index():
    return render_template('Index.html')

@app.route('/Horarios', methods=['GET', 'POST'])
def Horarios():
    if request.method == 'POST':
        # Handle form submission
        session['numberOfElements'] = int(request.form['numberOfElements'])
        session['selectedTimes'] = request.form.getlist('selectedTimes')
    else:
    # Default values or values from session
        numberOfElements = session.get('numberOfElements', 1)
        selectedTimes = session.get('selectedTimes', [''])

    return render_template('Horarios.html', numberOfElements=numberOfElements, selectedTimes=selectedTimes)

@app.route('/Niveles', methods=['GET', 'POST'])
def Niveles():
    if request.method == 'POST':
        # Handle form submission logic here
        session['progress1'] = int(request.form['inputProgress1'])
        session['progress2'] = int(request.form['inputProgress2'])
    else:
        # Default values for progress bars
        session.setdefault('progress1', 50)
        session.setdefault('progress2', 30)

    progress1 = session['progress1']
    progress2 = session['progress2']

    return render_template('Niveles.html', progress1=progress1, progress2=progress2)

@app.route('/Datos')
def Datos():
    return render_template('Datos.html')

@app.route('/Notificaciones')
def Notificaciones():
    return render_template('Notificaciones.html')

if __name__ == '__main__':
    app.run(debug=True)