export function EditUserModal({ user, isOpen, onClose, onSave }: EditUserModalProps) {
  const [roles, setRoles] = useState(user.roles || []);
  const [groups, setGroups] = useState(user.groups || []);
  const [accountingUnit, setAccountingUnit] = useState(user.accountingUnit || "");

  function handleSave() {
    onSave({ ...user, roles, groups, accountingUnit });
    onClose();
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Edit User</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          
          {/* Roles Selection */}
          <label className="block">
            <span className="text-sm font-medium">Roles</span>
            <div className="flex flex-wrap gap-2">
              {roles.map((role) => (
                <Badge key={role} type="role">
                  {role}
                  <button className="ml-2 text-red-500" onClick={() => setRoles(roles.filter((r) => r !== role))}>
                    ❌
                  </button>
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
                {allRoles.filter((r) => !roles.includes(r)).map((role) => (
                  <option key={role} value={role}>
                    {role}
                  </option>
                ))}
              </select>
            </div>
          </label>

          {/* Groups Selection */}
          <label className="block">
            <span className="text-sm font-medium">Groups</span>
            <div className="flex flex-wrap gap-2">
              {groups.map((group) => (
                <Badge key={group} type="group">
                  {group}
                  <button className="ml-2 text-red-500" onClick={() => setGroups(groups.filter((g) => g !== group))}>
                    ❌
                  </button>
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
                {allGroups.filter((g) => !groups.includes(g)).map((group) => (
                  <option key={group} value={group}>
                    {group}
                  </option>
                ))}
              </select>
            </div>
          </label>

          {/* Accounting Unit */}
          <label className="block">
            <span className="text-sm font-medium">Accounting Unit</span>
            <input
              type="text"
              value={accountingUnit}
              onChange={(e) => setAccountingUnit(e.target.value)}
              className="w-full border rounded p-2"
            />
          </label>

        </div>
        <DialogFooter>
          <button className="bg-gray-500 text-white px-4 py-2 rounded" onClick={onClose}>
            Cancel
          </button>
          <button className="bg-blue-500 text-white px-4 py-2 rounded" onClick={handleSave}>
            Save
          </button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}