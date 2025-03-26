<TableCell className="px-4 py-2">
  <div className="flex flex-wrap gap-2">
    {user.groups.length > 0 ? (
      user.groups.map((group, index) => (
        <Badge key={index} type="group">
          {group}
          <button className="ml-2 text-white hover:text-gray-300" onClick={() => removeGroup(user.id, group)}>
            ❌
          </button>
        </Badge>
      ))
    ) : (
      <span className="text-gray-500 italic">No groups</span> // Show placeholder if no groups
    )}

    {/* Add Group Button */}
    <button onClick={() => setShowGroupDropdown(user.id)} className="text-purple-500">
      ➕
    </button>
  </div>

  {/* Group Dropdown */}
  {showGroupDropdown === user.id && (
    <select
      onChange={(e) => {
        addGroup(user.id, e.target.value);
        setShowGroupDropdown(null);
      }}
      className="mt-2 p-1 border rounded"
    >
      <option value="">Select Group</option>
      {allGroups.map((group) => (
        <option key={group} value={group}>
          {group}
        </option>
      ))}
    </select>
  )}
</TableCell>