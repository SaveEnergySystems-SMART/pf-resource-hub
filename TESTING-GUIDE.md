# 🧪 TESTING YOUR PLANET FITNESS RESOURCE HUB

## ✅ SYSTEMS RUNNING

**Frontend:** https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai  
**Backend API:** http://localhost:5000  
**Status:** 🟢 ALL SYSTEMS OPERATIONAL

---

## 🎯 TEST PLAN

### **Test 1: Login Page** ✅

**URL to open:**
```
https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/login.html
```

**Test with SES Super Admin:**
- Username: `asoler`
- Password: `SES-Admin-2025!`
- Should redirect to admin dashboard (when built) or dashboard.html

**Test with PF Admin:**
- Username: `pfadmin`
- Password: `PF-Admin-2025!`
- Should redirect to PF admin dashboard (when built) or dashboard.html

**What to check:**
- ✅ Page loads with Planet Fitness branding
- ✅ Emergency banner shows (617) 564-4800
- ✅ Username and password fields work
- ✅ "Remember me" checkbox works
- ✅ "Forgot Password?" link is visible
- ✅ "Forgot Username?" link is visible

---

### **Test 2: Forgot Password** ✅

**URL to open:**
```
https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/forgot-password.html
```

**Test steps:**
1. Enter email: `asoler@saveenergysystems.com`
2. Click "Send Reset Link"
3. Check backend terminal for email output

**What to check:**
- ✅ Email input field works
- ✅ Success message appears
- ✅ Email is logged to backend console (console mode)
- ✅ "Back to Login" link works

---

### **Test 3: Forgot Username** ✅

**URL to open:**
```
https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/forgot-username.html
```

**Test steps:**
1. Enter email: `adrianasolercreative@gmail.com`
2. Click "Send Username Reminder"
3. Check backend terminal for email output

**What to check:**
- ✅ Email input field works
- ✅ Success message appears
- ✅ Username is logged to backend console
- ✅ "Back to Login" link works

---

### **Test 4: API Endpoints** ✅

**Test login API directly:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"asoler","password":"SES-Admin-2025!"}'
```

**Expected result:**
- Should return JWT token
- Should return user data with role: ses_admin

---

### **Test 5: Dashboard Pages** ✅

**Main Dashboard:**
```
https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/dashboard.html
```

**Help Now:**
```
https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/help-now.html
```

**Order Parts:**
```
https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/order-parts.html
```

**Resources:**
```
https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/resources.html
```

**Why SES:**
```
https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/why-ses.html
```

---

## 🐛 TROUBLESHOOTING

### **If login doesn't work:**
1. Open browser console (F12)
2. Check for API URL errors
3. Try demo mode (backend fallback)
4. Verify backend is running: `curl http://localhost:5000/api/health`

### **If password reset doesn't work:**
1. Check backend logs: `tail -f /home/user/pf-resource-hub/backend/backend.log`
2. Email should print to console in console mode
3. Verify API is accessible

### **If pages don't load:**
1. Verify frontend server is running on port 3000
2. Check URL is correct
3. Try refreshing the page

---

## 📧 VIEW EMAIL OUTPUT

**To see password reset emails:**
```bash
tail -f /home/user/pf-resource-hub/backend/backend.log
```

**Or check directly:**
```bash
cd /home/user/pf-resource-hub/backend
cat backend.log | grep -A 20 "EMAIL"
```

---

## ✅ WHAT TO TEST

### **Priority 1: Authentication**
- [ ] Login with SES admin (asoler / SES-Admin-2025!)
- [ ] Login with PF admin (pfadmin / PF-Admin-2025!)
- [ ] Test wrong password (should show error)
- [ ] Test "Remember me" checkbox
- [ ] Logout (if implemented)

### **Priority 2: Password Recovery**
- [ ] Request password reset for SES admin email
- [ ] Check backend console for reset link
- [ ] Request username reminder for PF admin email
- [ ] Check backend console for username

### **Priority 3: Navigation**
- [ ] Click all navigation links
- [ ] Verify all pages load correctly
- [ ] Check emergency phone number is visible
- [ ] Test Steph AI search bar (placeholder)

### **Priority 4: User Experience**
- [ ] Test on mobile (responsive design)
- [ ] Check all icons display correctly
- [ ] Verify Planet Fitness branding
- [ ] Test all buttons and links

---

## 🎯 TESTING CHECKLIST

**Frontend Pages:**
- [ ] login.html - Username/password form works
- [ ] forgot-password.html - Email submission works
- [ ] forgot-username.html - Email submission works
- [ ] dashboard.html - Page loads with navigation
- [ ] help-now.html - Emergency content displays
- [ ] order-parts.html - Parts catalog displays
- [ ] resources.html - Resources load correctly
- [ ] why-ses.html - Corporate info displays

**Backend API:**
- [ ] /api/health - Returns healthy status
- [ ] /api/auth/login - Login works
- [ ] /api/auth/forgot-password - Sends reset email
- [ ] /api/auth/forgot-username - Sends username
- [ ] /api/users - Returns user list (admin only)

**Security:**
- [ ] JWT tokens are generated
- [ ] Passwords are hashed in database
- [ ] Invalid credentials are rejected
- [ ] Activity is logged

---

## 📊 TEST RESULTS

**Backend Status:** 🟢 RUNNING  
**Frontend Status:** 🟢 RUNNING  
**Database Status:** 🟢 READY (2 admin accounts)  
**API Endpoints:** 🟢 ALL WORKING  

---

## 🚀 NEXT STEPS AFTER TESTING

Once testing is complete:

**If everything works:**
- ✅ Build admin dashboards
- ✅ Deploy to production (Railway + Cloudflare)
- ✅ Add Google Analytics
- ✅ Configure real emails (SendGrid)

**If issues found:**
- 🐛 Report the issue
- 🔧 I'll fix it immediately
- 🧪 Re-test

---

## 📞 QUICK REFERENCE

**Admin Logins:**
- SES: asoler / SES-Admin-2025!
- PF: pfadmin / PF-Admin-2025!

**Main URL:**
https://3000-i7ealb3ubmjtlryte4w5n-2b54fc91.sandbox.novita.ai/login.html

**Backend API:**
http://localhost:5000

**Emergency Contact:**
(617) 564-4800

---

**Ready to test? Open the main URL above and try logging in!** 🧪
