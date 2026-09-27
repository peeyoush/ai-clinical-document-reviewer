import { createBrowserRouter } from "react-router";

import App from "./App";
import Home from "./pages/Home";
import Analyze from "./pages/Analyze";
import Reports from "./pages/Reports";
import ReportDetails from "./pages/ReportDetails";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: "analyze",
        element: <Analyze />,
      },
      {
        path: "reports",
        element: <Reports />,
      },
      {
        path: "reports/:id",
        element: <ReportDetails />,
      },
    ],
  },
]);