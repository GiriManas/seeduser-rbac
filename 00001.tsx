<div className="flex flex-wrap gap-2 mt-2">
  {roles.map((role, index) => (
    <div
      key={`${role}-${index}`}
      className="flex items-center bg-blue-600 text-white rounded px-2 py-1"
    >
      <span className="mr-2">{role}</span>
      <button
        onClick={(e) => {
          e.stopPropagation(); // Prevent bubbling
          setRoles((prevRoles) => prevRoles.filter((_, i) => i !== index));
        }}
        className="hover:bg-blue-800 rounded-full px-2"
        title={`Remove ${role}`}
      >
        &minus;
      </button>
    </div>
  ))}
</div>