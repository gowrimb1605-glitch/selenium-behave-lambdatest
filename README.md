# Selenium 101 — Behave + LambdaTest (Parallel)

This repo contains an implementation of the **Selenium 101** assignment using **Python, Behave, and Selenium 4**.  
It covers all three scenarios from the PDF and is wired to run on **LambdaTest** with **network logs, video, screenshots, and console logs** enabled. A helper script runs the suite **in parallel across two browser/OS combinations**.

## Scenarios Implemented
1. **Simple Form Demo** — message echo verification
2. **Drag & Drop Sliders** — set default slider to 95
3. **Input Form Submit** — form validation & success message

## Quick Start (Local / Gitpod)

1. **Install deps**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set LambdaTest credentials**
   - Copy `.env.example` to `.env` and fill in:
     ```env
     LT_USERNAME=your_username
     LT_ACCESS_KEY=your_access_key
     ```

3. **Run once (single combination)**
   ```bash
   behave -k
   ```

4. **Run in parallel on two combos**
   ```bash
   python scripts/run_parallel.py
   ```
   The script will run Behave simultaneously against:
   - Windows 10 • Chrome (latest)
   - macOS Sonoma • Safari (latest)

### Environment overrides (optional)
You can override target combo per run:
```bash
LT_PLATFORM="Windows 11" LT_BROWSER="Edge" LT_VERSION="latest" behave -k
```

## Repository Requirements (per assignment)
- **3+ locator strategies** used (id, name, css selector, xpath, link text).
- **Parallel on at least 2 combos** (`scripts/run_parallel.py`).
- **Network logs, video, screenshots, console logs** enabled via `lt:options` in capabilities.
- **Gitpod-ready** via `.gitpod.yml`.
- **Behave** BDD with step definitions in `features/steps`.

## LambdaTest Notes
- Hub URL: `https://hub.lambdatest.com/wd/hub`
- Ensure your trial minutes are available.
- Each scenario is named in LT as: `Selenium 101 — <Feature> — <Scenario>`
  and the **status** is marked `passed/failed` via the LambdaTest REST endpoint.

## Pushing to GitHub
1. Create a new (private) GitHub repo.
2. Initialize and push:
   ```bash
   git init
   git add .
   git commit -m "Selenium 101 — Behave + LambdaTest"
   git branch -M main
   git remote add origin <YOUR_GIT_REMOTE_URL>
   git push -u origin main
   ```
3. Share repo access with `LambdaTest-Certifications` or `admin@lambdatestcertifications.com`.

## Running in CI (optional)
A sample **GitHub Actions** workflow is under `.github/workflows/behave.yml`.  
Set **LT_USERNAME** and **LT_ACCESS_KEY** in repo **Secrets**.

---

**Happy testing!**
