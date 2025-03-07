by# seeduser-rbac

UI Start Server -> npm run dev

API Start Server -> uvicorn main:app --reload

API Start Server -> python -m uvicorn main:app --reload


export function Badge({ children, type = "role" }: { children: React.ReactNode; type?: "role" | "group" }) {
  return (
    <span className={`inline-flex items-center gap-1 rounded-md px-2 py-1 text-xs font-medium text-white
        ${type === "role" ? "bg-blue-500" : "bg-gray-600"}
      `}
    >
      {type === "role" ? "👤" : "👥"} {/* Emoji Icons */}
      {children}
    </span>
  );
}



import { EyeIcon, PencilIcon, TrashIcon } from "@heroicons/react/24/solid"; // Import icons
import { users, User } from "@/data/users";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export default function UserTable() {
  return (
    <div className="p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-xl font-semibold mb-4">Users Table</h2>
      <div className="overflow-x-auto border rounded-lg shadow-sm">
        <Table className="w-full border-collapse">
          <TableHeader className="bg-gray-100 text-gray-700">
            <TableRow>
              <TableHead className="px-4 py-2">ID</TableHead>
              <TableHead className="px-4 py-2">Username</TableHead>
              <TableHead className="px-4 py-2">First Name</TableHead>
              <TableHead className="px-4 py-2">Last Name</TableHead>
              <TableHead className="px-4 py-2">Email</TableHead>
              <TableHead className="px-4 py-2">Roles</TableHead>
              <TableHead className="px-4 py-2">Groups</TableHead>
              <TableHead className="px-4 py-2">Created</TableHead>
              <TableHead className="px-4 py-2">Updated</TableHead>
              <TableHead className="px-4 py-2">Actions</TableHead> {/* ✅ NEW ACTION COLUMN */}
            </TableRow>
          </TableHeader>
          <TableBody>
            {users.map((user: User) => (
              <TableRow key={user.id} className="border-b hover:bg-gray-100">
                <TableCell className="px-4 py-2">{user.id}</TableCell>
                <TableCell className="px-4 py-2">{user.username}</TableCell>
                <TableCell className="px-4 py-2">{user.firstName}</TableCell>
                <TableCell className="px-4 py-2">{user.lastName}</TableCell>
                <TableCell className="px-4 py-2">{user.email}</TableCell>

                {/* Roles */}
                <TableCell className="px-4 py-2">
                  <div className="flex flex-wrap gap-2">
                    {user.roles.map((role, index) => (
                      <Badge key={index} type="role">{role}</Badge>
                    ))}
                  </div>
                </TableCell>

                {/* Groups */}
                <TableCell className="px-4 py-2">
                  <div className="flex flex-wrap gap-2">
                    {user.groups.map((group, index) => (
                      <Badge key={index} type="group">{group}</Badge>
                    ))}
                  </div>
                </TableCell>

                <TableCell className="px-4 py-2">{user.created}</TableCell>
                <TableCell className="px-4 py-2">{user.updated}</TableCell>

                {/* ✅ Actions: View, Edit, Delete */}
                <TableCell className="px-4 py-2 flex gap-3">
                  {/* View Button */}
                  <button 
                    onClick={() => handleView(user)}
                    className="text-blue-500 hover:text-blue-700"
                  >
                    <EyeIcon className="h-5 w-5" />
                  </button>

                  {/* Edit Button */}
                  <button 
                    onClick={() => handleEdit(user)}
                    className="text-yellow-500 hover:text-yellow-700"
                  >
                    <PencilIcon className="h-5 w-5" />
                  </button>

                  {/* Delete Button */}
                  <button 
                    onClick={() => handleDelete(user)}
                    className="text-red-500 hover:text-red-700"
                  >
                    <TrashIcon className="h-5 w-5" />
                  </button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}


function handleView(user: User) {
  console.log("Viewing user:", user);
}

function handleEdit(user: User) {
  console.log("Editing user:", user);
}

function handleDelete(user: User) {
  console.log("Deleting user:", user);
}
