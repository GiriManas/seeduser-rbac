import { useState, useEffect } from "react";
import { Badge } from "./badge"; // Ensure correct path
import type { EditUserModalProps } from "../types";

export function EditUserModal({
  isOpen,
  onClose,
  user,
  session,
  onUserUpdated,
}: EditUserModalProps) {
  const [roles, setRoles] = useState<string[]>([]);
  const [groups, setGroups] = useState<string[]>([]);
  const allRoles = ["ADMIN", "VALIDATOR", "DEVELOPER", "Role_demo_10", "role role", "ATest"];
  const allGroups = ["RMG", "TEST-GRP"];

  useEffect(() => {
    if (user) {
      setRoles(user.roles || []);
      setGroups(user.groups || []);
    }
  }, [user]);

  const handleRoleRemove = (roleToRemove: string) => {
    setRoles(roles.filter((r) => r !== roleToRemove));
  };

  const handleGroupRemove = (groupToRemove: string) => {
    setGroups(groups.filter((g) => g !== groupToRemove));
  };

  const handleAddRole = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newRole = e.target.value;
    if (newRole && !roles.includes(newRole)) {
      setRoles([...roles, newRole]);
    }
  };

  const handleAddGroup = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newGroup = e.target.value;
    if (newGroup && !groups.includes(newGroup)) {
      setGroups([...groups, newGroup]);
    }
  };

  return (
    <div className="p-4">
      {/* Roles Selection */}
      <label className="block">
        <span className="text-sm font-medium">Roles</span>
        <div className="flex flex-wrap gap-2 mt-2">
          {roles.map((role) => (
            <Badge key={role} type="role" onRemove={() => handleRoleRemove(role)}>
              {role}
            </Badge>
          ))}
        </div>
        <select
          className="border p-1 rounded mt-2"
          onChange={handleAddRole}
          value=""
        >
          <option value="">Add Role</option>
          {allRoles.filter((r) => !roles.includes(r)).map((role) => (
            <option key={role} value={role}>
              {role}
            </option>
          ))}
        </select>
      </label>

      {/* Groups Selection */}
      <label className="block mt-4">
        <span className="text-sm font-medium">Groups</span>
        <div className="flex flex-wrap gap-2 mt-2">
          {groups.map((group) => (
            <Badge key={group} type="group" onRemove={() => handleGroupRemove(group)}>
              {group}
            </Badge>
          ))}
        </div>
        <select
          className="border p-1 rounded mt-2"
          onChange={handleAddGroup}
          value=""
        >
          <option value="">Add Group</option>
          {allGroups.filter((g) => !groups.includes(g)).map((group) => (
            <option key={group} value={group}>
              {group}
            </option>
          ))}
        </select>
      </label>

      {/* Submit/Cancel buttons */}
      <div className="mt-6 flex justify-end gap-2">
        <button onClick={onClose} className="px-4 py-2 bg-gray-300 rounded">
          Cancel
        </button>
        <button
          onClick={() => {
            // Pass updated roles and groups to parent
            onUserUpdated({ ...user, roles, groups });
            onClose();
          }}
          className="px-4 py-2 bg-blue-600 text-white rounded"
        >
          Save
        </button>
      </div>
    </div>
  );
}