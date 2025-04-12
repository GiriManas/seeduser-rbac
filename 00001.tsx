{/* Roles Selection */}
<label className="block">
  <span className="text-sm font-medium">Roles</span>
  <div className="flex flex-wrap gap-2 mt-2">
    {roles.map((role, index) => (
      <div
        key={`${role}-${index}`}
        className="flex items-center bg-blue-600 text-white rounded px-2 py-1 text-sm"
      >
        <span className="mr-2">{role}</span>
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            setRoles((prev) => prev.filter((_, i) => i !== index));
          }}
          className="hover:bg-blue-800 rounded-full px-2 text-white"
          title={`Remove ${role}`}
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
        setRoles([...roles, newRole]);
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