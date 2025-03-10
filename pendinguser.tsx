export type PendingUser = {
  id: string;
  email: string;
  name: string;
  approver: string;
  status: "Pending" | "Approved" | "Declined";
};

export const pendingUsers: PendingUser[] = [
  { id: "u101", email: "alice@example.com", name: "Alice Doe", approver: "John Admin", status: "Pending" },
  { id: "u102", email: "bob@example.com", name: "Bob Smith", approver: "Sarah Manager", status: "Approved" },
  { id: "u103", email: "charlie@example.com", name: "Charlie Brown", approver: "Jane Supervisor", status: "Pending" },
  { id: "u104", email: "dave@example.com", name: "Dave Johnson", approver: "John Admin", status: "Declined" },
];


"use client";
import { useState } from "react";
import { CheckIcon, XCircleIcon, ArrowUpIcon, ArrowDownIcon } from "@heroicons/react/24/solid";
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
  const [currentPage, setCurrentPage] = useState(1);
  const usersPerPage = 10;
  const [statusFilter, setStatusFilter] = useState("All");
  const [sortColumn, setSortColumn] = useState("id");
  const [sortOrder, setSortOrder] = useState("asc");

  // 🔍 Filter Users based on Status
  const filteredUsers = userList.filter((user) =>
    statusFilter === "All" ? true : user.status === statusFilter
  );

  // 🔼🔽 Sorting Functionality
  const sortedUsers = [...filteredUsers].sort((a, b) => {
    if (sortColumn === "id") return sortOrder === "asc" ? a.id.localeCompare(b.id) : b.id.localeCompare(a.id);
    if (sortColumn === "name") return sortOrder === "asc" ? a.name.localeCompare(b.name) : b.name.localeCompare(a.name);
    if (sortColumn === "email") return sortOrder === "asc" ? a.email.localeCompare(b.email) : b.email.localeCompare(a.email);
    if (sortColumn === "approver") return sortOrder === "asc" ? a.approver.localeCompare(b.approver) : b.approver.localeCompare(a.approver);
    if (sortColumn === "status") return sortOrder === "asc" ? a.status.localeCompare(b.status) : b.status.localeCompare(a.status);
    return 0;
  });

  // 📄 **Pagination after sorting and filtering**
  const indexOfLastUser = currentPage * usersPerPage;
  const indexOfFirstUser = indexOfLastUser - usersPerPage;
  const paginatedUsers = sortedUsers.slice(indexOfFirstUser, indexOfLastUser);
  const totalPages = Math.ceil(sortedUsers.length / usersPerPage);

  function handleSort(column: string) {
    if (sortColumn === column) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortColumn(column);
      setSortOrder("asc");
    }
  }

  return (
    <div className="p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-xl font-semibold mb-4">Pending Users</h2>

      {/* 🔍 Status Filter Dropdown */}
      <select
        value={statusFilter}
        onChange={(e) => setStatusFilter(e.target.value)}
        className="p-2 border rounded mb-4"
      >
        <option value="All">All</option>
        <option value="Pending">Pending</option>
        <option value="Approved">Approved</option>
        <option value="Declined">Declined</option>
      </select>

      <div className="overflow-x-auto border rounded-lg shadow-sm">
        <Table className="w-full border-collapse">
          <TableHeader className="bg-gray-100 text-gray-700">
            <TableRow>
              <TableHead className="px-4 py-2 cursor-pointer" onClick={() => handleSort("id")}>
                User ID {sortColumn === "id" && (sortOrder === "asc" ? <ArrowUpIcon className="h-4 w-4 inline" /> : <ArrowDownIcon className="h-4 w-4 inline" />)}
              </TableHead>
              <TableHead className="px-4 py-2 cursor-pointer" onClick={() => handleSort("email")}>
                Email {sortColumn === "email" && (sortOrder === "asc" ? <ArrowUpIcon className="h-4 w-4 inline" /> : <ArrowDownIcon className="h-4 w-4 inline" />)}
              </TableHead>
              <TableHead className="px-4 py-2 cursor-pointer" onClick={() => handleSort("name")}>
                Name {sortColumn === "name" && (sortOrder === "asc" ? <ArrowUpIcon className="h-4 w-4 inline" /> : <ArrowDownIcon className="h-4 w-4 inline" />)}
              </TableHead>
              <TableHead className="px-4 py-2 cursor-pointer" onClick={() => handleSort("approver")}>
                Approver {sortColumn === "approver" && (sortOrder === "asc" ? <ArrowUpIcon className="h-4 w-4 inline" /> : <ArrowDownIcon className="h-4 w-4 inline" />)}
              </TableHead>
              <TableHead className="px-4 py-2 cursor-pointer" onClick={() => handleSort("status")}>
                Status {sortColumn === "status" && (sortOrder === "asc" ? <ArrowUpIcon className="h-4 w-4 inline" /> : <ArrowDownIcon className="h-4 w-4 inline" />)}
              </TableHead>
              <TableHead className="px-4 py-2">Approval</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {paginatedUsers.map((user: PendingUser) => (
              <TableRow key={user.id} className="border-b hover:bg-gray-100">
                <TableCell className="px-4 py-2">{user.id}</TableCell>
                <TableCell className="px-4 py-2">{user.email}</TableCell>
                <TableCell className="px-4 py-2">{user.name}</TableCell>
                <TableCell className="px-4 py-2">{user.approver}</TableCell>
                <TableCell className="px-4 py-2">{user.status}</TableCell>
                <TableCell className="px-4 py-2 flex gap-3">
                  {user.status === "Pending" && (
                    <>
                      <button className="text-green-500 hover:text-green-700">
                        <CheckIcon className="h-5 w-5" />
                      </button>
                      <button className="text-red-500 hover:text-red-700">
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