import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import IntakeForm from "./components/Can-intake-form";
import EvaluationForm from "./components/EvaluationForm";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<IntakeForm />} />
        <Route path="/candidate-form" element={<IntakeForm />} />
        <Route path="/evaluation" element={<EvaluationForm />} />
      </Routes>
    </Router>
  );
}

export default App;
