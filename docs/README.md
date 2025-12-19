# 🏋️ Planet Fitness Resource Hub - UI Demo

**Phase 1: Static UI Mockup** (No backend yet - Pure HTML/CSS/JS)

---

## 📦 What's Included

This is a **static UI mockup** showing what the Planet Fitness Resource Hub will look like. Perfect for getting feedback from Steph before building the backend!

### Files:
- **`index.html`** - Login page with GuideFlow-style sliding door animation
- **`dashboard.html`** - Main dashboard showing "How do I order parts?"
- **`dashboard-hvac.html`** - Alternate dashboard showing "My HVAC isn't working"
- **`images/`** - Logo files (PF logo + SES logo)

---

## 🎨 Design Features

### ✅ Planet Fitness Branding
- **Colors:**
  - Dark Purple: `#290241` (headers, accents)
  - Bright Purple: `#9600FA` (buttons, links)
  - Light Purple: `#FAEEFF` (backgrounds, hovers)
  - Yellow: `#FFDC00` (call-to-action accents)
  - Pure White: `#FFFFFF`

- **Typography:** San-serif fonts throughout (clean, modern)

### ✅ Dual Branding
- Planet Fitness logo (left)
- SES logo (right) with tagline: "AI-driven energy and facility management systems"

### ✅ Navigation
- Dashboard | Order Parts | FAQ | Franchise Info
- Clean, modern nav bar with purple accent on active link

### ✅ GuideFlow-Style Login
- Animated sliding door panels (purple)
- Email-based login
- Smooth transitions and animations

### ✅ AI Search Bar
- Fixed to bottom of page
- Purple "Send" button
- Placeholder shows example questions

---

## 🚀 How to View

### Option 1: Open Directly in Browser
1. **Replace the PF logo:**
   ```bash
   # Copy your actual Logo-Primary.svg to images/ folder
   cp /path/to/Logo-Primary.svg images/
   ```

2. **Open in browser:**
   - Open `index.html` in your web browser
   - Enter any email (e.g., `test@planetfitness.com`)
   - Click "Access Dashboard"
   - You'll see the main dashboard!

3. **Try the alternate view:**
   - After logging in, manually navigate to `dashboard-hvac.html`
   - This shows the "My HVAC isn't working" page

### Option 2: Run with Simple HTTP Server
```bash
# Python 3
python3 -m http.server 8000

# Then open: http://localhost:8000
```

---

## 📸 Screenshots to Show Steph

### 1. Login Page (`index.html`)
- Animated sliding doors
- Dual branding (PF + SES)
- Email input field
- Purple buttons

### 2. Dashboard - Order Parts (`dashboard.html`)
- Question: "How do I order parts for my location?"
- Detailed answer with numbered steps
- Quick action cards (Air Filters, HVAC Parts, Cleaning Supplies)
- Example questions at bottom
- Fixed search bar

### 3. Dashboard - HVAC Support (`dashboard-hvac.html`)
- Question: "My HVAC isn't working - What should I do?"
- Emergency alert box
- Troubleshooting steps
- Action buttons (Submit Work Order, Call Support)
- Emergency contact cards

---

## 🎯 Get Feedback From Steph

### Questions to Ask:
1. **Branding:**
   - Do you like the purple color scheme?
   - Is the dual branding (PF + SES) working?
   - Should we adjust any colors?

2. **Content:**
   - Are the example questions relevant?
   - Are the answers helpful and clear?
   - What other questions should we include?

3. **Layout:**
   - Is the navigation intuitive?
   - Do you like the fixed search bar at the bottom?
   - Should we add/remove any sections?

4. **Functionality:**
   - Do you want quick links to external vendors?
   - Should we add a "Submit Work Order" form?
   - What admin features do you need?

---

## 🔧 Easy Customizations

### Change Colors
Edit the `:root` section at the top of any HTML file:
```css
:root {
  --pf-dark-purple: #290241;    /* Change this */
  --pf-bright-purple: #9600FA;  /* Or this */
  --pf-yellow: #FFDC00;         /* Or this */
}
```

### Change Questions/Answers
Edit the `<div class="answer-box">` sections in:
- `dashboard.html` (Order Parts question)
- `dashboard-hvac.html` (HVAC troubleshooting)

### Add More Example Questions
Edit the `<span class="example-tag">` elements in `dashboard.html`

---

## ⏭️ Next Steps After Approval

Once Steph approves the UI design, we'll move to **Phase 2**:

### Phase 2: Backend Integration (Week 1-2)
1. ✅ Clone GuideFlowAI backend
2. ✅ Add real authentication (email-based login)
3. ✅ Connect AI search to OpenAI + Pinecone
4. ✅ Create 20+ Planet Fitness text files (content)
5. ✅ Upload content to Pinecone
6. ✅ Add Cloudflare D1 database (users, search logs)
7. ✅ Deploy to Cloudflare Pages

### Phase 3: Admin Panel for Steph (Week 3)
1. ✅ Build admin dashboard
2. ✅ Add user management (add/remove users by email)
3. ✅ Add analytics (top searches, active users)
4. ✅ Add SES super-admin access

### Phase 4: Testing & Launch (Week 4)
1. ✅ Pilot with 5 PF GMs
2. ✅ Collect feedback
3. ✅ Full rollout (500 GMs)
4. ✅ Monitor adoption metrics

---

## 📁 File Structure

```
planetfitness-demo/
├── index.html              # Login page with sliding doors
├── dashboard.html          # Main dashboard (Order Parts)
├── dashboard-hvac.html     # HVAC troubleshooting page
├── images/
│   ├── Logo-Primary.svg    # Planet Fitness logo (REPLACE THIS!)
│   └── ses-logo.png        # SES logo (already downloaded)
└── README.md               # This file
```

---

## 🎨 What Steph Will See

1. **Professional branding** - Purple Planet Fitness colors, clean fonts
2. **Dual logos** - PF + SES partnership visible
3. **Clear answers** - Step-by-step instructions for common questions
4. **Easy navigation** - Simple menu, intuitive layout
5. **Mobile-friendly** - Works on phones and tablets
6. **AI search** - Placeholder for future AI-powered search

---

## 💰 Cost Estimate (When We Build Backend)

**FREE TIER:**
- Cloudflare Pages: FREE
- Cloudflare D1 Database: FREE (up to 5GB)
- Pinecone: FREE (100K vectors)
- GitHub: FREE

**PAID (Minimal):**
- OpenAI API: ~$10-20/month (based on usage)

**TOTAL: ~$10-20/month** 🎉

---

## ✅ What to Do Next

1. **Show this to Steph** - Open `index.html` in a browser and walk through the demo
2. **Get feedback** - Colors, layout, content, functionality
3. **Make quick changes** - HTML/CSS changes are instant (no backend needed)
4. **Approve design** - Once Steph is happy, we build the backend!

---

## 📞 Questions?

Contact: support@saveenergysystems.com

**Built by:** SES Development Team  
**Date:** December 19, 2025  
**Version:** Phase 1 UI Mockup  
**Status:** Ready for Steph's Review ✅
