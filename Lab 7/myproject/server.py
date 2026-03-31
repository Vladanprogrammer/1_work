from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Головна сторінка</h1><p>Перейдіть на адресу <a href='/joke'>/joke</a>, щоб побачити результат попереднього завдання.</p>"

@app.route('/joke')
def joke_page():
    # Логіка з попереднього завдання для отримання жарту
    url = "https://v2.jokeapi.dev/joke/Programming?type=single"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            joke_text = response.json().get("joke", "Жарт десь загубився :(")
            
            # Повертаємо результат як просту HTML-сторінку
            return f"<h2>Випадковий IT-жарт:</h2><p style='font-size: 20px; color: blue;'>{joke_text}</p>"
        else:
            return "<h2>Помилка: сервер не відповідає.</h2>"
            
    except Exception as e:
        return f"<h2>Щось пішло не так: {e}</h2>"

if __name__ == '__main__':
    app.run(debug=True)