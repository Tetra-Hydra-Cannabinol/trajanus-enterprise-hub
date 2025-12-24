# Research Finding #51

**Date:** 2025-12-17 08:57
**Topic:** Electron Python subprocess security patterns
**Score:** 0.999089

---

## Command Injection in Python - Semgrep

**URL:** https://semgrep.dev/docs/cheat-sheets/python-command-injection
**Published:** Unknown date

---

## Content

Functions from the `subprocess` module have the `shell` argument for specifying if the command should be executed through the shell. Using `shell=True` is dangerous because it propagates current shell settings and variables. This means that variables, glob patterns, and other special shell features in the command string are processed before the command is run, making it much easier for a malicious actor to execute commands. The `subprocess` module allows you to start new processes, connect to [...] The `subprocess` module allows you to start new processes, connect to their input/output/error pipes, and obtain their return codes. Methods such as `Popen`, `run`, `call`, `check_call`, `check_output` are intended for running commands provided as an argument. Allowing user input in a command that is passed as an argument to one of these methods can create an opportunity for a command injection vulnerability.

Example: [...] The `asyncio.subprocess` is an async or await API to create and manage subprocesses. Such methods as `create_subprocess_shell` and Event Loop's `subprocess_shell` are intended for running shell commands provided as an argument 'cmd'. Allowing user input into a command that is passed as an argument to one of these methods can create an opportunity for a command injection vulnerability.

Example:

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:14*
