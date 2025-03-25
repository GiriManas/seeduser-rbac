import { ReactNode } from "react";

type BadgeProps = {
  children: ReactNode;
  type?: "role" | "group";
  onRemove?: () => void; // 🔴 Function to remove the role
};

export function Badge({ children, type, onRemove }: BadgeProps) {
  return (
    <span className={`inline-flex items-center gap-1 rounded-md px-2 py-1 text-xs font-medium
      ${type === "role" ? "bg-blue-500 text-white" : "bg-red-500 text-white"}`}
    >
      {type === "role" ? "👤" : "👥"} {/* Unicode Icon */}
      {children}
      {onRemove && (
        <button onClick={onRemove} className="ml-1 text-white hover:text-gray-300">
          ❌ {/* Remove Role Button */}
        </button>
      )}
    </span>
  );
}