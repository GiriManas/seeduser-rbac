import React, { useEffect, useState } from "react";
import { Modal, Button } from "@/components/ui"; // adjust path as needed
import { ActiveUser } from "@/types"; // your user type
import { modifyAdminActiveUser } from "@/api";
import { toast } from "react-toastify";
import { Badge } from "@/components/ui/badge"; // Ensure this is correctly imported
import InfoLabel from "@/components/custom/InfoLabel"; // Optional label component

type EditUserModalProps = {
  user: ActiveUser;
  isOpen: boolean;
  onClose: () => void;
  onUserUpdated: (user: ActiveUser) => void;
};

const EditUserModal: React.FC<EditUserModalProps> = ({
  user,
  isOpen,
  onClose,
  onUserUpdated,
}) => {
  const [editableUser, setEditableUser] = useState<ActiveUser>(user);
  const [isChanged, setIsChanged] = useState(false);

  useEffect(() => {
    setEditableUser(user);
    setIsChanged(false);
  }, [user]);

  useEffect(() => {
    const hasChanged =
      editableUser.role !== user.role ||
      editableUser.group !== user.group ||
      editableUser.au !== user.au;
    setIsChanged(hasChanged);
  }, [editableUser, user]);

  const handleSave = async () => {
    try {
      const payload = {
        role: editableUser.role,
        group: editableUser.group,
        au: editableUser.au,
      };

      const response = await modifyAdminActiveUser(null, editableUser, payload);

      if (response) {
        toast.success("User updated successfully!");
        onUserUpdated(response);
        onClose();
      }
    } catch (err) {
      toast.error("Failed to update user.");
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Edit User">
      <div className="space-y-4 p-4">

        <InfoLabel label="ID" value={user?.id ?? "-"} />
        <InfoLabel label="Email" value={user?.email ?? "-"} />
        <InfoLabel label="Name" value={user?.name ?? "-"} />

        {/* Display Roles as badges */}
        <div>
          <label className="text-sm font-medium">Roles</label>
          <div className="flex flex-wrap gap-2 mt-1">
            {editableUser?.role?.length > 0 ? (
              editableUser.role.map((role: string, idx: number) => (
                <Badge key={idx} variant="default">
                  {role}
                </Badge>
              ))
            ) : (
              <p className="text-sm text-muted-foreground">No roles assigned</p>
            )}
          </div>
        </div>

        {/* Display Groups as badges */}
        <div>
          <label className="text-sm font-medium">Groups</label>
          <div className="flex flex-wrap gap-2 mt-1">
            {editableUser?.group?.length > 0 ? (
              editableUser.group.map((group: string, idx: number) => (
                <Badge key={idx} variant="secondary">
                  {group}
                </Badge>
              ))
            ) : (
              <p className="text-sm text-muted-foreground">No groups assigned</p>
            )}
          </div>
        </div>

        {/* Accounting Unit */}
        <InfoLabel label="Accounting Unit" value={editableUser?.au ?? "-"} />

        <div className="mt-6 flex justify-end gap-3">
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button disabled={!isChanged} onClick={handleSave}>
            Save
          </Button>
        </div>
      </div>
    </Modal>
  );
};

export default EditUserModal;