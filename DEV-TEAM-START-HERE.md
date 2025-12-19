# 👨‍💻 Developer Team - START HERE

## 📋 Quick Overview

**Project:** Multi-tenant GuideFlow resource hubs for SES clients (starting with Planet Fitness)

**What we're building:** AI-powered search portals for facility managers - one codebase, multiple white-labeled microsites

**Timeline:** 4-6 weeks to MVP (Planet Fitness launch)

**Tech Stack:** Hono + TypeScript + Cloudflare Pages + D1 + Pinecone + OpenAI (we already have GuideFlowAI built!)

---

## 📚 Documentation Reading Order

### **For Understanding the Business:**

**1. Read First:** `STEPH-REQUIREMENTS-WITH-DEMOS.md` (20 min)
- **WHY:** See exactly what the client wants
- **WHAT:** 10 specific requirements with live GuideFlow demo examples
- **KEY SECTIONS:**
  - "What Steph Wants" (requirements breakdown)
  - Demo 1, 2, 3 (actual AI search responses)
  - "Good for Internal SES Too" (shows we need 2+ microsites from day 1)

**2. Read Second:** `SIMPLE-PITCH.md` (15 min)
- **WHY:** Understand the user pain points we're solving
- **WHAT:** Real GM scenarios (before/after), franchise opportunity
- **KEY SECTIONS:**
  - "The Problem (In Plain English)"
  - "Before vs. After Comparison" table
  - "The Franchise Angle"

---

### **For Understanding the Architecture:**

**3. Read Third:** `MULTI-TENANT-ARCHITECTURE.md` ⭐ MOST IMPORTANT (30 min)
- **WHY:** This is your technical blueprint
- **WHAT:** Complete multi-tenant system design
- **KEY SECTIONS:**
  - Domain Structure (subdomains)
  - Two-Level Admin System (super admin vs client admin)
  - Database Structure (4 tables with SQL schemas)
  - File Structure (how content is organized per client)
  - Permission Logic (who can see what)
  - Google Analytics Setup (per-microsite tracking)

**KEY TAKEAWAYS:**
```
✅ planetfitness.saveenergysystems.com (PF GMs)
✅ internal.saveenergysystems.com (SES employees)
✅ admin.saveenergysystems.com (Super admin - SES management)
✅ Each microsite = isolated (own users, content, branding)
✅ Super admin sees ALL, client admins see THEIRS only
```

---

### **For Business Context:**

**4. Optional:** `EXECUTIVE-SUMMARY.md` (20 min)
- **WHY:** Revenue opportunity, success metrics, long-term vision
- **WHAT:** Full business case with $2M-$7M revenue projections
- **KEY SECTIONS:**
  - "Revenue Opportunity Breakdown"
  - "White-Label Scalability" (clone for other fitness chains)

**5. Optional:** `ONE-PAGE-VISUAL.md` (10 min)
- **WHY:** Visual learner? This has ASCII diagrams
- **WHAT:** Complete project on one page with visuals

---

## 🏗️ Technical Architecture Summary

### **What We're Cloning:**

We already have **GuideFlowAI** (the facility maintenance knowledge base demo).

**URL:** https://guideflowai-demo.netlify.app

**What it does:**
- AI search bar (natural language queries)
- Searches Google Drive documents
- Uses Pinecone vector database
- OpenAI generates answers
- Cached responses (100x faster for repeat queries)

**What we need to do:** Make it multi-tenant!

---

### **Multi-Tenant Modifications Needed:**

**1. Subdomain Routing**
```typescript
// src/index.tsx
app.use('*', async (c, next) => {
  const host = c.req.header('host')
  const subdomain = host.split('.')[0] // 'planetfitness'
  
  const clientId = subdomain
  const config = await loadClientConfig(clientId)
  
  c.set('clientId', clientId)
  c.set('config', config)
  
  await next()
})
```

**2. Per-Client Content**
```
/clients/planetfitness/resources/*.txt → Pinecone with client_id='planetfitness'
/clients/internal/resources/*.txt → Pinecone with client_id='ses-internal'
```

**3. Dynamic Branding**
```typescript
// Load logo, colors from config.json per subdomain
const branding = {
  logo: config.logo,           // '/assets/pf-logo.png'
  primaryColor: config.primary_color,  // '#7B2CBF'
  clientName: config.name      // 'Planet Fitness'
}
```

