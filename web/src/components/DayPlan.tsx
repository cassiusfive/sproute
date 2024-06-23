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
  address: string;
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
          {activity.address}
        </div>
      </CardContent>
    </Card>
  );
}

type DayPlanProps = {
  day: number;
  activities: Activity[];
};

function DayPlan({ day, activities }: DayPlanProps) {
  return (
    <>
      <h3 className="text-2xl font-bold p-4">{"Day " + day}</h3>
      <div className="space-y-4">
        {activities.map((activity) => (
          <ActivityCard activity={activity} />
        ))}
      </div>
    </>
  );
}

export default DayPlan;
