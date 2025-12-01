# ⚡ Quick Deployment Checklist

## Pre-Deployment (5 minutes)

- [ ] Code is pushed to GitHub
- [ ] You have a Render account (sign up at render.com)
- [ ] All files are committed: `render.yaml`, `Procfile`, updated `settings.py`

## Deployment Steps (10-15 minutes)

### 1. Connect to Render
- [ ] Go to https://dashboard.render.com
- [ ] Click **"New +"** → **"New Blueprint"**
- [ ] Connect your GitHub repository
- [ ] Click **"Apply"** when Render detects `render.yaml`

### 2. Set Environment Variable
- [ ] Go to your service → **"Environment"** tab
- [ ] Add: `ALLOWED_HOSTS` = `your-app-name.onrender.com`
- [ ] Click **"Save Changes"**

### 3. Wait for Deployment
- [ ] Monitor build logs (5-10 minutes)
- [ ] Wait for **"Live"** status
- [ ] Copy your app URL

### 4. Test
- [ ] Visit your app URL
- [ ] Test API endpoints
- [ ] Check logs for errors

## Done! 🎉

Your app is live at: `https://your-app-name.onrender.com`

---

**Need detailed instructions?** See `DEPLOYMENT.md`

