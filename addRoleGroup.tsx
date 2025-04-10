function addRole(user: ActiveUser, newRole: string) {
  setUserRoles((prevRoles) => {
    const updatedRoles = prevRoles[user.user_id]?.includes(newRole)
      ? prevRoles[user.user_id]
      : [...(prevRoles[user.user_id] || []), newRole];

    // Call API to persist update
    modifyAdminActiveUser(session.accessToken, user, {
      roles: updatedRoles,
      groups: userGroups[user.user_id] || [],
      au: user.au,
    });

    return {
      ...prevRoles,
      [user.user_id]: updatedRoles,
    };
  });
}


function removeRole(user: ActiveUser, roleToRemove: string) {
  setUserRoles((prevRoles) => {
    const updatedRoles = (prevRoles[user.user_id] || []).filter((r) => r !== roleToRemove);

    modifyAdminActiveUser(session.accessToken, user, {
      roles: updatedRoles,
      groups: userGroups[user.user_id] || [],
      au: user.au,
    });

    return {
      ...prevRoles,
      [user.user_id]: updatedRoles,
    };
  });
}



function addGroup(user: ActiveUser, newGroup: string) {
  setUserGroups((prevGroups) => {
    const updatedGroups = prevGroups[user.user_id]?.includes(newGroup)
      ? prevGroups[user.user_id]
      : [...(prevGroups[user.user_id] || []), newGroup];

    modifyAdminActiveUser(session.accessToken, user, {
      roles: userRoles[user.user_id] || [],
      groups: updatedGroups,
      au: user.au,
    });

    return {
      ...prevGroups,
      [user.user_id]: updatedGroups,
    };
  });
}



function removeGroup(user: ActiveUser, groupToRemove: string) {
  setUserGroups((prevGroups) => {
    const updatedGroups = (prevGroups[user.user_id] || []).filter((g) => g !== groupToRemove);

    modifyAdminActiveUser(session.accessToken, user, {
      roles: userRoles[user.user_id] || [],
      groups: updatedGroups,
      au: user.au,
    });

    return {
      ...prevGroups,
      [user.user_id]: updatedGroups,
    };
  });
}



