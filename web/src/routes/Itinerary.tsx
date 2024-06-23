import Header from "../components/Header";
import { useState } from "react";

import DayPlan, { Activity } from "../components/DayPlan";

const SAMPLE_DATA: Activity[][] = [
  [
    {
      title: "Morning Yoga",
      description:
        "A relaxing yoga session to start your day with mindfulness and flexibility.",
      begin: "07:00 AM",
      end: "08:00 AM",
      address: "123 Wellness St, Health City, HC 12345",
    },
    {
      title: "Tech Talk: AI in Healthcare",
      description:
        "A seminar on the latest advancements in AI applications in the healthcare industry.",
      begin: "10:00 AM",
      end: "11:30 AM",
      address: "456 Innovation Blvd, Tech Hub, TH 67890",
    },
    {
      title: "Evening Concert: Jazz Night",
      description:
        "Enjoy a night of smooth jazz music performed by local artists.",
      begin: "08:00 PM",
      end: "10:00 PM",
      address: "202 Music Ln, Melody Town, MT 24680",
    },
  ],
];

function Itinerary() {
  const [dayPlans, setDayPlans] = useState<Activity[][]>(SAMPLE_DATA);

  return (
    <>
      <Header />
      <main className="flex flex-col px-4 items-center">
        <div>
          <h1 className="text-4xl font-bold text-center mt-4">Itinerary</h1>
          {dayPlans.map((dayPlan, i) => (
            <DayPlan day={i + 1} activities={dayPlan} />
          ))}
        </div>
      </main>
    </>
  );
}

export default Itinerary;
