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