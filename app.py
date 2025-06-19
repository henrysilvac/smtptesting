from flask import Flask, request, render_template_string, session
import smtplib
import ssl
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_session'

LOG_FILE = 'smtp_log.txt'

HTML_FORM = """
<!doctype html>
<title>SMTP Tester</title>
<h2>Probar conexión SMTP</h2>

<form method="post">
  <label>Servidor SMTP:</label><br>
  <input type="text" name="host" value="{{ form.host }}" required><br><br>

  <label>Puerto:</label><br>
  <input type="number" name="port" value="{{ form.port }}" required><br><br>

  <label>Email / Usuario:</label><br>
  <input type="email" name="username" value="{{ form.username }}" required><br><br>

  <label>Contraseña:</label><br>
  <input type="password" name="password" value="{{ form.password }}" required><br><br>

  <label>Modo de conexión:</label><br>
  <select name="security">
    <option value="none" {% if form.security == 'none' %}selected{% endif %}>Sin cifrado</option>
    <option value="starttls" {% if form.security == 'starttls' %}selected{% endif %}>STARTTLS</option>
    <option value="ssl" {% if form.security == 'ssl' %}selected{% endif %}>SSL</option>
  </select><br><br>

  <button type="submit">Probar conexión</button>
</form>

{% if result %}
<hr>
<h3>Resultado actual:</h3>
<pre>{{ result }}</pre>
{% endif %}

{% if logs %}
<hr>
<h3>Historial de conexiones en esta sesión:</h3>
<ul>
  {% for log in logs %}
    <li><strong>{{ log.time }}</strong>: {{ log.message }}</li>
  {% endfor %}
</ul>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def smtp_test():
    result = None

    if 'logs' not in session:
        session['logs'] = []

    form = {
        'host': '',
        'port': '',
        'username': '',
        'password': '',
        'security': 'none'
    }

    if request.method == 'POST':
        form['host'] = request.form['host']
        form['port'] = request.form['port']
        form['username'] = request.form['username']
        form['password'] = request.form['password']
        form['security'] = request.form['security']

        host = form['host']
        port = int(form['port'])
        username = form['username']
        password = form['password']
        security = form['security']

        try:
            if security == 'ssl':
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL(host, port, context=context)
            else:
                server = smtplib.SMTP(host, port, timeout=10)
                if security == 'starttls':
                    context = ssl.create_default_context()
                    server.starttls(context=context)
            server.login(username, password)
            server.quit()
            result = f"✅ Conexión exitosa a {host}:{port} como {username}"
        except Exception as e:
            result = f"❌ Error: {str(e)}"

        # Crear mensaje sin la contraseña
        log_entry = {
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'message': (
                f"{result} | "
                f"host={host}, port={port}, user={username}, security={security}"
            )
        }

        # Agregar al log de sesión
        session['logs'].append(log_entry)
        session.modified = True

        # Escribir también en archivo local
        with open(LOG_FILE, 'a') as f:
            f.write(f"{log_entry['time']} - {log_entry['message']}\n")

    return render_template_string(HTML_FORM, form=form, result=result, logs=session['logs'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)