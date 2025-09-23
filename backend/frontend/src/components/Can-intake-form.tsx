import { useRef, useState } from "react";
import type { ChangeEvent, FormEvent } from "react";
import { Link } from "react-router-dom";

type FormState = {
  firstName: string;
  lastName: string;
  appliedOn: string;
  jobTitle: string;
  email: string;
  phoneNumber: string;
  suburb: string;
};

const createInitialFormState = (): FormState => ({
  firstName: "",
  lastName: "",
  appliedOn: "",
  jobTitle: "",
  email: "",
  phoneNumber: "",
  suburb: "",
});

function IntakeForm() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [formData, setFormData] = useState<FormState>(() => createInitialFormState());
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [selectedFileName, setSelectedFileName] = useState<string | null>(null);

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    setSelectedFileName(file ? file.name : null);
  };

  const resetForm = () => {
    setFormData(createInitialFormState());
    setSelectedFileName(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setSuccess(null);

    const trimmedFirstName = formData.firstName.trim();
    const trimmedLastName = formData.lastName.trim();
    const trimmedEmail = formData.email.trim();
    const trimmedPhoneNumber = formData.phoneNumber.trim();
    const trimmedJobTitle = formData.jobTitle.trim();
    const trimmedSuburb = formData.suburb.trim();
    const trimmedAppliedOn = formData.appliedOn.trim();

    if (!trimmedFirstName || !trimmedLastName) {
      setError("First and last name are required.");
      return;
    }

    if (!trimmedEmail) {
      setError("Email address is required.");
      return;
    }

    setIsSubmitting(true);

    const payload = {
      first_name: trimmedFirstName,
      last_name: trimmedLastName,
      email: trimmedEmail,
      mobile: trimmedPhoneNumber || undefined,
      job_title: trimmedJobTitle || undefined,
      address: trimmedSuburb || undefined,
      applied_on: trimmedAppliedOn || undefined,
    };

    try {
      const response = await fetch("/api/v1/hr/recruitment/candidates/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify(payload),
      });

      const contentType = response.headers.get("content-type") ?? "";
      if (!contentType.includes("application/json")) {
        const fallbackText = await response.text().catch(() => "");
        const message = fallbackText.trim();
        throw new Error(
          message ||
            (response.ok
              ? "Unexpected response from the server."
              : `Unable to submit the form. (status ${response.status})`)
        );
      }

      const data = (await response.json().catch(() => null)) as
        | {
            detail?: unknown;
            id?: unknown;
          }
        | null;

      if (!response.ok) {
        const detail = typeof data?.detail === "string" ? data.detail : null;
        throw new Error(detail ?? "Unable to submit the form.");
      }

      const detail = typeof data?.detail === "string" ? data.detail : null;
      const id = typeof data?.id === "number" ? data.id : null;
      const baseMessage = detail
        ? detail.charAt(0).toUpperCase() + detail.slice(1)
        : "Candidate successfully submitted.";
      setSuccess(id ? `${baseMessage} (ID ${id}).` : baseMessage);
      resetForm();
    } catch (submissionError) {
      setError(
        submissionError instanceof Error
          ? submissionError.message
          : "Unable to submit the form."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto mt-8 p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Add Applicants</h1>
        <Link
          to="/evaluation"
          className="bg-gray-700 text-white px-5 py-2 rounded font-medium"
        >
          Evaluation
        </Link>
      </div>
      <p className="mb-8 text-gray-700">
        Please enter following details to create new applicant
      </p>
      <form className="space-y-6" onSubmit={handleSubmit}>
        {error && (
          <div className="rounded border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}
        {success && (
          <div className="rounded border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">
            {success}
          </div>
        )}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block mb-2 font-medium">First Name</label>
            <input
              type="text"
              name="firstName"
              value={formData.firstName}
              onChange={handleChange}
              placeholder="Enter first name"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium">Last Name</label>
            <input
              type="text"
              name="lastName"
              value={formData.lastName}
              onChange={handleChange}
              placeholder="Enter last name"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium">Applied On</label>
            <input
              type="date"
              name="appliedOn"
              value={formData.appliedOn}
              onChange={handleChange}
              placeholder="dd/mm/yyyy"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium">Job Title</label>
            <input
              type="text"
              name="jobTitle"
              value={formData.jobTitle}
              onChange={handleChange}
              placeholder="Enter job title"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium">Email Address</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Enter email address"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium">Phone Number</label>
            <input
              type="tel"
              name="phoneNumber"
              value={formData.phoneNumber}
              onChange={handleChange}
              placeholder="Enter phone number"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
        </div>
        <div>
          <label className="block mb-2 font-medium">Applicant Suburb</label>
          <input
            type="text"
            name="suburb"
            value={formData.suburb}
            onChange={handleChange}
            placeholder="Enter suburb"
            className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
          />
        </div>
        <div>
          <label className="block mb-2 font-medium">File Attachment</label>
          <div
            className="border-2 border-gray-200 border-dashed rounded-lg p-6 flex flex-col items-center justify-center cursor-pointer bg-gray-50"
            onClick={() => fileInputRef.current?.click()}
          >
            <svg
              className="w-10 h-10 text-gray-400 mb-2"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M12 4v16m8-8H4"
              />
            </svg>
            <p className="text-gray-700 mb-1">
              Drop your Documents here, or click to browse
            </p>
            <p className="text-xs text-gray-500">
              PDF, DOC, DOCX, up to 1MB max.
            </p>
            <input
              ref={fileInputRef}
              type="file"
              name="attachment"
              className="hidden"
              accept=".pdf,.doc,.docx"
              onChange={handleFileChange}
            />
            {selectedFileName && (
              <p className="mt-2 text-xs text-gray-500">{selectedFileName}</p>
            )}
          </div>
        </div>
        <button
          type="submit"
          className="bg-gray-700 text-white px-8 py-2 rounded font-medium mt-4 disabled:cursor-not-allowed disabled:opacity-60"
          disabled={isSubmitting}
        >
          {isSubmitting ? "Submitting..." : "ADD"}
        </button>
      </form>
    </div>
  );
}

export default IntakeForm;
