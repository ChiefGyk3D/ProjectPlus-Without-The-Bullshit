# Security Policy

This repository is a study guide: Markdown pages, two generator scripts and
a static site build. There is nothing here that handles credentials or user
data. The things that could still go wrong are supply chain (a pinned action
or a pip dependency) and the site's one runtime dependency, the markmap
library the mind map loads from jsDelivr.

## Reporting a Vulnerability

Please report security issues **privately**, not in a public issue.

- Preferred: open a
  [GitHub Security Advisory](https://github.com/ChiefGyk3D/ProjectPlus-Without-The-Bullshit/security/advisories/new)
  for this repository.
- Otherwise, contact the maintainer through the profile at
  [github.com/ChiefGyk3D](https://github.com/ChiefGyk3D).

Please include the affected file or workflow, what the issue is, and how to
reproduce it.

## What to Expect

A small, single-maintainer project with no formal SLA. Reports are
acknowledged within 14 days and anything affecting the build pipeline or
the published site is fixed as a priority.

## Scope

In scope: `.github/`, `scripts/`, `mkdocs.yml`, `requirements.txt` and the
published site. A factual error in the study material is a normal issue or
pull request, not a security report.
