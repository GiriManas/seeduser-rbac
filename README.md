""""

export type PendingUser = {
  id: string;
  email: string;
  name: string;
  approver: string;
  status: "Pending" | "Approved" | "Declined";
};

export const pendingUsers: PendingUser[] = [
  { id: "u101", email: "user1@example.com", name: "Alice Doe", approver: "John Admin", status: "Pending" },
  { id: "u102", email: "user2@example.com", name: "Bob Smith", approver: "Sarah Manager", status: "Pending" },
  { id: "u103", email: "user3@example.com", name: "Charlie Brown", approver: "Jane Supervisor", status: "Pending" },
];



"use client";
import { useState } from "react";
import { CheckIcon, XCircleIcon } from "@heroicons/react/24/solid";
import { pendingUsers, PendingUser } from "@/data/pendingUsers";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

export default function PendingUsers() {
  const [userList, setUserList] = useState(pendingUsers);

  function handleApprove(userId: string) {
    setUserList(userList.map(user => 
      user.id === userId ? { ...user, status: "Approved" } : user
    ));
  }

  function handleDecline(userId: string) {
    setUserList(userList.map(user => 
      user.id === userId ? { ...user, status: "Declined" } : user
    ));
  }

  return (
    <div className="p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-xl font-semibold mb-4">Pending Users</h2>
      <div className="overflow-x-auto border rounded-lg shadow-sm">
        <Table className="w-full border-collapse">
          <TableHeader className="bg-gray-100 text-gray-700">
            <TableRow>
              <TableHead className="px-4 py-2">User ID</TableHead>
              <TableHead className="px-4 py-2">Email</TableHead>
              <TableHead className="px-4 py-2">Name</TableHead>
              <TableHead className="px-4 py-2">Approver</TableHead>
              <TableHead className="px-4 py-2">Status</TableHead>
              <TableHead className="px-4 py-2">Approval</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {userList.map((user: PendingUser) => (
              <TableRow key={user.id} className="border-b hover:bg-gray-100">
                <TableCell className="px-4 py-2">{user.id}</TableCell>
                <TableCell className="px-4 py-2">{user.email}</TableCell>
                <TableCell className="px-4 py-2">{user.name}</TableCell>
                <TableCell className="px-4 py-2">{user.approver}</TableCell>
                <TableCell className={`px-4 py-2 font-medium ${user.status === "Approved" ? "text-green-600" : user.status === "Declined" ? "text-red-600" : "text-yellow-600"}`}>
                  {user.status}
                </TableCell>
                <TableCell className="px-4 py-2 flex gap-3">
                  {user.status === "Pending" && (
                    <>
                      <button onClick={() => handleApprove(user.id)} className="text-green-500 hover:text-green-700">
                        <CheckIcon className="h-5 w-5" />
                      </button>
                      <button onClick={() => handleDecline(user.id)} className="text-red-500 hover:text-red-700">
                        <XCircleIcon className="h-5 w-5" />
                      </button>
                    </>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}


""""