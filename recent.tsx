useEffect(() => {
  setRoles(user.roles || []);
  setGroups(user.groups || []);
  setAccountingUnit(user.accountingUnit || "");
}, [user]); // Re-run when `user` changes