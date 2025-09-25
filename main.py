from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import database_manager as dbHandler
import hashlib

app = Flask(__name__)
app.secret_key = "super-secret-key"  # required for sessions

# ----------------------
# HELPERS
# ----------------------
def hash_password(password):
    """Return SHA256 hash of the password."""
    return hashlib.sha256(password.encode()).hexdigest()

# ----------------------
# ROUTES
# ----------------------
@app.route('/')
@app.route('/index.html')
def index():
    """Home page (only for logged in users)."""
    if "user_id" not in session:
        return redirect(url_for('login'))
    data = dbHandler.listExtension()
    return render_template('index.html', content=data)

@app.route('/login', methods=['GET','POST'])
def login():
    """Login page and form handling."""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = hash_password(data.get('password'))

        user = dbHandler.check_user(email, password)
        if user:
            session["user_id"] = user["email"]
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'})
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    """Handle signup form submission."""
    data = request.get_json()
    first_name = data.get('name')
    last_name = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([first_name, last_name, email, password]):
        return jsonify({'success': False, 'message': 'All fields are required'})

    conn = dbHandler.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE email = ?", (email,))
    if cur.fetchone():
        conn.close()
        return jsonify({'success': False, 'message': 'Email already registered'})

    cur.execute(
        "INSERT INTO user (first_name, last_name, email, password) VALUES (?, ?, ?, ?)",
        (first_name, last_name, email, hash_password(password))
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/logout')
def logout():
    """Logout user and clear session."""
    session.pop("user_id", None)
    return redirect(url_for('login'))

# ----------------------
# START SERVER
# ----------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5100)
