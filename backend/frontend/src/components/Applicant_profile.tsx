import React from "react";

const ProfileOverview: React.FC = () => {
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
        <button className="px-3 py-1 font-medium border-b-2 border-gray-700 text-gray-900 text-sm">
          Overview
        </button>
        <button className="px-3 py-1 text-gray-500 text-sm">Documents</button>
        <button className="px-3 py-1 text-gray-500 text-sm">Settings</button>
        <button className="px-3 py-1 text-gray-500 text-sm">Forms &gt;</button>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Left Column */}
        <div className="space-y-4">
          <div className="bg-white rounded-md p-4 shadow-sm">
            <div className="w-full h-28 bg-gray-200 rounded mb-3" />
            <div className="font-medium text-gray-700 mb-1">Quik Spapshot</div>
            <div className="space-y-2">
              <div className="h-3 bg-gray-200 rounded w-3/4" />
              <div className="h-3 bg-gray-200 rounded w-5/6" />
              <div className="h-3 bg-gray-200 rounded w-2/3" />
              <div className="h-3 bg-gray-200 rounded w-4/5" />
              <div className="h-3 bg-gray-200 rounded w-1/2" />
            </div>
          </div>
        </div>
        {/* Right Column */}
        <div className="space-y-4">
          <div className="bg-white rounded-md p-4 shadow-sm">
            <div className="font-medium text-gray-700 mb-1">
              Key Strengths, Likes & Areas of Improvement
            </div>
            <div className="text-xs text-gray-400 mb-2">
              Quick glance of Profile&apos;s Skillset
            </div>
            <div className="h-6 bg-gray-200 rounded mb-2 w-3/4" />
            <div className="h-8 bg-gray-200 rounded mb-2 w-full" />
            <div className="flex items-center justify-between mb-1">
              <span className="font-medium text-gray-700 text-sm">
                Work Availability
              </span>
              <button className="text-xs text-gray-500 hover:underline">
                + Add availability
              </button>
            </div>
            <div className="space-y-2 mb-2">
              <div className="h-3 bg-gray-200 rounded w-2/3" />
              <div className="h-3 bg-gray-200 rounded w-1/2" />
              <div className="h-3 bg-gray-200 rounded w-3/4" />
            </div>
            <div className="font-medium text-gray-700 text-sm mb-1">
              Training And Developement
            </div>
            <div className="h-16 bg-gray-200 rounded w-full" />
          </div>
        </div>
      </div>

      {/* Add Information Section */}
      <div className="mt-6">
        <div className="font-medium text-gray-700 mb-2">Add information</div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white rounded-md p-4 shadow-sm">
            <div className="font-medium text-gray-700 mb-2">Participants</div>
            <div className="space-y-2">
              <div className="h-5 bg-gray-200 rounded w-3/4" />
              <div className="h-5 bg-gray-200 rounded w-2/3" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileOverview;
