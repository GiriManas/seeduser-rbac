modifyAdminActiveUser(session.accessToken, user, {
  role: updatedRoles,
  group: updatedGroups,
  au: user.au ?? "",
}).then(() => {
  const updatedUser = { ...user, roles: updatedRoles };
  setUsers((prevUsers) =>
    prevUsers.map((u) =>
      u.user_id === user.user_id ? updatedUser : u
    )
  );
  setUserList((prevList) =>
    prevList.map((u) =>
      u.user_id === user.user_id ? updatedUser : u
    )
  );
});