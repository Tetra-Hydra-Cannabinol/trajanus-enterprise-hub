# Research Finding #101

**Date:** 2025-12-17 08:57
**Topic:** resumable upload Google Drive large files
**Score:** 0.9998859

---

## Upload file data | Google Drive

**URL:** https://developers.google.com/workspace/drive/api/guides/manage-uploads
**Published:** Unknown date

---

## Content

Resumable upload (`uploadType=resumable`): Use this upload type for large files (greater than 5 MB) and when there's a high chance of network interruption, such as when creating a file from a mobile app. Resumable uploads are also a good choice for most applications because they also work for small files at a minimal cost of one additional HTTP request per upload. To perform a resumable upload, refer to Perform a resumable upload. [...] 1. Create a `PUT` request to the resumable session URI.
2. Add the chunk's data to the request body. Create chunks in multiples of 256 KB (256 x 1024 bytes) in size, except for the final chunk that completes the upload. Keep the chunk size as large as possible so that the upload is efficient.
3. Add these HTTP headers: [...] 1. Send the initial request and retrieve the resumable session URI.
2. Upload the data and monitor upload state.
3. (optional) If the upload is disturbed, resume the upload.

### Send the initial request

To initiate a resumable upload, use the `create` method on the `files` resource with `uploadType=resumable`.

### HTTP

1. Create a `POST` request to the method's /upload URI with the query parameter of `uploadType=resumable`:

   `POST

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:15*
