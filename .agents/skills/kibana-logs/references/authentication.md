# Import and refresh browser cookies

The user has authorized the agent to manage a local cookie file. Ask them to sign in to Kibana, open DevTools → Network, refresh, select a successful request to the exact Kibana host, and copy the Cookie request-header value. Copy all cookie fragments (including both AWS load-balancer session cookie parts). Do not use `document.cookie`, which omits HttpOnly credentials.

Run the helper from this skill's directory. It requires Python 3.8+ and has no package dependencies.

```sh
python3 scripts/import_cookies.py --prompt
```

Use `--prompt` only in a user-accessible terminal where the user can type without their input being captured by the agent as a message. An agent-only PTY is not sufficient. Open the terminal panel if supported; tell the user to paste at the hidden prompt. Do not relay cookie text through tool-call arguments, shell history, chat, or a question tool.

If an interactive terminal is unavailable, on macOS ask the user to copy the header and confirm that it is ready; then run:

```sh
python3 scripts/import_cookies.py --clipboard
```

This consumes the clipboard directly into the private file without showing it to the agent. Do not read the clipboard separately or poll it. Tell the user they can clear the clipboard after import. On other systems, offer a private local file-entry surface and run `--stdin` with that file redirected to stdin; remove the temporary credential file after successful import. Do not ask the user to run Python. If no safe input surface is available, explain that limitation instead of requesting a chat paste.

Default output: `~/.config/kibana/cookies.txt`. Existing files are replaced atomically after validation with mode 0600. The helper restricts cookies to the exact host over HTTPS and synthesizes session-cookie metadata from a Cookie header; it cannot recover original expiry/path attributes. The server still controls session expiry. For a different host use `--host` and a separate `--output`; never reuse this host's credentials elsewhere.

After import, validate with the selected Space's data-view request. Check status and JSON; file creation alone does not prove login success. Do not automatically reimport a stale clipboard when validation fails. Ask the user to sign in again and copy a fresh header, with at most one refresh/retry per failed query.

Sources: [curl cookie format](https://curl.se/docs/http-cookies.html), [DevTools Network reference](https://developer.chrome.com/docs/devtools/network/reference/).
