# AGENTS.md

`kokeb-labs-drivers/.github` holds the organization profile and the community files, issue forms, discussion forms
and pull request template that every repository in `kokeb-labs-drivers` inherits.

Agents working here or in any driver repository follow the Kokeb Labs
[agent rules](https://github.com/kokeb-labs/.github/blob/main/standards/agents.md). Read them first.

## This repository

- `profile/README.md`: the organization page. Keep the driver table in step with the repositories.
- Community files: adapted from `kokeb-labs/.github`. A change of rule goes there first, with an ADR.
- No settings code, tokens or private material here; the organization's settings live in
  `kokeb-labs/.github/org/`.

## Checks before pushing

- Markdown: markdownlint with line length 120 (tables and code blocks exempt).
- YAML: yamllint on `.github/`.
- Commits are signed off (`git commit -s`).
