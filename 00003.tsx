{/* Groups Selection */}
<div className="block mt-4">
  <span className="text-sm font-medium">Groups</span>
  <div
    className="flex flex-wrap gap-2 mt-2"
    onClick={(e) => e.stopPropagation()} // prevent accidental triggers
  >
    {groups.map((group: string) => (
      <div
        key={group}
        className="bg-green-600 text-white px-2 py-1 rounded flex items-center"
      >
        <span className="mr-2">{group}</span>
        <button
          className="text-red-300 hover:text-red-500"
          onClick={(e) => {
            e.stopPropagation();
            e.preventDefault();
            setGroups(groups.filter((g: string) => g !== group));
          }}
        >
          ❌
        </button>
      </div>
    ))}
  </div>

  {/* Add Group Dropdown */}
  <select
    className="border p-1 rounded mt-2"
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