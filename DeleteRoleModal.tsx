import React, { useState } from "react";
import { Dialog, DialogContent, DialogFooter } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

interface DeleteRoleModalProps {
  isOpen: boolean;
  onClose: () => void;
  roleId: number | null;
  roleName: string;
  onRoleDeleted: (roleId: number) => void;
  accessToken: string;
}

const DeleteRoleModal: React.FC<DeleteRoleModalProps> = ({
  isOpen,
  onClose,
  roleId,
  roleName,
  onRoleDeleted,
  accessToken,
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleDelete = async () => {
    if (!roleId) return;

    setIsLoading(true);
    setErrorMessage("");

    try {
      const response = await fetch(`/admin/role/delete/${roleId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Failed to delete role");
      }

      onRoleDeleted(roleId);
      onClose();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "An error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <h2 className="text-lg font-semibold">Confirm Deletion</h2>
        <p>Are you sure you want to delete the role <strong>{roleName}</strong>?</p>

        {errorMessage && <p className="text-red-500">{errorMessage}</p>}

        <DialogFooter>
          <Button variant="outline" onClick={onClose} disabled={isLoading}>
            Cancel
          </Button>
          <Button variant="destructive" onClick={handleDelete} disabled={isLoading}>
            {isLoading ? "Deleting..." : "Delete"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default DeleteRoleModal;






const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
const [selectedRoleId, setSelectedRoleId] = useState<number | null>(null);
const [selectedRoleName, setSelectedRoleName] = useState("");





const handleDeleteClick = (role) => {
  setSelectedRoleId(role.id);
  setSelectedRoleName(role.name);
  setIsDeleteModalOpen(true);
};




const handleRoleDeleted = (deletedRoleId) => {
  set_roles_api_data((prevData) => ({
    ...prevData,
    roles: prevData.roles.filter((role) => role.id !== deletedRoleId),
  }));
};





<DeleteRoleModal
  isOpen={isDeleteModalOpen}
  onClose={() => setIsDeleteModalOpen(false)}
  roleId={selectedRoleId}
  roleName={selectedRoleName}
  onRoleDeleted={handleRoleDeleted}
  accessToken={accessToken}
/>




<Button variant="destructive" size="sm" onClick={() => handleDeleteClick(role)}>
  Delete
</Button>
