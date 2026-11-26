# The project

In teams of 3–4, you build a small web app on a real dataset: FastAPI, Flask or Streamlit (Nov 27
lecture), pandas for the data, and, if it fits, one simple scikit-learn model. Ideas are in
[IDEAS.md](IDEAS.md); your own idea is welcome.

|  |  |
|---|---|
| **AI level** | **2**: AI allowed. In every PR description: which prompts you used, or a short note on how you used AI. **Every team member must be able to explain and change any part of the code**, including what the AI wrote. On Dec 11 you may be asked to. |
| **Teams** | 3–4 people, formed on Fri Nov 27 |
| **Milestone** | Thu Dec 10, 17:00 |
| **Demo and reviews** | Fri Dec 11, in class |
| **Counts as** | one PR (the milestone) and one review (of another team's milestone), as for an exercise |

## Dates

| When | What |
|---|---|
| **Fri Nov 27** | Form a team, pick an idea and a dataset. Send one mail per team to `dhbw@tauschinsky.de`: team name, the GitHub logins, the idea in one sentence. You get a repository for your team. |
| **by Fri Dec 4** | Plan in your repository: the README says what the app does and which data it uses (with source and licence), and a GitHub Project board lists the work packages and who does what. |
| **Fri Dec 4** (7 h) | Building in class. Bring questions. |
| **Wed Dec 9** | Online: questions, and where you're stuck. |
| **Thu Dec 10, 17:00** | Milestone: open the milestone PR (see below). |
| **Fri Dec 11** | Demo (5 minutes per team) and the cross-team reviews, in class. |

## Your repository

Each team gets a private repository `dhbw-ma-ppp/ppp-2026-<team>`, made from a template:
`pyproject.toml` with the libraries from the lecture, CI (ruff and pytest on every PR), a PR
template and a README to fill in.

Work as in the exercises, only now within the team: a branch per work package, a PR into
`main`, a teammate reviews it, then merge. Small PRs are easier to review than one big one at the
end.

## The milestone (Thu Dec 10, 17:00)

It counts as done if:

- **The app works:** someone who clones the repository can start it with `uv sync` and the
  command in your README. CI is green.
- **There are tests that check values,** not just that a key or a page exists, including the
  cases where your data is awkward (missing values, empty results, unexpected input).
- **The README** says what the app does, how to start it, where the data comes from (source and
  licence), and **what the data reflects and what it doesn't**: who collected it, what's missing,
  what your app can't tell you.
- **The work split is visible:** the Project board, and every team member has merged PRs of their
  own.
- **The milestone PR is open:** a PR from `main` into the branch `start` (the empty template the
  repository began with), titled "Milestone". It shows all your code as one diff, so the other
  team can comment on any line. It is never merged.

## The cross-team review (Fri Dec 11, in class)

Each team reviews another team's milestone PR. The rules are the usual ones (REVIEWING.md in
ppp-2026): at least **one concrete suggested test** and at least **one genuine question** about a
design choice. The other team answers in the PR. You will know which team you review on Dec 10,
after the deadline.

## The demo (Fri Dec 11, in class)

Five minutes per team: show the app, one thing about the data you didn't expect, and one thing
you'd do differently. Then questions. Anyone in the team may be asked to explain a piece of the
code.
