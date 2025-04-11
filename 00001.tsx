import { useState, useEffect } from "react";
import { ActiveUser } from "@/types";
import { modifyAdminActiveUser } from "@/api/admin";
import { toast } from "react-toastify";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface EditUserModalProps {
  isOpen: boolean;
  onClose: () => void;
  user: ActiveUser | null;
  session: any;
  onUserUpdated: (updatedUser: ActiveUser) => void;
}

export default function EditUserModal({
  isOpen,
  onClose,
  user,
  session,
  onUserUpdated,
}: EditUserModalProps) {
  const [editedUser, setEditedUser] = useState<ActiveUser | null>(user);
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    setEditedUser(user);
  }, [user]);

  if (!isOpen || !editedUser) return null;

  const handleChange = (field: keyof ActiveUser, value: any) => {
    setEditedUser((prev) => (prev ? { ...prev, [field]: value } : prev));
  };

  const handleSave = async () => {
    if (!editedUser || !session?.accessToken) return;
    setIsSaving(true);

    try {
      const response = await modifyAdminActiveUser(session.accessToken, editedUser, {
        role: editedUser.roles ?? [],
        group: editedUser.groups ?? [],
        au: editedUser.au ?? "",
      });

      if (response) {
        toast.success("User updated successfully");
        onUserUpdated(response);
        onClose();
      } else {
        toast.error("Failed to update user");
      }
    } catch (error) {
      toast.error("Something went wrong");
      console.error("Update error:", error);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white dark:bg-gray-900 rounded-lg w-full max-w-2xl p-6">
        <h2 className="text-xl font-bold mb-4">Edit User</h2>

        {/* Non-editable fields */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <InfoLabel label="ID" value={editedUser.id ?? "—"} />
          <InfoLabel label="User ID" value={editedUser.user_id ?? "—"} />
          <InfoLabel label="Name" value={editedUser.name ?? "—"} />
          <InfoLabel label="Email" value={editedUser.email ?? "—"} />
          <InfoLabel label="Status" value={editedUser.status ?? "—"} />
          <InfoLabel label="Approver" value={editedUser.approver ?? "—"} />
          <InfoLabel label="Created" value={editedUser.created_at ?? "—"} />
          <InfoLabel label="Updated" value={editedUser.updated_at ?? "—"} />
        </div>

        {/* Editable Fields */}
        <div className="space-y-4 mb-6">
          <div>
            <Label>Roles</Label>
            <div className="flex flex-wrap gap-2 mt-1">
              {editedUser.roles?.map((role, idx) => (
                <Badge key={idx} variant="secondary">{role}</Badge>
              ))}
            </div>
          </div>

          <div>
            <Label>Groups</Label>
            <div className="flex flex-wrap gap-2 mt-1">
              {editedUser.groups?.map((group, idx) => (
                <Badge key={idx} variant="secondary">{group}</Badge>
              ))}
            </div>
          </div>

          <div>
            <Label htmlFor="au">Accounting Unit</Label>
            <Input
              id="au"
              value={editedUser.au ?? ""}
              onChange={(e) => handleChange("au", e.target.value)}
              placeholder="Enter AU"
            />
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-end gap-2">
          <Button variant="outline" onClick={onClose} disabled={isSaving}>
            Cancel
          </Button>
          <Button onClick={handleSave} disabled={isSaving}>
            {isSaving ? "Saving..." : "Save"}
          </Button>
        </div>
      </div>
    </div>
  );
}

function InfoLabel({ label, value }: { label: string; value: string | number | null }) {
  return (
    <div>
      <Label className="text-muted-foreground text-xs uppercase">{label}</Label>
      <p className="text-sm font-medium">{value}</p>
    </div>
  );
}