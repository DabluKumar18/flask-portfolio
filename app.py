from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__, static_folder="static")
app.secret_key = "supersecretkey"

# ---------- DATABASE CONNECTION ----------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",        # ya cloud host
        user="root",             # db user
        password="123456789",     # db password
        database="portfolio_db"
    )

# ---------- CREATE TABLE ----------
def create_table():
    conn = get_db_connection() 
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(20),
            message VARCHAR(500)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE,
            password VARCHAR(255)
        )
    """)

    cursor.execute("SELECT * FROM admin")
    admin = cursor.fetchone()

    if not admin:
        hashed_password = generate_password_hash("admin123")
        cursor.execute(
            "INSERT INTO admin (username, password) VALUES (%s, %s)",
            ("admin", hashed_password)
        )

    conn.commit()
    cursor.close()
    conn.close()

# ---------- HOME ----------
@app.route('/')
def home():
    return render_template('index.html')

# ---------- CONTACT API ----------
@app.route('/api/contact', methods=['POST'])
def contact_api():
    data = request.json

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
    "INSERT INTO contact (name, email, phone, message) VALUES (%s, %s, %s, %s)",
    (name, email, phone, message)
)

    conn.commit()
    cursor.close()
    conn.close()


    return jsonify({
        "status": "success",
        "message": "Message saved successfully"
    })

# ---------- ADMIN API (VIEW DATA) ----------
@app.route('/api/messages')
def view_messages():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, name, email, phone, message
        FROM contact
        ORDER BY id DESC
    """)

    messages = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(messages)


# ---------- ADMIN PANEL ----------
@app.route('/admin')
def admin_panel():
    if not session.get('admin'):
        return redirect('/login')
    return render_template('admin.html')

# ---------- About Page ----------
@app.route('/about')
def about():
    return render_template('index.html')

# ---------- Education PAGE ----------
@app.route('/education')
def education():
    return render_template('index.html')

# ---------- Projects Page ----------
@app.route('/projects')
def projects():
    return render_template('index.html')

# ---------- Resume Page ----------
@app.route('/resume')
def resume():
    return render_template('index.html')

# ---------- Certifications PAGE ----------
@app.route('/certifications')
def certifications():
    return render_template('index.html')

    

#---------- CONTACT PAGE ----------
@app.route('/contact')
def contact():
    return render_template('index.html')

# ---------- DELETE MESSAGE ----------
@app.route('/delete/<int:id>')
def delete_message(id):
    # 🔐 security: sirf admin hi delete kar sake
    if not session.get('admin'):
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contact WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/admin')

# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM admin WHERE username=%s", (username,))
        admin = cursor.fetchone()

        cursor.close()
        conn.close()

        if admin and check_password_hash(admin["password"], password):
            session['admin'] = True
            return redirect('/admin')
        else:
            return "Invalid Login"

    return render_template('login.html')

# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/login')

# ---------- RUN ----------
if __name__ == '__main__':
    create_table()
    app.run(debug=True)

