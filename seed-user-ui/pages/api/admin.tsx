import { useSession } from "next-auth/react";
import React from 'react'


export default function AdminPage() {
  const { data: session } = useSession();

  if (!session) return <p>Access Denied</p>;

  return (
    <div>
      <h1>Admin Panel</h1>
      <p>Welcome, {session.user?.role}!</p>
    </div>
  );
}
