from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Ssniper bot is running with new token."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)