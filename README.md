# seeduser-rbac

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