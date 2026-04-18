from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__, template_folder='.')

# Use your LATEST Google Script URL here
SHEET_URL = "https://script.google.com/macros/s/AKfycbxIVfJjFmot2_7fdMOytLfEkGtscJ8zjD3iZedK8C5POY0c1OX2C7BvMvSrtChc-uK1/exec"

@app.route('/')
def index():
    return render_template('Nis1index.html')

@app.route('/register')
def register():
    return render_template('Nis1register.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Capture all form data including the NEW DOB
    name = request.form.get('username')
    dob = request.form.get('dob')
    standard = request.form.get('standard')
    gender = request.form.get('gender')
    mobile = request.form.get('parent_mobile')
    address = request.form.get('address')
    
    # Updated Logs to show DOB
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

    return f"<h1>Success!</h1><p>Registration for {name} (DOB: {dob}) received.</p><a href='/'>Go Home</a>"

@app.route('/<path:filename>')
def serve_any_page(filename):
    try:
        return render_template(filename)
    except:
        return "404 Not Found", 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
