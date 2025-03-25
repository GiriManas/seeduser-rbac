import { useState } from "react";
import { PlusCircleIcon, MinusCircleIcon } from "@heroicons/react/24/solid";
import { users, User, allRoles } from "@/data/users"; // Ensure `allRoles` is an array of all available roles

export default function UserTable() {
  const [userRoles, setUserRoles] = useState(
    users.reduce((acc, user) => ({ ...acc, [user.id]: user.roles }), {})
  );

  function addRole(userId: string, newRole: string) {
    setUserRoles((prevRoles) => ({
      ...prevRoles,
      [userId]: [...prevRoles[userId], newRole],
    }));
  }

  function removeRole(userId: string, roleToRemove: string) {
    setUserRoles((prevRoles) => ({
      ...prevRoles,
      [userId]: prevRoles[userId].filter((role) => role !== roleToRemove),
    }));
  }












Modify the Roles Column inside the HTML

<TableCell className="px-4 py-2">
  <div className="flex flex-wrap gap-2">
    {userRoles[user.id].map((role, index) => (
      <div key={index} className="flex items-center gap-1 bg-blue-500 text-white px-2 py-1 rounded">
        <span>{role}</span>
        <button onClick={() => removeRole(user.id, role)} className="text-red-500">
          <MinusCircleIcon className="h-4 w-4" />
        </button>
      </div>
    ))}
    <button onClick={() => setShowDropdown(user.id)} className="text-green-500">
      <PlusCircleIcon className="h-5 w-5" />
    </button>
  </div>

  {showDropdown === user.id && (
    <select
      onChange={(e) => {
        addRole(user.id, e.target.value);
        setShowDropdown(null);
      }}
      className="mt-2 p-1 border rounded"
    >
      <option value="">Select Role</option>
      {allRoles.map((role) => (
        <option key={role} value={role}>
          {role}
        </option>
      ))}
    </select>
  )}
</TableCell>
