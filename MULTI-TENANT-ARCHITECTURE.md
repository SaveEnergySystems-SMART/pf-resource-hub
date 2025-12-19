# 🏗️ Multi-Tenant GuideFlow Architecture - SES Implementation

## 🌐 Domain Structure

### **Primary Domain Setup:**

```
saveenergysystems.com (Main SES website)
│
├── /planetfitness → planetfitness.saveenergysystems.com (subdomain redirect)
├── /lafitness → lafitness.saveenergysystems.com (future)
├── /24hourfitness → 24hourfitness.saveenergysystems.com (future)
├── /internal → internal.saveenergysystems.com (SES employees)
└── /admin → admin.saveenergysystems.com (Super Admin Portal)
```

### **OR Clean Subdomain Structure (RECOMMENDED):**

```
saveenergysystems.com (Main SES website)
│
Subdomains (Each is separate microsite):
├── planetfitness.saveenergysystems.com (PF GMs)
├── lafitness.saveenergysystems.com (future)
├── 24hourfitness.saveenergysystems.com (future)
├── internal.saveenergysystems.com (SES employees)
└── admin.saveenergysystems.com (Super Admin - SES only)
```

**Why subdomains?**
- ✅ Clean URLs (easier to remember)
- ✅ Separate SSL certs per client
- ✅ Independent deployments
- ✅ Better security isolation
- ✅ Professional appearance

---

## 🔐 Password Protection Per Microsite

### **Each Microsite is SEPARATE:**

**Example: Planet Fitness**
```
URL: planetfitness.saveenergysystems.com
Password: Separate per microsite
Users: Only PF GMs (stored in D1 with client_id='planetfitness')
Branding: PF logo, purple colors
Content: /clients/planetfitness/*.txt files
Admin: Steph Wilson (can manage PF users only)
```

**Example: LA Fitness (Future)**
```
URL: lafitness.saveenergysystems.com
Password: Different from PF
Users: Only LA Fitness GMs (client_id='lafitness')
Branding: LA Fitness logo, orange/blue colors
Content: /clients/lafitness/*.txt files
Admin: LA Facilities Manager (can manage LA users only)
```

**Example: Internal SES**
```
URL: internal.saveenergysystems.com
Password: SES employee access only
Users: SES techs, office staff (client_id='ses-internal')
Branding: SES logo, company colors
Content: /clients/ses-internal/*.txt files
Admin: SES Operations Manager
```

---

## 👥 Two-Level Admin System

### **Level 1: Super Admin (SES Corporate)**

**Access:** `admin.saveenergysystems.com`

**Who:** You, SES executives, operations manager

