# PF Resource Hub

A private web portal built for **Planet Fitness** club managers and staff, developed and maintained by **Save Energy Systems (SES)**. The hub provides AI-assisted support, resource access, parts ordering, and administrative tools — all in one place.

**Live Site:** [https://pf-resource-hub.pages.dev](https://pf-resource-hub.pages.dev)

---

## Pages

| File | URL | Description |
|------|-----|-------------|
| `frontend/index.html` | `/` | Login page (entry point) |
| `frontend/dashboard.html` | `/dashboard` | AI Assistant — main hub after login |
| `frontend/resources.html` | `/resources` | SES portals, contacts, schedules & training |
| `frontend/order-parts.html` | `/order-parts` | Parts ordering through SES |
| `frontend/help-now.html` | `/help-now` | Immediate troubleshooting support |
| `frontend/why-ses.html` | `/why-ses` | SES overview & value proposition |
| `frontend/analytics.html` | `/analytics` | Usage & performance analytics |
| `frontend/admin-ses.html` | `/admin-ses` | SES super admin dashboard (restricted) |
| `frontend/admin-pf.html` | `/admin-pf` | PF admin dashboard (restricted) |
| `frontend/forgot-password.html` | `/forgot-password` | Password recovery |
| `frontend/forgot-username.html` | `/forgot-username` | Username recovery |
| `frontend/reset-password.html` | `/reset-password` | Password reset (via email link) |

---

## Project Structure

```
pf-resource-hub/
├── frontend/               # All HTML pages served by Cloudflare Pages
│   ├── index.html          # Login
│   ├── dashboard.html      # AI Assistant
│   ├── resources.html      # Resources
│   ├── order-parts.html    # Order Parts
│   ├── help-now.html       # Help Now
│   ├── why-ses.html        # Why SES
│   ├── analytics.html      # Analytics
│   ├── admin-ses.html      # SES Admin
│   ├── admin-pf.html       # PF Admin
│   ├── forgot-password.html
│   ├── forgot-username.html
│   ├── reset-password.html
│   └── images/             # Logo assets
├── backend/                # Python AI/API backend services
│   ├── app.py              # Main Flask app
│   ├── gemini_service.py   # Gemini AI integration
│   ├── openai_service.py   # OpenAI integration
│   ├── email_service.py    # Email (SendGrid)
│   ├── analytics_service.py
│   ├── knowledge_base/     # AI knowledge base documents
│   └── requirements.txt
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Hosting | Cloudflare Pages |
| Frontend | HTML, CSS, JavaScript |
| Icons | Bootstrap Icons |
| Backend | Python / Flask |
| AI | Google Gemini + OpenAI |
| Email | SendGrid |
| Analytics | Google Analytics (G-N3GWJBMD4C) |

---

## Access & Roles

The hub uses role-based access. Users log in with credentials managed through the SES backend. There are three access levels:

- **Staff** — Access to AI Assistant, Resources, Order Parts, Help Now, Why SES
- **PF Admin** — Above + PF Admin dashboard and analytics
- **SES Super Admin** — Full access including SES Admin dashboard

---

## Developed By

**Adriana Soler** — [adrianasoler.com](https://adrianasoler.com)
For **Save Energy Systems** — [saveenergysystems.com](https://saveenergysystems.com)
Contact: [(617) 564-4800](tel:6175644800)
