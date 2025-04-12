import { ReactNode } from "react";
import { MinusCircleIcon } from "@heroicons/react/24/solid";

type BadgeProps = {
  children: ReactNode;
  type?: "role" | "group";
  onRemove?: () => void;
};

export function Badge({ children, type = "role", onRemove }: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center gap-1 rounded-md px-2 py-1 text-xs font-medium 
        ${type === "role" ? "bg-blue-600 text-white" : "bg-red-600 text-white"}`}
      onClick={(e) => {
        // Prevent accidental bubbling from the span itself
        e.stopPropagation();
      }}
    >
      <span className="flex items-center gap-1">
        {type === "role" ? "🧑‍💼" : "👥"} {children}
      </span>
      {onRemove && (
        <button
          type="button"
          title="Remove"
          onClick={(e) => {
            e.stopPropagation(); // Important: prevents parent div from registering click
            onRemove();
          }}
          className="ml-1 rounded-full hover:bg-blue-800 p-1"
        >
          <MinusCircleIcon className="h-4 w-4 text-white" />
        </button>
      )}
    </span>
  );
}