**Can See/Do:**
```
┌─────────────────────────────────────────────────┐
│  🔐 SES Super Admin Dashboard                   │
├─────────────────────────────────────────────────┤
│                                                  │
│  🏢 All Client Microsites:                      │
│                                                  │
│  ┌───────────────────────────────────────────┐ │
│  │ 🏋️ Planet Fitness                         │ │
│  │ URL: planetfitness.saveenergysystems.com  │ │
│  │ Status: ✅ Active                         │ │
│  │ Users: 523 GMs                            │ │
│  │ Searches this month: 2,847                │ │
│  │ Admin: Steph Wilson (steph@pf.com)        │ │
│  │ [View Analytics] [Manage Users] [Settings]│ │
│  └───────────────────────────────────────────┘ │
│                                                  │
│  ┌───────────────────────────────────────────┐ │
│  │ 🏃 LA Fitness (Coming Soon)               │ │
│  │ URL: lafitness.saveenergysystems.com      │ │
│  │ Status: 🟡 Pending Setup                  │ │
│  │ [Configure Now]                           │ │
│  └───────────────────────────────────────────┘ │
│                                                  │
│  ┌───────────────────────────────────────────┐ │
│  │ 🔧 SES Internal                           │ │
│  │ URL: internal.saveenergysystems.com       │ │
│  │ Status: ✅ Active                         │ │
│  │ Users: 47 employees                       │ │
│  │ Searches this month: 892                  │ │
│  │ [View Analytics] [Manage Users]           │ │
│  └───────────────────────────────────────────┘ │
│                                                  │
│  📊 Global Analytics (All Clients):             │
│  ├─ Total Users: 570                            │
│  ├─ Total Searches: 3,739 this month           │
│  ├─ Top Search: "work order submission"        │
│  ├─ Avg Response Time: 0.08s                   │
│  └─ Cache Hit Rate: 84%                        │
│                                                  │
│  🔗 Google Analytics Dashboard:                 │
│  [View GA4 Dashboard] (all properties)          │
│                                                  │
│  ⚙️ System Management:                          │
│  ├─ [Add New Client Microsite]                 │
│  ├─ [Global Settings]                           │
│  ├─ [Content Library]                           │
│  └─ [Billing & Usage Reports]                  │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Super Admin Powers:**
- ✅ See ALL microsites in one dashboard
- ✅ View cross-client analytics (compare PF vs LA Fitness usage)
- ✅ Add/remove entire microsites
- ✅ Assign client admins (give Steph admin rights for PF only)
- ✅ Override any permissions
- ✅ Access billing/revenue data
- ✅ Global content library (share resources across clients)
- ✅ Google Analytics aggregated view

---

### **Level 2: Client Admin (Per Microsite)**

**Access:** `planetfitness.saveenergysystems.com/admin` (within each microsite)

**Who:** Steph Wilson (for PF), LA Facilities Manager (for LA), etc.

**Can See/Do (Steph's View for PF Only):**

```
┌─────────────────────────────────────────────────┐
│  🏋️ Planet Fitness - Admin Dashboard           │
│  Logged in as: Steph Wilson                     │
├─────────────────────────────────────────────────┤
│                                                  │
│  👥 User Management (Planet Fitness Only):      │
│                                                  │
│  ├─ Add New GM by Email:                        │
│  │  [john.smith@pf.com] [Add User] 📧          │
│  │                                               │
│  ├─ Active Users (523):                         │
│  │  ┌──────────────────────────────────────┐   │
│  │  │ john.smith@pf.com                    │   │
│  │  │ Location: Boston Downtown            │   │
│  │  │ Last Login: 2 hours ago              │   │
│  │  │ Searches: 34 this month              │   │
│  │  │ [View Activity] [Revoke Access] ❌   │   │
│  │  └──────────────────────────────────────┘   │
│  │                                               │
│  │  ┌──────────────────────────────────────┐   │
│  │  │ sarah.jones@pf.com                   │   │
│  │  │ Location: Phoenix North              │   │
│  │  │ Last Login: 5 days ago ⚠️            │   │
│  │  │ Searches: 2 this month               │   │
│  │  │ [Send Reminder Email] [Revoke]       │   │
│  │  └──────────────────────────────────────┘   │
│  │                                               │
│  └─ [Export User List] [Bulk Import]            │
│                                                  │
│  📊 Analytics (Planet Fitness Only):            │
│  ├─ This Week:                                  │
│  │  • Total Searches: 412                       │
│  │  • Active Users: 287/523 (55%)              │
│  │  • Avg Response Time: 0.06s                  │
│  │                                               │
│  ├─ Top Searches:                               │
│  │  1. "winter maintenance" (67 searches)      │
│  │  2. "submit work order" (54 searches)       │
│  │  3. "billing questions" (41 searches)       │
│  │  4. "emergency contact" (38 searches)       │
│  │  5. "order filters" (29 searches)           │
│  │                                               │
│  ├─ User Engagement:                            │
│  │  • Daily logins: 156 avg                     │
│  │  • Peak hours: 8am-10am                      │
│  │  • Mobile vs Desktop: 62% / 38%             │
│  │                                               │
│  └─ [Download Full Report] [View GA4]           │
│                                                  │
│  🔗 Google Analytics (PF Only):                 │
│  [View Planet Fitness Analytics] → GA4          │
│                                                  │
│  📄 Content Management:                         │
│  ├─ Last Content Update: Dec 15, 2024          │
│  ├─ Pending Updates: 2 files                    │
│  ├─ [Request Content Change] (SES approves)    │
│  └─ [View Content Library]                      │
│                                                  │
│  ⚙️ Settings (Planet Fitness):                  │
│  ├─ Branding:                                   │
│  │  • Logo: [pf-logo.png] [Change]             │
│  │  • Primary Color: #7B2CBF                   │
│  │  • Company Name: Planet Fitness              │
│  │                                               │
│  ├─ Notifications:                              │
│  │  ☑ Email me when new users join             │
│  │  ☑ Weekly analytics summary                 │
│  │  ☐ Daily usage reports                      │
│  │                                               │
│  └─ Contact Info:                               │
│     • Your Email: steph@planetfitness.com      │
│     • Support Phone: 555-9876                   │
│     • [Update Contact Info]                     │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Client Admin Powers (Steph for PF):**
- ✅ Add/remove users for PF ONLY (not LA Fitness, not SES internal)
- ✅ View analytics for PF microsite ONLY
- ✅ See who's active/inactive
- ✅ Export user lists
- ✅ Request content updates (SES super admin approves)
- ✅ Update branding (logo, colors) within limits
- ✅ Manage notification preferences
- ❌ CANNOT see other clients (LA Fitness, SES internal)
- ❌ CANNOT delete the microsite
- ❌ CANNOT access super admin features

