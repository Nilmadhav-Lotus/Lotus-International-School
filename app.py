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
def admission():
    return render_template('Nis1admission.html')

@app.route('/Nis1register.html') 
def register_page(): 
    return render_template('Nis1register.html')

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
    # 1. Capture ALL form data from the website
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
    
    # 2. Send to Google Sheets
    try:
        requests.post(SHEET_URL, json=payload, timeout=10)
    except Exception as e:
        print(f"Error: {e}")

    # 3. Modern Success Page with ALL details
    return f"""
    <!DOCTYPE HTML>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Registration Successful</title>
        <style>
            body {{
                margin: 0;
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
            }}
            .card {{
                background: white;
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 500px;
                width: 100%;
            }}
            .checkmark {{
                font-size: 60px;
                color: #4caf50;
                margin-bottom: 10px;
                animation: scaleIn 0.5s ease-out;
            }}
            @keyframes scaleIn {{
                0% {{ transform: scale(0); }}
                100% {{ transform: scale(1); }}
            }}
            h1 {{ color: #2e7d32; margin-top: 0; font-size: 1.6rem; }}
            .details {{
                background: #f9f9f9;
                padding: 15px;
                border-radius: 12px;
                margin: 20px 0;
                text-align: left;
                border-left: 6px solid #4caf50;
                font-size: 0.95rem;
                line-height: 1.6;
            }}
            .details strong {{ color: #555; width: 120px; display: inline-block; }}
            .btn {{
                display: inline-block;
                padding: 12px 30px;
                background: #4caf50;
                color: white;
                text-decoration: none;
                border-radius: 30px;
                font-weight: bold;
                transition: all 0.3s ease;
            }}
            .btn:hover {{
                background: #45a049;
                transform: translateY(-2px);
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="checkmark">✔</div>
            <h1>Registration Complete!</h1>
            <p style="color: #666;">Official details recorded for NIS admission:</p>
            
            <div class="details">
                <div><strong>Student:</strong> {name}</div>
                <div><strong>Standard:</strong> {standard}</div>
                <div><strong>Father:</strong> {father}</div>
                <div><strong>Mother:</strong> {mother}</div>
                <div><strong>DOB:</strong> {dob}</div>
                <div><strong>Blood Group:</strong> {blood}</div>
                <div><strong>Email:</strong> {email}</div>
                <div><strong>Mobile:</strong> {mobile}</div>
                <div><strong>Address:</strong> {address}</div>
            </div>
            
            <a href="/" class="btn">Back to Home</a>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    # Fix for Render: It listens to the dynamic port provided by the environment
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
