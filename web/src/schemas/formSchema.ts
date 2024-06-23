"use client";

import { z } from "zod";

export const formSchema = z.object({
  location: z.string().min(2, {
    message: "Location must be at least 2 characters.",
  }),
  budget: z.number().min(0, {
    message: "Budget must be a positive number.",
  }),
  dateRange: z
    .object({
      from: z.date().optional(),
      to: z.date().optional(),
    })
    .optional(),
  type: z
    .array(
      z.enum([
        "sightseeing",
        "cultural",
        "adventure",
        "relaxation",
        "culinary",
      ]),
      {
        required_error: "You need to select at least one interest.",
      },
    )
    .nonempty("You need to select at least one interest."),
});
