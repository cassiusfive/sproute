import Header from "../components/Header";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import DayPlan, { DayItinerary } from "../components/DayPlan";

async function fetchItinerary(formdata: any): Promise<DayItinerary[]> {
  const payload = JSON.parse(formdata);
  payload.start_date = payload.dateRange.from.split("T")[0];
  payload.end_date = payload.dateRange.to.split("T")[0];
  payload.interests = payload.type;

  console.log("Payload:", payload); // Debugging line

  const res = await fetch(import.meta.env.VITE_BACKEND_API + "/travel", {
    method: "POST",
    body: JSON.stringify(payload),
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!res.ok) {
    console.error("Failed to fetch itinerary", await res.text());
    return [];
  }

  const itinerary = await res.json();
  if (!Array.isArray(itinerary)) {
    console.error("Invalid itinerary format", itinerary);
    return [];
  }

  return itinerary as DayItinerary[];
}

function Itinerary() {
  const location = useLocation();
  const { formdata } = location.state;
  const [itinerary, setItinerary] = useState<DayItinerary[]>();
  const [fetchInProgress, setFetchInProgress] = useState<boolean>(false);

  useEffect(() => {
    if (!fetchInProgress) {
      setFetchInProgress(true);
      fetchItinerary(formdata).then((plans) => setItinerary(plans));
    }
  }, [formdata, fetchInProgress]);

  const itineraryComponent = itinerary ? (
    itinerary.map((dayItinerary, i) => (
      <DayPlan title={`Day ${i + 1}`} plan={dayItinerary} />
    ))
  ) : (
    <></>
  );

  return (
    <>
      <Header />
      <main className="flex flex-col px-4 items-center">
        <div>
          <h1 className="text-4xl font-bold text-center mt-4">Itinerary</h1>
          {itineraryComponent}
        </div>
      </main>
    </>
  );
}

export default Itinerary;
