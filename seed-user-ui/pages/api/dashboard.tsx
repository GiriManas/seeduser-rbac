import { useSession } from "next-auth/react";
import React from 'react'

export default function Dashboard() {
  const { data: session } = useSession();

  if (!session) return <p>Not authenticated</p>;

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {session.user?.email}</p>
    </div>
  );
}
