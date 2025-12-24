# Research Finding #151

**Date:** 2025-12-17 08:57
**Topic:** Node.js Python subprocess error handling
**Score:** 0.6246834

---

## Child process | Node.js v25.2.1 Documentation

**URL:** https://nodejs.org/api/child_process.html
**Published:** Unknown date

---

## Content

- `subprocess.killed`
    - `subprocess.pid`
    - `subprocess.ref()`
    - [`subprocess.send(message[, sendHandle[, options]][, callback])`](#subprocesssendmessage-sendhandle-options-callback)
       Example: sending a server object
       Example: sending a socket object
    - `subprocess.signalCode`
    - `subprocess.spawnargs`
    - `subprocess.spawnfile`
    - `subprocess.stderr`
    - `subprocess.stdin`
    - `subprocess.stdio`
    - `subprocess.stdout`
    - `subprocess.unref()` [...] If a `callback` function is provided, it is called with the arguments `(error, stdout, stderr)`. On success, `error` will be `null`. On error, `error` will be an instance of `Error`. The `error.code` property will be the exit code of the process. By convention, any exit code other than `0` indicates an error. `error.signal` will be the signal that terminated the process. [...] const require'node:child_process' const spawn 'ps' 'ax' const spawn 'grep' 'ssh' stdout on 'data'(data) => data stdin write stderr on 'data'(data) => data console error`ps stderr: ${data}`${data} on 'close'(code) => code if 0 console log`ps process exited with code ${code}`${code} stdin end stdout on 'data'(data) => data console log toString stderr on 'data'(data) => data console error`grep stderr: ${data}`${data} on 'close'(code) => code if 0 console log`grep process exited with code

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:16*
