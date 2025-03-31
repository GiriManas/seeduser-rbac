const [isEditModalOpen, setEditModalOpen] = useState(false);
const [selectedRole, setSelectedRole] = useState(null);


const openEditModal = (role) => {
  setSelectedRole(role);
  setEditModalOpen(true);
};



const handleRoleUpdated = (updatedRole) => {
  set_roles_api_data((prevData) => ({
    ...prevData,
    roles: prevData.roles.map((role) =>
      role.id === updatedRole.id ? updatedRole : role
    ),
  }));
};



{isEditModalOpen && selectedRole && (
  <EditRoleModal
    isOpen={isEditModalOpen}
    onClose={() => setEditModalOpen(false)}
    accessToken={accessToken}
    role={selectedRole}
    onRoleUpdated={handleRoleUpdated}
  />
)}



<Button variant="outline" size="sm" onClick={() => openEditModal(role)}>
  Edit
</Button>
