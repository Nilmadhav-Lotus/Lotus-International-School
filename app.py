from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__, template_folder='.')

# Your latest Google Script URL
SHEET_URL = "https://script.google.com/macros/s/AKfycbzVEMtyhqwezagpSGMpW3-qYMKF3NjcuB0QiUs6zfPTEOqnVJvyXRGIaDdGMNBP8Sg/exec"

@app.route('/')
def index():
    return render_template('Nis1index.html')

@app.route('/register')
def register():
    return render_template('Nis1register.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Capture all form data
    name = request.form.get('username')
    dob = request.form.get('dob')
    standard = request.form.get('standard')
    gender = request.form.get('gender')
    mobile = request.form.get('parent_mobile')
    address = request.form.get('address')
    
    # Logs for Render Dashboard
    print("\n" + "⭐"*30)
    print(f" NEW REGISTRATION ")
    print(f" NAME:    {name}")
    print(f" DOB:     {dob}")
    print(f" CLASS:   {standard}")
    print(f" MOBILE:  {mobile}")
    print("⭐"*30 + "\n")

    # Send data to Google
    payload = {
        "name": name,
        "dob": dob,
        "standard": standard,
        "gender": gender,
        "mobile": mobile,
        "address": address
    }
    
    try:
        response = requests.post(SHEET_URL, json=payload, timeout=10)
        print(f"✅ Google Sheets Sync Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # The Exciting Success Page
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
            }}
            .card {{
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 450px;
                width: 90%;
            }}
            .checkmark {{
                font-size: 80px;
                color: #4caf50;
                margin-bottom: 10px;
                animation: scaleIn 0.5s ease-out;
            }}
            @keyframes scaleIn {{
                0% {{ transform: scale(0); }}
                100% {{ transform: scale(1); }}
            }}
            h1 {{ color: #2e7d32; margin-top: 0; font-size: 1.8rem; }}
            p {{ color: #666; font-size: 1.1rem; }}
            .details {{
                background: #f9f9f9;
                padding: 20px;
                border-radius: 12px;
                margin: 25px 0;
                text-align: left;
                border-left: 6px solid #4caf50;
            }}
            .details div {{
                margin-bottom: 8px;
                font-size: 1rem;
                color: #333;
            }}
            .btn {{
                display: inline-block;
                padding: 15px 35px;
                background: #4caf50;
                color: white;
                text-decoration: none;
                border-radius: 30px;
                font-weight: bold;
                font-size: 1.1rem;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
            }}
            .btn:hover {{
                background: #45a049;
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="checkmark">✔</div>
            <h1>Registration Complete!</h1>
            <p>Thank you for choosing NIS. We've saved your details:</p>
            <div class="details">
                <div><strong>Student:</strong> {name}</div>
                <div><strong>Standard:</strong> {standard}</div>
                <div><strong>DOB:</strong> {dob}</div>
            </div>
            <a href="/" class="btn">Return to School Portal</a>
        </div>
    </body>
    </html>
    """

@app.route('/<path:filename>')
def serve_any_page(filename):
    try:
        return render_template(filename)
    except:
        return "404 Not Found", 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
