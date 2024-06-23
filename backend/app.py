from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
import openai
import os
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the model
llm = ChatOpenAI(model="gpt-4o")

class ItineraryItem(BaseModel):
    begin: str = Field(description="The start time of the activity")
    end: str = Field(description="The end time of the activity")
    location: str = Field(description="The location of the activity")
    title: str = Field(description="A description of the activity")
    description: str = Field(description="A detailed longer description of the activity")
    cost: float = Field(description="The cost of the activity in dollars")
    carbon: float = Field(description="The carbon footprint of the activity in kg")
    mode: str = Field(description="Mode of transportation between previous activity and this activity")
    distance: float = Field(description="The distance traveled for the activity in mi")
    emissions: float = Field(description="The estimated CO2 emissions of transportation in kg")
    transportation_time_from_prev_to_here: str = Field(description="The total time of transportation between last activity and this activity")
    transportation_cost_from_prev_to_here: float = Field(description="The total cost of transportation between last activity and this activity")

class DayItinerary(BaseModel):
    date: str = Field(description="Date of the itinerary")
    activities: List[ItineraryItem] = Field(description="List of activities for the day")

class Itinerary(BaseModel):
    itinerary: List[DayItinerary] = Field(description="Day by day itinerary")

structured_llm = llm.with_structured_output(Itinerary)

def get_emission_factor(vehicle_type):
    emission_factors = {"car": 0.121, "bus": 0.028, "train": 0.041, "airplane": 0.150}
    return emission_factors.get(vehicle_type.lower(), 0)

def calculate_co2_emissions(vehicle_type, group_size, distance):
    emission_factor = get_emission_factor(vehicle_type)
    total_emissions = emission_factor * distance * group_size
    return total_emissions

def get_travel_recommendation(location, budget, interests, start_date, end_date):
    prompt = (
        f"Create a detailed and sustainable itinerary for a trip to {location} from {start_date} to {end_date} with a budget of {budget} dollars. "
        f"The traveler is interested in {interests}. "
        "Each event should include: "
        "- Time range (start_time - end_time) "
        "- Detailed location address suitable for Google Maps "
        "- Title of activity"
        "- Enticing description of the activity "
        "- Cost of the activity "
        "- carbon footprint from the activity "
        "- most sustainable mode of transportation to get there from the previous activity while also being realistic "
        "- time of transportation to get there using that mode "
        "- distance between this activity and previous activity "
        "- transportation cost from previous activity to this one "
        "- emissions from the trip to the activity from the previous activity "
        "Plan for multiple activities each day, starting at 9 am and ending at 10 pm, make sure each day has a breakfast, lunch and dinner. Make sure you take into consideration the time of transportation when giving the start date of the event by making sure to leave a buffer. "
        "Suggest the most eco-friendly activities possible. "
        "The itinerary should be structured day by day, with each day containing a list of event in the following format: "
        "{'date': 'YYYY-MM-DD', 'activities': [\n"
        "    {\n"
        "        'mode': 'mode of transportation',\n"
        "        'distance': 'total_distance_in_km',\n"
        "        'emissions': 'transportation emissions',\n"
        "        'transportation_time_from_prev_to_here': 'duration of travel time between previous activity to this activity',\n"
        "        'transportation_cost_from_prev_to_here': 'transportation cost from previous activity to here',\n"
        "        'begin': 'start_time',\n"
        "        'end': 'end_time',\n"
        "        'location': 'full_address',\n"
        "        'title': 'title of activity',\n"
        "        'description': 'detailed activity description',\n"
        "        'cost': 'activity cost',\n"
        "        'carbon': 'carbon footprint'\n"
        "    }\n"
        "]}"
    )

    return structured_llm.stream(prompt)

@app.route("/")
def home():
    return "Welcome to the Eco-Friendly Travel App!"

@app.route("/travel", methods=["POST"])
def travel():
    data = request.json
    location = data.get("location")
    budget = data.get("budget")
    interests = data.get("interests")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    # Validate the inputs
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    if not location or not budget or not start_date or not end_date:
        return (
            jsonify(
                {
                    "error": "Please provide location, budget, interests, start_date, and end_date"
                }
            ),
            400,
        )

    if start_date_obj > end_date_obj:
        return jsonify({"error": "start_date must be before end_date"}), 400

    def generate():
        for chunk in get_travel_recommendation(location, budget, interests, start_date, end_date):
            yield f"data: {chunk}\n\n"

    return Response(generate(), content_type="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)
