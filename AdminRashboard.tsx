import Link from "next/link";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

// Icon Components (Using Lucide SVG paths)
const UsersIcon = () => (
  <svg className="w-6 h-6 text-gray-700 mb-2" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path strokeLinecap="round" strokeLinejoin="round" d="M17 20h5v-2a3 3 0 00-5.83-1M4 20v-2a3 3 0 015.83-1M9 10a3 3 0 100-6 3 3 0 000 6zM15 10a3 3 0 100-6 3 3 0 000 6zM15 20h5v-2a3 3 0 00-5.83-1M4 20v-2a3 3 0 015.83-1"></path>
  </svg>
);

const ShieldCheckIcon = () => (
  <svg className="w-6 h-6 text-gray-700 mb-2" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path strokeLinecap="round" strokeLinejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
    <path strokeLinecap="round" strokeLinejoin="round" d="M9 11l2 2 4-4"></path>
  </svg>
);

const UsersRoundIcon = () => (
  <svg className="w-6 h-6 text-gray-700 mb-2" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path strokeLinecap="round" strokeLinejoin="round" d="M18 21v-2a4 4 0 00-3-3.87M6 21v-2a4 4 0 013-3.87M12 12a4 4 0 100-8 4 4 0 000 8z"></path>
  </svg>
);

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
            <div className="flex flex-col items-center">
              <UsersIcon />
              <CardTitle className="text-lg font-semibold">User Controls</CardTitle>
            </div>
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
            <div className="flex flex-col items-center">
              <ShieldCheckIcon />
              <CardTitle className="text-lg font-semibold">Roles</CardTitle>
            </div>
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
            <div className="flex flex-col items-center">
              <UsersRoundIcon />
              <CardTitle className="text-lg font-semibold">Groups</CardTitle>
            </div>
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