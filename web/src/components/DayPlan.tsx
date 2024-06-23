import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "./ui/card";

import { Clock, MapPin } from "lucide-react";

export type Activity = {
  title: string;
  description: string;
  begin: string;
  end: string;
  location: string;
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
    <Card className="w-max-92">
      <CardHeader>
        <CardTitle>{activity.title}</CardTitle>
        <CardDescription>{activity.description}</CardDescription>
      </CardHeader>
      <CardContent className="grid grid-cols-2">
        <div className="flex items-center gap-1">
          <Clock />
          {activity.begin + " - " + activity.end}
        </div>
        <div className="flex items-center gap-1">
          <MapPin />
          {activity.location}
        </div>
      </CardContent>
    </Card>
  );
}

type DayPlanProps = {
  title: string;
  plan: DayItinerary;
};

function DayPlan({ title, plan }: DayPlanProps) {
  const activityMap = plan.activities ? (
    plan.activities.map((activity) => <ActivityCard activity={activity} />)
  ) : (
    <></>
  );

  return (
    <>
      <h3 className="text-2xl font-bold p-4">{title}</h3>
      <div className="space-y-4">{activityMap}</div>
    </>
  );
}

export default DayPlan;
