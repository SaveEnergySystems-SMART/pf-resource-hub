# ✅ Implementation Checklist - SES Multi-Tenant GuideFlow Hubs

**Project:** Multi-tenant AI resource hubs for SES clients  
**First Client:** Planet Fitness (500 GMs + 47 SES employees)  
**Timeline:** 6 weeks to launch  
**Last Updated:** December 19, 2025

---

## 📋 Week 1-2: Core Multi-Tenant System

### **Day 1: Environment Setup**
- [ ] Clone GuideFlowAI repository from GitHub
- [ ] Run `npm install` to install dependencies
- [ ] Set up Cloudflare account (D1 database access)
- [ ] Create local `.dev.vars` file with API keys
  - [ ] `OPENAI_API_KEY`
  - [ ] `PINECONE_API_KEY`
  - [ ] `PINECONE_INDEX_NAME`
- [ ] Test existing GuideFlowAI locally (`npm run dev`)
- [ ] Verify GuideFlowAI responds to test queries

**Success Criteria:** GuideFlowAI running locally on `localhost:3000`

---

### **Day 2-3: Database Setup**
- [ ] Create production D1 database: `wrangler d1 create ses-hub-production`
- [ ] Copy database ID to `wrangler.jsonc`
- [ ] Create `migrations/0001_multi_tenant_setup.sql` with 4 tables:
  - [ ] `clients` table (id, name, subdomain, logo_url, primary_color, admin_email)
  - [ ] `users` table (id, email, client_id, role, status, last_login)
  - [ ] `search_logs` table (id, user_email, client_id, query, response_time_ms, cached)
  - [ ] `admin_permissions` table (id, user_email, client_id, permissions)
- [ ] Run migrations locally: `wrangler d1 migrations apply ses-hub-production --local`
- [ ] Create `seed.sql` with test data:
  - [ ] 2 test clients (planetfitness, ses-internal)
  - [ ] 5 test users (2 PF, 2 SES, 1 super admin)
  - [ ] Sample search logs
- [ ] Seed local database: `wrangler d1 execute ses-hub-production --local --file=./seed.sql`
- [ ] Verify tables exist: `wrangler d1 execute ses-hub-production --local --command="SELECT * FROM clients"`

**Success Criteria:** D1 database with 4 tables and test data

---

### **Day 4-5: Subdomain Routing**
- [ ] Create `src/middleware/tenant-routing.ts`
- [ ] Extract subdomain from `c.req.header('host')`
- [ ] Map subdomain to `client_id` (e.g., `planetfitness` → `planetfitness`)
- [ ] Load client from D1 database
- [ ] Set `c.set('clientId', clientId)` for downstream use
- [ ] Handle special case: `admin` subdomain (super admin portal)
- [ ] Return 404 if client not found
- [ ] Test with local subdomains:
  - [ ] Add `127.0.0.1 planetfitness.localhost` to `/etc/hosts`
  - [ ] Add `127.0.0.1 internal.localhost` to `/etc/hosts`
  - [ ] Add `127.0.0.1 admin.localhost` to `/etc/hosts`
  - [ ] Visit `http://planetfitness.localhost:3000` (should show PF)
  - [ ] Visit `http://internal.localhost:3000` (should show SES Internal)

**Success Criteria:** Subdomain routing works, different clients identified correctly

---

### **Day 6-7: Dynamic Branding**
- [ ] Create `src/middleware/tenant-branding.ts`
- [ ] Load `clients/{client_id}/config.json` based on subdomain
- [ ] Parse config for:
  - [ ] `logo` (path to logo file)
  - [ ] `primary_color` (hex color)
  - [ ] `name` (client name)
  - [ ] `ga4_property_id` (Google Analytics)
- [ ] Set `c.set('config', config)` for templating
- [ ] Create `/clients/planetfitness/config.json`:
  ```json
  {
    "client_id": "planetfitness",
    "name": "Planet Fitness",
    "subdomain": "planetfitness",
    "logo": "/assets/pf-logo.png",
    "primary_color": "#7B2CBF",
    "admin_email": "steph@planetfitness.com",
    "ga4_property_id": "G-XXXXXXXXX"
  }
  ```