---

## 🗄️ Database Structure (Cloudflare D1)

### **Tables for Multi-Tenant System:**

**1. Clients Table (Microsites)**
```sql
CREATE TABLE clients (
  id TEXT PRIMARY KEY,              -- 'planetfitness', 'lafitness', 'ses-internal'
  name TEXT NOT NULL,               -- 'Planet Fitness', 'LA Fitness'
  subdomain TEXT UNIQUE NOT NULL,   -- 'planetfitness', 'lafitness'
  logo_url TEXT,                    -- '/assets/pf-logo.png'
  primary_color TEXT DEFAULT '#7B2CBF',
  status TEXT DEFAULT 'active',     -- 'active', 'suspended', 'trial'
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  contract_value DECIMAL(10,2),     -- Annual contract value (for SES tracking)
  admin_email TEXT,                 -- Primary client admin (Steph's email)
  admin_name TEXT                   -- 'Steph Wilson'
);
```

**2. Users Table (Per Client)**
```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL,
  client_id TEXT NOT NULL,          -- Links to clients.id
  role TEXT DEFAULT 'user',         -- 'user', 'client-admin', 'super-admin'
  status TEXT DEFAULT 'active',     -- 'active', 'suspended', 'pending'
  full_name TEXT,
  location TEXT,                    -- 'Boston Downtown' (for PF GMs)
  added_by TEXT,                    -- Who added them (admin email)
  last_login DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (client_id) REFERENCES clients(id),
  UNIQUE(email, client_id)          -- Same email can exist in multiple clients
);
```

**3. Search Logs (Analytics)**
```sql
CREATE TABLE search_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_email TEXT,
  client_id TEXT NOT NULL,          -- Which microsite
  query TEXT NOT NULL,
  response_time_ms INTEGER,
  cached BOOLEAN DEFAULT 0,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (client_id) REFERENCES clients(id)
);
```

**4. Admin Permissions**
```sql
CREATE TABLE admin_permissions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_email TEXT NOT NULL,
  client_id TEXT,                   -- NULL = super admin (all clients)
  permissions TEXT,                 -- JSON: {"can_add_users": true, "can_delete": false}
  granted_by TEXT,                  -- Who gave them admin rights
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (client_id) REFERENCES clients(id)
);
```

