import React from "react";

const CanInviteEmail: React.FC = () => {
  return (
    <div className="bg-[#f9fafb] min-h-screen flex flex-col items-center py-10">
      {/* Logo */}
      <div className="mb-6">
        <img
          src="/logo.png" // Replace with your logo path
          alt="nDigital Logo"
          className="h-14 mx-auto"
        />
      </div>
      {/* Email Card */}
      <div className="bg-white rounded-xl shadow-md max-w-2xl w-full px-8 py-10">
        <h2 className="text-2xl font-semibold text-center mb-6">
          You&apos;re Invite to interview with nDigital !
        </h2>
        <div className="text-gray-700 space-y-4">
          <p>Hello [Candidate First Name],</p>
          <p>
            Thank you for applying for the [Job Title] position with us at
            [Company Name], an NDIS-registered provider. We were impressed with
            your application and would like to invite you to attend an
            interview.
          </p>
          <div>
            <span className="font-medium">Interview Details:</span>
            <ul className="list-disc ml-6 mt-1">
              <li>Position: [Job Title]</li>
              <li>Date &amp; Time: [Insert Date &amp; Time]</li>
              <li>Location: [Physical Address / Online Link]</li>
              <li>Contact Person: [Name, Title, Phone/Email]</li>
            </ul>
          </div>
          <p>
            Please confirm your availability by clicking the button below or
            reply to this email if you need to reschedule.
          </p>
        </div>
        <div className="flex justify-center mt-8 mb-6">
          <button className="bg-[#1a2341] hover:bg-[#232d57] text-white px-7 py-2 rounded-full font-medium shadow">
            Confirm my interview
          </button>
        </div>
        <div className="text-gray-700 text-sm space-y-2">
          <p>
            We look forward to meeting you and learning more about how you can
            support our participants and team.
          </p>
          <p>
            Kind regards,
            <br />
            [Recruitment Team / Hiring Manager]
            <br />
            [Company Name]
          </p>
        </div>
        <div className="border-t border-gray-200 mt-8 pt-4 text-xs text-gray-500">
          This email was sent by nDigital, an NDIS-registered provider (Provider
          No: [XXXXXX]). If you need assistance accessing this information in an
          alternate format, please contact us at [phone/email].
        </div>
      </div>
      {/* Decorative footer shape */}
      <div className="w-full mt-12">
        <svg
          viewBox="0 0 1440 120"
          className="w-full h-20"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            fill="#1a2341"
            d="M0,120 C360,0 1080,0 1440,120 L1440,0 L0,0 Z"
          />
        </svg>
      </div>
    </div>
  );
};

export default CanInviteEmail;
