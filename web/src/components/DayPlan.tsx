import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "./ui/card";

import {
  Clock,
  MapPin,
  CircleDollarSign,
  Earth,
  Map,
  Timer,
  Footprints,
} from "lucide-react";

export type Activity = {
  title: string;
  description: string;
  begin: string;
  end: string;
  location: string;
  cost: number;
  carbon_footprint: number;
  transportation_emissions: number;
  distance: number;
  transportation_method: string;
  travel_time_to_next: string;
  transportation_cost_to_next: number;
};

export type DayItinerary = {
  activities: Activity[];
  date: string; // YYYY-MM-DD
};

type ActivityCardProps = {
  activity: Activity;
  hideTransport?: boolean;
};

function ActivityCard({ activity, hideTransport = false }: ActivityCardProps) {
  return (
    <div className="relative">
      <Card className="rounded-lg shadow-lg border-2 border-green-300 bg-white">
        <CardHeader>
          <CardTitle className="text-black">{activity.title}</CardTitle>
          <CardDescription className="text-secondary-foreground">
            {activity.description}
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col space-y-2 md:flex-row justify-between items-start md:items-center text-green-900">
          <div className="flex items-center gap-2">
            <Clock />
            <span>{activity.begin + " - " + activity.end}</span>
          </div>
          <div className="flex items-center gap-2">
            <CircleDollarSign className="min-w-[1.25rem]" />
            <span>{activity.cost}</span>
          </div>
          <div className="flex items-center gap-2">
            <MapPin />
            <span>{activity.location}</span>
          </div>
          <div className="flex items-center gap-2">
            <Earth />
            <span className="text-green-700 font-semibold">
              {activity.carbon_footprint} kg CO2
            </span>
          </div>
        </CardContent>
      </Card>
      {!hideTransport && (
        <div className="w-full p-4 rounded-md my-2 border-2 border-green-300 shadow-lg bg-green-50">
          <div className="flex justify-between items-center text-green-900">
            <div className="flex items-center gap-2">
              <Map />
              <span>{activity.transportation_method}</span>
            </div>
            <div className="flex items-center gap-2">
              <CircleDollarSign className="min-w-[1.25rem]" />
              <span>{activity.transportation_cost_to_next}</span>
            </div>
            <div className="flex items-center gap-2">
              <Timer />
              <span>{activity.travel_time_to_next}</span>
            </div>
            <div className="flex items-center gap-2">
              <Footprints />
              <span>{activity.distance} km</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

type DayPlanProps = {
  title: string;
  plan: DayItinerary;
};

function DayPlan({ title, plan }: DayPlanProps) {
  return (
    <div className="bg-green-100 p-6 rounded-lg shadow-lg">
      <h3 className="text-3xl font-bold text-green-900 mb-6">{title}</h3>
      <div className="">
        {plan.activities.map((activity, i) => (
          <ActivityCard
            key={activity.title}
            activity={activity}
            hideTransport={plan.activities.length == i + 1}
          />
        ))}
      </div>
    </div>
  );
}

export default DayPlan;
