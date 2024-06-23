import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import Home from "./routes/Home.tsx";
import Planner from "./routes/Planner.tsx";
import Rewards from "./routes/Rewards.tsx";
import Itinerary from "./routes/Itinerary.tsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  { path: "/planner", element: <Planner /> },
  { path: "/rewards", element: <Rewards /> },
  { path: "/itinerary", element: <Itinerary /> },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
);
