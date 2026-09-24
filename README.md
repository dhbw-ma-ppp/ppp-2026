# ppp-2026
Documents and exercises for 'Programming and Problem Solving with Python' at DHBW Mannheim 2026


# Setup
You need [uv](https://docs.astral.sh/uv/getting-started/installation/), [git](https://git-scm.com/),
[VS Code](https://code.visualstudio.com/) and an account on github.com.

```
git clone https://github.com/dhbw-ma-ppp/ppp-2026.git
cd ppp-2026
uv sync          # installs Python 3.14 and all libraries into .venv
uv run pytest    # should report "2 passed"
```

Open the `ppp-2026` folder in VS Code and install the recommended extensions when asked.
Whenever the course needs new libraries, run `uv sync` again after `git pull`.


# Repository layout
- `exercises/ex01/`, `exercises/ex02/`, ...: exercise descriptions, starter code and starter tests
- `students/<github-login>/ex01/`, ...: **your solutions**. Copy the exercise folder here and work in the copy.
  Use your GitHub login exactly as GitHub spells it; CI rejects PRs that change files anywhere else.
- `data/`: input data for exercises
- `lectures/`: lecture notebooks
- `REVIEWING.md`: what a code review must contain


# Checking your work
The same checks run automatically (CI) on every pull request:
```
uv run pytest students/<github-login>/ex01      # run the tests for one exercise
uv run ruff check students/<github-login>/ex01  # find likely bugs and bad style
uv run ruff format students/<github-login>/ex01 # format the code automatically
```
To see exactly what CI will say about your branch:
`uv run python .github/scripts/check_pr.py --author <github-login>`


# Notes on using git
## the most important commands
 - git **status**: show the current branch and which files are untracked/changed/staged
 - git **checkout <branch_name>**: change into the branch specified
 - git **checkout -b <branch_name>**: create the specified branch and change into that branch
 - git **pull**: sync changes from remote (github.com) to local branch
 - git **push**: sync changes from local to remote (github.com)

 - git **add <filename>**: add files to 'staging area'
 - git **add -u**: add all already tracked but changed files to staging area
 - git **commit**: create commit of staged changes

 - git **stash**: store local changes to 'temporary' stash
 - git **stash pop**: restore changes from the stash


## step-by-step instructions for exercises
- first: checkout main branch: git checkout main
- make sure remote changes are pulled: git pull
- checkout working branch for current exercises: git checkout -b <exercise_N_NAME>
- < MAKE ALL NECESSARY CHANGES in students/<github-login>/exNN/ >
- run the tests and ruff (see "Checking your work" above)
- add the new file to the staging area: git add <filename>
- verify the correct files/changes are staged: git status
- detailed diff of staged changes: git diff --staged
- commit changes: git commit -m "<commit-message>"
- push changes upstream: git push --set-upstream origin <branch_name>
- < CREATE PULL REQUEST, WAIT FOR REVIEW >
- < MAKE NECESSARY CHANGES >
- add the new file to the staging area: git add <filename>
- verify the correct files/changes are staged: git status
- detailed diff of staged changes: git diff --staged
- commit changes: git commit -m "<commit-message>"
- push changes upstream: git push

< NEW EXERCISES WEEK N+1 > 
- first: checkout main branch: git checkout main
- make sure remote changes are pulled: git pull
- checkout working branch for current exercises (NEW NAME!): git checkout -b <exercise_N+1_NAME>
< PROCEED AS ABOVE > 
