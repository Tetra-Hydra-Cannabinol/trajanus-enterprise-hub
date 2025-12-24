# Research Finding #57

**Date:** 2025-12-17 08:57
**Topic:** IPC message validation Electron
**Score:** 0.99890983

---

## [Feature Request]: allow to validate IPC before handling it centrally

**URL:** https://github.com/electron/electron/issues/33517
**Published:** Unknown date

---

## Content

Introduce a new event in `app` that enables to `preventDefault()` the IPC handling in case validation fails. Similar to the `web-contents-created` event that allows to validate web contents and web views.

`app`
`preventDefault()`
`web-contents-created`

### Alternatives Considered

Introducing a utility method that wraps around the `ipcMain` module would be our workaround which is not so nice because it is easy to forget this utility when new code is added.

`ipcMain`

//cc @deepak1556 [...] # [Feature Request]: allow to validate IPC before handling it centrally #33517

@bpasero

## Description

@bpasero

### Preflight Checklist

### Problem Description

The new security topic  suggests to validate IPC messages. We need a way to do this validation in a central place without changing each and every IPC handler that gets installed.

### Proposed Solution [...] ## Metadata

## Metadata

### Assignees

### Labels

### Type

### Projects

### Milestone

### Relationships

### Development

## Issue actions

## Footer

### Footer navigation

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:14*
