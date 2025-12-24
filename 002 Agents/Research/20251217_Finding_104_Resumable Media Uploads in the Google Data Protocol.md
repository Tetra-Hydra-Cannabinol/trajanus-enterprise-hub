# Research Finding #104

**Date:** 2025-12-17 08:57
**Topic:** resumable upload Google Drive large files
**Score:** 0.9996458

---

## Resumable Media Uploads in the Google Data Protocol

**URL:** https://developers.google.com/gdata/docs/resumable_upload
**Published:** Unknown date

---

## Content

To initiate a resumable upload session, send an HTTP `POST` request to the resumable-post link. This link is found at the feed level.
The DocList API's resumable-post link looks like:

`POST`

The body of your `POST` request should be empty or contain an Atom XML entry and must not include the actual file contents.
The example below creates a resumable request to upload a large PDF, and includes a title for the future document using the
`Slug` header.

`POST`
`Slug` [...] Current web standards provide no reliable mechanism to facilitate the HTTP upload of large files. As a result, file uploads at Google and other sites have traditionally been limited to moderate sizes (e.g. 100 MB). For services like the YouTube and the Google Documents List APIs which support large file uploads, this presents a major hurdle. [...] // Create {@link ResumableGDataFileUploader} for each file to upload
List uploaders = Lists.newArrayList();

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:15*
