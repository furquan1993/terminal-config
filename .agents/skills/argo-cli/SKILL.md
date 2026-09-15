---
name: argo-cli
description: Use whenever an Argo Workflows CLI interaction is needed, including installing argo, connecting to Argo Server, finding read-only Kubernetes tokens, inspecting workflows and logs, and managing workflows, templates, schedules, artifacts, or archives. Load before running argo commands. This skill covers Argo Workflows, not the separate Argo CD argocd CLI.
---

# Argo CLI

Use the native `argo` CLI through Argo Server. Complete setup below before operational commands. Local help, version checks, and linting do not require a running server.

## Setup and connection

1. Check `command -v argo`. If missing, suggest installation and identify OS and architecture. On macOS with Homebrew, suggest `brew install argo`; otherwise consult the official [CLI installation instructions](https://argo-workflows.readthedocs.io/en/latest/walk-through/argo-cli/) for an appropriate release binary. Install when authorized, then verify `argo version --short`. If present, reuse it without reinstalling or upgrading. Read installed subcommand help for supported flags.
2. Resolve the Kubernetes context and token namespace from the user or established session context. Ask for missing values; a machine's current context alone is not confirmation of the intended cluster. Keep token namespace, Argo Server namespace, and workflow namespace distinct when they differ. Do not ask the user to paste a token.
3. Use a supplied Argo Server host and port, otherwise existing non-secret `ARGO_SERVER`, otherwise **localhost:2746**. Normalize the CLI address to `host:port`; preserve a supplied ingress base path separately. All operational invocations use **plain HTTP**, HTTP/1, and the insecure flag: `--argo-http1 --secure=false --insecure-skip-verify`. The insecure flag alone does not select HTTP or make a TLS-only server accept plaintext.
4. Before each operational invocation, perform a bounded HTTP probe of the selected endpoint (for example `/api/v1/info`, including any base path). Require recognizable Argo API JSON rather than accepting any listening TCP port or HTML page as Argo. A 401/403 means authentication needs resolution; it is not proof of an available authorized Argo connection. Never follow redirects with credentials to another endpoint. Do not send a token to an unidentified service.
5. If unreachable, suggest the user open a port-forward or supply the correct host and port. Discover the server Service and port using the confirmed Kubernetes context and server namespace before producing an exact command, such as `kubectl --context "$ARGO_KUBE_CONTEXT" -n "$ARGO_SERVER_NAMESPACE" port-forward --address 127.0.0.1 svc/"$ARGO_SERVICE" 2746:"$ARGO_SERVICE_PORT"`. Check that the local port is free before starting a forward; do not kill an existing listener. Start a forward only if requested, retain its process handle, then recheck connectivity. Port-forwarding does not convert HTTPS to HTTP; if the server is TLS-only, report the mismatch and ask for a compatible endpoint or revised transport preference.
6. Follow [Kubernetes token retrieval](references/authentication.md) to obtain the existing read-only token, then verify authenticated read access. Keep the token in process memory/environment, out of command arguments, logs, chat, files, shell startup configuration, and Git.

Use this command shape after setup, with the token provided through `ARGO_TOKEN` and the workflow namespace explicitly set:

```sh
argo --argo-server "$ARGO_SERVER" --namespace "$ARGO_WORKFLOW_NAMESPACE" \
  --argo-http1 --secure=false --insecure-skip-verify \
  --request-timeout 15s list
```

Do not silently fall back to direct Kubernetes API mode. Use `kubectl` for credential discovery, port-forwarding, and supporting pod/event diagnostics. Set any environment overrides per process, preserving the user's global configuration.

## Workflows and other resources

- Inspect with scoped `list`, `get -o json` or `-o yaml`, and filtered `logs`. Resolve “latest” to a concrete workflow name before changing anything. Avoid exposing secrets embedded in parameters or logs.
- Use `template`, `cluster-template`, `cron`, `archive`, and `cp` as appropriate; read their help. ClusterWorkflowTemplates are cluster-scoped; archived workflows may require an archive ID rather than a live workflow name.
- Read-only credentials support inspection. For requested writes, explain the access requirement and obtain separately authorized credentials through the same Kubernetes lookup flow; never silently substitute a more privileged account or use Kubernetes credentials to bypass the restriction.
- Lint new or edited manifests before submitting. Capture the workflow name returned by `submit` or `resubmit` for verification.
- `retry` reruns failed steps in the same workflow; `resubmit` creates a new run. Successful-node restarts and parameter changes must match the request.
- `stop` allows exit handlers; `terminate` skips them. Clarify ambiguous cancellation intent when cleanup matters. Suspend/resume and cron changes must target the intended resource.
- Preview exact targets before bulk actions. Existing user authorization is sufficient for its stated scope; do not add routine confirmations. Do not widen namespaces, add `--all`, or delete resources as troubleshooting shortcuts.
- After uncertain mutation responses, inspect state before retrying to avoid duplicate runs. Stop and report uncertainty if the outcome cannot be resolved.

## Verify and report

Read back the exact resource with the same connection and namespace. Distinguish accepted, running, succeeded, and failed. Use bounded polling or resumable waits; request timeout does not bound the entire workflow duration. Report the target, action, observed result, and remaining blocker.

Use installed help and the version-appropriate [official CLI reference](https://argo-workflows.readthedocs.io/en/latest/cli/argo/) for unfamiliar commands.
