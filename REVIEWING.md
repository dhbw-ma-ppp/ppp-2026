# How to review a pull request

You will be assigned one pull request (PR) to review each week. Reviews are due on
**Tuesday, 18:00**, and authors answer by the **Wednesday session**. But start early: on
Friday, any PR may be picked for a live review in class, and then you, as its reviewer, ask
your question in front of everyone.

CI (the automatic checks on the PR) already runs the tests and ruff. Your review is about
what CI cannot check: correctness in cases nobody tested, design and readability.

## A review counts only if it contains

1. **At least one concrete suggested test case.** Give the input and the expected result, and
   say why it is interesting (edge case, error case, ...). The author adds the test or explains
   why it is unnecessary.
2. **At least one genuine question about a design choice.** A real question you do not know
   the answer to, e.g. "Why did you use a dict here rather than a list?". Not "Why didn't
   you add comments?".
3. **An answer from the author.** A review without an exchange does not count. Authors:
   reply in the PR thread before the Wednesday session.

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
