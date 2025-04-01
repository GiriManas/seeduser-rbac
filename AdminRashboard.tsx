import Link from "next/link";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

const AdminDashboard = () => {
  return (
    <div className="p-6 flex flex-col items-center">
      <h1 className="text-2xl font-semibold mb-6">Admin Controls</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl">
        {/* User Controls Card */}
        <Card className="text-center">
          <CardHeader>
            <CardTitle>User Controls</CardTitle>
          </CardHeader>
          <CardContent>
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
          </CardContent>
        </Card>

        {/* Roles Card */}
        <Card className="text-center">
          <CardHeader>
            <CardTitle>Roles</CardTitle>
          </CardHeader>
          <CardContent>
            <Link href="/admin/roles" className="text-blue-600 hover:underline">
              Manage Roles
            </Link>
          </CardContent>
        </Card>

        {/* Groups Card */}
        <Card className="text-center">
          <CardHeader>
            <CardTitle>Groups</CardTitle>
          </CardHeader>
          <CardContent>
            <Link href="/admin/groups" className="text-blue-600 hover:underline">
              Manage Groups
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AdminDashboard;