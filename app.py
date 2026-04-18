from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__, template_folder='.')

# Your Google Script Web App URL
SHEET_URL = "https://script.google.com/macros/s/AKfycbxIVfJjFmot2_7fdMOytLfEkGtscJ8zjD3iZedK8C5POY0c1OX2C7BvMvSrtChc-uK1/exec"

@app.route('/')
def index():
    return render_template('Nis1index.html')

@app.route('/register')
def register():
    return render_template('Nis1register.html')

@app.route('/submit', methods=['POST'])
def submit():
    # 1. Collect Data from Form
    name = request.form.get('username')
    standard = request.form.get('standard')
    gender = request.form.get('gender')
    mobile = request.form.get('parent_mobile')
    address = request.form.get('address')
    
    # 2. FULL INFO PRINT (This shows up in your Stars Logs)
    print("\n" + "⭐"*30)
    print(f" NEW REGISTRATION RECEIVED ")
    print(f" NAME:    {name}")
    print(f" CLASS:   {standard}")
    print(f" GENDER:  {gender}")
    print(f" MOBILE:  {mobile}")
    print(f" ADDRESS: {address}")
    print("⭐"*30 + "\n")

    # 3. Send to Google Sheets
    payload = {
        "name": name,
        "standard": standard,
        "gender": gender,
        "mobile": mobile,
        "address": address
    }
    
    try:
        response = requests.post(SHEET_URL, json=payload, timeout=10)
        print(f"✅ Google Sheets Sync Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Google Sheets Error: {e}")

    # 4. Success Screen
    return f"""
    <div style="text-align:center; padding:50px; font-family:sans-serif; background-color:#f4f4f4; min-height:100vh;">
        <h1 style="color:#2ecc71;">Registration Successful!</h1>
        <p style="font-size:1.2rem;">Thank you <b>{name}</b>. Your data is now in the school database.</p>
        <hr style="width:50%; margin:20px auto; border: 1px solid #ddd;">
        <a href="/" style="text-decoration:none; color:white; background:#3498db; padding:12px 25px; border-radius:8px; font-weight:bold;">Return to Home</a>
    </div>
    """

# Catch-all for other HTML files
@app.route('/<path:filename>')
def serve_any_page(filename):
    if filename == 'favicon.ico':
        return '', 204
    try:
        return render_template(filename)
    except:
        return f"<h1>404: {filename} Not Found</h1>", 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
