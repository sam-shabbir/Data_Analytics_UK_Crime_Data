# How to open the notebooks

The `.ipynb` files in `notebooks/` aren't plain web pages — they're JSON
files that need a running Jupyter *server* to render properly (that's what
gives you the runnable code cells, not just static text). Jupyter starts
that server on your machine and then opens a browser tab pointing at it.

**Important:** steps 1–3 below all happen in **one single terminal
window** that you open once and keep using — you don't close it and
reopen a new one between steps. Step 1 opens it, step 2 and 3 are commands
you type into that same window, one after another.

## Step 1 — Open a terminal, sitting in the project folder

Two ways to do this — pick whichever you already have open:

**Option A — from VS Code (easiest if you're already in there):**
1. Open the `data-projs` folder in VS Code if it isn't already open
   (File → Open Folder).
2. Go to the top menu: **Terminal → New Terminal**.
3. A terminal panel opens at the bottom. VS Code automatically starts it
   *inside* the project folder, so you don't need to type `cd` — you can
   check this by typing `pwd` and pressing Enter; it should print
   `C:\Users\Maria\Downloads\samad\Study\2_Data_Analytics_Projects\crime_data-projs`.

**Option B — from the Windows Start menu:**
1. Press the Windows key, type `powershell`, press Enter. This opens a
   plain PowerShell window, but it starts you in your home folder
   (`C:\Users\Maria`), not the project — so you need to navigate there:
2. Type this and press Enter:
   ```powershell
   cd "C:\Users\Maria\Downloads\samad\Study\2_Data_Analytics_Projects\crime_data-projs"
   ```
3. Confirm it worked by typing `pwd` and pressing Enter — it should print
   that same path back to you.

From here on, "the terminal" means this one window, whichever option you used.

## Step 2 — Activate the virtual environment

Still in that same terminal. The project already has a `.venv` folder
(created once, sitting in the project folder — you're not creating
anything new here, just switching your terminal to use it). Activating it
points this terminal session at the project's own copies of pandas,
jupyterlab, etc., instead of whatever Python is installed system-wide.

Type this and press Enter:

```powershell
.venv\Scripts\Activate.ps1
```

**What should happen:** your prompt changes to show `(.venv)` at the very
start of the line, e.g. `(.venv) PS C:\Users\Maria\Downloads\samad\Study\2_Data_Analytics_Projects\crime_data-projs>`.
That prefix is your confirmation it worked — if you don't see it, the
next step will likely fail (it'll use the wrong Python and probably say
`jupyter` isn't recognized).

**If you get a red "execution policy" error instead:** that's a Windows
security setting blocking scripts, not a mistake on your part — stop and
let me know rather than trying to force past it.

**Note:** activation only lasts for this terminal window. If you close it
and open a new one later, you'll need to run this command again — that's
normal, not something going wrong.

## Step 3 — Launch JupyterLab, forced to open in Chrome

Still the same terminal, right after step 2 — no new window, no `cd`
needed (you're already in the right folder from step 1).

Normally `jupyter lab` opens your **system default browser**, which is
Edge on this machine. Rather than changing your Windows-wide default
browser (which would affect everything, not just this), this command
tells *just this launch* to use Chrome, by passing Chrome's exe path with
a `%s` placeholder that Jupyter fills in with the URL:

Type this and press Enter:

```powershell
jupyter lab --browser="C:/Program Files/Google/Chrome/Application/chrome.exe %s"
```

**What should happen:** the terminal prints a bunch of log lines (this is
normal — it's the server starting up), and within a couple of seconds a
new Chrome tab opens automatically showing the JupyterLab file browser.

**Leave this terminal window open** for as long as you want to use
Jupyter — it's running the server in the background. Minimizing it is
fine; closing it shuts the whole thing down (including any notebook you
have open, unsaved work included).

**Tip — avoid typing that long command every time:** run this once, in
the same terminal:

```powershell
jupyter lab --generate-config
```

It prints the path to a new file, something like
`C:\Users\Maria\.jupyter\jupyter_lab_config.py`. Open that file in VS
Code or Notepad, scroll to the bottom, and add this line:

```python
c.ServerApp.browser = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
```

Save the file. From then on, plain `jupyter lab` (no `--browser` flag
needed) will always open in Chrome.

## Step 4 — Open a notebook

In the Chrome tab that just opened, you'll see a file-browser panel on
the left listing the project's folders. Click into `notebooks/`, then
into whichever sub-folder you want (`london/`, `west-mercia/`, or
`comparison/`), then double-click any `.ipynb` file — e.g.
`01_explore.ipynb` — to open it as a running notebook.

## Step 5 — When you're done

Go back to the terminal window from steps 1–3 (don't close the Chrome tab
first — that alone does **not** stop the server, it keeps running in the
background). Click into that terminal window and press `Ctrl+C`. It may
ask you to confirm — type `y` and press Enter. That shuts the server down
completely.
