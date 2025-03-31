import React, { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { toast } from "@/components/ui/use-toast";

interface EditRoleModalProps {
  isOpen: boolean;
  onClose: () => void;
  accessToken: string;
  role: {
    id: number;
    name: string;
    entitlement?: string;
    description?: string;
  };
  onRoleUpdated: (updatedRole: any) => void;
}

const EditRoleModal: React.FC<EditRoleModalProps> = ({ isOpen, onClose, accessToken, role, onRoleUpdated }) => {
  const [name, setName] = useState(role.name);
  const [entitlement, setEntitlement] = useState(role.entitlement || "");
  const [description, setDescription] = useState(role.description || "");
  const [loading, setLoading] = useState(false);

  // Handle form submission
  const handleSubmit = async () => {
    if (!name.trim()) {
      toast({ title: "Role Name is required!", variant: "destructive" });
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`/admin/role/update/${role.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ name, entitlement, description }),
      });

      if (!response.ok) {
        throw new Error("Failed to update role");
      }

      const updatedRole = await response.json();
      toast({ title: "Role updated successfully!", variant: "success" });

      onRoleUpdated(updatedRole); // Update table
      onClose(); // Close modal
    } catch (error) {
      toast({ title: "Error updating role", description: error.message, variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Edit Role</DialogTitle>
        </DialogHeader>

        {/* Role Name */}
        <div>
          <label className="block text-sm font-medium">Role Name *</label>
          <Input value={name} onChange={(e) => setName(e.target.value)} required />
        </div>

        {/* Entitlement */}
        <div>
          <label className="block text-sm font-medium">Entitlement</label>
          <Input value={entitlement} onChange={(e) => setEntitlement(e.target.value)} />
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm font-medium">Description</label>
          <Input value={description} onChange={(e) => setDescription(e.target.value)} />
        </div>

        {/* Buttons */}
        <div className="flex justify-end gap-2">
          <Button variant="outline" onClick={onClose} disabled={loading}>Cancel</Button>
          <Button onClick={handleSubmit} disabled={loading}>
            {loading ? "Saving..." : "Save Changes"}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default EditRoleModal;