from flask import Flask, request, jsonify
import openai
import os
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Dict

app = Flask(__name__)

# Set your OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define the model
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

class ItineraryItem(BaseModel):
    begin: str = Field(description="The start time of the activity")
    end: str = Field(description="The end time of the activity")
    location: str = Field(description="The location of the activity")
    description: str = Field(description="A description of the activity")

class DayItinerary(BaseModel):
    day: int = Field(description="Day number of the itinerary")
    activities: List[ItineraryItem] = Field(description="List of activities for the day")

class Itinerary(BaseModel):
    itinerary: List[DayItinerary] = Field(description="Day by day itinerary")

structured_llm = llm.with_structured_output(Itinerary)

def get_travel_recommendation(location, budget, duration):
    prompt = f"Create a detailed itinerary for a trip to {location} for {duration} days with a budget of {budget} dollars. Each event should include the time range, a detailed location address suitable for Google Maps, and a description. The itinerary should be structured day by day, with each day containing a list of events, in the format: {{'day': day_number, 'activities': [{{'begin': 'start_time', 'end': 'end_time', 'location': 'full_address', 'description': 'activity description'}}]}}."
    result = structured_llm.invoke(prompt)
    return result.dict()

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
        'itinerary': recommendation['itinerary']
    })

if __name__ == '__main__':
    app.run(debug=True)
