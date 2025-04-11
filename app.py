from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

# Function to calculate real size
def calculate_real_size(microscope_size, magnification_factor):
    return microscope_size / magnification_factor

@app.route('/', methods=['GET', 'POST'])
def index():
    real_size = None
    if request.method == 'POST':
        username = request.form['username']
        microscope_size = float(request.form['microscope_size'])
        magnification_factor = float(request.form['magnification_factor'])

        real_size = calculate_real_size(microscope_size, magnification_factor)

        # Save to database
        conn = sqlite3.connect('specimens.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS specimen_data (
                            username TEXT,
                            microscope_size REAL,
                            magnification_factor REAL,
                            real_size REAL)''')
        cursor.execute('''INSERT INTO specimen_data (username, microscope_size, magnification_factor, real_size)
                          VALUES (?, ?, ?, ?)''',
                       (username, microscope_size, magnification_factor, real_size))
        conn.commit()
        conn.close()

    return render_template('index.html', real_size=real_size)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

