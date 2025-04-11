import React, { useEffect, useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { modifyAdminActiveUser } from "@/lib/api"; // Adjust the path accordingly
import { ActiveUser } from "@/types/user"; // Adjust based on your project
import { toast } from "sonner";

interface EditUserModalProps {
  isOpen: boolean;
  onClose: () => void;
  user: ActiveUser | null;
  session: any;
  onUserUpdated: (updatedUser: ActiveUser) => void; // Callback to update table
}

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
      onUserUpdated(response); // Notify table to refresh
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
        <div className="grid gap-4">
          <Label>ID: {user?.id}</Label>
          <Label>User ID: {user?.user_id}</Label>
          <Label>Name: {user?.name}</Label>
          <Label>Email: {user?.email}</Label>
          <Label>Status: {user?.status}</Label>
          <Label>Approver: {user?.approver}</Label>
          <Label>Created: {user?.created_at}</Label>
          <Label>Updated: {user?.updated_at}</Label>
        </div>

        {/* Editable Fields */}
        <div className="grid gap-4 mt-6">
          <Label>Roles</Label>
          <Input
            value={updatedUser?.role?.join(", ") || ""}
            onChange={(e) => handleChange("role", e.target.value)}
            placeholder="Comma-separated roles"
          />

          <Label>Groups</Label>
          <Input
            value={updatedUser?.group?.join(", ") || ""}
            onChange={(e) => handleChange("group", e.target.value)}
            placeholder="Comma-separated groups"
          />

          <Label>Accounting Unit</Label>
          <Input
            value={updatedUser?.au || ""}
            onChange={(e) => handleChange("au", e.target.value)}
            placeholder="Accounting Unit"
          />
        </div>

        <div className="mt-6 flex justify-end gap-4">
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleSave} disabled={!isModified}>Save</Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}