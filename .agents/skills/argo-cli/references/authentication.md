# Kubernetes token retrieval

Use the explicitly resolved Kubernetes context and token namespace on every lookup. If absent, ask for them before accessing Secrets. Context names can be listed without displaying kubeconfig credentials. Do not assume the token namespace equals the workflow or server namespace.

## Discover the account and Secret

List only Secret names, types, and service-account annotations; never print whole Secret objects. For example:

```sh
kubectl --context "$ARGO_KUBE_CONTEXT" -n "$ARGO_TOKEN_NAMESPACE" get secrets \
  -o 'custom-columns=NAME:.metadata.name,TYPE:.type,ACCOUNT:.metadata.annotations.kubernetes\.io/service-account\.name'
```

Select an existing `kubernetes.io/service-account-token` Secret associated with the intended read-only account. Do not rely on a name containing “readonly”. Inspect the account's RoleBindings and applicable ClusterRoleBindings and referenced rules when permitted, including group bindings. `kubectl auth can-i --list --as=system:serviceaccount:<namespace>:<account> -n <workflow-namespace>` can assist when impersonation is permitted; inability to impersonate is not proof the account lacks access. If permissions cannot be established, report the gap and ask the user to identify the approved read-only account. Never test read-only status by attempting a write.

If several candidates remain, ask which account to use. If the Secret is missing, empty, or unreadable, ask the user to correct the context/namespace/account as needed. Kubernetes may not have created a persistent service-account token Secret. Do not create Secrets, mint tokens, modify RBAC, or substitute privileged credentials as an automatic fallback.

## Extract without exposing

Run extraction and the consuming command in the same shell or subprocess environment. Disable shell tracing before extraction. Use pipeline failure handling; require nonempty decoded bytes before prefixing with `Bearer `. Do not echo the token, use a token CLI argument, or enable HTTP/header debug logging. Clear transient variables when finished. Retrieve it again in a later process if needed instead of saving it to disk.

The following fallback command is for the user to run locally when agent retrieval cannot work. Fill in confirmed non-secret values, or clearly mark unresolved placeholders. It captures the token without printing it; never ask the user to paste its value back into chat.

```sh
set +x
set -o pipefail
ARGO_KUBE_CONTEXT='YOUR_CONTEXT'
ARGO_TOKEN_NAMESPACE='TOKEN_NAMESPACE'
ARGO_TOKEN_SECRET='READ_ONLY_TOKEN_SECRET'
if argo_token_value="$(kubectl --context "$ARGO_KUBE_CONTEXT" \
  -n "$ARGO_TOKEN_NAMESPACE" get secret "$ARGO_TOKEN_SECRET" \
  -o jsonpath='{.data.token}' | base64 --decode)" && [ -n "$argo_token_value" ]; then
  export ARGO_TOKEN="Bearer $argo_token_value"
else
  unset ARGO_TOKEN
  printf '%s\n' 'Token retrieval failed; check context, namespace, Secret, and permissions.' >&2
fi
unset argo_token_value
```

Check the platform's decoder syntax; use `base64 -D` if its implementation does not support `--decode`. This example targets bash/zsh. Adapt explicitly for other shells.

For authenticated HTTP probes, pass the Authorization header through stdin (for example `curl --header @-`) using a shell builtin to supply the variable, not a token-bearing command argument. Use finite connect/total timeouts and no redirect following. Verify the chosen Argo endpoint before transmitting credentials. A 401 suggests an invalid/expired token or incompatible server auth mode; a 403 suggests insufficient permission. Diagnose those without repeatedly retrying or requesting pasted credentials.

Source: [Argo access tokens](https://argo-workflows.readthedocs.io/en/latest/access-token/). Use its service-account Secret model, but do not copy its token-printing example or create its sample RBAC as part of retrieval.
