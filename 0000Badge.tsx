export function Badge({ children, type = "role", onRemove }: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center gap-1 rounded-md px-2 py-1 text-xs font-medium ${
        type === "role" ? "bg-blue-600 text-white" : "bg-red-600 text-white"
      }`}
      onClick={(e) => e.stopPropagation()} // Prevent accidental removal
    >
      <span className="flex items-center gap-1">
        {type === "role" ? "👤" : "👥"} {/* Emoji Icons */}
        {children}
      </span>
      {onRemove && (
        <button
          onClick={(e) => {
            e.stopPropagation(); // Also stop event from bubbling here
            onRemove();
          }}
          className="ml-1 rounded-full hover:bg-blue-800 p-1"
          title="Remove"
        >
          <MinusCircleIcon className="h-4 w-4 text-white" />
        </button>
      )}
    </span>
  );
}