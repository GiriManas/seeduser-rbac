<Dialog open={isOpen} onOpenChange={onClose}>
  <DialogContent className="max-h-[90vh] overflow-y-auto">
    <DialogHeader>
      <DialogTitle>Edit User</DialogTitle>
    </DialogHeader>

    <div className="space-y-2">
      <div><strong>ID:</strong> {user.id}</div>
      <div><strong>User ID:</strong> {user.user_id}</div>
      <div><strong>Name:</strong> {user.name}</div>
      <div><strong>Email:</strong> {user.email}</div>
      <div><strong>Status:</strong> {user.status}</div>
      <div><strong>Approver:</strong> {user.approver}</div>
      <div><strong>Created:</strong> {user.created_at}</div>
      <div><strong>Updated:</strong> {user.updated_at}</div>
    </div>

    {/* Existing Editable Fields follow... */}