---

## 📁 File Structure (Content per Client)

### **Directory Layout:**

```
/home/user/webapp/
├── src/
│   ├── index.tsx                  # Main Hono app
│   ├── routes/
│   │   ├── auth.ts                # Login/logout
│   │   ├── search.ts              # AI search endpoints
│   │   ├── admin-super.ts         # Super admin routes
│   │   └── admin-client.ts        # Client admin routes
│   └── middleware/
│       ├── auth-check.ts          # JWT validation
│       └── tenant-check.ts        # Verify user belongs to client
│
├── clients/                       # Content per microsite
│   ├── planetfitness/
│   │   ├── config.json            # PF branding config
│   │   └── resources/
│   │       ├── work-order-submission.txt
│   │       ├── billing-guide.txt
│   │       ├── client-protocols.txt
│   │       └── winter-maintenance.txt
│   │
│   ├── lafitness/                 # Future
│   │   ├── config.json
│   │   └── resources/
│   │       └── (LA Fitness content)
│   │
│   ├── ses-internal/
│   │   ├── config.json
│   │   └── resources/
│   │       ├── lockbox-codes.txt
│   │       ├── pricing-guidelines.txt
│   │       └── tech-procedures.txt
│   │
│   └── template/                  # Clone this for new clients
│       ├── config.json.example
│       └── resources/
│           └── README.md
│
├── public/
│   └── assets/
│       ├── pf-logo.png            # Planet Fitness logo
│       ├── la-logo.png            # LA Fitness logo
│       └── ses-logo.png           # SES logo
│
└── wrangler.jsonc                 # Cloudflare config with D1
```

### **config.json Example (Per Client):**

**Planet Fitness:**
```json
{
  "client_id": "planetfitness",
  "name": "Planet Fitness",
  "subdomain": "planetfitness",
  "logo": "/assets/pf-logo.png",
  "primary_color": "#7B2CBF",
  "secondary_color": "#FDD023",
  "admin_email": "steph@planetfitness.com",
  "admin_name": "Steph Wilson",
  "support_email": "support@saveenergysystems.com",
  "support_phone": "555-1234",
  "ga4_property_id": "G-XXXXXXXXX",
  "features": {
    "ticket_tracking": true,
    "parts_ordering": true,
    "franchise_demo": true
  }
}
```

**LA Fitness (Future):**
```json
{
  "client_id": "lafitness",
  "name": "LA Fitness",
  "subdomain": "lafitness",
  "logo": "/assets/la-logo.png",
  "primary_color": "#FF6600",
  "secondary_color": "#003366",
  "admin_email": "facilities@lafitness.com",
  "admin_name": "Michael Rodriguez",
  "support_email": "support@saveenergysystems.com",
  "support_phone": "555-1234",
  "ga4_property_id": "G-YYYYYYYYY",
  "features": {
    "ticket_tracking": true,
    "parts_ordering": false,
    "franchise_demo": false
  }
}
```

---

## 🔐 Permission Logic

### **How Access Control Works:**

**User Login Flow:**
```
1. User visits: planetfitness.saveenergysystems.com
2. Enters email: john.smith@pf.com
3. Backend checks:
   - Does user exist in users table?
   - Does client_id = 'planetfitness'?
   - Is status = 'active'?
4. If yes: Generate JWT with claims:
   {
     email: 'john.smith@pf.com',
     client_id: 'planetfitness',
     role: 'user'
   }
5. User sees PF-branded dashboard with PF content
```

**Client Admin Access (Steph):**
```
1. Steph visits: planetfitness.saveenergysystems.com/admin
2. Backend checks:
   - Is she in admin_permissions table?
   - Does her client_id = 'planetfitness' OR NULL (super admin)?
3. If client_id = 'planetfitness':
   - Show PF admin dashboard
   - Can only manage PF users
   - Can only see PF analytics
4. If client_id = NULL:
   - She's super admin
   - Can access ALL microsites
```

