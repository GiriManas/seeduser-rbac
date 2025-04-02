import Link from "next/link";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

const AdminDashboard = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen w-full px-4">
      {/* Title */}
      <h1 className="text-3xl font-bold mb-8 text-center">Admin Controls</h1>

      {/* Grid Layout */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl mx-auto justify-center">
        
        {/* User Controls Card */}
        <Card className="p-6 w-full h-48 flex flex-col justify-between shadow-lg hover:shadow-xl transition duration-300 text-center">
          <CardHeader>
            <CardTitle className="text-lg font-semibold">User Controls</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col items-center justify-between flex-grow overflow-auto space-y-2">
            <Link href="/admin/users" className="text-blue-500 font-medium hover:underline">
              Active Users
            </Link>
            <Link href="/admin/pending-users" className="text-blue-500 font-medium hover:underline">
              Pending Users
            </Link>
            <Link href="/admin/password-reset" className="text-blue-500 font-medium hover:underline">
              Password Reset Request
            </Link>
          </CardContent>
        </Card>

        {/* Roles Card */}
        <Card className="p-6 w-full h-48 flex flex-col justify-between shadow-lg hover:shadow-xl transition duration-300 text-center">
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Roles</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col items-center justify-center flex-grow">
            <Link href="/admin/roles" className="text-blue-500 font-medium hover:underline">
              Manage Roles
            </Link>
          </CardContent>
        </Card>

        {/* Groups Card */}
        <Card className="p-6 w-full h-48 flex flex-col justify-between shadow-lg hover:shadow-xl transition duration-300 text-center">
          <CardHeader>
            <CardTitle className="text-lg font-semibold">Groups</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col items-center justify-center flex-grow">
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