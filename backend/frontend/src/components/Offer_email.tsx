import React from "react";

const OfferEmail: React.FC = () => {
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
          We&apos;re excited to Offer You the Role of [Job Title]
        </h2>
        <div className="text-gray-700 space-y-4">
          <p>Dear [Candidate First Name],</p>
          <p>
            Congratulations! Following your successful interview, we are
            delighted to offer you the position of [Job Title] with [Company
            Name], an NDIS-registered provider.
          </p>
          <div>
            <span className="font-medium">Offer Summary:</span>
            <ul className="list-disc ml-6 mt-1">
              <li>Position: [Job Title]</li>
              <li>Start Date: [Insert Start Date]</li>
              <li>Location: [Worksite Address / Remote]</li>
              <li>Employment Type: [Full-Time / Part-Time / Casual]</li>
              <li>
                Salary: [Base Salary / Hourly Rate] + applicable NDIS allowances
              </li>
            </ul>
          </div>
          <p>
            You&apos;ll find your formal employment contract attached to this
            email. Please review and accept the offer by [deadline date].
          </p>
        </div>
        <div className="flex justify-center mt-8 mb-6">
          <button className="bg-[#1a2341] hover:bg-[#232d57] text-white px-7 py-2 rounded-full font-medium shadow">
            Review &amp; Accept Offer
          </button>
        </div>
        <div className="text-gray-700 text-sm space-y-2">
          <p>
            We are excited for you to join our team in making a difference for
            people with disabilities.
            <br />
            If you have any questions, feel free to contact [HR contact name] at
            [phone/email].
          </p>
          <p>
            Kind regards,
            <br />
            [HR Manager / Hiring Team]
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

export default OfferEmail;
