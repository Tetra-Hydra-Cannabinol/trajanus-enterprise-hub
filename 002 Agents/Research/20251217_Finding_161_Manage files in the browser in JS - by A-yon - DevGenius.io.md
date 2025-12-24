# Research Finding #161

**Date:** 2025-12-17 08:57
**Topic:** file browser UI JavaScript implementation
**Score:** 0.53181785

---

## Manage files in the browser in JS | by A-yon - DevGenius.io

**URL:** https://blog.devgenius.io/manage-files-in-the-browser-in-js-512ec5fb3478
**Published:** Unknown date

---

## Content

Yes, you’re not misread. File system management is possible in modern browsers by JavaScript, via the File System API. However, this API is very verbose and low-level, it would be much easier if we could manipulate files as we do in Node.js. In other words, we need a higher-level API to operate on the file system. And we’ll introduce it in the following examples. [...] In the browser, the file system APIs by default use Origin Private File System, we don’t need to do anything to use it, just like in Node.js. However, as I’ve said earlier, in this article, we’re going to operate on the real file system of the computer, so we need to obtain a directory handle and pass it into the functions we’re going to use.

```
const root = await window.showDirectoryPicker()
``` [...] The browser will pop up another message box asking for permission to save changes to the `root` directory, just click `Save changes` to allow.

## Get A-yon’s stories in your inbox

Join Medium for free to get updates from this writer.

Now if I run the `readTree` function again, we’ll see something like this:

Now let’s see the real effect through the file browser.

The new folder is written to the local file system as expected.

## Create a file and read/write the content of it

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:17*
