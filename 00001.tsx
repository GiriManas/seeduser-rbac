function addRole(user: ActiveUser, newRole: string) {
  const existingRoles = user.roles ?? [];
  const updatedRoles = existingRoles.includes(newRole)
    ? existingRoles
    : [...existingRoles, newRole];

  const updatedGroups = user.groups ?? [];

  setUserRoles((prevRoles) => ({
    ...prevRoles,
    [user.user_id]: updatedRoles,
  }));

  modifyAdminActiveUser(session.accessToken, user.user_id, {
    roles: updatedRoles,
    groups: updatedGroups,
    au: user.au ?? "",
  });
}

function removeRole(user: ActiveUser, roleToRemove: string) {
  const existingRoles = user.roles ?? [];
  const updatedRoles = existingRoles.filter((role) => role !== roleToRemove);
  const updatedGroups = user.groups ?? [];

  setUserRoles((prevRoles) => ({
    ...prevRoles,
    [user.user_id]: updatedRoles,
  }));

  modifyAdminActiveUser(session.accessToken, user.user_id, {
    roles: updatedRoles,
    groups: updatedGroups,
    au: user.au ?? "",
  });
}

function addGroup(user: ActiveUser, newGroup: string) {
  const existingGroups = user.groups ?? [];
  const updatedGroups = existingGroups.includes(newGroup)
    ? existingGroups
    : [...existingGroups, newGroup];

  const updatedRoles = user.roles ?? [];

  setUserGroups((prevGroups) => ({
    ...prevGroups,
    [user.user_id]: updatedGroups,
  }));

  modifyAdminActiveUser(session.accessToken, user.user_id, {
    roles: updatedRoles,
    groups: updatedGroups,
    au: user.au ?? "",
  });
}

function removeGroup(user: ActiveUser, groupToRemove: string) {
  const existingGroups = user.groups ?? [];
  const updatedGroups = existingGroups.filter((group) => group !== groupToRemove);
  const updatedRoles = user.roles ?? [];

  setUserGroups((prevGroups) => ({
    ...prevGroups,
    [user.user_id]: updatedGroups,
  }));

  modifyAdminActiveUser(session.accessToken, user.user_id, {
    roles: updatedRoles,
    groups: updatedGroups,
    au: user.au ?? "",
  });
}