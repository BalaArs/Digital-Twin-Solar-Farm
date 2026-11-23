---
name: sut-fix-pr
description: Fix a defect (F<n>) in the system under test (Solar_Farm.ino, index.html or Untitled3.ipynb) as its own pull request, flipping its strict-xfail test to passing and keeping the Python firmware model in sync. Use when asked to fix a finding from the coverage report or docs/SIMULATION_HARNESS.md.
---

# Fix a system-under-test defect

The rule: **one defect per PR, on a `fix/f<n>-<slug>` branch.** The PR removes that defect's `xfail(strict=True)` marker. Strictness means that if the fix doesn't make the test pass, the suite goes red.

## 1. Locate

* `grep -rn '"F<n>' sim/tests` finds the xfail tests that define "fixed".
* Read the finding row in `docs/SIMULATION_HARNESS.md` (section 5).
* Reproduce it first: `uv run pytest -q -rxX <test ids>` should show `xfail`.

## 2. Branch

* Base it on `main`.
* If another open firmware fix also edits `Solar_Farm.ino`, stack the new branch on that PR to avoid conflicts, and say so in the PR body.
* Run `git -c filter.nbstripout.clean=cat switch -c fix/f<n>-<slug>`. The flag stops the nbstripout filter from blocking the switch.
* Run `git checkout -- graphify-out/` if the graphify hook left rebuild noise.

## 3. Fix

* **Firmware** (`Solar_Farm.ino`):
  * Keep the change minimal and keep the existing style.
  * Mirror the behaviour change in `sim/firmware_model.py`, including the float32 casts and `%.2f` formatting.
  * `sim/tests/test_fil.py::test_fil_differential_10000_random_vectors` must still pass. It compares the real sketch with the model, byte for byte.
  * If the fix uses a new Arduino, ESP32 or Blynk API, add it to the shim (`sim/fil/include/*.h`, `sim/fil/shim.cpp`).
* **Web UI** (`index.html`): vanilla JS only, no build step. The Playwright tests open it from `file://`.
* **Notebook**:
  * Edit with `nbformat` (`uv run python -I`), not by hand.
  * Clear outputs when you save.
  * The data path comes from `SOLAR_DATA_DIR`.

## 4. Verify

```bash
uv run ruff check --fix sim && uv run ruff format sim
uv run pytest -q                                          # all green except the remaining F-xfails
uv run pytest -q --run-slow sim/tests/test_esp32_compile.py  # firmware changes: real ESP32 build
```

Then:

* Remove the F<n> `xfail` marker(s).
* Update the status in `docs/SIMULATION_HARNESS.md`, and in the README findings table if the resolution changed.
* Update README setup steps if user-visible behaviour changed.

## 5. PR (fork only)

```bash
git push -u origin fix/f<n>-<slug>
gh pr create --repo BalaArs/Digital-Twin-Solar-Farm --base <main or stacked branch> --head fix/f<n>-<slug> ...
```

Always pass `--repo BalaArs/...`: `gh` defaults to the upstream repo for forks.

The body must contain:

* **Summary:** the defect, how the harness showed it, and the change.
* **Test plan:** checkboxes, with any hardware-only checks left unchecked.
* The Claude Code footer.

Never open PRs against `xvishnuprasad/...` unless explicitly asked.
