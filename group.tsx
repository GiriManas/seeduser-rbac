function addGroup(userId: number, newGroup: string) {
  if (!newGroup) return; // Prevent empty values
  setUserGroups((prevGroups) => ({
    ...prevGroups,
    [userId]: [...(prevGroups[userId] || []), newGroup], // Add new group
  }));
}



<TableCell className="px-4 py-2">
  <div className="flex flex-wrap gap-2">
    {userGroups[user.id]?.length > 0 ? (
      userGroups[user.id].map((group, index) => (
        <Badge key={index} type="group">
          {group}
          <button className="ml-2 text-white hover:text-gray-300" onClick={() => removeGroup(user.id, group)}>
            ❌
          </button>
        </Badge>
      ))
    ) : (
      <span className="text-gray-500 italic">No groups</span>
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
        setShowGroupDropdown(null); // Close dropdown after selection
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