**4. User Authentication**
```sql
-- Users scoped to clients
SELECT * FROM users 
WHERE email = ? AND client_id = ? AND status = 'active'
```

**5. Two-Level Admin**
- Super admin: `admin.saveenergysystems.com` (see ALL clients)
- Client admin: `planetfitness.saveenergysystems.com/admin` (see PF only)

---

## 🗄️ Database Schema (Cloudflare D1)

### **4 Tables to Create:**

```sql
-- 1. Clients (Microsites)
CREATE TABLE clients (
  id TEXT PRIMARY KEY,              -- 'planetfitness', 'internal'
  name TEXT NOT NULL,               -- 'Planet Fitness'
  subdomain TEXT UNIQUE NOT NULL,   -- 'planetfitness'
  logo_url TEXT,
  primary_color TEXT DEFAULT '#7B2CBF',
  status TEXT DEFAULT 'active',
  admin_email TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Users (Per Client)
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL,
  client_id TEXT NOT NULL,          -- Links to clients.id
  role TEXT DEFAULT 'user',         -- 'user', 'client-admin', 'super-admin'
  status TEXT DEFAULT 'active',
  full_name TEXT,
  location TEXT,
  last_login DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (client_id) REFERENCES clients(id),
  UNIQUE(email, client_id)
);

-- 3. Search Logs (Analytics)
CREATE TABLE search_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_email TEXT,
  client_id TEXT NOT NULL,
  query TEXT NOT NULL,
  response_time_ms INTEGER,
  cached BOOLEAN DEFAULT 0,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- 4. Admin Permissions
CREATE TABLE admin_permissions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_email TEXT NOT NULL,
  client_id TEXT,                   -- NULL = super admin (all clients)
  permissions TEXT,                 -- JSON: {"can_add_users": true}
  granted_by TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (client_id) REFERENCES clients(id)
);
```

**Migration file:** `migrations/0001_multi_tenant_setup.sql`

---

## 📁 File Structure

```
/home/user/webapp/
├── src/
│   ├── index.tsx                  # Main Hono app
│   ├── routes/
│   │   ├── auth.ts                # Login/logout/JWT
│   │   ├── search.ts              # AI search (uses GuideFlowAI logic)
│   │   ├── admin-super.ts         # Super admin dashboard
│   │   └── admin-client.ts        # Client admin dashboard
│   ├── middleware/
│   │   ├── auth-check.ts          # JWT validation
│   │   ├── tenant-routing.ts      # Subdomain → client_id mapping
│   │   └── tenant-branding.ts     # Load config.json per client
│   └── lib/
│       ├── pinecone.ts            # Vector search (filter by client_id)
│       ├── openai.ts              # GPT responses
│       └── cache.ts               # Response caching
│
├── clients/                       # Content per microsite
│   ├── planetfitness/
│   │   ├── config.json            # Branding, admin email, GA4 ID
│   │   └── resources/
│   │       ├── work-order-submission.txt
│   │       ├── billing-guide.txt
│   │       ├── client-protocols.txt
│   │       └── (20+ text files)
│   │
│   ├── internal/                  # SES employees
│   │   ├── config.json
│   │   └── resources/
│   │       ├── lockbox-codes.txt
│   │       ├── pricing-guidelines.txt
│   │       └── (15+ text files)
│   │
│   └── template/                  # Clone for new clients
│       ├── config.json.example
│       └── resources/
│           └── README.md
│
├── public/
│   └── assets/
│       ├── pf-logo.png
│       ├── ses-logo.png
│       └── (client logos)
│
├── migrations/
│   └── 0001_multi_tenant_setup.sql
│
├── wrangler.jsonc                 # Cloudflare config with D1
└── package.json
```

---

## 🚀 Development Phases

### **Phase 1: Core Multi-Tenant (Week 1-2)**

**Tasks:**
1. ✅ Clone existing GuideFlowAI codebase
2. ✅ Set up D1 database with 4 tables
3. ✅ Implement subdomain routing middleware
4. ✅ Create tenant config loader (reads `clients/{id}/config.json`)
5. ✅ Modify Pinecone queries to filter by `client_id`
6. ✅ Add user authentication (JWT with client_id claim)
7. ✅ Dynamic branding (logo, colors per subdomain)

