import { useState } from "react";
import { EyeIcon, PencilIcon, TrashIcon } from "@heroicons/react/24/solid";
import { users, User } from "@/data/users";
import { Badge } from "@/components/ui/badge";
import { EditUserModal } from "@/components/EditUserModal"; // Import Modal
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export default function UserTable() {
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [isEditModalOpen, setEditModalOpen] = useState(false);

  function handleEdit(user: User) {
    setSelectedUser(user);
    setEditModalOpen(true);
  }

  function handleSave(updatedUser: User) {
    console.log("Updated User:", updatedUser);
    setEditModalOpen(false);
  }

  return (
    <div className="p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-xl font-semibold mb-4">Users Table</h2>
      <div className="overflow-x-auto border rounded-lg shadow-sm">
        <Table className="w-full border-collapse">
          <TableHeader className="bg-gray-100 text-gray-700">
            <TableRow>
              <TableHead className="px-4 py-2">ID</TableHead>
              <TableHead className="px-4 py-2">Username</TableHead>
              <TableHead className="px-4 py-2">Roles</TableHead>
              <TableHead className="px-4 py-2">Groups</TableHead>
              <TableHead className="px-4 py-2">Accounting Unit</TableHead>
              <TableHead className="px-4 py-2">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {users.map((user: User) => (
              <TableRow key={user.id} className="border-b hover:bg-gray-100">
                <TableCell className="px-4 py-2">{user.id}</TableCell>
                <TableCell className="px-4 py-2">{user.username}</TableCell>
                
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

                <TableCell className="px-4 py-2">{user.accountingUnit}</TableCell>

                {/* Actions */}
                <TableCell className="px-4 py-2 flex gap-3">
                  {/* View Button */}
                  <button className="text-blue-500 hover:text-blue-700">
                    <EyeIcon className="h-5 w-5" />
                  </button>

                  {/* Edit Button */}
                  <button onClick={() => handleEdit(user)} className="text-yellow-500 hover:text-yellow-700">
                    <PencilIcon className="h-5 w-5" />
                  </button>

                  {/* Delete Button */}
                  <button className="text-red-500 hover:text-red-700">
                    <TrashIcon className="h-5 w-5" />
                  </button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      {/* Edit Modal */}
      {selectedUser && (
        <EditUserModal
          user={selectedUser}
          isOpen={isEditModalOpen}
          onClose={() => setEditModalOpen(false)}
          onSave={handleSave}
        />
      )}
    </div>
  );
}