{/* Roles Selection */}
<div className="block">
  <span className="text-sm font-medium">Roles</span>
  <div
    className="flex flex-wrap gap-2 mt-2"
    onClick={(e) => e.stopPropagation()} // prevent bubbling
  >
    {roles.map((role: string) => (
      <div
        key={role}
        className="bg-blue-600 text-white px-2 py-1 rounded flex items-center"
      >
        <span className="mr-2">{role}</span>
        <button
          className="text-red-300 hover:text-red-500"
          onClick={(e) => {
            e.stopPropagation();
            e.preventDefault();
            setRoles(roles.filter((r: string) => r !== role));
          }}
        >
          ❌
        </button>
      </div>
    ))}
  </div>

  {/* Add Role Dropdown */}
  <select
    className="border p-1 rounded mt-2"
    onChange={(e) => {
      const newRole = e.target.value;
      if (newRole && !roles.includes(newRole)) {
        setRoles([...roles, newRole]);
      }
    }}
  >
    <option value="">Add Role</option>
    {allRoles
      .filter((r: string) => !roles.includes(r))
      .map((role: string) => (
        <option key={role} value={role}>
          {role}
        </option>
      ))}
  </select>
</div>