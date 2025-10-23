from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Flask 서버가 정상적으로 작동 중입니다!"

if __name__ == '__main__':
    app.run(debug=True)

print()