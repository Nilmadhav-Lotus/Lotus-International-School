from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__, template_folder='.')

# Your latest Google Script URL
SHEET_URL = "https://script.google.com/macros/s/AKfycbzdGbEUMgw28ySotKoT-opBMsfckz5rljJOEp58ow5z_s1TZPafVCytDPQb1EVpPTUb/exec"

@app.route('/')
def index():
    return render_template('Nis1index.html')

# --- DASHBOARD ROUTES ---

@app.route('/Nis1admission.html')
def register():
    return render_template('Nis1admission.html')

@app.route('/Nis1events.html')
def events():
    return render_template('Nis1events.html')

@app.route('/Nis1sports.html')
def sports():
    return render_template('Nis1sports.html')

@app.route('/Nis1activities.html')
def activities():
    return render_template('Nis1activities.html')

@app.route('/Nis1about.html')
def about():
    return render_template('Nis1about.html')

@app.route('/Nis1contact.html')
def contact():
    return render_template('Nis1contact.html')

# --- DATA SUBMISSION ---

@app.route('/submit', methods=['POST'])
def submit():
    # Capture ALL form data
    name = request.form.get('username')
    father = request.form.get('father_name')
    mother = request.form.get('mother_name')
    dob = request.form.get('dob')
    blood = request.form.get('blood_group')
    email = request.form.get('parent_email')
    standard = request.form.get('standard')
    gender = request.form.get('gender')
    mobile = request.form.get('parent_mobile')
    address = request.form.get('address')
    
    payload = {
        "name": name, "father": father, "mother": mother,
        "dob": dob, "blood": blood, "email": email,
        "standard": standard, "gender": gender, 
        "mobile": mobile, "address": address
    }
    
    try:
        requests.post(SHEET_URL, json=payload, timeout=10)
    except Exception as e:
        print(f"Error: {e}")

    # Professional Success Report
    return f"""
    <!DOCTYPE HTML>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Registration Successful</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #e8f5e9; display: flex; justify-content: center; padding: 20px; }}
            .report {{ background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 500px; width: 100%; border-top: 10px solid #4caf50; }}
            h1 {{ color: #2e7d32; font-size: 1.5rem; text-align: center; }}
            .details {{ margin: 20px 0; line-height: 1.8; }}
            .btn {{ display: block; text-align: center; background: #4caf50; color: white; padding: 10px; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="report">
            <h1>🏫 Nilmadhav International School</h1>
            <p style="text-align:center; font-weight:bold; text-decoration:underline;">OFFICIAL NOTICE</p>
            <p>To the Parent/Guardian of <strong>{name}</strong>,</p>
            <div class="details">
                • <strong>Student Name:</strong> {name}<br>
                • <strong>Date of Birth:</strong> {dob}<br>
                • <strong>Standard:</strong> {standard}<br>
                • <strong>Blood Group:</strong> {blood}<br>
                • <strong>Parent Email:</strong> {email}<br>
                • <strong>Registered Address:</strong> {address}
            </div>
            <p style="font-size: 0.9rem;">Registration details for {name} have been securely recorded.</p>
            <a href="/" class="btn">Return to Portal</a>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
