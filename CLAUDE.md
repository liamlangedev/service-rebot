# Claude rules for this repo

## Worktrees

- Do feature work in a git worktree under `.claude/worktrees/<name>`, on branch
  `worktree-<name>`. It reaches `main` through a PR.
- **After the PR is merged, delete the worktree and its local branch.** Check first that
  the branch is merged and that the worktree has no uncommitted or unpushed work:

  ```bash
  git fetch origin
  git merge-base --is-ancestor worktree-<name> origin/main && echo merged
  git -C .claude/worktrees/<name> status --short   # only the symlinks below may remain
  git worktree remove --force .claude/worktrees/<name>
  git branch -d worktree-<name>
  git worktree prune
  ```

  If a worktree has uncommitted work, or its branch isn't merged, leave it and ask.
  Keep the remote branch unless asked to delete it.
- New worktrees don't get the gitignored teleop files. Symlink them from the main checkout
  instead of re-downloading: `teleoperation/.venv`, `teleoperation/assets` and
  `teleoperation/third_party`. Don't commit the symlinks. Don't run `uv sync` through the
  `.venv` symlink, because it would repoint the main checkout's environment at the
  worktree.
