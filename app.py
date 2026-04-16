from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('Nis1index.html')

@app.route('/register')
def register():
    return render_template('Nis1register.html')

# --- THIS IS THE MAGIC PART ---
@app.route('/<path:filename>')
def serve_any_page(filename):
    # This automatically handles Nis1events.html, Nis1admission.html, etc.
    return render_template(filename)
# ------------------------------

@app.route('/submit', methods=['POST'])
def submit():
    student_name = request.form.get('username')
    standard = request.form.get('standard')
    print(f"New Registration: {student_name} for {standard}")
    return f"<h1>Success!</h1><p>Thank you {student_name}, registration complete.</p>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
