from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
import openai
import os
from langchain_groq import ChatGroq
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from typing import List
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app)

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(temperature=0, model="mixtral-8x7b-32768")


class ItineraryItem(BaseModel):
    title: str = Field(description="Title of the activity")
    description: str = Field(description="Description of the activity")
    location: str = Field(description="Location of the activity")
    begin: str = Field(description="Start time of the activity")
    end: str = Field(description="End time of the activity")
    cost: float = Field(description="Cost of the activity (USD)")
    carbon_footprint: float = Field(
        description="Carbon footprint of the activity (kg CO2e)"
    )
    transportation_method: str = Field(
        description="Method of transportation to the next activity"
    )
    distance: float = Field(description="Distance traveled for the activity (miles)")
    transportation_emissions: float = Field(
        description="Estimated CO2 emissions from transportation (kg CO2e)"
    )
    travel_time_to_next: str = Field(
        description="Total travel time to the next destination"
    )
    transportation_cost_to_next: float = Field(
        description="Total travel cost to the next destination (USD)"
    )


class DayItinerary(BaseModel):
    date: str = Field(description="Date of the itinerary")
    activities: List[ItineraryItem] = Field(description="List of activities")

class Itinerary(BaseModel):
    days: List[DayItinerary] = Field(description="Daily itinerary")


def get_travel_recommendation_stream(location, budget, interests, start_date, end_date):
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    num_days = (end_date_obj - start_date_obj).days + 1

    prompt = ChatPromptTemplate.from_template(
        """Create a detailed and sustainable itinerary for a {num_days}-day trip to {location} from {start_date} to {end_date} with a total budget of {budget} dollars.
    The traveler is interested in {interests}.
    Plan for multiple activities each day, starting at 9 am and ending at 10 pm. Include breakfast, lunch, and dinner each day.
    Consider transportation time between activities and suggest eco-friendly options.
    Provide a variety of activities across all days, avoiding repetition.
    Ensure each day has a unique set of activities that showcase different aspects of {location}.
    Provide detailed information for each activity as specified in the ItineraryItem model.
    The itinerary should cover all {num_days} days of the trip.

    Follow this verbage for your trip descriptions:

    "description": "Take a hike up Grizzly Peak for stunning views of the Bay Area. This eco-friendly activity is perfect for nature lovers."
    "description": "End your day with a delicious vegan dinner at Souley Vegan, a restaurant known for its plant-based soul food and commitment to sustainability."
    "description": "Enjoy a peaceful evening stroll at the Berkeley Marina, taking in the beautiful sunset views over the bay."
    "description": "Start your day with a unique breakfast experience at Cheeseboard Collective, a worker-owned cooperative bakery known for its fresh and organic baked goods."
    "description": "Explore the beautiful Berkeley Rose Garden, a historic landmark featuring over 1,500 rose bushes and stunning views of the Golden Gate Bridge."
    "description": "Engage with interactive exhibits and learn about science, technology, and the environment at the Lawrence Hall of Science."

    Format the output as a valid JSON object representing the Itinerary model."""
    )

    chain = prompt | llm

    return chain.stream(
        {
            "num_days": num_days,
            "location": location,
            "budget": budget,
            "interests": interests,
            "start_date": start_date,
            "end_date": end_date,
        }
    )


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

    if not all([location, budget, interests, start_date, end_date]):
        return (
            jsonify(
                {
                    "error": "Please provide all required fields: location, budget, interests, start_date, end_date"
                }
            ),
            400,
        )

    if start_date_obj > end_date_obj:
        return jsonify({"error": "start_date must be before end_date"}), 400

    def generate():
        for chunk in get_travel_recommendation_stream(
            location, budget, interests, start_date, end_date
        ):
            yield f"data: {json.dumps(chunk.content)}\n\n"

    return Response(generate(), content_type="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)