**Super Admin Access (You):**
```
1. You visit: admin.saveenergysystems.com
2. Backend checks:
   - Is your client_id = NULL in admin_permissions?
3. If yes:
   - Show all microsites
   - Full system access
   - Cross-client analytics
```

---

## 🎨 Branding Per Microsite

### **How Each Microsite Looks Different:**

**Dynamic Theming (Hono Middleware):**
```typescript
// middleware/tenant-branding.ts
import { Next } from 'hono'

export async function applyBranding(c: Context, next: Next) {
  const subdomain = c.req.header('host')?.split('.')[0]
  
  // Load config based on subdomain
  const config = await loadClientConfig(subdomain) // reads clients/planetfitness/config.json
  
  // Inject branding into context
  c.set('branding', {
    logo: config.logo,
    primaryColor: config.primary_color,
    clientName: config.name
  })
  
  await next()
}
```

**Frontend Rendering:**
```html
<!DOCTYPE html>
<html>
<head>
  <title>{{clientName}} Resource Hub</title>
  <style>
    :root {
      --primary-color: {{primaryColor}};
    }
    .header { background-color: var(--primary-color); }
  </style>
</head>
<body>
  <header class="header">
    <img src="{{logo}}" alt="{{clientName}} Logo">
    <h1>{{clientName}} Resource Hub</h1>
  </header>
  <!-- Rest of page -->
</body>
</html>
```

**Result:**
- Planet Fitness sees: Purple header, PF logo, "Planet Fitness Resource Hub"
- LA Fitness sees: Orange header, LA logo, "LA Fitness Resource Hub"
- SES Internal sees: SES colors, SES logo, "SES Internal Resources"

---

## 📊 Google Analytics Setup

### **Per-Microsite GA4 Properties:**

**Google Analytics Structure:**
```
GA4 Account: Save Energy Systems
│
├── Property 1: Planet Fitness Hub (G-XXXXXXXXX)
│   └── Data Stream: planetfitness.saveenergysystems.com
│
├── Property 2: LA Fitness Hub (G-YYYYYYYYY)
│   └── Data Stream: lafitness.saveenergysystems.com
│
├── Property 3: SES Internal (G-ZZZZZZZZZ)
│   └── Data Stream: internal.saveenergysystems.com
│
└── Property 4: Admin Portal (G-AAAAAAAA)
    └── Data Stream: admin.saveenergysystems.com
```

**Tracking Code Injection (Per Client):**
```typescript
// Based on subdomain, load different GA4 property
const gaPropertyId = config.ga4_property_id // From config.json

<script async src="https://www.googletagmanager.com/gtag/js?id={{gaPropertyId}}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '{{gaPropertyId}}');
</script>
```

**Access Control:**
- **Steph (PF Admin):** Can access GA4 Property 1 only (PF data)
- **LA Admin (Future):** Can access GA4 Property 2 only (LA data)
- **You (Super Admin):** Can access ALL properties (cross-client view)

---

## 🚀 Adding a New Client Microsite (5-Day Process)

### **Step-by-Step:**

**Day 1: Super Admin Creates Microsite**
```
1. Go to: admin.saveenergysystems.com
2. Click "Add New Client Microsite"
3. Fill form:
   - Client Name: LA Fitness
   - Subdomain: lafitness
   - Upload logo
   - Choose colors
   - Admin email: facilities@lafitness.com
4. System creates:
   - Entry in clients table
   - /clients/lafitness/ folder
   - GA4 property
   - Subdomain DNS record
```

**Day 2-3: Content Creation**
```
1. Copy /clients/template/ → /clients/lafitness/
2. Edit config.json with LA branding
3. Create resource text files:
   - work-order-submission.txt (LA-specific)
   - billing-guide.txt (LA-specific)
   - client-protocols.txt (LA-specific)
   - maintenance-schedules.txt
4. Upload to Pinecone (index with client_id='lafitness')
```

