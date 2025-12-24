# Research Finding #102

**Date:** 2025-12-17 08:57
**Topic:** resumable upload Google Drive large files
**Score:** 0.9998859

---

## Resumable uploads | Cloud Storage - Google Cloud Documentation

**URL:** https://docs.cloud.google.com/storage/docs/resumable-uploads
**Published:** Unknown date

---

## Content

By default, `UploadFile()` performs a resumable upload when the object is larger than 20 MiB. Otherwise, it performs a simple upload or multipart upload. You can configure this threshold by setting `MaximumSimpleUploadsSizeOption` when creating a `storage::Client`.

8 MiB is the default buffer size, which you can modify with the `UploadBufferSizeOption` option. [...] By default, resumable uploads occur automatically when the object size is larger than 5 MB. Otherwise, multipart uploads occur. This threshold cannot be changed. You can force a resumable upload by setting the `resumable` option in the `upload` function. [...] Resumable uploads occur when the object is larger than 8 MiB, and multipart uploads occur when the object is smaller than 8 MiB This threshold cannot be changed. The Python client library uses a buffer size that's equal to the chunk size. 100 MiB is the default buffer size used for a resumable upload, and you can change the buffer size by setting the `blob.chunk_size` property.

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:15*
