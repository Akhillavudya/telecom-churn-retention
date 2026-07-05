# Step 7 — Pushing public + deploying the live report

> Beginner explainer for **Task 7** of `docs/final_plan.md` — the final step.
> New words are defined the first time they appear; the full list lives in
> [`GLOSSARY.md`](./GLOSSARY.md).

---

## 1. Big Picture — why this step exists

Everything so far lived on your laptop. A portfolio piece nobody can click is worth almost nothing to a
recruiter. This step makes two things public and permanent:

1. **The code** — pushed to a public GitHub repository, so anyone can read the analysis and re-run it.
2. **The live report** — the Quarto page (with the interactive ROI calculator) published to a real URL
   anyone can open in a browser, no install required.

After this step the project is **CV-ready**: a link in your CV goes straight to a working, interactive
analytics report backed by a clean, reproducible repo.

---

## 2. Core concepts, explained simply

- **Remote** — a copy of your git repository that lives on a server (here, GitHub). `origin` is the
  default name for "the main remote." `git push origin main` uploads your local `main` branch commits to
  it.

- **Branch** — a named line of commits. This repo uses two: `main` (all the source code and docs) and
  `gh-pages` (a *separate* branch holding **only the built website**). Keeping the site on its own branch
  is a common convention so generated HTML never clutters your source branch.

- **GitHub Pages** — GitHub's free static-website host. Its long-standing rule: if a repo has a branch
  literally named `gh-pages`, GitHub automatically serves its contents at
  `https://<user>.github.io/<repo>/`. That is why we named the branch exactly `gh-pages` — the name is
  the trigger.

- **`.nojekyll`** — an empty marker file. By default GitHub Pages runs your files through *Jekyll*, a
  site generator that **ignores files and folders beginning with an underscore** (`_`). Quarto sometimes
  emits such names, so this file tells Pages "serve my files exactly as-is, don't process them."

- **Static site** — a site made of plain files (HTML/CSS/JS) with no server-side code. Because our page
  is self-contained HTML with the calculator running in the browser, a static host is all we need — free,
  fast, and nothing to keep running.

---

## 3. File-by-file / step-by-step — what we actually did

1. **Committed Tasks 2–6 in four logical commits.** One commit per task (requirements / README /
   provenance / Quarto+calculator) so the history reads as a clean progression a reviewer can follow —
   each commit maps to one explanation doc in this folder.
2. **`git push origin main`** — uploaded all of it to the public repo
   `github.com/Akhillavudya/telecom-churn-retention`.
3. **Rendered the report** — `quarto render` produced one self-contained `_site/index.html` (3.4 MB, with
   every figure, the OJS runtime, and `data.json` inlined thanks to `embed-resources: true`).
4. **Published to `gh-pages`** — copied that HTML (plus a `.nojekyll`) into a throwaway folder, made it an
   orphan `gh-pages` branch, and force-pushed it to GitHub. GitHub Pages picked it up automatically.
5. **Pinned the live URL** at the top of `README.md` and verified the page loads at
   `https://akhillavudya.github.io/telecom-churn-retention/`.

---

## 4. Issues hit while building

### Issue #1 — Quarto's one-command publish failed with an SSL certificate error
- **What happened:** `quarto publish gh-pages` aborted with
  `SSL: no alternative certificate subject name matches target host name 'github.com'` — yet a plain
  `git push` to the same repo had **just worked seconds earlier.**
- **Why it happened:** two different programs were talking to GitHub two different ways. Normal `git`
  uses the **system's** certificate store and network settings (including any corporate/antivirus HTTPS
  proxy on the machine, which re-signs traffic with its own certificate that the system already trusts).
  Quarto's *bundled* publisher uses its **own** networking that doesn't consult that same trust store, so
  the proxy's substitute certificate looked invalid to it. Same destination, different trust plumbing.
- **How we solved it:** we bypassed Quarto's publisher entirely and did the publish with **system git**,
  which we already knew worked — build the site with `quarto render`, then push the `_site` output to a
  `gh-pages` branch by hand. Same end result (a live Pages site), using the tool that could actually
  authenticate.
- **How to recognise it next time:** when a *wrapper* tool fails to reach a host but the *underlying* tool
  succeeds, suspect a **networking/trust mismatch** (proxy, cert store, credential helper), not a broken
  URL or bad password. The fix is usually "do the same action with the tool that already works."
- **Lesson (transferable):** a convenience command that bundles several steps (render → branch → push) is
  only as reliable as its weakest bundled part. When it breaks, you can almost always fall back to the
  underlying primitives and do the steps yourself — and you learn what the convenience command was doing.

### Issue #2 — the push "timed out" but had actually succeeded
- **What happened:** one `git push` appeared to time out after two minutes; a moment later the retry said
  `Everything up-to-date`, and the remote already had the commit.
- **Why:** the upload finished, but the wrapper waited on the credential/connection handshake long enough to hit
  our time limit before returning. The *network action* completed; only the *waiting process* was cut off.
- **Lesson (transferable):** after a push (or any network write) that seems to fail on a timeout, **check
  the actual remote state** (`git ls-remote origin main`) before re-running. Don't assume failure and
  blindly force-push — verify first.

---

## 5. Where things stand + what's next

**Done.** The project is public and live:

- **Repo:** `github.com/Akhillavudya/telecom-churn-retention` (branch `main`).
- **Live report:** <https://akhillavudya.github.io/telecom-churn-retention/> — interactive ROI calculator
  included.

Every item on the `docs/final_plan.md` must-do checklist (Tasks 1–7) is complete. The pipeline runs from a
clean clone, deps are pinned, the README carries the honest headline numbers with the live link, and the
diversifying Quarto + Observable JS + GitHub Pages deploy is shipped.

**Optional next (the §6 nice-to-haves, only if you want to keep going):** a SHAP interpretability panel,
a segment-level ROI breakdown, or a downloadable top-N target-list export. None are required for CV-ready —
the project is already there.

> **One thing to check in the browser yourself:** open the live URL and drag the calculator sliders — the
> six result cards and the net-benefit curve should update instantly. That confirms the client-side OJS is
> working end-to-end on the deployed page, which is the one thing a static file-inspection can't prove.
