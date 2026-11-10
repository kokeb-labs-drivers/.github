# Contributing to Kokeb Labs Drivers

This applies to every repository in the `kokeb-labs-drivers` organization unless the repository has its own
`CONTRIBUTING.md`. The full rules are in the Kokeb Labs
[engineering standard](https://github.com/kokeb-labs/.github/blob/main/standards/README.md), in particular the
[driver standard](https://github.com/kokeb-labs/.github/blob/main/standards/driver.md), and in the
[handbook](https://kokeb-labs.github.io/handbook/). This page is the short version for a first pull request.
Where they differ, the standard wins.

## Before you start

- For anything larger than a small fix, open an issue or a discussion first so we can agree on the approach.
- New chip driver? Open a **Driver request** first, then start from
  [`driver-template`](https://github.com/kokeb-labs/driver-template) and run `python3 tools/setup.py`; it produces
  a complete, tested repository for your chip.

## Branches and pull requests

- `main` is the only long-lived branch and only changes through pull requests.
- Branch from `main` as `feat/<topic>`, `fix/<topic>`, `docs/<topic>`, `ci/<topic>` or `chore/<topic>`.
- One change per pull request; prefer under about 400 changed lines and split larger work into a series.
- Fill in the pull request template: what changed, why, how you verified it.
- Pull requests are squash-merged. The title becomes the commit subject on `main`, so write it as one.
- Add an entry under `## [Unreleased]` in `CHANGELOG.md` for anything a user would notice; under `### Breaking`
  if they must change their code.

## Commit messages

- Subject in the imperative mood, under about 72 characters, no trailing period: `Add FIFO read`, not `Added fifo`.
- An optional body after a blank line says why, not what.
- No attribution trailers other than the sign-off below.

## Sign-off (DCO)

Every commit carries a `Signed-off-by:` line certifying the
[Developer Certificate of Origin](https://developercertificate.org/): that you wrote the change or have the right to
submit it under the repository's licence. Add it with `git commit -s`. The name and email must match the commit
author. CI checks it; a pull request with an unsigned commit can't merge. Edits made in the GitHub web editor are
signed off automatically.

To fix a missing sign-off on your branch: `git rebase --signoff main`, then force-push your branch.

## The CI gate

Every pull request must pass its repository's CI, built from the reusable workflows in
[`ci-tools`](https://github.com/kokeb-labs/ci-tools). The one required check is `CI gate / gate`. For a driver it
runs host tests with coverage and sanitizers, the fuzzers, C++ lint, the MISRA C++:2023 checks, cross builds for
Cortex-M and ESP32, the ESP32 examples, Markdown and YAML lint, the docs build and a link check. Don't merge on red;
fix the cause, or fix the check and say why.

Run the repository's `tools/preflight.sh` before you push; it runs the same checks locally.

If a change affects behaviour on hardware, say in the pull request which MCU and board you ran it on and what you
observed, or write "not verified on hardware" with the steps someone should run.

## What a driver must not do

- Include MCU or SDK headers, allocate from the heap, throw, or use RTTI or virtual calls.
- Carry a brand: namespaces, CMake targets and macros are named after the chip.
- Ship a vendor datasheet. Link the vendor's page and record the revision the driver follows.

## Documentation

Update the README and `docs/` in the same pull request as the code they describe. Public headers carry Doxygen
comments, and a change to what the chip does updates its diagrams. See
[documentation](https://github.com/kokeb-labs/.github/blob/main/standards/docs.md).

## Conduct and security

By taking part you agree to the [code of conduct](CODE_OF_CONDUCT.md). Report vulnerabilities privately as
[SECURITY.md](SECURITY.md) describes, never in an issue.
