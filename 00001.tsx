function addRole(user: ActiveUser, newRole: string) {
  const existingRoles = user.roles ?? [];
  const updatedRoles = existingRoles.includes(newRole)
    ? existingRoles
    : [...existingRoles, newRole];

  const updatedGroups = user.groups ?? [];

  modifyAdminActiveUser(session.accessToken, user.user_id, {
    roles: updatedRoles,
    groups: updatedGroups,
    au: user.au ?? "",
  }).then(() => {
    setUsers((prevUsers) =>
      prevUsers.map((u) =>
        u.user_id === user.user_id
          ? { ...u, roles: updatedRoles }
          : u
      )
    );
  });
}

function removeRole(user: ActiveUser, roleToRemove: string) {
  const existingRoles = user.roles ?? [];
  const updatedRoles = existingRoles.filter(role => role !== roleToRemove);
  const updatedGroups = user.groups ?? [];

  modifyAdminActiveUser(session.accessToken, user.user_id, {
    roles: updatedRoles,
    groups: updatedGroups,
    au: user.au ?? "",
  }).then(() => {
    setUsers((prevUsers) =>
      prevUsers.map((u) =>
        u.user_id === user.user_id
          ? { ...u, roles: updatedRoles }
          : u
      )
    );
  });
}


function addGroup(user: ActiveUser, newGroup: string) {
  const existingGroups = user.groups ?? [];
  const updatedGroups = existingGroups.includes(newGroup)
    ? existingGroups
    : [...existingGroups, newGroup];

  const updatedRoles = user.roles ?? [];

  modifyAdminActiveUser(session.accessToken, user.user_id, {
    roles: updatedRoles,
    groups: updatedGroups,
    au: user.au ?? "",
  }).then(() => {
    setUsers((prevUsers) =>
      prevUsers.map((u) =>
        u.user_id === user.user_id
          ? { ...u, groups: updatedGroups }
          : u
      )
    );
  });
}

function removeGroup(user: ActiveUser, groupToRemove: string) {
  const existingGroups = user.groups ?? [];
  const updatedGroups = existingGroups.filter(group => group !== groupToRemove);
  const updatedRoles = user.roles ?? [];

  modifyAdminActiveUser(session.accessToken, user.user_id, {
    roles: updatedRoles,
    groups: updatedGroups,
    au: user.au ?? "",
  }).then(() => {
    setUsers((prevUsers) =>
      prevUsers.map((u) =>
        u.user_id === user.user_id
          ? { ...u, groups: updatedGroups }
          : u
      )
    );
  });
}

