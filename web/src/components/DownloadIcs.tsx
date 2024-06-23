import * as ics from "ics";

import { DayItinerary } from "./DayPlan";

type DownloadIcsProps = {
  itinerary: DayItinerary[];
};

type IcsEvent = {
  title: string;
  description: string;
  location: string;
  start: [number, number, number, number, number];
  end: [number, number, number, number, number];
};

function createIcs(itinerary: DayItinerary[]): string {
  const events = itinerary.flatMap((dayItinerary) => {
    const [year, month, date] = dayItinerary.date.split("-").map((x) => +x);
    return dayItinerary.activities.map((activity) => {
      const [startHour, startMinute] = activity.begin.split(":").map((x) => +x);
      const [endHour, endMinute] = activity.end.split(":").map((x) => +x);
      return {
        title: activity.title,
        description: activity.description,
        location: activity.location,
        start: [year, month, date, startHour, startMinute],
        end: [year, month, date, endHour, endMinute],
      } as IcsEvent;
    });
  });

  console.log(events);

  const { error, value } = ics.createEvents(events);

  if (!error) {
    return value!;
  }
  return "";
}

function DownloadIcs({ itinerary }: DownloadIcsProps) {
  function handleDownload() {
    const icsContent = createIcs(itinerary);

    const blob = new Blob([icsContent], { type: "text/calendar" });

    // Create a download link
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "events.ics";

    // Trigger the download
    link.click();

    // Clean up the URL object
    URL.revokeObjectURL(link.href);
  }

  return <button onClick={handleDownload}>Download ICS</button>;
}

export default DownloadIcs;
