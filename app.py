from flask import Flask, render_template, request, jsonify # Added jsonify
import os
import requests
import google.generativeai as genai # 1. Import Gemini

app = Flask(__name__, template_folder='.')

# --- CONFIGURATION ---
# 2. Setup Gemini API Key (Make sure this is set in your Render environment variables!)
genai.configure(api_key=os.environ.get("AIzaSyBoagfRrlDlxS99mBmK2JqvJS9dPlewDnQ"))
model = genai.GenerativeModel('gemini-1.5-flash')

SHEET_URL = "https://script.google.com/macros/s/AKfycbzdGbEUMgw28ySotKoT-opBMsfckz5rljJOEp58ow5z_s1TZPafVCytDPQb1EVpPTUb/exec"

@app.route('/')
def index():
    return render_template('Nis1index.html')

# --- AI ROUTE (The missing piece!) ---
@app.route('/ask-ai', methods=['POST'])
def ask_ai():
    data = request.get_json()
    user_message = data.get("message")
    
    try:
        # We give the AI a "Persona" so it knows it's the NIS assistant
        prompt = f"You are the Nilmadhav International School (NIS) assistant. Answer this: {user_message}"
        response = model.generate_content(prompt)
        return jsonify({"answer": response.text})
    except Exception as e:
        print(f"AI Error: {e}")
        return jsonify({"answer": "I'm having trouble connecting to my brain. Try again later!"}), 500

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
    # ... (Your existing submit logic remains the same)
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

    # (Your success HTML string goes here...)
    return f"Registration Complete! Student: {name}" 

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
