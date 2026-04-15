from flask import Flask, render_template, request
import os

# Setting template_folder to '.' tells Flask to look in the same folder as app.py
app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    # Serves the registration page as the home route
    return render_template('Nis1register.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Extracting data using the 'name' attributes from your HTML form
    student_name = request.form.get('username')
    standard = request.form.get('standard')
    gender = request.form.get('gender')
    parent_mobile = request.form.get('parent_mobile')
    address = request.form.get('address')
    
    # Printing the entries to the terminal (or Render logs)
    print(f"\n--- New Registration Received ---")
    print(f"Name:    {student_name}")
    print(f"Class:   {standard}")
    print(f"Gender:  {gender}")
    print(f"Mobile:  {parent_mobile}")
    print(f"Address: {address}")
    print(f"---------------------------------\n")
    
    return f"<h1>Thank you, {student_name}!</h1><p>Registration received for Standard {standard}.</p>"

if __name__ == '__main__':
    # This logic allows the app to run locally OR on Render automatically
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)