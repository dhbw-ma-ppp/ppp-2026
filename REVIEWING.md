# How to review a pull request

You will be assigned one pull request (PR) to review each week. Reviews are due on
**Tuesday, 17:00**, and authors answer by the **Wednesday session**. But start early: on
Friday, any PR may be picked for a live review in class, and then you, as its reviewer, ask
your question in front of everyone.

Only students who submitted a PR get one to review. So submit late rather than never: a late
PR still gets you a PR to review. No PR means nothing to review that week.

CI (the automatic checks on the PR) already runs the tests and ruff. Your review is about
what CI cannot check: correctness in cases nobody tested, design and readability.

## A review counts only if it contains

1. **At least one concrete suggested test case.** Give the input and the expected result, and
   say why it is interesting (edge case, error case, ...). The author adds the test or explains
   why it is unnecessary.
2. **At least one genuine question about a design choice.** A real question you do not know
   the answer to, e.g. "Why did you use a dict here rather than a list?". Not "Why didn't
   you add comments?".

## Answering a review of your PR

Answer every review of your PR in the PR thread before the Wednesday session: add the
suggested test or explain why it is unnecessary, and answer the question. This is part of
your own PR: a PR whose review goes unanswered does not count. (Your reviewer's review counts
either way.)

## Template

Copy this into your review and fill it in:

```markdown
**Suggested test case**
Input: ...
Expected: ...
Why: ...

**Question**
...

**Other remarks** (optional)
...
```

## Good to know

- Comment on specific lines: in the "Files changed" tab, click the `+` next to a line.
- Be specific and kind. Criticise the code, not the person.
- You are not expected to find everything. One good test case beats ten style remarks.
