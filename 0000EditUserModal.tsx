{/* Roles Selection */}
<label className="block">
  <span className="text-sm font-medium">Roles</span>
  <div className="flex flex-wrap gap-2 mt-2">
    {roles.map((role: string) => (
      <Badge
        key={role}
        type="role"
        onRemove={() => setRoles(roles.filter((r: string) => r !== role))}
      >
        {role}
      </Badge>
    ))}
    <select
      className="border p-1 rounded"
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
</label>

{/* Groups Selection */}
<label className="block mt-4">
  <span className="text-sm font-medium">Groups</span>
  <div className="flex flex-wrap gap-2 mt-2">
    {groups.map((group: string) => (
      <Badge
        key={group}
        type="group"
        onRemove={() => setGroups(groups.filter((g: string) => g !== group))}
      >
        {group}
      </Badge>
    ))}
    <select
      className="border p-1 rounded"
      onChange={(e) => {
        const newGroup = e.target.value;
        if (newGroup && !groups.includes(newGroup)) {
          setGroups([...groups, newGroup]);
        }
      }}
    >
      <option value="">Add Group</option>
      {allGroups
        .filter((g: string) => !groups.includes(g))
        .map((group: string) => (
          <option key={group} value={group}>
            {group}
          </option>
        ))}
    </select>
  </div>
</label>