**Deliverable:** 
- `planetfitness.saveenergysystems.com` works
- `internal.saveenergysystems.com` works
- Each shows different branding + content

---

### **Phase 2: Admin Dashboards (Week 3)**

**Tasks:**
1. ✅ Build super admin dashboard (`admin.saveenergysystems.com`)
   - List all microsites
   - View cross-client analytics
   - Add/remove clients
   - Assign client admins
2. ✅ Build client admin dashboard (`/admin` route per microsite)
   - Add/remove users for their client only
   - View analytics for their client only
   - Manage branding (within limits)

**Deliverable:**
- Super admin can manage all clients
- Steph can manage PF users only (not SES internal)

---

### **Phase 3: Content & Testing (Week 4)**

**Tasks:**
1. ✅ Create Planet Fitness content (20+ text files)
   - Work with Steph to get requirements
   - Write clear, searchable content
   - Upload to Pinecone with `client_id='planetfitness'`
2. ✅ Create SES Internal content (15+ text files)
   - Lockbox codes, pricing, procedures
   - Upload with `client_id='ses-internal'`
3. ✅ Google Analytics setup (2 GA4 properties)
4. ✅ Testing with pilot users (5 PF GMs, 5 SES employees)

**Deliverable:**
- Real content searchable
- Analytics tracking works
- Pilot users give feedback

---

### **Phase 4: Polish & Launch (Week 5-6)**

