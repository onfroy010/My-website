from flask import Flask, request
import os

app = Flask(__name__)

STYLE = """
<style>
body { font-family: Arial; background: #f0f2f5; text-align: center; padding-top: 50px; }
.box { background: white; width: 300px; margin: auto; padding: 30px; border-radius: 15px; box-shadow: 0 0 15px #ccc; }
input { width: 90%; padding: 10px; margin: 8px 0; border-radius: 8px; border: 1px solid #ccc; }
button { background: #1877f2; color: white; padding: 12px 20px; border: none; border-radius: 8px; width: 95%; font-size: 16px; }
a { color: #1877f2; text-decoration: none; }
</style>
"""

@app.route('/')
def home():
    return STYLE + '''
    <div class="box">
    <h2>Welcome to My Website</h2>
    <p>Your first Flask App - Now Live!</p>
    <a href="/login">Login</a> | <a href="/all-logins">See All Logins</a>
    </div>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        with open('logins.txt', 'a') as f:
            f.write(f"Username: {username} | Password: {password}\n")
        return STYLE + f"<div class='box'><h3>Hello {username}!</h3><p>Saved.</p><a href='/all-logins'>See All Logins</a></div>"
    return STYLE + '''
    <div class="box">
    <h2>Login</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Username"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <button type="submit">Login</button>
    </form>
    </div>
    '''

@app.route('/all-logins')
def all_logins():
    try:
        with open('logins.txt') as f:
            data = f.read()
    except:
        data = "No logins yet"
    return STYLE + f"<div class='box'><h2>All Logins</h2><pre>{data}</pre><a href='/'>Home</a></div>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
