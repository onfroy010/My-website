from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: white;
                text-align: center;
                font-family: Arial, sans-serif;
            }
            h1 {
                font-size: 80px;
                line-height: 1.1;
                margin: 0;
            }
            p {
                font-size: 32px;
            }
        </style>
    </head>
    <body>
        <div>
            <h1>Hello World!</h1>
            <p>My Website Is Live</p>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run()
