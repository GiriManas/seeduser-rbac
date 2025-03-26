const [userGroups, setUserGroups] = useState<{ [key: string]: string[] }>({});
const [showGroupDropdown, setShowGroupDropdown] = useState<string | null>(null);



const addGroup = (userId: string, newGroup: string) => {
  setUserGroups((prevGroups) => ({
    ...prevGroups,
    [userId]: [...(prevGroups[userId] || []), newGroup],
  }));
};

const removeGroup = (userId: string, groupToRemove: string) => {
  setUserGroups((prevGroups) => ({
    ...prevGroups,
    [userId]: prevGroups[userId]?.filter((group) => group !== groupToRemove) || [],
  }));
};



<TableCell className="px-4 py-2">
  <div className="flex flex-wrap gap-2">
    {userGroups[user.id]?.map((group, index) => (
      <Badge key={index} type="group">
        {group}
        <button className="ml-2 text-red-500" onClick={() => removeGroup(user.id, group)}>
          ❌
        </button>
      </Badge>
    ))}

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