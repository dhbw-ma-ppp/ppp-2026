# Exercise 00: your first pull request

Done together in class on Oct 2. Not graded. The point is to go through the whole workflow
once, while help is in the room: branch → code → test → commit → push → pull request (PR)
→ CI → review.

In the commands below, replace `<login>` with your GitHub login, spelled exactly as on GitHub.

## 1. Create a branch and your folder

```
git checkout main
git pull
git checkout -b ex00-<login>
```

Copy the folder `exercises/ex00` to `students/<login>/ex00`
(in VS Code: right-click → Copy, then Paste into a new folder `students/<login>`).

## 2. Run the test: it fails

```
uv run pytest students/<login>/ex00
```

The test calls the function `greet` in `ex00.py`, which doesn't do anything yet.
Read the error message: what did the test expect, and what did it get?

## 3. Commit, push, open a PR: see CI fail

```
git add students/<login>/ex00
git status
git commit -m "ex00: start"
git push --set-upstream origin ex00-<login>
```

On github.com, open a pull request for your branch. Fill in the template.
After a minute, the check at the bottom of the PR turns **red**: CI ran the same test and it
failed. Click *Details* and find the error message.

## 4. Make it pass

Fill in the body of `greet` in `students/<login>/ex00/ex00.py`, until
`uv run pytest students/<login>/ex00` passes. Then:

```
git add -u
git commit -m "ex00: implement greet"
git push
```

The PR updates itself, and CI runs again. Now it's **green**.

## 5. Review your neighbour's PR

- Open your neighbour's PR, go to *Files changed*, and click *Review changes*.
- Use the template from `REVIEWING.md`: suggest a test case (What should `greet("")` return?
  Is that what happens?) and ask a question.
- Answer the review on your own PR.
