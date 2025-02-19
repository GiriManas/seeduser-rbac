import { useSession, signIn, signOut } from "next-auth/react";
import Link from "next/link";

export default function Home() {
  const { data: session } = useSession();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-3xl font-bold">Welcome to the NextAuth + FastAPI App</h1>

      {session ? (
        <>
          <p className="mt-4">Signed in as {session.user?.email}</p>
          <p>Role: {session.user?.role}</p>
          <button className="mt-2 px-4 py-2 bg-red-500 text-white" onClick={() => signOut()}>
            Sign Out
          </button>
          <div className="mt-4">
            <Link href="/dashboard" className="text-blue-500">
              Go to Dashboard
            </Link>
            <br />
            {session.user?.role === "admin" && (
              <Link href="/admin" className="text-green-500">
                Go to Admin Panel
              </Link>
            )}
          </div>
        </>
      ) : (
        <>
          <p className="mt-4">You are not signed in.</p>
          <button className="mt-2 px-4 py-2 bg-blue-500 text-white" onClick={() => signIn()}>
            Sign In
          </button>
        </>
      )}
    </div>
  );
}
