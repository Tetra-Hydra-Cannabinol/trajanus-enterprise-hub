# Research Finding #66

**Date:** 2025-12-17 08:57
**Topic:** Python stdout parsing Electron reliable
**Score:** 0.32283598

---

## ways to build a desktop app with electron and python - Adarsha Regmi

**URL:** https://adarsharegmi121.medium.com/ways-to-build-a-desktop-app-with-electron-and-python-b0b31217688c
**Published:** Unknown date

---

## Content

function sendToPython() { var python = require('child_process').spawn('python', ['./py/calc.py', input.value]); python.stdout.on('data', function (data) { console.log("Python response: ", data.toString('utf8')); result.textContent = data.toString('utf8'); }); python.stderr.on('data', (data) => { console.error(`stderr: ${data}`); }); python.on('close', (code) => { console.log(`child process exited with code ${code}`); });}btn.addEventListener('click', () => { [...] b) using python-shell

`python-shell` is an npm package that provides an easy way to run Python scripts from Node.js with basic and efficient inter-process communication and error handling.

You can use `python-shell` for:

 Spawning Python scripts,
 Switching between text, JSON and binary modes,
 Doing data transfers through `stdin` and `stdout` streams,
 Getting stack traces in case of errors. [...] sendToPython();});btn.dispatchEvent(new Event('click'));

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:14*
