# Research Finding #91

**Date:** 2025-12-17 08:57
**Topic:** Google Drive API rate limits per user
**Score:** 0.8851659

---

## What is the limit on Google Drive API usage? - Stack Overflow

**URL:** https://stackoverflow.com/questions/10311969/what-is-the-limit-on-google-drive-api-usage
**Published:** Unknown date

---

## Content

After you've enabled the Drive API you can also set a per user rate limit (by default 1000 req per 100 sec) to prevent one user from depleting your app's quota. That's available in the "Quotas" tab.

There is also a link to request more quota in the "Quotas" tab in case you need more than the default 10M req/day such requests will go through a (light) manual review process. [...] answered Sep 21, 2017 at 13:17

snickers2k

41433 silver badges55 bronze badges

## Comments

3

I seen the free request quota as for Google Drive Api's is. 1,000,000,000 requests/day.

and Default Per-user limit is:(you can increase it) 10 requests/second/user

you can visit this and login with valid account for more information 

Share

Improve this answer

answered Sep 14, 2015 at 9:23

Mahadev Bichewar

4944 bronze badges

## Comments

3 [...] ## 7 Answers 7

Reset to default

79

To view your allowed quota please create a project in the Google APIs Console. In the "Service" tab, the default quota allowed for each service is indicated.

Currently for the Drive API it reads "Courtesy limit: 1,000,000,000 queries/day". It's a per app quota.

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:15*
