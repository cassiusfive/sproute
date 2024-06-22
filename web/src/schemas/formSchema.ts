"use client";

import { z } from "zod";

export const formSchema = z.object({
  location: z.string().min(2, {
    message: "Location must be at least 2 characters.",
  }),
 
  budget: z.string().min(1, {
    message: "Duration must be provided.",
  }),
  dateRange: z.object({
    from: z.date().optional(),
    to: z.date().optional(),
  }).optional(),
});