- [ ] Create `/clients/ses-internal/config.json` (similar structure)
- [ ] Modify frontend template to use dynamic values:
  - [ ] Logo: `<img src="{{config.logo}}">`
  - [ ] Title: `<h1>{{config.name}} Resource Hub</h1>`
  - [ ] CSS: `:root { --primary-color: {{config.primary_color}}; }`
- [ ] Test branding changes per subdomain:
  - [ ] Planet Fitness: Purple colors, PF logo
  - [ ] SES Internal: SES colors, SES logo

**Success Criteria:** Each subdomain shows correct branding (logo, colors, name)

---

### **Day 8-9: User Authentication**
- [ ] Create `src/routes/auth.ts` with endpoints:
  - [ ] `POST /api/auth/login` (email + client_id)
  - [ ] `POST /api/auth/logout`
  - [ ] `GET /api/auth/me` (get current user)
- [ ] Implement login logic:
  - [ ] Query D1: `SELECT * FROM users WHERE email = ? AND client_id = ? AND status = 'active'`
  - [ ] Generate JWT with claims: `{ email, client_id, role }`
  - [ ] Return JWT as HTTP-only cookie
- [ ] Create `src/middleware/auth-check.ts`:
  - [ ] Verify JWT signature
  - [ ] Extract `client_id` from JWT
  - [ ] Match JWT's `client_id` with subdomain's `client_id`
  - [ ] Set `c.set('user', userPayload)`
- [ ] Protect routes:
  - [ ] `/api/search` requires authentication
  - [ ] `/admin` requires role='client-admin' or 'super-admin'
- [ ] Test authentication:
  - [ ] Login as PF user on `planetfitness.*` → Success
  - [ ] Try accessing `internal.*` with PF JWT → Fail (wrong client_id)

**Success Criteria:** User auth works, client isolation enforced

---

### **Day 10-11: Multi-Tenant Content**
- [ ] Modify `functions_rag.py` (or TypeScript equivalent):
  - [ ] Add `client_id` to Pinecone metadata during upload
  - [ ] Filter Pinecone queries by `client_id`
- [ ] Create content structure:
  - [ ] `/clients/planetfitness/resources/work-order-submission.txt`
  - [ ] `/clients/planetfitness/resources/billing-guide.txt`
  - [ ] `/clients/ses-internal/resources/lockbox-codes.txt`
  - [ ] `/clients/ses-internal/resources/pricing-guidelines.txt`
- [ ] Write upload script:
  - [ ] Read all `.txt` files from `/clients/{client_id}/resources/`
  - [ ] Generate embeddings with OpenAI
  - [ ] Upload to Pinecone with metadata: `{ client_id: 'planetfitness', source: 'work-order-submission.txt' }`
- [ ] Upload content:
  - [ ] Run upload script for `planetfitness`
  - [ ] Run upload script for `ses-internal`
- [ ] Test search isolation:
  - [ ] Search "work order" on PF → Returns PF-specific content
  - [ ] Search "lockbox" on PF → Returns no results (SES content only)
  - [ ] Search "lockbox" on SES Internal → Returns lockbox content

**Success Criteria:** Content isolated per client, search results scoped correctly

---

### **Day 12-14: Search Integration**
- [ ] Modify `src/routes/search.ts`:
  - [ ] Extract `client_id` from JWT or middleware
  - [ ] Pass `client_id` to Pinecone query
  - [ ] Log search to D1: `INSERT INTO search_logs (user_email, client_id, query, response_time_ms, cached) VALUES (?, ?, ?, ?, ?)`
- [ ] Test end-to-end flow:
  - [ ] Login as PF user
  - [ ] Search "how to submit work order"
  - [ ] Verify response is PF-specific
  - [ ] Check D1 logs: `SELECT * FROM search_logs WHERE client_id = 'planetfitness'`
