from flask import Flask, request, jsonify
import os
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
from datetime import datetime, timedelta
from langchain_core.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain.chains import LLMChain

app = Flask(__name__)

# Set your OpenAI API key from environment variables
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


# Define the model
# llm = ChatOpenAI(model="gpt-3.5-turbo")
llm = ChatGroq(temperature=0, model="llama3-70b-8192")


class ItineraryItem(BaseModel):
    title: str = Field(description="Title of the activity")
    description: str = Field(description="Description of the activity")
    location: str = Field(description="Location of the activity")
    begin: str = Field(description="Start time of the activity")
    end: str = Field(description="End time of the activity")
    cost: float = Field(description="Cost of the activity (USD)")
    transportation_method: str = Field(
        description="Method of transportation to the next activity, if public transportation,  specify bus or train."
    )
    distance: float = Field(description="Distance traveled for the activity (miles)")
    transportation_emissions: float = Field(
        description="Estimated CO2 emissions from selected source of transportation (kg CO2e), result should be 0 if walking or biking and 0.03 kg for a 30 min bus ride."
    )
    travel_time_to_next: str = Field(
        description="Total travel time to from the previous destination to the next destination, do not underestimate, use the distance to find time of travel"
    )
    transportation_cost_to_next: float = Field(
        description="Total travel cost to the next destination (USD), if bike anticipate the bike rental cost. "
    )


class DayItinerary(BaseModel):
    date: str = Field(description="Date of the itinerary")
    activities: List[ItineraryItem] = Field(description="List of activities")


class Itinerary(BaseModel):
    days: List[DayItinerary] = Field(description="Daily itinerary")


structured_llm = llm.with_structured_output(Itinerary)


# def get_travel_recommendation(location, budget, interests, start_date, end_date):
#     start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
#     end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
#     num_days = (end_date_obj - start_date_obj).days + 1

#     prompt = f"""Create a detailed and sustainable itinerary for a {num_days}-day trip to {location} from {start_date} to {end_date} with a total budget of {budget} dollars.
#     The traveler is interested in {interests}.
#     Plan for multiple activities each day, starting at 9 am and ending at 10 pm. Include breakfast, lunch, and dinner each day.
#     Consider transportation time between activities and suggest eco-friendly options.
#     Provide a variety of activities across all days, avoiding repetition.
#     Ensure each day has a unique set of activities that showcase different aspects of {location}.
#     Provide detailed information for each activity as specified in the ItineraryItem model.
#     The itinerary should cover all {num_days} days of the trip.


#     follow this verbage for your trip descriptions:

#     "description": "Take a hike up Grizzly Peak for stunning views of the Bay Area. This eco-friendly activity is perfect for nature lovers.
#     "description": "End your day with a delicious vegan dinner at Souley Vegan, a restaurant known for its plant-based soul food and commitment to sustainability.
#     "description": "Enjoy a peaceful evening stroll at the Berkeley Marina, taking in the beautiful sunset views over the bay.
#     "description": "Start your day with a unique breakfast experience at Cheeseboard Collective, a worker-owned cooperative bakery known for its fresh and organic baked goods.
#     "description": "Explore the beautiful Berkeley Rose Garden, a historic landmark featuring over 1,500 rose bushes and stunning views of the Golden Gate Bridge.
#     "description": "Engage with interactive exhibits and learn about science, technology, and the environment at the Lawrence Hall of Science.",

#     """

#     model = llm

#     result = structured_llm.invoke(prompt)
#     return result

travel_recommendation_template = PromptTemplate(
    input_variables=[
        "num_days",
        "location",
        "start_date",
        "end_date",
        "budget",
        "interests",
    ],
    template="""Create a detailed and sustainable itinerary for a {num_days}-day trip to {location} from {start_date} to {end_date} with a total budget of {budget} dollars.
    The traveler is interested in {interests}.
    Plan for multiple activities each day, starting at 9 am and ending at 10 pm. Include breakfast, lunch, and dinner each day.
    Consider transportation time between activities and suggest eco-friendly options.
    Provide a variety of activities across all days, avoiding repetition.
    Ensure each day has a unique set of activities that showcase different aspects of {location}.
    Provide detailed information for each activity as specified in the ItineraryItem model.
    The itinerary should cover all {num_days} days of the trip.
    
    Follow this verbiage for your trip descriptions:
    
    "description": "Take a hike up Grizzly Peak for stunning views of the Bay Area. This eco-friendly activity is perfect for nature lovers."
    "description": "End your day with a delicious vegan dinner at Souley Vegan, a restaurant known for its plant-based soul food and commitment to sustainability."
    "description": "Enjoy a peaceful evening stroll at the Berkeley Marina, taking in the beautiful sunset views over the bay."
    "description": "Start your day with a unique breakfast experience at Cheeseboard Collective, a worker-owned cooperative bakery known for its fresh and organic baked goods."
    "description": "Explore the beautiful Berkeley Rose Garden, a historic landmark featuring over 1,500 rose bushes and stunning views of the Golden Gate Bridge."
    "description": "Engage with interactive exhibits and learn about science, technology, and the environment at the Lawrence Hall of Science."
    
    Remember to include all required fields for each ItineraryItem: title, description, location, begin, end, cost, transportation_method, distance, transportation_emissions, travel_time_to_next, and transportation_cost_to_next.
    
    Return the itinerary as a JSON object with an 'itinerary' key containing the full itinerary.
    """,
)

json_parser = SimpleJsonOutputParser()
travel_chain = LLMChain(
    llm=llm, prompt=travel_recommendation_template, output_parser=json_parser
)


def get_travel_recommendation(location, budget, interests, start_date, end_date):
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    num_days = (end_date_obj - start_date_obj).days + 1

    result = travel_chain.run(
        num_days=num_days,
        location=location,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        interests=interests,
    )

    return result


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

    recommendation = get_travel_recommendation(
        location, budget, interests, start_date, end_date
    )

    return jsonify(recommendation)


if __name__ == "__main__":
    app.run(debug=True)
