from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>🎉 Your PM Assistant is working!</h1><p>Flask is running successfully</p>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