- [ ] Test caching:
  - [ ] First query: ~2-3 seconds
  - [ ] Repeat same query: <0.1 seconds (cached)
  - [ ] Verify `cached = 1` in search_logs

**Success Criteria:** AI search works per microsite, logs captured correctly

---

## 📊 Week 3: Admin Dashboards

### **Day 15-16: Super Admin Dashboard**
- [ ] Create `src/routes/admin-super.ts`
- [ ] Build `GET /admin/dashboard` route:
  - [ ] Check if user is super admin (client_id = NULL in admin_permissions)
  - [ ] Query D1 for all clients: `SELECT * FROM clients`
  - [ ] Aggregate stats per client:
    - [ ] User count: `SELECT COUNT(*) FROM users WHERE client_id = ?`
    - [ ] Search count: `SELECT COUNT(*) FROM search_logs WHERE client_id = ?`
    - [ ] Active users: `SELECT COUNT(*) FROM users WHERE client_id = ? AND last_login > DATE('now', '-7 days')`
  - [ ] Return dashboard data
- [ ] Build frontend at `admin.saveenergysystems.com`:
  - [ ] List all microsites (PF, SES Internal, etc.)
  - [ ] Show stats per microsite
  - [ ] "Add New Client" button
  - [ ] "View Analytics" links
- [ ] Test super admin access:
  - [ ] Login as super admin
  - [ ] See all clients in dashboard
  - [ ] Verify cross-client analytics

**Success Criteria:** Super admin dashboard shows all microsites and stats

---

### **Day 17: Add/Remove Clients (Super Admin)**
- [ ] Build `POST /admin/clients/create` route:
  - [ ] Insert into D1 clients table
  - [ ] Create `/clients/{new_client_id}/` folder
  - [ ] Copy template config.json
  - [ ] Return success
- [ ] Build `DELETE /admin/clients/:id` route:
  - [ ] Mark client as `status = 'suspended'` (soft delete)
- [ ] Build frontend forms:
  - [ ] "Create New Client" form (name, subdomain, logo upload, colors)
  - [ ] "Suspend Client" button (with confirmation)
- [ ] Test:
  - [ ] Create test client "lafitness"
  - [ ] Verify it appears in clients table
  - [ ] Verify folder created

**Success Criteria:** Super admin can add/remove clients dynamically

---

### **Day 18-19: Client Admin Dashboard**
- [ ] Create `src/routes/admin-client.ts`
- [ ] Build `GET /admin/dashboard` route (per microsite):
  - [ ] Check if user is client admin for THIS client
  - [ ] Query D1 for users in this client: `SELECT * FROM users WHERE client_id = ?`
  - [ ] Query search logs: `SELECT query, COUNT(*) as count FROM search_logs WHERE client_id = ? GROUP BY query ORDER BY count DESC LIMIT 10`
  - [ ] Return dashboard data
- [ ] Build frontend at `planetfitness.saveenergysystems.com/admin`:
  - [ ] List users (email, location, last login, searches)
  - [ ] "Add User" form (email, full_name, location)
  - [ ] "Revoke Access" button per user
  - [ ] Top searches widget
  - [ ] Analytics summary (total searches, active users)
- [ ] Test with Steph's account:
  - [ ] Login as client admin (Steph)
  - [ ] See PF users only (not SES internal)
  - [ ] Verify can add PF user
  - [ ] Verify cannot access other clients

**Success Criteria:** Client admins can manage their own microsite users/analytics only

---

### **Day 20: User Management (Client Admin)**
- [ ] Build `POST /admin/users/add` route:
  - [ ] Check client admin permissions
  - [ ] Insert user: `INSERT INTO users (email, client_id, role, status, added_by) VALUES (?, ?, 'user', 'active', ?)`
  - [ ] Send welcome email (optional)
- [ ] Build `DELETE /admin/users/:id` route:
  - [ ] Check client admin permissions
  - [ ] Update user: `UPDATE users SET status = 'suspended' WHERE id = ? AND client_id = ?`
