"use client";

import * as React from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm, Controller } from "react-hook-form";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import { formSchema } from "../schemas/formSchema"; // Adjust the import path as necessary
import { addDays, format } from "date-fns";
import { Calendar as CalendarIcon } from "lucide-react";
import { DateRange } from "react-day-picker";

import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Slider } from "@/components/ui/slider";
import { Checkbox } from "@/components/ui/checkbox";
import { toast } from "@/components/ui/use-toast";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils"; // Ensure this import path is correct

export function ProfileForm() {
  const navigate = useNavigate();
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      location: "",
      budget: 500, // Set an initial value for budget
      dateRange: {
        from: new Date(2024, 7, 22),
        to: addDays(new Date(2024, 7, 23), 0),
      },
      type: [], // Initialize as empty array for multiple interests
    },
  });

  const [budget, setBudget] = React.useState(1000); // Define the state for budget

  function onSubmit(values: any) {
    // Adjust type as necessary
    // toast({
    //   title: "You submitted the following values:",
    //   description: (
    //     <pre className="mt-2 w-[340px] rounded-md bg-slate-950 p-4">
    //       <code className="text-white">{JSON.stringify(values, null, 2)}</code>
    //     </pre>
    //   ),
    // });
    navigate("/itinerary", { state: { formdata: JSON.stringify(values) } });
  }

  return (
    <div className="max-w-lg mx-auto p-4">
      <h1 className="text-2xl font-semibold text-center mb-6">
        Travel Preferences Form
      </h1>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <FormField
            control={form.control}
            name="location"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Where do you want to travel?</FormLabel>
                <FormControl>
                  <Input placeholder="Enter location" {...field} />
                </FormControl>
                <FormDescription></FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="budget"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Budget: ${budget}</FormLabel>
                <FormControl>
                  <Slider
                    defaultValue={[field.value]}
                    min={50}
                    max={5000}
                    step={50}
                    onValueChange={(value) => {
                      setBudget(value[0]);
                      field.onChange(value[0]);
                    }}
                  />
                </FormControl>
                <FormDescription>
                  This is your preferred budget.
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <Controller
            control={form.control}
            name="dateRange"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Date Range</FormLabel>
                <FormControl>
                  <DatePickerWithRange
                    value={field.value}
                    onChange={field.onChange}
                  />
                </FormControl>
                <FormDescription>
                  Select your preferred date range.
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="type"
            render={({ field }) => (
              <FormItem className="space-y-3">
                <FormLabel>Interests</FormLabel>
                <FormControl>
                  <div className="flex flex-col space-y-1">
                    {["sightseeing", "adventure", "relaxation", "cultural", "food_and_drink"].map((interest) => (
                      <FormItem key={interest} className="flex items-center space-x-3 space-y-0">
                        <FormControl>
                          <Checkbox
                            checked={field.value.includes(interest)}
                            onCheckedChange={(checked) => {
                              if (checked) {
                                field.onChange([...field.value, interest]);
                              } else {
                                field.onChange(field.value.filter((value: string) => value !== interest));
                              }
                            }}
                          />
                        </FormControl>
                        <FormLabel className="font-normal capitalize">{interest.replace('_', ' ')}</FormLabel>
                      </FormItem>
                    ))}
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <Button type="submit" className="w-full">
            Submit
          </Button>
        </form>
      </Form>
    </div>
  );
}

function DatePickerWithRange({
  className,
  value,
  onChange,
}: {
  className?: string;
  value: DateRange;
  onChange: (value: DateRange) => void;
}) {
  const [date, setDate] = React.useState<DateRange | undefined>(value);

  React.useEffect(() => {
    setDate(value);
  }, [value]);

  const handleSelect = (selectedDate: DateRange | undefined) => {
    setDate(selectedDate);
    onChange(selectedDate as DateRange);
  };

  return (
    <div className={cn("grid gap-2", className)}>
      <Popover>
        <PopoverTrigger asChild>
          <Button
            id="date"
            variant={"outline"}
            className={cn(
              "w-full justify-start text-left font-normal",
              !date && "text-muted-foreground"
            )}
          >
            <CalendarIcon className="mr-2 h-4 w-4" />
            {date?.from ? (
              date.to ? (
                <>
                  {format(date.from, "LLL dd, y")} -{" "}
                  {format(date.to, "LLL dd, y")}
                </>
              ) : (
                format(date.from, "LLL dd, y")
              )
            ) : (
              <span>Pick a date</span>
            )}
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-auto p-0" align="start">
          <Calendar
            initialFocus
            mode="range"
            defaultMonth={date?.from}
            selected={date}
            onSelect={handleSelect}
            numberOfMonths={2}
          />
        </PopoverContent>
      </Popover>
    </div>
  );
}
