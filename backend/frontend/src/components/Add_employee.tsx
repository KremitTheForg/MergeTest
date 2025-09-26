import React from "react";

const AddEmployee: React.FC = () => {
  return (
    <div className="max-w-6xl mx-auto mt-8 p-8">
      <h1 className="text-xl font-medium mb-2">Add Employee</h1>
      <p className="mb-8 text-gray-700">
        Please enter following details to create new Employee
      </p>
      <form className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block mb-2 font-medium text-gray-700">
              First Name
            </label>
            <input
              type="text"
              name="firstName"
              placeholder="Enter first name"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium text-gray-700">
              Last Name
            </label>
            <input
              type="text"
              name="lastName"
              placeholder="Enter last name"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium text-gray-700">
              Joining Date
            </label>
            <input
              type="text"
              name="joiningDate"
              placeholder="dd/mm/yyyy"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium text-gray-700">
              Job Title
            </label>
            <input
              type="text"
              name="jobTitle"
              placeholder="Enter job title"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium text-gray-700">
              Email Address
            </label>
            <input
              type="email"
              name="email"
              placeholder="Enter email address"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium text-gray-700">
              Phone Number
            </label>
            <input
              type="tel"
              name="phoneNumber"
              placeholder="Enter phone number"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium text-gray-700">
              Applicant Suburb
            </label>
            <input
              type="text"
              name="suburb"
              placeholder="Enter suburb"
              className="w-full border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
          </div>
          <div>
            <label className="block mb-2 font-medium text-gray-700">Role</label>
            <select
              name="role"
              className="w-full border border-gray-300 rounded px-4 py-2 bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-400"
              defaultValue=""
            >
              <option value="" disabled>
                Select Role
              </option>
              <option value="admin">Admin</option>
              <option value="manager">Manager</option>
              <option value="employee">Employee</option>
            </select>
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
};

export default AddEmployee;
