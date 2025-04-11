import React, { useEffect, useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { modifyAdminActiveUser } from "@/lib/api";
import { ActiveUser } from "@/types/user";
import { toast } from "sonner"; // or use useToast from ShadCN

interface EditUserModalProps {
  isOpen: boolean;
  onClose: () => void;
  user: ActiveUser | null;
  session: any;
  onUserUpdated: (updatedUser: ActiveUser) => void;
}

const InfoLabel = ({ label, value }: { label: string; value: string | number | null }) => (
  <p className="text-sm text-muted-foreground">
    <strong>{label}:</strong> {value ?? "—"}
  </p>
);

export default function EditUserModal({ isOpen, onClose, user, session, onUserUpdated }: EditUserModalProps) {
  const [updatedUser, setUpdatedUser] = useState<ActiveUser | null>(null);
  const [isModified, setIsModified] = useState(false);

  useEffect(() => {
    setUpdatedUser(user);
  }, [user]);

  useEffect(() => {
    if (!user || !updatedUser) return;
    const hasChanges =
      JSON.stringify(user.role) !== JSON.stringify(updatedUser.role) ||
      JSON.stringify(user.group) !== JSON.stringify(updatedUser.group) ||
      user.au !== updatedUser.au;
    setIsModified(hasChanges);
  }, [user, updatedUser]);

  if (!updatedUser) return null;

  const handleSave = async () => {
    try {
      const response = await modifyAdminActiveUser(session.accessToken, user!, {
        role: updatedUser.role ?? [],
        group: updatedUser.group ?? [],
        au: updatedUser.au ?? "",
      });

      toast.success("User updated successfully");
      onUserUpdated(response);
      onClose();
    } catch (err) {
      toast.error("Error updating user");
    }
  };

  const handleChange = (field: "role" | "group" | "au", value: string | string[]) => {
    if (!updatedUser) return;
    setUpdatedUser((prev) =>
      prev ? { ...prev, [field]: field === "au" ? value : Array.isArray(value) ? value : value.split(",") } : prev
    );
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Edit User</DialogTitle>
        </DialogHeader>

        {/* Non-editable fields */}
        <div className="grid gap-2">
          <InfoLabel label="ID" value={user?.id} />
          <InfoLabel label="User ID" value={user?.user_id} />
          <InfoLabel label="Name" value={user?.name} />
          <InfoLabel label="Email" value={user?.email} />
          <InfoLabel label="Status" value={user?.status} />
          <InfoLabel label="Approver" value={user?.approver} />
          <InfoLabel label="Created" value={user?.created_at} />
          <InfoLabel label="Updated" value={user?.updated_at} />
        </div>

        {/* Editable Fields */}
        <div className="grid gap-4 mt-6">
          <div>
            <label className="text-sm font-medium">Roles</label>
            <Input
              value={updatedUser?.role?.join(", ") || ""}
              onChange={(e) => handleChange("role", e.target.value)}
              placeholder="Comma-separated roles"
            />
          </div>

          <div>
            <label className="text-sm font-medium">Groups</label>
            <Input
              value={updatedUser?.group?.join(", ") || ""}
              onChange={(e) => handleChange("group", e.target.value)}
              placeholder="Comma-separated groups"
            />
          </div>

          <div>
            <label className="text-sm font-medium">Accounting Unit</label>
            <Input
              value={updatedUser?.au || ""}
              onChange={(e) => handleChange("au", e.target.value)}
              placeholder="Accounting Unit"
            />
          </div>
        </div>

        <div className="mt-6 flex justify-end gap-4">
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleSave} disabled={!isModified}>Save</Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}