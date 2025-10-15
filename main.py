from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import database_manager as dbHandler
import hashlib
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "super-secret-key"

# ----------------------
# Profile Pic Upload Config
# ----------------------
UPLOAD_FOLDER = 'static/images/profiles'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ----------------------
# ROUTES
# ----------------------
@app.route('/')
@app.route('/index.html')
def index():
    if "user_id" not in session:
        return redirect(url_for('login'))

    conn = dbHandler.get_connection()
    cur = conn.cursor()

    # Get posts
    cur.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = [dict(row) for row in cur.fetchall()]

    # Attach likes + comments
    for post in posts:
        cur.execute("SELECT COUNT(*) as like_count FROM likes WHERE post_id = ?", (post["id"],))
        post["like_count"] = cur.fetchone()["like_count"]

        cur.execute("SELECT * FROM comments WHERE post_id = ? ORDER BY created_at ASC", (post["id"],))
        post["comments"] = [dict(c) for c in cur.fetchall()]

    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/games')
def games():
    if "user_id" not in session:
        return redirect(url_for('login'))
    return render_template('games.html')

@app.route('/players')
def players():
    if "user_id" not in session:
        return redirect(url_for('login'))
    return render_template('players.html')

@app.route('/profile')
def profile():
    if "user_id" not in session:
        return redirect(url_for('login'))

    user_email = session["user_id"]
    # Fetch user info including profile_pic
    user = dbHandler.get_user_by_email(user_email)  # Should return dict with keys: first_name, last_name, email, gender, profile_pic
    if not user:
        return redirect(url_for('logout'))

    return render_template('profile.html', user=user)

@app.route('/upload_profile_pic', methods=['GET', 'POST'])
def upload_profile_pic():
    if "user_id" not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            # Update user in DB
            conn = dbHandler.get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE user SET profile_pic = ? WHERE email = ?", (f'images/profiles/{filename}', session["user_id"]))
            conn.commit()
            conn.close()

            return redirect(url_for('profile'))

    return '''
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file" accept="image/*" required>
      <button type="submit">Upload</button>
    </form>
    '''

@app.route('/login', methods=['GET','POST'])
def login():
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
    session.pop("user_id", None)
    return redirect(url_for('login'))

# ----------------------
# POSTS
# ----------------------
@app.route('/post', methods=['POST'])
def create_post():
    if "user_id" not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})

    data = request.get_json()
    content = data.get('content')

    if not content.strip():
        return jsonify({'success': False, 'message': 'Post cannot be empty'})

    conn = dbHandler.get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO posts (author, content) VALUES (?, ?)", (session["user_id"], content))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    conn = dbHandler.get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    cur.execute("DELETE FROM likes WHERE post_id = ?", (post_id,))
    cur.execute("DELETE FROM comments WHERE post_id = ?", (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    conn = dbHandler.get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO likes (post_id) VALUES (?)", (post_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/comment_post/<int:post_id>', methods=['POST'])
def comment_post(post_id):
    content = request.form.get("comment")
    if not content.strip():
        return redirect(url_for('index'))
    conn = dbHandler.get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO comments (post_id, content) VALUES (?, ?)", (post_id, content))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5100)
