import os, json, subprocess, sys, pathlib

root = pathlib.Path(__file__).resolve().parents[1]
configs = [
    root / "configs" / "win10_chrome_latest.json",
    root / "configs" / "macos_sonoma_safari_latest.json",
]

procs = []
env = os.environ.copy()
for cfg_path in configs:
    cfg = json.loads(cfg_path.read_text())
    child_env = env.copy()
    child_env.update(cfg)
    print(f"Starting Behave for {cfg['LT_PLATFORM']} • {cfg['LT_BROWSER']} {cfg['LT_VERSION']}")
    p = subprocess.Popen([sys.executable, "-m", "behave", "-k"], cwd=root, env=child_env)
    procs.append(p)

exit_codes = [p.wait() for p in procs]
combined = 0 if all(c == 0 for c in exit_codes) else 1
sys.exit(combined)
