# Logo Setup Instructions

## Adding Your Logo

1. **Save your logo file** as `logo.png` in the `static/` folder:
   ```
   /Users/hadia/mvp-cs391/static/logo.png
   ```

2. **Recommended logo specifications:**
   - Format: PNG (with transparent background preferred)
   - Size: 200x200px or larger (will be scaled down)
   - The logo should be the LawyerConnect logo with scales of justice and handshake

3. **The logo will automatically appear:**
   - In the navigation bar (top left)
   - On the landing page (centered, larger size)

4. **If the logo doesn't load:**
   - The code includes `onerror="this.style.display='none'"` so the page won't break
   - Check that the file is named exactly `logo.png` (case-sensitive)
   - Ensure the file is in the `static/` directory

## Current Status

The website is configured to display the logo, but you need to add the actual `logo.png` file to the `static/` folder.

