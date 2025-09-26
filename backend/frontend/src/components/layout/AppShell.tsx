import React from "react";

type AppShellProps = {
  children: React.ReactNode;
  showLogout?: boolean;
};

const AppShell: React.FC<AppShellProps> = ({ children, showLogout = true }) => {
  return (
    <div className="min-h-screen bg-[#f7f8fa]">
      <header className="bg-white shadow-sm">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
          <div className="flex items-center gap-4">
            <a
              href="/"
              className="text-lg font-semibold text-gray-800 hover:text-gray-900"
            >
              NDIS HRM
            </a>
            <nav className="hidden items-center gap-4 text-sm text-gray-600 sm:flex">
              <a className="hover:text-gray-900" href="/admin/users">
                Workers
              </a>
              <a className="hover:text-gray-900" href="/admin/applicants">
                Applicants
              </a>
              <a className="hover:text-gray-900" href="/portal/profile">
                My Profile
              </a>
            </nav>
          </div>

          {showLogout ? (
            <form method="post" action="/auth/logout">
              <button
                type="submit"
                className="rounded border border-gray-300 px-3 py-1 text-sm font-medium text-gray-700 transition hover:bg-gray-100"
              >
                Log out
              </button>
            </form>
          ) : (
            <a
              className="rounded border border-gray-300 px-3 py-1 text-sm font-medium text-gray-700 transition hover:bg-gray-100"
              href="/auth/login"
            >
              Log in
            </a>
          )}
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-6">{children}</main>
    </div>
  );
};

export default AppShell;
