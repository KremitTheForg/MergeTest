import { useRef } from "react";
import { Link } from "react-router-dom"; // Add this import

function IntakeForm() {
  const fileInputRef = useRef<HTMLInputElement>(null);

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
      <form className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block mb-2 font-medium">First Name</label>
            <input
              type="text"
              name="firstName"
              placeholder="Enter first name"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium">Last Name</label>
            <input
              type="text"
              name="lastName"
              placeholder="Enter last name"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium">Applied On</label>
            <input
              type="date"
              name="appliedOn"
              placeholder="dd/mm/yyyy"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium">Job Title</label>
            <input
              type="text"
              name="jobTitle"
              placeholder="Enter job title"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium">Email Address</label>
            <input
              type="email"
              name="email"
              placeholder="Enter email address"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium">Phone Number</label>
            <input
              type="tel"
              name="phoneNumber"
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
            />
          </div>
        </div>
        <button
          type="submit"
          className="bg-gray-700 text-white px-8 py-2 rounded font-medium mt-4"
        >
          ADD
        </button>
      </form>
    </div>
  );
}

export default IntakeForm;
