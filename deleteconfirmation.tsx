// components/DeleteConfirmationDialog.tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"

type DeleteConfirmationDialogProps = {
  open: boolean;
  onConfirm: () => void;
  onCancel: () => void;
  userName?: string;
};

export function DeleteConfirmationDialog({
  open,
  onConfirm,
  onCancel,
  userName,
}: DeleteConfirmationDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onCancel}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Confirm Delete</DialogTitle>
        </DialogHeader>
        <div className="text-sm text-gray-700">
          Are you sure you want to delete <strong>{userName || "this user"}</strong>? This action cannot be undone.
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onCancel}>
            Cancel
          </Button>
          <Button variant="destructive" onClick={onConfirm}>
            Delete
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}






const [showDeleteDialog, setShowDeleteDialog] = useState(false);

const handleDeleteUser = async () => {
  try {
    await deleteUserApi(user.id); // Call your API
    toast.success("User deleted successfully");
    setShowDeleteDialog(false);
    onClose(); // Close modal if needed
  } catch (error) {
    toast.error("Failed to delete user");
  }
};



<Button
  variant="destructive"
  onClick={() => setShowDeleteDialog(true)}
>
  Delete User
</Button>



<DeleteConfirmationDialog
  open={showDeleteDialog}
  onConfirm={handleDeleteUser}
  onCancel={() => setShowDeleteDialog(false)}
  userName={user?.name}
/>