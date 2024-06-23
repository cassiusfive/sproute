from flask import Flask, request, jsonify
import openai
import os
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
from datetime import datetime

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
    cost: float = Field(description="The cost of the activity in dollars")
    distance: float = Field(description="The distance traveled for the activity in km")
    co2_emissions: float = Field(description="The estimated CO2 emissions of the activity in kg")

class DayItinerary(BaseModel):
    date: str = Field(description="Date of the itinerary")
    activities: List[ItineraryItem] = Field(description="List of activities for the day")

class Itinerary(BaseModel):
    itinerary: List[DayItinerary] = Field(description="Day by day itinerary")

structured_llm = llm.with_structured_output(Itinerary)

def get_emission_factor(vehicle_type):
    emission_factors = {
        "car": 0.121,
        "bus": 0.028,
        "train": 0.041,
        "airplane": 0.150
    }
    return emission_factors.get(vehicle_type.lower(), 0)

def calculate_co2_emissions(vehicle_type, group_size, distance):
    emission_factor = get_emission_factor(vehicle_type)
    total_emissions = emission_factor * distance * group_size
    return total_emissions

def get_travel_recommendation(location, budget, interests, start_date, end_date, vehicle_type, group_size):
    prompt = (f"Create a detailed itinerary for a trip to {location} from {start_date} to {end_date} with a budget of {budget} dollars who is interested in {interests}. "
              "Each event should include the time range, a detailed location address suitable for Google Maps, a description, the cost of the activity, and the total distance to be traveled. "
              "Plan for multiple activities each day, totaling around 8-10 hours of activities per day. "
              "Suggest the most eco-friendly activities possible. "
              "The itinerary should be structured day by day, with each day containing a list of events, in the format: "
              "{'date': 'YYYY-MM-DD', 'activities': [{'begin': 'start_time', 'end': 'end_time', 'location': 'full_address', 'description': 'activity description', 'cost': activity_cost, 'distance': total_distance_in_km}]}.")

    result = structured_llm.invoke(prompt).dict()
    
    # Calculate CO2 emissions for each activity
    for day in result['itinerary']:
        for activity in day['activities']:
            distance = activity.get('distance', 0)  # Ensure distance is obtained correctly
            activity['co2_emissions'] = calculate_co2_emissions(vehicle_type, group_size, distance)

    return result

@app.route('/')
def home():
    return "Welcome to the Eco-Friendly Travel App!"

@app.route('/travel', methods=['POST'])
def travel():
    data = request.json
    location = data.get('location')
    budget = data.get('budget')
    interests = data.get('interests')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    vehicle_type = data.get('vehicle_type')
    group_size = data.get('group_size')

    # Validate the inputs
    try:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    if not location or not budget or not start_date or not end_date or not vehicle_type or not group_size:
        return jsonify({
            'error': 'Please provide location, budget, interests, start_date, end_date, vehicle_type, and group_size'
        }), 400

    if start_date_obj > end_date_obj:
        return jsonify({'error': 'start_date must be before end_date'}), 400

    recommendation = get_travel_recommendation(location, budget, interests, start_date, end_date, vehicle_type, group_size)

    return jsonify({
        'location': location,
        'budget': budget,
        'interests': interests,
        'start_date': start_date,
        'end_date': end_date,
        'itinerary': recommendation['itinerary']
    })

if __name__ == '__main__':
    app.run(debug=True)
