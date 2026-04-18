from flask import Flask, render_template, request
import os
import requests

# Tells Flask to look for HTML files in the main folder
app = Flask(__name__, template_folder='.')

# Paste your Google Script URL here
SHEET_URL = "https://script.google.com/macros/s/AKfycbxIVfJjFmot2_7fdMOytLfEkGtscJ8zjD3iZedK8C5POY0c1OX2C7BvMvSrtChc-uK1/exec"

# 1. HOME PAGE
@app.route('/')
def index():
    return render_template('Nis1index.html')

# 2. REGISTRATION FORM PAGE
@app.route('/register')
def register():
    return render_template('Nis1register.html')

# 3. SUBMISSION LOGIC (Sends to Google Sheets)
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('username')
    standard = request.form.get('standard')
    gender = request.form.get('gender')
    mobile = request.form.get('parent_mobile')
    address = request.form.get('address')
    
    # Print to Render Logs for you to see
    print("\n" + "⭐"*20)
    print(f" NEW REGISTRATION: {name}")
    print(f" CLASS: {standard}")
    print("⭐"*20 + "\n")

    # Send data to your Google Sheet
    payload = {
        "name": name,
        "standard": standard,
        "gender": gender,
        "mobile": mobile,
        "address": address
    }
    
    try:
        requests.post(SHEET_URL, json=payload, timeout=10)
    except Exception as e:
        print(f"Sheet Error: {e}")

    return f"""
    <div style="text-align:center; padding:50px; font-family:sans-serif;">
        <h1 style="color:#2ecc71;">Registration Received!</h1>
        <p>Thank you <b>{name}</b>. Your details are saved in the school database.</p>
        <a href="/" style="text-decoration:none; color:white; background:#3498db; padding:10px 20px; border-radius:5px;">Return to Home</a>
    </div>
    """

# 4. THE SMART CATCH-ALL (Fixes the "Not Found" error)
@app.route('/<path:filename>')
def serve_any_page(filename):
    if filename == 'favicon.ico':
        return '', 204
    
    # This looks for the file exactly as named in your GitHub folder
    try:
        return render_template(filename)
    except Exception as e:
        print(f"❌ File Not Found: {filename}")
        return f"<h1>404: {filename} Not Found</h1><p>Check if the filename matches GitHub exactly!</p>", 404

if __name__ == '__main__':
    # Detects the Port automatically for Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
