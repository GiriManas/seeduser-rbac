import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";

type DeleteUserDialogProps = {
  user: any; // Replace with User type if available
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
};

export function DeleteUserDialog({ user, isOpen, onClose, onConfirm }: DeleteUserDialogProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Confirm Deletion</DialogTitle>
        </DialogHeader>

        <p className="text-gray-700">Are you sure you want to delete <strong>{user?.username}</strong>? This action cannot be undone.</p>

        <DialogFooter>
          <button onClick={onClose} className="px-4 py-2 bg-gray-500 text-white rounded">Cancel</button>
          <button onClick={onConfirm} className="px-4 py-2 bg-red-500 text-white rounded">Delete</button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}