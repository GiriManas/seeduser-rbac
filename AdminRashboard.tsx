import Link from "next/link";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

const AdminDashboard = () => {
  return (
    <div className="p-10 flex flex-col items-center min-h-screen">
      <h1 className="text-3xl font-bold mb-8">Admin Controls</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-5xl">
        {/* User Controls Card */}
        <Card className="p-4 shadow-lg hover:shadow-xl transition duration-300">
          <CardHeader>
            <CardTitle className="text-lg font-semibold">User Controls</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              <li>
                <Link href="/admin/users" className="text-blue-500 font-medium hover:underline">
                  Active Users
                </Link>
              </li>
              <li>
                <Link href="/admin/pending-users" className="text-blue-500 font-medium hover:underline">
                  Pending Users
                </Link>
              </li>
              <li>
                <Link href="/admin/password-reset" className="text-blue-500 font-medium hover:underline">
                  Password Reset Request
                </Link>
              </li>
            </ul>
          </CardContent>
        </Card>

        {/* Roles Card */}
        <Card className="p-4 shadow-lg hover:shadow-xl transition duration-300">
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Roles</CardTitle>
          </CardHeader>
          <CardContent>
            <Link href="/admin/roles" className="text-blue-500 font-medium hover:underline">
              Manage Roles
            </Link>
          </CardContent>
        </Card>

        {/* Groups Card */}
        <Card className="p-4 shadow-lg hover:shadow-xl transition duration-300">
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Groups</CardTitle>
          </CardHeader>
          <CardContent>
            <Link href="/admin/groups" className="text-blue-500 font-medium hover:underline">
              Manage Groups
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AdminDashboard;