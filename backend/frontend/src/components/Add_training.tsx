import React, { useRef } from "react";

const AddTraining: React.FC = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  return (
    <div className="max-w-6xl mx-auto mt-8 p-8">
      <h1 className="text-xl font-medium mb-1">Create Training</h1>
      <div className="text-xs text-gray-400 mb-6">
        Dashboard &gt; HRM &gt; Create Training &gt;
      </div>
      <form className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block mb-2 font-medium text-gray-700">
              Training Name
            </label>
            <input
              type="text"
              name="trainingName"
              placeholder=""
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium text-gray-700">
              Instructor/Trainer
            </label>
            <input
              type="text"
              name="instructor"
              placeholder=""
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
        </div>
        <div>
          <label className="block mb-2 font-medium text-gray-700">
            Description
          </label>
          <textarea
            name="description"
            placeholder="Write  description here"
            rows={4}
            className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400 resize-none"
          />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block mb-2 font-medium text-gray-700">
              Target Audience
            </label>
            <select
              name="audience"
              className="w-full border border-gray-300 rounded px-4 py-2 bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-400"
              defaultValue=""
            >
              <option value="" disabled>
                Select ..
              </option>
              <option value="staff">Staff</option>
              <option value="managers">Managers</option>
              <option value="all">All Employees</option>
            </select>
          </div>
          <div>
            <label className="block mb-2 font-medium text-gray-700">
              Maximum Attendees
            </label>
            <input
              type="number"
              name="maxAttendees"
              placeholder=""
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
              min={1}
            />
          </div>
        </div>
        <div>
          <label className="block mb-2 font-medium text-gray-700">
            Training Materials
          </label>
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
              name="materials"
              className="hidden"
              accept=".pdf,.doc,.docx"
            />
          </div>
        </div>
        <button
          type="submit"
          className="bg-gray-700 text-white px-8 py-2 rounded font-medium mt-2"
        >
          SUBMIT
        </button>
      </form>
    </div>
  );
};

export default AddTraining;
