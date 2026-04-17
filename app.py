from flask import Flask, render_template, request
import os

# Flask looks for HTML files in the same folder
app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('Nis1index.html')

@app.route('/register')
def register():
    return render_template('Nis1register.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('username')
    standard = request.form.get('standard')
    gender = request.form.get('gender')
    mobile = request.form.get('parent_mobile')
    address = request.form.get('address')
    
    # This shows the data in your RENDER LOGS and your VS CODE terminal
    print("\n" + "⭐"*20)
    print(f" NEW REGISTRATION: {name}")
    print(f" CLASS:   {standard}")
    print(f" GENDER:  {gender}")
    print(f" MOB:     {mobile}")
    print(f" ADDRESS: {address}")
    print("⭐"*20 + "\n")
    
    # Save to file (registrations.txt)
    with open("registrations.txt", "a") as f:
        f.write(f"NAME: {name} | CLASS: {standard} | ADDRESS: {address} | MOB: {mobile}\n")
    
    return f"""
    <div style="text-align:center; padding:50px; font-family:sans-serif; background-color:#f4f4f4;">
        <h1 style="color:#2ecc71;">Registration Received!</h1>
        <p>Thank you <b>{name}</b>, your details for Class {standard} are saved.</p>
        <hr style="width:50%; margin:20px auto;">
        <a href="/" style="text-decoration:none; color:white; background:#3498db; padding:10px 20px; border-radius:5px;">Return to Home</a>
    </div>
    """

@app.route('/view-my-data-123')
def view_data():
    try:
        with open("registrations.txt", "r") as f:
            content = f.read()
        return f"<h2>School Registration List</h2><pre>{content}</pre>"
    except FileNotFoundError:
        return "<h2>No registrations found yet.</h2>"

@app.route('/<path:filename>')
def serve_any_page(filename):
    if filename == 'favicon.ico':
        return '', 204
    try:
        return render_template(filename)
    except:
        return f"<h1>404: {filename} Not Found</h1>", 404

if __name__ == '__main__':
    # This line detects if it's on Render (PORT) or your PC (5000)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
