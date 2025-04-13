from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


system_prompts = """
You are a assistant who give weather based responses to use and nothing else than weather

example:
  user-query : Can I go outside and play 
  responce - if temparture is belove 30 than allow him other wise do not

  user-query : what is life ?
  response : please ask weaher related query 

"""

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    city = data.get('city', 'Unknown')
    temperature = 34  # Replace with live data if needed
    weather_report = f"The temperature in {city} is {temperature}°C with clear skies."
    return jsonify({'weather': weather_report})


@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.get_json()
    weather = data.get("weather", "")
    question = data.get("question", "")

    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompts},
                {"role": "system", "content": "You are a helpful assistant who gives weather-based suggestions."},
                {"role": "user", "content": f"The current weather is: {weather}"},
                {"role": "user", "content": question}
            ]
        )
        reply = completion.choices[0].message.content.strip()
        return jsonify({'answer': reply})
    except Exception as e:
        print(f"AI error: {e}")
        return jsonify({'answer': 'Error getting AI response.'}), 500


if __name__ == '__main__':
    app.run(debug=True)