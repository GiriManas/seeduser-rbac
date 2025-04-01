import Link from "next/link";

const AdminDashboard = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Admin Controls</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* User Controls Card */}
        <div className="p-4 bg-white shadow rounded-lg">
          <h2 className="text-lg font-semibold mb-2">User Controls</h2>
          <ul className="space-y-2">
            <li>
              <Link href="/admin/users" className="text-blue-600 hover:underline">
                Active Users
              </Link>
            </li>
            <li>
              <Link href="/admin/pending-users" className="text-blue-600 hover:underline">
                Pending Users
              </Link>
            </li>
            <li>
              <Link href="/admin/password-reset" className="text-blue-600 hover:underline">
                Password Reset Request
              </Link>
            </li>
          </ul>
        </div>

        {/* Roles Card */}
        <div className="p-4 bg-white shadow rounded-lg">
          <h2 className="text-lg font-semibold mb-2">Roles</h2>
          <Link href="/admin/roles" className="text-blue-600 hover:underline">
            Manage Roles
          </Link>
        </div>

        {/* Groups Card */}
        <div className="p-4 bg-white shadow rounded-lg">
          <h2 className="text-lg font-semibold mb-2">Groups</h2>
          <Link href="/admin/groups" className="text-blue-600 hover:underline">
            Manage Groups
          </Link>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;