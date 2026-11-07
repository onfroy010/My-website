from flask import Flask, request, redirect, session, render_template_string
import sqlite3, os

app = Flask(__name__)
app.secret_key = "change-this-to-something-secret-123"

# Create database
def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
    conn.commit()
    conn.close()
init_db()

STYLE = """
<style>
body{font-family:Arial;text-align:center;padding:20px;background:#f5f5f5}
h1{font-size:50px}
input{font-size:22px;padding:12px;margin:8px;width:90%;max-width:350px;display:block;margin-left:auto;margin-right:auto}
button{font-size:22px;padding:12px 25px;background:black;color:white;border:none;border-radius:8px}
a{font-size:20px;display:block;margin-top:15px}
.box{background:white;padding:25px;border-radius:12px;max-width:450px;margin:auto}
</style>
"""

@app.route('/')
def home():
    if 'user' in session:
        return f"<html><head>{STYLE}</head><body><div class='box'><h1>Welcome {session['user']}!</h1><p style='font-size:24px'>You are logged in.</p><a href='/logout'>Logout</a><a href='/admin'>View Users</a></div></body></html>"
    return f"<html><head>{STYLE}</head><body><div class='box'><h1>My Website</h1><p style='font-size:24px'>Please login or sign up</p><a href='/login'>Login</a><a href='/signup'>Sign Up</a></div></body></html>"

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']  # PLAIN TEXT NOW - saved as-is
        try:
            conn = sqlite3.connect("users.db")
            conn.execute("INSERT INTO users (username, password) VALUES (?,?)", (u,p))
            conn.commit(); conn.close()
            return redirect('/login')
        except:
            return f"<html><head>{STYLE}</head><body><div class='box'><h1>Username taken!</h1><a href='/signup'>Try again</a></div></body></html>"
    return f"<html><head>{STYLE}</head><body><div class='box'><h1>Sign Up</h1><form method='POST'><input name='username' placeholder='Username' required><input name='password' type='password' placeholder='Password' required><button>Create Account</button></form><a href='/login'>Already have account? Login</a></div></body></html>"

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        conn = sqlite3.connect("users.db")
        row = conn.execute("SELECT password FROM users WHERE username=?", (u,)).fetchone()
        conn.close()
        if row and row[0] == request.form['password']:  # PLAIN TEXT CHECK
            session['user'] = u
            return redirect('/')
        return f"<html><head>{STYLE}</head><body><div class='box'><h1>Wrong login!</h1><a href='/login'>Try again</a></div></body></html>"
    return f"<html><head>{STYLE}</head><body><div class='box'><h1>Login</h1><form method='POST'><input name='username' placeholder='Username' required><input name='password' type='password' placeholder='Password' required><button>Login</button></form><a href='/signup'>No account? Sign Up</a></div></body></html>"

@app.route('/admin')
def admin():
    conn = sqlite3.connect("users.db")
    users = conn.execute("SELECT username FROM users").fetchall()
    conn.close()
    names = "<br>".join([f"<p style='font-size:24px'>{u[0]}</p>" for u in users]) or "<p>No users yet</p>"
    return f"<html><head>{STYLE}</head><body><div class='box'><h1>All Users</h1><p>This shows USERNAMES ONLY</p>{names}<a href='/'>Home</a></div></body></html>"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run()
