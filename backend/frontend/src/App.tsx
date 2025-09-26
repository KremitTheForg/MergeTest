import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import IntakeForm from "./components/Can-intake-form";
import EvaluationForm from "./components/EvaluationForm";
import AddEmployee from "./components/Add_employee";
import AddTraining from "./components/Add_training";
import ApplicantProfile from "./components/Applicant_profile";
import ApplicantProfileForm from "./components/Applicant_profile_form";
import ApplicantProfileDocument from "./components/Applicant_profile_document";
import CandidateInviteEmail from "./components/Can_Invite_email";
import OfferEmail from "./components/Offer_email";
import AppShell from "./components/layout/AppShell";

function App() {
  const withShell = (element: JSX.Element, showLogout = true) => (
    <AppShell showLogout={showLogout}>{element}</AppShell>
  );

  return (
    <Router>
      <Routes>
        <Route path="/" element={<IntakeForm />} />
        <Route path="/candidate-form" element={<IntakeForm />} />
        <Route path="/evaluation" element={withShell(<EvaluationForm />)} />
        <Route path="/add-employee" element={withShell(<AddEmployee />)} />
        <Route path="/admin/users/new" element={withShell(<AddEmployee />)} />
        <Route path="/add-training" element={withShell(<AddTraining />)} />
        <Route path="/applicant-profile" element={withShell(<ApplicantProfile />)} />
        <Route path="/portal/profile" element={withShell(<ApplicantProfile />)} />
        <Route
          path="/portal/profile/admin/:userId"
          element={withShell(<ApplicantProfile />)}
        />
        <Route
          path="/applicant-profile/form"
          element={withShell(<ApplicantProfileForm />)}
        />
        <Route path="/evaluation" element={<EvaluationForm />} />
        <Route path="/add-employee" element={<AddEmployee />} />
        <Route path="/admin/users/new" element={<AddEmployee />} />
        <Route path="/add-training" element={<AddTraining />} />
        <Route path="/applicant-profile" element={<ApplicantProfile />} />
        <Route path="/portal/profile" element={<ApplicantProfile />} />
        <Route
          path="/portal/profile/admin/:userId"
          element={<ApplicantProfile />}
        />
        <Route path="/applicant-profile/form" element={<ApplicantProfileForm />} />
        <Route
          path="/applicant-profile/documents"
          element={withShell(<ApplicantProfileDocument />)}
        />
        <Route
          path="/candidate-invite-email"
          element={withShell(<CandidateInviteEmail />)}
        />
        <Route path="/offer-email" element={withShell(<OfferEmail />)} />
      </Routes>
    </Router>
  );
}

export default App;
