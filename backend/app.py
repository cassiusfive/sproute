from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key (make sure to set your API key in the environment variables)
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_travel_recommendation(location, budget, duration):
    prompt = f"I am traveling to {location} with a budget of {budget} dollars for {duration} days. Can you suggest eco-friendly travel tips and destinations?"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

@app.route('/')
def home():
    return "Welcome to the Eco-Friendly Travel App!"

@app.route('/travel', methods=['POST'])
def travel():
    data = request.json
    location = data.get('location')
    budget = data.get('budget')
    duration = data.get('duration')

    if not location or not budget or not duration:
        return jsonify({
            'error': 'Please provide location, budget, and duration'
        }), 400

    recommendation = get_travel_recommendation(location, budget, duration)

    return jsonify({
        'location': location,
        'budget': budget,
        'duration': duration,
        'recommendation': recommendation
    })

if __name__ == '__main__':
    app.run(debug=True)
