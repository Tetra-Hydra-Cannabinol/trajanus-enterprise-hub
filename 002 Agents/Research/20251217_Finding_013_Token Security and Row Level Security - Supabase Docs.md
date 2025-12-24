# Research Finding #13

**Date:** 2025-12-17 08:57
**Topic:** Supabase RLS policies for multi-user apps
**Score:** 0.735737

---

## Token Security and Row Level Security | Supabase Docs

**URL:** https://supabase.com/docs/guides/auth/oauth-server/token-security
**Published:** Unknown date

---

## Content

When you enable OAuth 2.1 in your Supabase project, third-party applications can access user data on their behalf. Row Level Security (RLS) policies are crucial for controlling exactly what data each OAuth client can access.

Scopes control OIDC data, not database access

The OAuth scopes (`openid`, `email`, `profile`, `phone`) control what user information is included in ID tokens and returned by the UserInfo endpoint. They do not control access to your database tables or API endpoints. [...] auth.uid() = user_id AND

6

(auth.jwt() ->> 'client_id') = 'analytics-client-id'

7

);

8

9

-- Admin client can read and modify all data

10

CREATE POLICY "Admin client full access"

11

ON user_data FOR ALL

12

USING (

13

auth.uid() = user_id AND

14

(auth.jwt() ->> 'client_id') = 'admin-client-id'

15

);

```

## Real-world examples#

### Example 1: Multi-platform application#

You have a web app, mobile app, and third-party integrations:

```

1

-- Web app: Full access

2 [...] oc.client_id,

4

oc.name,

5

oc.created_at,

6

COUNT(DISTINCT s.user_id) as active_users

7

FROM auth.oauth_clients oc

8

LEFT JOIN auth.sessions s ON s.client_id = oc.client_id

9

WHERE s.created_at > NOW() - INTERVAL '30 days'

10

GROUP BY oc.client_id, oc.name, oc.created_at;

```

## Testing your policies#

Always test your RLS policies before deploying to production:

```

1

-- Test as a specific OAuth client

2

SET request.jwt.claims = '{

3

"sub": "test-user-uuid",

4

---

*Source: Research Agent v2.0 | Search Provider: Tavily AI | Retrieved: 2025-12-17 08:57:13*
