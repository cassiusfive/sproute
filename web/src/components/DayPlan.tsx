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
  Leaf,
  Wind,
  Bike,
} from "lucide-react";

export type Activity = {
  title: string;
  description: string;
  begin: string;
  end: string;
  location: string;
  cost: number;
  emissions: number;
  carbon: number;
  distance: number;
  mode: string;
  transportation_time_from_prev_to_here: string;
  transportation_cost_from_prev_to_here: number;
};

export type DayItinerary = {
  activities: Activity[];
  date: string; // YYYY-MM-DD
};

type ActivityCardProps = {
  activity: Activity;
};

function ActivityCard({ activity }: ActivityCardProps) {
  return (
    <div className="relative mb-8">
      <div className="w-full p-4 rounded-md mt-2 border-2 border-green-300 shadow-lg bg-green-50">
        <div className="flex justify-between items-center text-green-900">
          <div className="flex items-center gap-2">
            <Map />
            <span>{activity.mode}</span>
          </div>
          <div className="flex items-center gap-2">
            <CircleDollarSign className="min-w-[1.25rem]" />
            <span>{activity.transportation_cost_from_prev_to_here}</span>
          </div>
          <div className="flex items-center gap-2">
            <Timer />
            <span>{activity.transportation_time_from_prev_to_here}</span>
          </div>
          <div className="flex items-center gap-2">
            <MapPin />
            <span>{activity.distance} km</span>
          </div>
        </div>
      </div>
      <Card className="mt-4 rounded-lg shadow-lg border-2 border-green-300 bg-white">
        <CardHeader>
          <CardTitle className="text-green-900">{activity.title}</CardTitle>
          <CardDescription className="text-green-700">
            {activity.description}
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col md:flex-row justify-between items-start md:items-center text-green-900">
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
            <span>{activity.emissions} kg CO2</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

type DayPlanProps = {
  title: string;
  plan: DayItinerary;
};

function DayPlan({ title, plan }: DayPlanProps) {
  return (
    <div className="bg-green-100 p-6 rounded-lg shadow-lg my-8">
      <h3 className="text-3xl font-bold text-green-900 mb-6">{title}</h3>
      <div className="space-y-8">
        {plan.activities.map((activity) => (
          <ActivityCard key={activity.title} activity={activity} />
        ))}
      </div>
    </div>
  );
}

export default DayPlan;
