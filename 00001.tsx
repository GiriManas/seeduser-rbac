<label className="block">
  <span className="text-sm font-medium">Roles</span>
  <div className="flex flex-wrap gap-2 mt-2">
    {roles.map((role, index) => (
      <div
        key={`${role}-${index}`}
        className="flex items-center bg-blue-600 text-white rounded-md px-2 py-1 text-xs font-medium shadow-sm"
      >
        <span>{role}</span>
        <button
          type="button"
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            setRoles((prevRoles) => prevRoles.filter((_, i) => i !== index));
          }}
          className="ml-2 text-white hover:text-red-300 focus:outline-none"
          title="Remove Role"
        >
          &minus;
        </button>
      </div>
    ))}
  </div>

  <select
    className="mt-2 border p-1 rounded"
    onChange={(e) => {
      const newRole = e.target.value;
      if (newRole && !roles.includes(newRole)) {
        setRoles((prev) => [...prev, newRole]);
      }
    }}
  >
    <option value="">Add Role</option>
    {allRoles
      .filter((r) => !roles.includes(r))
      .map((role) => (
        <option key={role} value={role}>
          {role}
        </option>
      ))}
  </select>
</label>