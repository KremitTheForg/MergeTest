import React from "react";

const ApplicantProfileDocument: React.FC = () => {
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
        <button className="bg-gray-100 border border-gray-300 text-gray-700 px-4 py-1 rounded hover:bg-gray-200 text-sm">
          Send Email
        </button>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-gray-200 h-2 rounded mb-2">
        <div className="bg-gray-400 h-2 rounded" style={{ width: "60%" }} />
      </div>
      <div className="text-xs text-gray-500 mb-2 ml-1">Progress Indicator</div>

      {/* Tabs */}
      <div className="bg-white rounded-md shadow-sm flex items-center px-2 py-1 mb-4">
        <button className="px-3 py-1 text-gray-500 text-sm">Overview</button>
        <button className="px-3 py-1 font-medium border-b-2 border-gray-700 text-gray-900 text-sm">
          Documents
        </button>
        <button className="px-3 py-1 text-gray-500 text-sm">Settings</button>
        <button className="px-3 py-1 text-gray-500 text-sm">Forms &gt;</button>
      </div>

      {/* Documents Dashboard */}
      <div className="flex items-center justify-between mb-4">
        <div className="font-medium text-gray-700">Documents Dashboard</div>
        <div className="flex gap-2">
          <button className="bg-gray-100 border border-gray-300 text-gray-700 px-3 py-1 rounded text-sm hover:bg-gray-200">
            + Create Folder
          </button>
          <button className="bg-gray-100 border border-gray-300 text-gray-700 px-3 py-1 rounded text-sm hover:bg-gray-200">
            Upload File
          </button>
        </div>
      </div>

      {/* Required Documents Card */}
      <div className="flex flex-wrap gap-4">
        <div className="bg-white rounded-md p-4 shadow-sm w-64 flex flex-col items-start">
          <div className="w-16 h-12 bg-gray-200 rounded mb-2" />
          <div className="text-gray-700 text-sm font-medium">
            Required Documents
          </div>
        </div>
      </div>
    </div>
  );
};

export default ApplicantProfileDocument;