**Tasks:**
1. ✅ Refine based on pilot feedback
2. ✅ Performance optimization
3. ✅ Documentation for admins (Steph's user guide)
4. ✅ Full rollout (500 PF GMs, 47 SES employees)
5. ✅ Monitor adoption metrics

**Deliverable:**
- Production-ready system
- All users onboarded
- Analytics dashboard live

---

## 🎯 Key Technical Decisions

### **Why Cloudflare Pages + D1?**
- ✅ We already use it for GuideFlowAI
- ✅ D1 is free, fast, globally distributed
- ✅ Easy subdomain routing
- ✅ Scales to millions of requests

### **Why Text Files vs Database for Content?**
- ✅ Easy to update (edit .txt file, re-index)
- ✅ Version control with Git
- ✅ Clone-friendly (copy folder for new client)
- ✅ Non-technical staff can edit

### **Why Pinecone?**
- ✅ Already integrated in GuideFlowAI
- ✅ Metadata filtering (by `client_id`)
- ✅ Fast vector search
- ✅ Handles multi-tenancy well

### **Why Two-Level Admin?**
- ✅ Clients self-manage users (less support burden)
- ✅ SES retains global control
- ✅ Data isolation (clients can't see each other)

---

## 🔧 Local Development Setup

### **Step 1: Clone GuideFlowAI**
```bash
cd /home/user
git clone <guideflowai-repo> webapp-multi-tenant
cd webapp-multi-tenant
```

### **Step 2: Install Dependencies**
```bash
npm install
```

### **Step 3: Set Up D1 Database**
```bash
# Create local D1 database
npx wrangler d1 create ses-hub-production

# Run migrations
npx wrangler d1 migrations apply ses-hub-production --local

# Seed with test data
npx wrangler d1 execute ses-hub-production --local --file=./seed.sql
```

### **Step 4: Create Client Folders**
```bash
mkdir -p clients/planetfitness/resources
mkdir -p clients/internal/resources

# Copy config examples
cp clients/template/config.json.example clients/planetfitness/config.json
cp clients/template/config.json.example clients/internal/config.json

# Edit configs with actual values
```

### **Step 5: Local Dev Server**
```bash
npm run build
npm run dev:local
# Or: npx wrangler pages dev dist --local --d1=ses-hub-production
```

### **Step 6: Test Subdomains Locally**
Add to `/etc/hosts`:
```
127.0.0.1 planetfitness.localhost
127.0.0.1 internal.localhost
127.0.0.1 admin.localhost
```

Then visit:
- `http://planetfitness.localhost:3000`
- `http://internal.localhost:3000`
- `http://admin.localhost:3000`

---

## 🧪 Testing Checklist

### **Multi-Tenancy:**
- [ ] User from PF can log into planetfitness.* but NOT internal.*
- [ ] PF search only returns PF content (not SES internal content)
- [ ] Branding changes per subdomain (logo, colors)
- [ ] Each subdomain has separate GA4 tracking

### **Permissions:**
- [ ] Super admin sees all clients in dashboard
- [ ] Steph (PF admin) only sees PF users, not SES internal
- [ ] PF GM cannot access admin panel
- [ ] Search logs scoped correctly (PF queries don't appear in SES analytics)

### **Performance:**
- [ ] Cached responses return in <0.1s
- [ ] First-time queries return in <3s
- [ ] Subdomain routing adds <10ms overhead
- [ ] Database queries use indexes (check EXPLAIN)

### **Content:**
- [ ] Search "work order" on PF → returns PF-specific instructions
- [ ] Search "work order" on SES Internal → returns SES internal process
- [ ] Updating text file + re-index updates search results

---

## 📞 Key Contacts

**Business Side:**
- **Client Contact:** Steph Wilson (steph@planetfitness.com) - PF Facilities Manager
- **SES Owner:** [Your name/email] - Project sponsor

**Technical Questions:**
- **Architecture:** Review `MULTI-TENANT-ARCHITECTURE.md`
- **Requirements:** Review `STEPH-REQUIREMENTS-WITH-DEMOS.md`
- **Existing Code:** GuideFlowAI demo at https://guideflowai-demo.netlify.app

---

## 🎯 Success Criteria

### **Week 2 (MVP Demo):**
- ✅ 2 working microsites (PF + SES Internal)
- ✅ Different branding per subdomain
- ✅ Basic search works
- ✅ User login works

### **Week 4 (Pilot):**
- ✅ Admin dashboards functional
- ✅ Real content uploaded
- ✅ 5 pilot users testing each microsite
- ✅ Analytics tracking

### **Week 6 (Launch):**
- ✅ 500 PF GMs onboarded
- ✅ 47 SES employees onboarded
- ✅ 80%+ adoption rate
- ✅ <3s average query time
- ✅ 60% reduction in support calls (Steph's team)

---

## 🚨 Common Pitfalls to Avoid

**1. Don't Mix Client Data**
- ✅ Always filter by `client_id` in database queries
- ✅ Always filter by `client_id` in Pinecone queries
- ✅ Test with multiple users from different clients

**2. Don't Hardcode Client Logic**
- ❌ `if (clientId === 'planetfitness') { ... }`
- ✅ Read from `config.json` dynamically

**3. Don't Forget Subdomain in URLs**
- ✅ Test with actual subdomains (not just localhost)
- ✅ Verify cookies work across subdomains

**4. Don't Skip Permission Checks**
- ✅ Every admin action needs permission validation
- ✅ Client admins should never see other clients' data

**5. Don't Ignore Performance**
- ✅ Index database columns (email, client_id, timestamps)
- ✅ Cache config.json (don't read from disk every request)
- ✅ Use Pinecone metadata filtering (faster than post-filtering)

---

## 📚 Additional Resources

**Code Reference:**
- Existing GuideFlowAI: https://guideflowai-demo.netlify.app (clone this!)
- Hono docs: https://hono.dev/
- Cloudflare D1 docs: https://developers.cloudflare.com/d1/
- Pinecone docs: https://docs.pinecone.io/

**Business Context:**
- All 6 documentation files in `/home/user/pf-resource-hub/`
- Start with `STEPH-REQUIREMENTS-WITH-DEMOS.md` for use cases
- Reference `MULTI-TENANT-ARCHITECTURE.md` for technical details

---

## ✅ You're Ready!

**Read these 3 files first:**
1. `STEPH-REQUIREMENTS-WITH-DEMOS.md` (what we're building)
2. `MULTI-TENANT-ARCHITECTURE.md` (how to build it)
3. This file (where to start)

**Then:**
1. Clone GuideFlowAI codebase
2. Set up D1 database (4 tables)
3. Implement subdomain routing
4. Create 2 test microsites (PF + SES Internal)
5. Demo to leadership

**Questions?** Reference the architecture doc. It has everything:
- Database schemas
- Permission logic
- File structure
- Code examples

---

**Let's build this! 🚀**

*Last Updated: December 19, 2025*
*Project: SES Multi-Tenant GuideFlow Hubs*