**Day 4: Admin Setup**
```
1. Assign LA Facilities Manager as client admin
2. Insert into admin_permissions:
   - user_email: facilities@lafitness.com
   - client_id: 'lafitness'
   - permissions: {"can_add_users": true, "can_view_analytics": true}
3. Send welcome email with login instructions
```

**Day 5: Testing & Launch**
```
1. Test login at: lafitness.saveenergysystems.com
2. Verify branding (LA logo, colors)
3. Test search queries
4. Verify analytics tracking
5. Add 5 pilot users
6. Full rollout
```

---

## 🎯 Summary: Two-Level Admin System

### **Level 1: Super Admin (You)**

**Access:** admin.saveenergysystems.com

**Powers:**
- ✅ See ALL microsites in one dashboard
- ✅ Add/remove entire clients
- ✅ Cross-client analytics comparison
- ✅ Assign client admins
- ✅ Global system settings
- ✅ Billing/revenue reports
- ✅ Override any permission

**Database:** client_id = NULL in admin_permissions

---

### **Level 2: Client Admin (Steph for PF)**

**Access:** planetfitness.saveenergysystems.com/admin

**Powers:**
- ✅ Add/remove users for PF ONLY
- ✅ View PF analytics ONLY
- ✅ Manage PF branding (within limits)
- ✅ Request content updates
- ❌ Cannot see other clients
- ❌ Cannot delete microsite
- ❌ Cannot access super admin

**Database:** client_id = 'planetfitness' in admin_permissions

---

## ✅ Architecture Benefits

### **Why This Structure Works:**

**Security:**
- ✅ Data isolation per client (can't see each other's data)
- ✅ Separate passwords per microsite
- ✅ Admin permissions scoped properly

**Scalability:**
- ✅ Add new clients in 5 days
- ✅ Same codebase for all
- ✅ Independent deployments possible

**Management:**
- ✅ Client admins self-manage their users
- ✅ You control global settings
- ✅ Clear permission hierarchy

**Branding:**
- ✅ Each client sees their own logo/colors
- ✅ Professional white-label appearance
- ✅ No SES branding visible to end users

**Analytics:**
- ✅ Client admins see only their data
- ✅ You see cross-client insights
- ✅ Compare performance across clients

---

## 🔧 Technical Implementation

**Subdomain Routing (Cloudflare Pages):**
```typescript
// src/index.tsx
import { Hono } from 'hono'

const app = new Hono()

// Middleware: Determine client from subdomain
app.use('*', async (c, next) => {
  const host = c.req.header('host') || ''
  const subdomain = host.split('.')[0]
  
  // Load client config
  const clientId = subdomain === 'admin' ? 'admin' : subdomain
  const config = await loadClientConfig(clientId)
  
  if (!config) {
    return c.text('Client not found', 404)
  }
  
  c.set('clientId', clientId)
  c.set('config', config)
  
  await next()
})

// Routes
app.get('/', (c) => {
  const config = c.get('config')
  // Render with client branding
})

export default app
```

**Database Queries (Scoped by Client):**
```typescript
// Get users for specific client only
async function getClientUsers(clientId: string) {
  const { results } = await env.DB.prepare(
    'SELECT * FROM users WHERE client_id = ? AND status = "active"'
  ).bind(clientId).all()
  
  return results
}

// Search logs for specific client only
async function getClientSearchLogs(clientId: string) {
  const { results } = await env.DB.prepare(
    'SELECT query, COUNT(*) as count FROM search_logs WHERE client_id = ? GROUP BY query ORDER BY count DESC LIMIT 10'
  ).bind(clientId).all()
  
  return results
}
```

---

**This is your complete multi-tenant architecture! Each client is separate, but you control everything from one super admin dashboard.** 🎯
