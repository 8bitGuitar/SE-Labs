# Issues Found and Fixed

Reports for the original code are in `before/`, reports for the fixed code are in `after/`.

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.64/10 | 10.00/10 |
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | 0 issues |
| Flake8 | 4 issues | 0 issues |

Line numbers refer to the original `event_manager.py`.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection (Bandit B605, High) | Security | 56 | `os.system("lp badges_" + eventName + ".txt")` runs a shell string built from input, so an event name such as `x; rm -rf ~` would run extra commands. | Use `subprocess.run([lp_path, badge_file], check=True)` with an argument list and no shell; resolve `lp` with `shutil.which` and handle it being missing. The remaining low-severity B404/B603 notices were reviewed and marked `# nosec`. |
| Unsafe deserialization with pickle (Bandit B301 Medium, B403 Low) | Security | 2, 44-51 | `pickle.load` can execute arbitrary code if `events.pkl` is replaced or tampered with. | Save and load with `json` (`events.json`) and open files with `encoding="utf-8"`. The data is only strings, ints, lists and dicts, so JSON holds it fully. |
| Mutable default argument (Pylint W0102) | Bug | 9-11 | `guests=[]` is created once, so every event shares one guest list. In the demo, Alumni Dinner looked full ("cannot add Meena") and showed 0 seats left. | Default to `None` and create a new list inside `create_event`. Alumni Dinner now accepts Meena and shows 1 seat left. |
| Weak random generator (Bandit B311, Low) | Security | 72 | `random.choice` is predictable, which is not suitable for a fair lucky draw. | Use `secrets.choice`. |
| Unused argument (Pylint W0613) | Code smell | 39 | `guestReport` accepted `sortOrder` but ignored it. | `guest_report` now uses `sort_order`: `"name"` sorts alphabetically, `"registration"` keeps sign-up order, and anything else raises `ValueError`. |
| Non-snake_case names (Pylint C0103) | Style | 9-54 | Functions and arguments used camelCase (`createEvent`, `eventName`, ...). | Renamed to snake_case (`create_event`, `event_name`, ...). |
| Missing docstrings (Pylint C0114, C0116) | Style | 1, every function | No module or function docstrings. | Added a module docstring and one for each function. |
| Unnecessary `else` after `return` (Pylint R1705) | Style | 33-36 | `eventStatus` used `else` after a `return`. | Removed the `else` and de-indented the second return. |
| Missing whitespace (Flake8 E231, E225) | Style | 61, 66 | `"Rooftop",2` and `left=seatsLeft(...)`. | Added a space after the comma and around `=`. |
| Inline comment spacing (Flake8 E261) | Style | 75 | Only one space before `# reload ...`. | Used two spaces. |
| Top-level call without spacing or main guard (Flake8 E305) | Style | 79 | `main()` ran on import, directly after a function with one blank line. | Added two blank lines and wrapped the call in `if __name__ == "__main__":`. |
