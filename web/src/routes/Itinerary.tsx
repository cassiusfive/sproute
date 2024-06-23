import Header from "../components/Header";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

import DayPlan, { DayItinerary } from "../components/DayPlan";

async function fetchItinerary(formdata: any): Promise<DayItinerary[]> {
  const payload = JSON.parse(formdata);
  payload.start_date = payload.dateRange.from.split("T")[0];
  payload.end_date = payload.dateRange.to.split("T")[0];
  payload.interests = ["sightseeing"];

  const res = await fetch(import.meta.env.VITE_BACKEND_API + "/travel", {
    method: "POST",
    body: JSON.stringify(payload),
    headers: {
      "Content-Type": "application/json",
    },
  });

  const itinerary = await res.json();

  return itinerary as DayItinerary[];
}

function Itinerary() {
  const location = useLocation();
  const [itinerary, setItinerary] = useState<DayItinerary[]>();

  useEffect(() => {
    fetchItinerary(location.state.formdata).then((plans) =>
      setItinerary(plans),
    );
  }, [location]);

  return (
    <>
      <Header />
      <main className="flex flex-col px-4 items-center">
        <div>
          <h1 className="text-4xl font-bold text-center mt-4">Itinerary</h1>
          {itinerary &&
            itinerary.map((dayItinerary, i) => (
              <DayPlan title={`Day ${i + 1}`} plan={dayItinerary} />
            ))}
        </div>
      </main>
    </>
  );
}

export default Itinerary;
