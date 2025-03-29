import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";

{isAddRoleModalOpen && (
  <Dialog open={isAddRoleModalOpen} onOpenChange={setIsAddRoleModalOpen}>
    <DialogContent>
      <DialogHeader>
        <DialogTitle>Add New Role</DialogTitle>
      </DialogHeader>
      <div>
        {/* Role Name Input */}
        <input
          type="text"
          placeholder="Enter Role Name"
          className="w-full p-2 border rounded"
        />
      </div>
      <DialogFooter>
        <Button variant="outline" onClick={() => setIsAddRoleModalOpen(false)}>
          Cancel
        </Button>
        <Button onClick={() => console.log("Submit Role")}>Save</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
)}