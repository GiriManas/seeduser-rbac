import Link from "next/link";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

const AdminDashboard = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Admin Controls</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* User Controls Card */}
        <Card>
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
        <Card>
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
        <Card>
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