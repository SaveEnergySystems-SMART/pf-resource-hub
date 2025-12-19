# 🧪 TESTING YOUR PLANET FITNESS RESOURCE HUB - QUICK START

## ✅ YOUR SYSTEM IS READY TO TEST!

### 🌐 **FRONTEND URL**
```
https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai
```

### 🔌 **BACKEND API**
```
http://localhost:5000
Status: 🟢 RUNNING
```

---

## 🎯 **QUICK TEST LINKS**

### **Start Here: Main Dashboard (Original Login)**
📍 **URL:** https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/index.html

This is the original login page (email-only demo mode). It works and will redirect you to dashboard.html.

### **New Login Page (Username/Password)**
📍 **URL:** https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/login.html

**Login with:**
- Username: `asoler`
- Password: `SES-Admin-2025!`

### **Password Reset**
📍 **URL:** https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/forgot-password.html

**Test with:** asoler@saveenergysystems.com

### **Username Recovery**
📍 **URL:** https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/forgot-username.html

**Test with:** adrianasolercreative@gmail.com

---

## 📄 **ALL PAGES**

### **Authentication Pages (NEW)**
1. **Login** - https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/login.html
2. **Forgot Password** - https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/forgot-password.html
3. **Forgot Username** - https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/forgot-username.html

### **Resource Pages (Existing)**
4. **Dashboard** - https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/dashboard.html
5. **Help Now** - https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/help-now.html
6. **Order Parts** - https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/order-parts.html
7. **Resources** - https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/resources.html
8. **Why SES** - https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/why-ses.html

---

## 👤 **TEST CREDENTIALS**

### **SES Super Admin**
```
Username: asoler
Password: SES-Admin-2025!
Email: asoler@saveenergysystems.com
Role: Full access to all features
```

### **PF Test Admin**
```
Username: pfadmin
Password: PF-Admin-2025!
Email: adrianasolercreative@gmail.com
Role: Location-specific access
```

---

## 🧪 **WHAT TO TEST**

### **1. Login Flow** ✅
- [ ] Open login.html
- [ ] Enter username: `asoler`
- [ ] Enter password: `SES-Admin-2025!`
- [ ] Check "Remember me"
- [ ] Click "Sign In"
- [ ] Should get JWT token and redirect

### **2. Password Reset** ✅
- [ ] Open forgot-password.html
- [ ] Enter email: `asoler@saveenergysystems.com`
- [ ] Click "Send Reset Link"
- [ ] Check backend logs for email

### **3. Username Recovery** ✅
- [ ] Open forgot-username.html
- [ ] Enter email: `adrianasolercreative@gmail.com`
- [ ] Click "Send Username Reminder"
- [ ] Check backend logs for username

### **4. Navigation** ✅
- [ ] Click through all resource pages
- [ ] Verify Steph AI search bar appears
- [ ] Check emergency contact (617) 564-4800
- [ ] Test all navigation links

---

## 📧 **VIEW EMAIL OUTPUT**

**To see password reset/username emails:**
```bash
tail -f /home/user/pf-resource-hub/backend/backend.log
```

**Or view all emails:**
```bash
cat /home/user/pf-resource-hub/backend/backend.log | grep -A 30 "EMAIL"
```

---

## 🔍 **TEST BACKEND API DIRECTLY**

### **Test Health Check**
```bash
curl http://localhost:5000/api/health
```

### **Test Login**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"asoler","password":"SES-Admin-2025!"}'
```

### **Test Password Reset**
```bash
curl -X POST http://localhost:5000/api/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email":"asoler@saveenergysystems.com"}'
```

### **Test Username Recovery**
```bash
curl -X POST http://localhost:5000/api/auth/forgot-username \
  -H "Content-Type: application/json" \
  -d '{"email":"adrianasolercreative@gmail.com"}'
```

---

## 🐛 **TROUBLESHOOTING**

### **If login doesn't connect to backend:**
The login.html file is configured for localhost:5000. This works in the sandbox but won't work from external browsers. 

**Two options:**

**Option A: Test in sandbox** (Current)
- Backend works locally
- Login connects to http://localhost:5000
- All API calls work

**Option B: Deploy to production**
- Deploy backend to Railway
- Deploy frontend to Cloudflare Pages
- Update API URLs
- Test from anywhere

### **Current Testing Limitation:**
The new login.html requires backend API connection, which only works within the sandbox environment. The original index.html uses demo mode and works everywhere.

**For full testing, we should:**
1. Deploy backend to Railway first
2. Update API URL in login.html to Railway URL
3. Then test the full authentication flow

---

## ✅ **WHAT WORKS NOW**

**Fully Working (Local Testing):**
- ✅ Backend API on localhost:5000
- ✅ All API endpoints tested and working
- ✅ Database with 2 admin accounts
- ✅ Email service (console mode)
- ✅ JWT token generation
- ✅ Password reset flow
- ✅ Username recovery flow

**Fully Working (Remote Access):**
- ✅ Original demo pages (index.html, dashboard.html, etc.)
- ✅ All resource pages (help-now, order-parts, resources, why-ses)
- ✅ Page navigation and Steph AI interface
- ✅ Emergency contact information

**Needs Deployment for Full Testing:**
- ⏳ New login.html with backend connection
- ⏳ Admin dashboards (when built)
- ⏳ Real email sending (when SendGrid configured)

---

## 🚀 **RECOMMENDED NEXT STEPS**

### **Option 1: Deploy to Production Now** (Recommended)
This will make everything fully testable:
1. Deploy backend to Railway
2. Deploy frontend to Cloudflare Pages
3. Update API URLs
4. Test full authentication flow

**Say:** "Deploy to production"

### **Option 2: Build Admin Dashboards First**
Build the user management interfaces, then deploy everything:
**Say:** "Build admin dashboards"

### **Option 3: Test What Works Now**
Test the resource pages and original demo mode:
- Open: https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/index.html
- Test: All resource pages and navigation
- Verify: Page design and content

---

## 📊 **TEST RESULTS SO FAR**

**Backend API:**
- Health check: ✅ PASS
- Login endpoint: ✅ PASS (both admins)
- Forgot password: ✅ PASS
- Forgot username: ✅ PASS

**Frontend Pages:**
- Resource pages: ✅ ACCESSIBLE
- New auth pages: ✅ CREATED (needs deployment for full test)

**Database:**
- Admin accounts: ✅ CREATED
- Password hashing: ✅ WORKING
- Activity logs: ✅ READY

---

## 💡 **WHAT WOULD YOU LIKE TO DO?**

1. **"Deploy to production"** - Make everything fully functional
2. **"Build admin dashboards"** - Create management interfaces first  
3. **"Test the resource pages"** - Test what's fully working now
4. **"Show me backend logs"** - View API activity and emails
5. **"Create backup package"** - Download everything

**What's your choice?** 🚀
