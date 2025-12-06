# Vercel Deployment - Super Simple Guide

## What You're Doing

You're putting your website on the internet so anyone can visit it. Think of it like:
- **Your computer** = Your house (where you build the website)
- **Vercel** = A free hosting service (like a free apartment for your website)
- **Database** = A storage room (where all your data lives)

---

## The Problem

Vercel is like a hotel room - you can't store things permanently. So we need a separate "storage room" (database) that stays permanent.

---

## Step-by-Step (Like Following a Recipe)

### STEP 1: Get a Free Storage Room (Database) - 5 minutes

**What you're doing:** Getting a free place to store your data (users, lawyers, etc.)

1. **Go to this website:** https://supabase.com
2. **Click "Start your project"** (big green button)
3. **Sign up** - Use your email or GitHub account
4. **Click "New Project"**
5. **Fill in:**
   - Name: `lawyerconnect` (or anything you want)
   - Password: Make up a password (WRITE IT DOWN!)
   - Region: Pick the one closest to you
6. **Click "Create new project"**
7. **Wait 2-3 minutes** (it's setting up your storage room)

**Once it's ready:**
8. **Click the gear icon** (⚙️) on the left side
9. **Click "Database"**
10. **Scroll down** until you see "Connection string"
11. **Click the "URI" tab**
12. **Copy the text** - it looks like:
    ```
    postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
    ```
13. **Replace `[YOUR-PASSWORD]`** with the password you made in step 5
14. **Save this somewhere** - you'll need it later!

**✅ Done with Step 1!** You now have a storage room.

---

### STEP 2: Put Your Website on Vercel - 5 minutes

**What you're doing:** Uploading your website to Vercel so people can visit it

1. **Open Terminal** (on your Mac, press Cmd + Space, type "Terminal", press Enter)

2. **Type this and press Enter:**
   ```bash
   npm install -g vercel
   ```
   (This installs a tool to talk to Vercel)
   
   **If it says "command not found":**
   - Install Node.js first: https://nodejs.org (download and install)
   - Then try the command again

3. **Type this and press Enter:**
   ```bash
   vercel login
   ```
   - A browser window will open
   - Click "Continue with GitHub" (or sign up if you don't have an account)
   - Click "Authorize" or "Allow"

4. **Type this and press Enter:**
   ```bash
   cd /Users/hadia/mvp-cs391
   ```
   (This goes to your project folder)

5. **Type this and press Enter:**
   ```bash
   vercel
   ```
   
   **It will ask you questions - answer like this:**
   - "Set up and deploy?" → Type `Y` and press Enter
   - "Which scope?" → Press Enter (use default)
   - "Link to existing project?" → Type `N` and press Enter
   - "What's your project's name?" → Press Enter (use default)
   - "In which directory is your code located?" → Press Enter (use `.`)
   - "Want to override settings?" → Type `N` and press Enter

6. **Wait 1-2 minutes** - Vercel is uploading your website

7. **You'll see a URL** like: `https://lawyerconnect-mvp-xxxxx.vercel.app`
   - **Copy this URL** - this is your website!

**✅ Done with Step 2!** Your website is now on the internet, but it's not connected to the storage room yet.

---

### STEP 3: Connect Your Website to the Storage Room - 3 minutes

**What you're doing:** Telling your website where to find the storage room (database)

1. **Go to:** https://vercel.com/dashboard
2. **Click on your project** (the one you just created)
3. **Click "Settings"** (at the top)
4. **Click "Environment Variables"** (on the left side)

5. **Add the first secret:**
   - Click "Add New"
   - Name: Type `SECRET_KEY`
   - Value: Open Terminal and type:
     ```bash
     python -c "import secrets; print(secrets.token_hex(32))"
     ```
     - Copy the long text that appears
     - Paste it in the "Value" box
   - Check all three boxes: Production, Preview, Development
   - Click "Save"

6. **Add the second secret:**
   - Click "Add New" again
   - Name: Type `DATABASE_URL`
   - Value: Paste the connection string you saved from Step 1 (the one with your password)
   - Check all three boxes: Production, Preview, Development
   - Click "Save"

7. **Go back to Terminal** and type:
   ```bash
   vercel --prod
   ```
   (This updates your website with the new secrets)

**✅ Done with Step 3!** Your website now knows where the storage room is.

---

### STEP 4: Set Up the Storage Room - 2 minutes

**What you're doing:** Creating the tables (shelves) in your storage room

1. **Open your website URL** (the one from Step 2)
2. **Add this to the end:** `/admin/setup-db`
   - Full URL looks like: `https://your-app.vercel.app/admin/setup-db`
3. **Press Enter** - You should see "Database Setup Complete!"
4. **Now add this:** `/admin/seed-db`
   - Full URL: `https://your-app.vercel.app/admin/seed-db`
5. **Press Enter** - You should see "Database Seeded!"

**✅ Done with Step 4!** Your storage room now has shelves and some sample data.

---

### STEP 5: Clean Up (Important!) - 2 minutes

**What you're doing:** Removing the setup pages so strangers can't mess with your database

1. **Open the file:** `app/routes.py` in your code editor
2. **Find these lines** (near the end of the file):
   - `@main_bp.route("/admin/setup-db"` 
   - `@main_bp.route("/admin/seed-db"`
3. **Delete everything from those lines** until you see the next `@main_bp.route` or the end of the file
4. **Save the file**

5. **Go back to Terminal** and type:
   ```bash
   vercel --prod
   ```
   (This updates your website without the setup pages)

**✅ Done with Step 5!** Your website is now secure.

---

### STEP 6: Test Your Website - 1 minute

1. **Visit your website URL** (from Step 2)
2. **Try to:**
   - Sign up for an account
   - Log in
   - Submit an issue
   - See if lawyers appear

**✅ If everything works, you're done!**

---

## Troubleshooting (If Something Goes Wrong)

### "Command not found" when running `npm`
- **Fix:** Install Node.js from https://nodejs.org

### "Could not connect to database"
- **Fix:** 
  - Check that you replaced `[YOUR-PASSWORD]` in the connection string
  - Make sure Supabase project is still active (not paused)
  - Check the `DATABASE_URL` in Vercel settings

### "Tables not found"
- **Fix:** Make sure you visited `/admin/setup-db` first

### "No lawyers showing"
- **Fix:** Make sure you visited `/admin/seed-db` after setup

### Website shows an error
- **Fix:** 
  - Check Vercel dashboard → Deployments → Click on latest → View logs
  - Look for error messages

---

## Quick Checklist

Before you start:
- [ ] Have your code saved and pushed to GitHub (optional but recommended)
- [ ] Have Terminal open
- [ ] Have a browser open

During setup:
- [ ] Created Supabase account
- [ ] Created Supabase project
- [ ] Copied connection string (with password replaced)
- [ ] Installed Vercel CLI (`npm install -g vercel`)
- [ ] Logged into Vercel (`vercel login`)
- [ ] Deployed to Vercel (`vercel`)
- [ ] Added `SECRET_KEY` in Vercel dashboard
- [ ] Added `DATABASE_URL` in Vercel dashboard
- [ ] Redeployed (`vercel --prod`)
- [ ] Visited `/admin/setup-db`
- [ ] Visited `/admin/seed-db`
- [ ] Removed setup endpoints from code
- [ ] Redeployed again (`vercel --prod`)
- [ ] Tested the website

---

## What Each Step Does (Simple Explanation)

1. **Step 1 (Database):** Like renting a storage unit to keep your stuff
2. **Step 2 (Deploy):** Like moving your website to a free apartment (Vercel)
3. **Step 3 (Connect):** Like giving your website the address of the storage unit
4. **Step 4 (Setup):** Like organizing shelves in the storage unit
5. **Step 5 (Clean up):** Like locking the door so strangers can't get in
6. **Step 6 (Test):** Like checking everything works

---

## Need Help?

If you get stuck:
1. **Read the error message** - it usually tells you what's wrong
2. **Check the logs** - In Vercel dashboard → Deployments → Click latest → Logs
3. **Double-check your connection string** - Make sure password is correct
4. **Make sure Supabase project is active** - Go to Supabase dashboard and check

---

## Summary

**In simple terms:**
1. Get a free database (Supabase) - 5 min
2. Upload your website (Vercel) - 5 min  
3. Connect them together - 3 min
4. Set up the database - 2 min
5. Clean up - 2 min
6. Test - 1 min

**Total time: ~18 minutes**

**Your website will be live at:** `https://your-app-name.vercel.app`

Good luck! You've got this! 🚀

