# Research Finding #92

**Date:** 2025-12-17 08:57
**Topic:** Google Drive API rate limits per user
**Score:** 0.7598145

---

## Usage limits | Google Drive

**URL:** https://developers.google.com/workspace/drive/api/guides/limits
**Published:** Unknown date

---

## Content

| Queries | |  |  |  --- | | Per 60 seconds | 12,000 | | Per 60 seconds per user | 12,000 | |

## Resolve time-based quota errors

For all time-based errors (maximum of N requests per X minutes), we recommend your code catches the exception and uses a truncated exponential backoff to make sure your devices don't generate excessive load. [...] If you exceed a quota, you'll receive a `403: User rate limit exceeded` HTTP status code response. Additional rate limit checks on the Drive backend might also generate a `429: Too many requests` response. If this happens, you should use an exponential backoff algorithm and try again later. Provided you stay within the per-minute quotas below, there's no limit to the number of requests you can make per day.

The following table details the query limits:

| Quotas | [...] As the Google Drive API is a shared service, we apply quotas and limitations to make sure it's used fairly by all users and to protect the overall performance of the Google Workspace system.

Notifications delivered to the address specified when opening a notification channel don't count against your quota limits. However, calls to the `changes.watch`, `channels.stop`, and `files.watch` methods do count against your quota.

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:15*
