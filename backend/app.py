from flask import Flask, request, jsonify, send_file
import os
import requests
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
from icalendar import Calendar, Event
from datetime import datetime

app = Flask(__name__)

# Set your OpenAI and Google API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
google_cse_id = os.getenv("GOOGLE_CSE_ID")

# Define the model
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=openai_api_key)


class ItineraryItem(BaseModel):
    date: str = Field(description="The date range of the activity")
    location: str = Field(description="The location of the activity")
    description: str = Field(description="A description of the activity")
    image_url: str = Field(description="URL of the image associated with the activity")


class DayItinerary(BaseModel):
    day: int = Field(description="Day number of the itinerary")
    activities: List[ItineraryItem] = Field(
        description="List of activities for the day"
    )


class Itinerary(BaseModel):
    itinerary: List[DayItinerary] = Field(description="Day by day itinerary")


structured_llm = llm.with_structured_output(Itinerary)


def get_image_url(activity):
    # Use the location address to search for an appropriate image
    query = f"{activity['location']}"
    image_urls = search_images(query, google_api_key, google_cse_id)
    return image_urls[0] if image_urls else None


def get_travel_recommendation(location, budget, date_range, interests):
    prompt = f"Create a detailed itinerary for a trip to {location} from {date_range[0]} to {date_range[1]} with a budget of {budget} dollars. Each event should include the date range, a detailed location address suitable for Google Maps, and a description. The itinerary should be structured day by day, with each day containing multiple events. Consider the day of travel; on travel days, include fewer activities, while non-travel days should have multiple experiences or things to see. Format each day's itinerary as: {{'day': day_number, 'activities': [{{'date': 'date_range', 'location': 'full_address', 'description': 'activity description', 'image_url': 'image_url'}}]}}."
    new_prompt = prompt = f"Create a detailed and sustainable itinerary for a trip to {location} from {date_range[0]} to {date_range[1]} with a budget of {budget} dollars. " \
             f"The traveler is interested in {interests}. " \
             f"Each event should include: " \
             f"- Time range (start_time - end_time) " \
             f"- Detailed location address suitable for Google Maps " \
             f"- Description of the activity " \
             f"- Cost of the activity " \
             f"- carbon footprint from the activity " \
             f"- most sustaiable mode of transportation to get there from the previous activity while also being realistic" \
             f"- time of transporatation to get there using that mode" \
             f"- distance between this activity and previous activity" \
             f"- emmissions from the trip to the activity from the previous activity" \
             f"Plan for multiple activities each day, starting at 9 am and ending at 10 pm, make sure each day has a breakfast, lunch and dinner. " \
             f"Suggest the most eco-friendly activities possible. " \
             f"The itinerary should be structured day by day, with each day containing a list of event in the following format: " \
             f"{{'date': 'YYYY-MM-DD', 'activities': [{{'begin': 'start_time', 'end': 'end_time', 'location': 'full_address', 'description': 'activity description', 'carbon': 'carbon footprint', 'mode': 'mode of transportation', 'distance': total_distance_in_km, 'emissions': 'transportation emissions', 'time': 'duration of travel time between previous activity to this activity'}}]}}."

    
    result = structured_llm.invoke(prompt)

    # Enhance the result with image URLs
    enhanced_itinerary = []
    for day in result.dict()["itinerary"]:
        enhanced_day = {"day": day["day"], "activities": []}
        for activity in day["activities"]:
            image_url = get_image_url(activity)
            if image_url:
                activity["image_url"] = image_url
            enhanced_day["activities"].append(activity)
        enhanced_itinerary.append(enhanced_day)

    return {"itinerary": enhanced_itinerary}


def create_ics_file(itinerary, file_path):
    cal = Calendar()
    for day in itinerary["itinerary"]:
        for activity in day["activities"]:
            event = Event()
            # Assuming the time is not specified and defaulting to all-day events
            dt = datetime.strptime(activity["date"], "%Y-%m-%d").date()
            event.add("summary", activity["description"])
            event.add("dtstart", dt)
            event.add("dtend", dt)
            event.add("location", activity["location"])
            cal.add_component(event)
    with open(file_path, "wb") as f:
        f.write(cal.to_ical())


@app.route("/")
def home():
    return "Welcome to the Eco-Friendly Travel App!"


@app.route("/travel", methods=["POST"])
def travel():
    data = request.json
    location = data.get("location")
    budget = data.get("budget")
    date_range = data.get("date_range")

    if not location or not budget or not date_range or len(date_range) != 2:
        return (
            jsonify(
                {
                    "error": "Please provide location, budget, and a valid date range (start_date, end_date)"
                }
            ),
            400,
        )

    recommendation = get_travel_recommendation(location, budget, date_range)

    # Define the ICS file path
    ics_file_path = os.path.join("ics_files", "calendar.ics")

    # Ensure the directory exists
    os.makedirs("ics_files", exist_ok=True)

    # Create the ICS file
    create_ics_file(recommendation, ics_file_path)

    return jsonify(
        {
            "location": location,
            "budget": budget,
            "date_range": date_range,
            "itinerary": recommendation["itinerary"],
            "ics_file_path": ics_file_path,
        }
    )


@app.route("/download_ics", methods=["GET"])
def download_ics():
    ics_file_path = request.args.get("ics_file_path")
    if not ics_file_path or not os.path.exists(ics_file_path):
        return (
            jsonify(
                {"error": "ICS file not found. Please ensure the file path is correct."}
            ),
            400,
        )

    return send_file(ics_file_path, as_attachment=True)


def search_images(query, api_key, cse_id):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cse_id,
        "q": query,
        "searchType": "image",
        "num": 1,
        "rights": "cc_publicdomain|cc_attribute",  # Filter by Creative Commons licenses
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses
        data = response.json()

        image_urls = []
        if "items" in data:
            for item in data["items"]:
                image_urls.append(item["link"])

        return image_urls

    except requests.exceptions.RequestException as e:
        print(f"Error fetching images: {e}")
        return []


if __name__ == "__main__":
    app.run(debug=True)
