export type Role = {
  id: string;
  name: string;
};

export const roles: Role[] = [
  { id: "1", name: "Developer" },
  { id: "2", name: "Validator" },
  { id: "3", name: "Gatekeeper" },
  { id: "4", name: "Proxy Gatekeeper" },
  { id: "5", name: "Validation Manager" },
  { id: "6", name: "Model Monitoring" },
];

export const allRoles = roles.map((role) => role.name);