- [ ] Test:
  - [ ] Add user as Steph (PF admin)
  - [ ] Verify user can login to PF microsite
  - [ ] Revoke user access
  - [ ] Verify user cannot login

**Success Criteria:** Client admins can add/remove users for their client

---

## 📝 Week 4: Content & Testing

### **Day 21-22: Planet Fitness Content Creation**
- [ ] Work with Steph to collect requirements
- [ ] Create 20+ text files in `/clients/planetfitness/resources/`:
  - [ ] `work-order-submission.txt`
  - [ ] `billing-guide.txt`
  - [ ] `client-protocols.txt`
  - [ ] `winter-maintenance.txt`
  - [ ] `emergency-contacts.txt`
  - [ ] `filter-ordering.txt`
  - [ ] `hvac-troubleshooting.txt`
  - [ ] `lighting-issues.txt`
  - [ ] `plumbing-procedures.txt`
  - [ ] `cleaning-standards.txt`
  - [ ] `security-protocols.txt`
  - [ ] `snow-removal.txt`
  - [ ] `parking-lot-maintenance.txt`
  - [ ] `equipment-warranties.txt`
  - [ ] `vendor-contacts.txt`
  - [ ] (5+ more based on Steph's needs)
- [ ] Write clear, searchable content:
  - [ ] Use natural language
  - [ ] Include common questions
  - [ ] Add examples
- [ ] Upload to Pinecone with `client_id = 'planetfitness'`
- [ ] Test search queries:
  - [ ] "how to submit work order"
  - [ ] "who do I call for billing"
  - [ ] "what is the client protocol"
  - [ ] "how to order filters"
  - [ ] "emergency contact number"

**Success Criteria:** 20+ PF content files, searchable, accurate responses

---

### **Day 23: SES Internal Content Creation**
- [ ] Create 15+ text files in `/clients/ses-internal/resources/`:
  - [ ] `lockbox-codes.txt`
  - [ ] `pricing-guidelines.txt`
  - [ ] `tech-procedures.txt`
  - [ ] `equipment-manuals.txt`
  - [ ] `safety-protocols.txt`
  - [ ] `time-tracking.txt`
  - [ ] `expense-reporting.txt`
  - [ ] `parts-ordering.txt`
  - [ ] `client-communication-templates.txt`
  - [ ] `troubleshooting-guides.txt`
  - [ ] (5+ more internal resources)
- [ ] Upload to Pinecone with `client_id = 'ses-internal'`
- [ ] Test SES-specific queries

**Success Criteria:** 15+ SES internal files, isolated from PF content

---

### **Day 24-25: Google Analytics Setup**
- [ ] Create 4 GA4 properties:
  - [ ] **Property 1:** Planet Fitness Hub (G-XXXXXXXXX)
  - [ ] **Property 2:** SES Internal Hub (G-YYYYYYYYY)
  - [ ] **Property 3:** Admin Portal (G-ZZZZZZZZZ)
  - [ ] (Keep 4th for future LA Fitness)
- [ ] Add GA4 IDs to `config.json` files:
  - [ ] `planetfitness/config.json`: `"ga4_property_id": "G-XXXXXXXXX"`
  - [ ] `ses-internal/config.json`: `"ga4_property_id": "G-YYYYYYYYY"`
- [ ] Inject GA4 tracking code in frontend template:
  ```html
  <script async src="https://www.googletagmanager.com/gtag/js?id={{config.ga4_property_id}}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', '{{config.ga4_property_id}}');
  </script>
  ```
- [ ] Test GA4 tracking:
  - [ ] Visit `planetfitness.*` → Check GA4 Property 1 for pageview
  - [ ] Search on `planetfitness.*` → Check for event
  - [ ] Visit `internal.*` → Check GA4 Property 2 for pageview
- [ ] Grant access:
  - [ ] Steph: Access to PF property only
  - [ ] SES Operations: Access to SES Internal property
  - [ ] You: Access to all properties (super admin)

**Success Criteria:** GA4 tracking live on all microsites, proper access control

---

### **Day 26-27: Pilot Testing**
- [ ] Recruit pilot users:
  - [ ] 5 Planet Fitness GMs
  - [ ] 5 SES employees
- [ ] Onboard pilot users:
  - [ ] Add to D1 users table
  - [ ] Send login instructions
  - [ ] Provide quick start guide
- [ ] Monitor usage:
  - [ ] Check D1 search_logs daily
  - [ ] Review GA4 analytics
  - [ ] Track adoption rate
- [ ] Collect feedback:
  - [ ] Survey after 1 week
  - [ ] Ask about:
    - [ ] Ease of use
    - [ ] Answer accuracy
    - [ ] Content gaps
    - [ ] Feature requests
- [ ] Iterate based on feedback:
  - [ ] Fix bugs
  - [ ] Add missing content
  - [ ] Improve UX

**Success Criteria:** 10 pilot users actively searching, 80%+ satisfaction

---

## 🚀 Week 5-6: Polish & Launch

### **Day 28-30: Refinement**
- [ ] Address pilot feedback:
  - [ ] Bug fixes
  - [ ] Content updates
  - [ ] UI improvements
- [ ] Performance optimization:
  - [ ] Verify caching works (repeat queries <0.1s)
  - [ ] Check database query performance
  - [ ] Optimize Pinecone filtering
- [ ] Security review:
  - [ ] Verify client isolation (no data leaks)
  - [ ] Test JWT validation
  - [ ] Check admin permissions
- [ ] Documentation:
  - [ ] Admin user guides (for Steph)
  - [ ] End user quick start (for GMs)
  - [ ] Troubleshooting FAQ

**Success Criteria:** All pilot issues resolved, system stable

---

### **Day 31-32: Production Deployment**
- [ ] Deploy to Cloudflare Pages:
  - [ ] Run migrations on production D1: `wrangler d1 migrations apply ses-hub-production`
  - [ ] Build: `npm run build`
  - [ ] Deploy: `wrangler pages deploy dist --project-name ses-hub`
- [ ] Configure DNS:
  - [ ] `planetfitness.saveenergysystems.com` → Cloudflare Pages
  - [ ] `internal.saveenergysystems.com` → Cloudflare Pages
  - [ ] `admin.saveenergysystems.com` → Cloudflare Pages
- [ ] Upload production content:
  - [ ] Upload PF content to production Pinecone
  - [ ] Upload SES content to production Pinecone
- [ ] Set up UptimeRobot:
  - [ ] Monitor `planetfitness.*/health` every 5 minutes
  - [ ] Monitor `internal.*/health` every 5 minutes
- [ ] SSL certificates:
  - [ ] Verify HTTPS works on all subdomains
- [ ] Test production:
  - [ ] Login to each microsite
  - [ ] Run test searches
  - [ ] Verify branding
  - [ ] Check GA4 tracking

**Success Criteria:** Production deployment live, all subdomains working

---

### **Day 33-35: Full Rollout**
- [ ] Onboard remaining Planet Fitness GMs:
  - [ ] Bulk import users via CSV (500 GMs)
  - [ ] Send welcome emails in batches
- [ ] Onboard SES employees:
  - [ ] Add 47 SES employees to internal microsite
- [ ] Train admins:
  - [ ] Steph: Client admin training (PF)
  - [ ] SES Ops: Internal microsite management
- [ ] Announce launch:
  - [ ] Email to all users
  - [ ] Quick start guide attached
  - [ ] Support contact info
- [ ] Monitor initial adoption:
  - [ ] Daily active users (DAU)
  - [ ] Search volume
  - [ ] Top queries
  - [ ] User feedback

**Success Criteria:** 500+ PF GMs + 47 SES employees onboarded, system live

---

### **Day 36-42: Monitoring & Optimization (Week 6)**
- [ ] Daily monitoring:
  - [ ] Check super admin dashboard
  - [ ] Review GA4 analytics
  - [ ] Monitor error logs
  - [ ] Track adoption rate
- [ ] Weekly metrics:
  - [ ] DAU / WAU / MAU
  - [ ] Total searches
  - [ ] Cache hit rate
  - [ ] Average response time
  - [ ] Support tickets (should decrease!)
- [ ] Success metrics (by end of Week 6):
  - [ ] 80%+ adoption rate (GMs using it)
  - [ ] <3s average query time
  - [ ] 60% reduction in support calls to Steph
  - [ ] 85%+ user satisfaction
- [ ] Prepare for franchise expansion:
  - [ ] Document cloning process
  - [ ] Create franchise demo page
  - [ ] Get Steph's endorsement
- [ ] Plan next client (LA Fitness):
  - [ ] Reach out to LA Fitness facilities team
  - [ ] Schedule demo
  - [ ] Prepare proposal

**Success Criteria:** System stable, adoption goals met, ready for expansion

---

## 🎯 Launch Success Metrics

### **Adoption Targets:**
- [ ] **Week 2:** 80%+ pilot users active (8/10)
- [ ] **Week 4:** 60%+ pilot retention (6/10 still using)
- [ ] **Week 6:** 70%+ full rollout adoption (350/500 PF GMs)
- [ ] **Week 8:** 80%+ full rollout adoption (400/500 PF GMs)

### **Performance Targets:**
- [ ] First-time query: <3 seconds
- [ ] Cached query: <0.1 seconds
- [ ] Uptime: 99.9% (via UptimeRobot)
- [ ] Cache hit rate: 80%+

### **Business Impact Targets:**
- [ ] Support call reduction: 60% (Steph's team)
- [ ] GM time savings: 15 min/day per GM
- [ ] User satisfaction: 85%+ (survey)
- [ ] Franchise interest: 5+ inquiries from PF franchise owners

---

## 🚨 Risk Mitigation

### **Technical Risks:**
- [ ] **Render spin-down:** UptimeRobot monitoring set up
- [ ] **Pinecone costs:** Monitor query volume, optimize filtering
- [ ] **OpenAI rate limits:** Implement request throttling
- [ ] **D1 limits:** Monitor row counts (1M free rows)
- [ ] **Client data leak:** Test client isolation thoroughly

### **Business Risks:**
- [ ] **Low adoption:** Aggressive onboarding, training, reminders
- [ ] **Content accuracy:** Pilot testing, feedback loops
- [ ] **Steph leaves PF:** Document system, cross-train backup admin
- [ ] **Contract renewal risk:** Track usage metrics, ROI demonstration

---

## ✅ Final Pre-Launch Checklist

**Before announcing to 500 GMs:**
- [ ] All pilot feedback addressed
- [ ] 100% uptime for 7 consecutive days
- [ ] All 20+ PF content files accurate
- [ ] Admin dashboards functional
- [ ] GA4 tracking verified
- [ ] User documentation complete
- [ ] Support process defined
- [ ] Backup/disaster recovery plan in place

---

## 📊 Post-Launch Tracking

**Daily (First 2 Weeks):**
- [ ] Check super admin dashboard
- [ ] Review error logs
- [ ] Monitor support tickets
- [ ] Track DAU

**Weekly:**
- [ ] Analyze top searches
- [ ] Review GA4 reports
- [ ] Check cache performance
- [ ] Survey user satisfaction

**Monthly:**
- [ ] Business metrics review (adoption, support reduction)
- [ ] Content updates based on feedback
- [ ] Plan for next client (LA Fitness, etc.)
- [ ] Franchise outreach (via Steph)

---

**Total Implementation Time:** 6 weeks (42 days)  
**Team Size:** 2-3 developers + 1 project manager  
**Budget:** $0 (using free tiers: Cloudflare, Pinecone, OpenAI within limits)

**Let's ship this! 🚀**

*Reference: `DEV-TEAM-START-HERE.md` for technical details, `MULTI-TENANT-ARCHITECTURE.md` for architecture specifics.*
