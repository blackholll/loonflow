// src/access.ts
export default function access(initialState: { currentUser?: API.CurrentUser | undefined }) {
  const { currentUser } = initialState || {};
  return {
    superAdmin: currentUser && currentUser.type_id === 2,
    workflowAdmin: currentUser && (currentUser.type_id === 1 || currentUser.type_id === 2),
  };
}
