import React, { useState } from "react";

const formCategories = [
  "Compliance",
  "Onboarding",
  "Other",
  "Performance management",
  "Exit/ Transit",
];

const ApplicantProfileForm: React.FC = () => {
  const [showDropdown, setShowDropdown] = useState(false);

  return (
    <div className="bg-[#f7f8fa] min-h-screen p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-500 font-bold">
            P
          </div>
          <span className="font-medium text-gray-700">Profile Details</span>
        </div>
        <div className="flex gap-2">
          <button className="bg-gray-100 border border-gray-300 text-gray-700 px-4 py-1 rounded hover:bg-gray-200 text-sm font-medium">
            + Onboarding
          </button>
          <button className="bg-gray-100 border border-gray-300 text-gray-700 px-4 py-1 rounded hover:bg-gray-200 text-sm font-medium">
            Send An Email
          </button>
          <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-400 ml-2">
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              viewBox="0 0 24 24"
            >
              <circle cx="12" cy="12" r="10" />
              <path d="M12 16h.01M12 8v4" />
            </svg>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-md shadow-sm flex items-center px-2 py-1 mb-4 relative">
        <button className="px-3 py-1 text-gray-500 text-sm">Overview</button>
        <button className="px-3 py-1 text-gray-500 text-sm">Documents</button>
        <button className="px-3 py-1 text-gray-500 text-sm">Settings</button>
        <div
          className="relative"
          onMouseEnter={() => setShowDropdown(true)}
          onMouseLeave={() => setShowDropdown(false)}
        >
          <button
            className="px-3 py-1 font-medium border-b-2 border-gray-700 text-gray-900 text-sm"
            aria-haspopup="true"
            aria-expanded={showDropdown}
          >
            Forms &gt;
          </button>
          {showDropdown && (
            <div className="absolute left-0 top-full mt-2 bg-[#f7f8fa] shadow-lg rounded-md py-2 w-64 z-10">
              {formCategories.map((cat) => (
                <div
                  key={cat}
                  className="px-4 py-2 hover:bg-gray-100 text-gray-700 cursor-pointer text-sm"
                >
                  {cat}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Onboarding Section */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-2">
        <div className="font-medium text-gray-700 mb-2 md:mb-0">Onboarding</div>
        <div className="flex flex-col md:flex-row md:items-center gap-2 w-full md:w-auto">
          <div className="w-full md:w-56">
            <select className="w-full border border-gray-300 rounded px-4 py-2 bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-400 text-sm">
              <option value="">Select..</option>
              <option value="compliance">Compliance</option>
              <option value="onboarding">Onboarding</option>
              <option value="other">Other</option>
            </select>
          </div>
          <div className="w-full md:w-56 flex items-center">
            <input
              type="text"
              placeholder="Search"
              className="w-full border border-gray-300 rounded px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
            <svg
              className="w-5 h-5 text-gray-400 -ml-8"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              viewBox="0 0 24 24"
            >
              <circle cx="11" cy="11" r="8" />
              <path d="M21 21l-4.35-4.35" />
            </svg>
          </div>
        </div>
      </div>

      {/* Table Header */}
      <div className="grid grid-cols-7 bg-gray-100 rounded-t-md px-4 py-2 text-xs text-gray-500 font-medium mb-1">
        <div>FORM NAME</div>
        <div>CREATED BY</div>
        <div>LAST UPDATED BY</div>
        <div>EXPIRY DATE</div>
        <div>VERSION</div>
        <div className="col-span-2">ACTION</div>
      </div>

      {/* Table Rows (Skeletons) */}
      <div className="space-y-3">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="bg-[#f7f8fa] border border-gray-100 rounded-md px-4 py-4 grid grid-cols-7 gap-4"
          >
            <div className="h-4 bg-gray-200 rounded w-full" />
            <div className="h-4 bg-gray-200 rounded w-full" />
            <div className="h-4 bg-gray-200 rounded w-full" />
            <div className="h-4 bg-gray-200 rounded w-full" />
            <div className="h-4 bg-gray-200 rounded w-full" />
            <div className="h-4 bg-gray-200 rounded w-full col-span-2" />
          </div>
        ))}
      </div>
    </div>
  );
};

export default ApplicantProfileForm;
