import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import ProfileOverview from "./components/Applicant_profile";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ProfileOverview />
  </StrictMode>
);
