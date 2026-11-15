# AGENTS.md

`kokeb-labs-drivers/.github` holds the organization profile and the community files, issue forms, discussion forms
and pull request template that every repository in `kokeb-labs-drivers` inherits.

Agents working here or in any driver repository follow the Kokeb Labs
[agent rules](https://github.com/kokeb-labs/.github/blob/main/standards/agents.md). Read them first.

## This repository

- `profile/README.md`: the organization page. The driver catalogue and the summary line between the
  `GENERATED` markers are written by `python3 tools/gen_profile.py` from the drivers' own repositories; never edit them
  by hand. A new driver needs a group in that script. CI (`Profile catalogue`) runs `--check` on every pull request
  and weekly.
- `profile/img/`: the figures the page shows, light and dark. Their models are in `tools/figures/docs/model/`; rebuild
  with `tools/build_figures.sh` (needs the `kokeb-mkdocs-theme` package from `kokeb-labs/ci-tools`).
- Community files: adapted from `kokeb-labs/.github`. A change of rule goes there first, with an ADR.
- No settings code, tokens or private material here; the organization's settings live in
  `kokeb-labs/.github/org/`.

## Checks before pushing

- Markdown: markdownlint with line length 120 (tables and code blocks exempt).
- YAML: yamllint on `.github/`.
- Commits are signed off (`git commit -s`).
