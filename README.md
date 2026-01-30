# Zulip overview

[Zulip](https://zulip.com) is an open-source organized team chat app with unique
[topic-based threading][why-zulip] that combines the best of email and chat to
make remote work productive and delightful. Fortune 500 companies, [leading open
source projects][rust-case-study], and thousands of other organizations use
Zulip every day. Zulip is the only [modern team chat app][features] that is
designed for both live and asynchronous conversations.

Zulip is built by a distributed community of developers from all around the
world, with 99+ people who have each contributed 100+ commits. With
over 1,500 contributors merging over 500 commits a month, Zulip is the
largest and fastest growing open source team chat project.

Come find us on the [development community chat](https://zulip.com/development-community/)!

[![GitHub Actions build status](https://github.com/zulip/zulip/actions/workflows/zulip-ci.yml/badge.svg)](https://github.com/zulip/zulip/actions/workflows/zulip-ci.yml?query=branch%3Amain)
[![coverage status](https://img.shields.io/codecov/c/github/zulip/zulip/main.svg)](https://codecov.io/gh/zulip/zulip)
[![Mypy coverage](https://img.shields.io/badge/mypy-100%25-green.svg)][mypy-coverage]
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://github.com/prettier/prettier)
[![GitHub release](https://img.shields.io/github/release/zulip/zulip.svg)](https://github.com/zulip/zulip/releases/latest)
[![docs](https://readthedocs.org/projects/zulip/badge/?version=latest)](https://zulip.readthedocs.io/en/latest/)
[![Zulip chat](https://img.shields.io/badge/zulip-join_chat-brightgreen.svg)](https://chat.zulip.org)
[![Twitter](https://img.shields.io/badge/twitter-@zulip-blue.svg?style=flat)](https://twitter.com/zulip)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/zulip)](https://github.com/sponsors/zulip)

[mypy-coverage]: https://blog.zulip.org/2016/10/13/static-types-in-python-oh-mypy/
[why-zulip]: https://zulip.com/why-zulip/
[rust-case-study]: https://zulip.com/case-studies/rust/
[features]: https://zulip.com/features/

## Getting started

- **Contributing code**. Check out our [guide for new
  contributors](https://zulip.readthedocs.io/en/latest/contributing/contributing.html)
  to get started. We have invested in making Zulip’s code highly
  readable, thoughtfully tested, and easy to modify. Beyond that, we
  have written an extraordinary 185K words of documentation for Zulip
  contributors.

- **Contributing non-code**. [Report an
  issue](https://zulip.readthedocs.io/en/latest/contributing/reporting-bugs.html),
  [translate](https://zulip.readthedocs.io/en/latest/translating/translating.html)
  Zulip into your language, or [give us
  feedback](https://zulip.readthedocs.io/en/latest/contributing/suggesting-features.html).
  We'd love to hear from you, whether you've been using Zulip for years, or are just
  trying it out for the first time.

- **Checking Zulip out**. The best way to see Zulip in action is to [drop
  by](https://chat.zulip.org/?show_try_zulip_modal) the Zulip development
  community (no account required). We also recommend reading about Zulip's
  [unique approach](https://zulip.com/why-zulip/) to organizing conversations.

- **Running a Zulip server**. Self-host Zulip directly on Ubuntu or Debian
  Linux, in [Docker](https://github.com/zulip/docker-zulip), or with prebuilt
  images for [Digital Ocean](https://marketplace.digitalocean.com/apps/zulip) and
  [Render](https://render.com/docs/deploy-zulip).
  Learn more about [self-hosting Zulip](https://zulip.com/self-hosting/).

- **Using Zulip without setting up a server**. Learn about [Zulip
  Cloud](https://zulip.com/zulip-cloud/) hosting options. Zulip sponsors free [Zulip
  Cloud Standard](https://zulip.com/plans/) for hundreds of worthy
  organizations, including [fellow open-source
  projects](https://zulip.com/for/open-source/).

- **Participating in [outreach
  programs](https://zulip.readthedocs.io/en/latest/contributing/contributing.html#outreach-programs)**
  like [Google Summer of Code](https://developers.google.com/open-source/gsoc/).

- **Supporting Zulip**. Learn about all the ways you can [support
  Zulip](https://zulip.com/help/support-zulip-project), including contributing
  financially, and helping others discover it.

You may also be interested in reading our [blog](https://blog.zulip.org/), and
following us on [LinkedIn](https://www.linkedin.com/company/zulip-project/),
[Mastodon](https://fosstodon.org/@zulip), and [X](https://x.com/zulip).

Zulip is distributed under the
[Apache 2.0](https://github.com/zulip/zulip/blob/main/LICENSE) license.

# Zulip (development) — quick start (Vagrant)

This repository contains a Zulip development environment with two LLM-based features:
- Message Recap — generates a concise recap of unread messages (frontend: `web/src/recap.ts`, backend: `zerver/lib/ai.py`).
- Topic Title Improver — suggests better topic titles when a topic drifts (frontend: `web/src/topic_improver.ts`, backend: `zerver/views/topic_improver.py`).

These notes show how to install and run the development server using Vagrant (recommended for development) and how to provide an LLM API key.

Prerequisites (host)
- Git
- Vagrant (with Docker provider) or a supported VM provider
- Docker (for the Vagrant Docker provider)
- Node.js (recommended LTS) and pnpm (for local frontend builds if needed)
  - Install pnpm: `npm install -g pnpm` (if you will run frontend builds locally)

Get the code
1. Clone the repo:
   git clone <your-fork-or-upstream-url> zulip
   cd zulip

Start with Vagrant (recommended)
1. Start the Vagrant development environment (Docker provider is common):
   vagrant up --provider=docker

2. SSH into the VM:
   vagrant ssh

3. Inside the VM, change to the repository root (usually `/vagrant` or `/srv/zulip`):
   cd /vagrant   # or cd /srv/zulip

4. Provision / prepare the dev environment (only needed if not already provisioned):
   ./tools/provision

5. Activate the Python venv and start the development server:
   source .venv/bin/activate
   ./tools/run-dev

6. Open the site in your browser:
   http://localhost:9991

If you prefer running locally without Vagrant
- Install required system packages per `docs/development/setup-recommended.md`.
- Run `./tools/provision`, `source .venv/bin/activate`, then `./tools/run-dev.py`.

Frontend (assets) build notes
- The dev run will rebuild assets automatically in the VM. If you edit frontend code and need to build manually:
  pnpm install
  pnpm build
- After building, restart the dev server (`./tools/run-dev.py`) and hard-refresh the browser (Ctrl/Cmd+Shift+R).

Providing an LLM API token (OpenAI or other configured provider)
- The code looks for an LLM API key via your Django settings (setting name `LLM_API_KEY`).
- For development, simplest options:
  - Put your API key into the file `openai_api.key` in the repo root (one line, the key). The development settings in this environment may read this file.
  - Or, set an environment variable when starting the server in the VM:
    export LLM_API_KEY="sk-..."
    ./tools/run-dev.py
- Confirm the key is available to the Django process (check server logs for LLM config debug lines).

Notes about cost, rate limits, and safety
- Topic suggestions are guarded by cheap heuristics on the server to avoid unnecessary LLM calls (see `zerver/views/topic_improver.py`).
- Recaps and suggestions use bounded context, truncated messages, and conservative token limits (see `zerver/lib/ai.py`).
- Server sanitizes LLM-generated HTML before sending to client (see `generate_message_recap`).

Verify the frontend changes are loaded
- After building and starting the dev server, hard-refresh the browser.
- In DevTools Console:
  - Check the sidebar entry: `!!document.getElementById('recap-unread-entry')`
  - Quick manual call (debug): `window.show_unread_recap && window.show_unread_recap()`

Where to look in the code (quick pointers)
- Recap frontend: `web/src/recap.ts` — `show_unread_recap`
- Recap server: `zerver/lib/ai.py` — `generate_message_recap`
- Topic improver frontend: `web/src/topic_improver.ts` — `maybe_request_topic_suggestion`
- Topic improver server: `zerver/views/topic_improver.py` — heuristics + `suggest_topic_title`
- Frontend entry: `web/src/index.ts`
- Unread canonical source: `web/src/unread.ts` — `get_all_msg_ids`

If you added dependencies
- Node deps are managed via pnpm (`package.json` + `pnpm-lock.yaml`).
  Run: `pnpm install`
- Python dependencies are managed by the project's provisioning; running `./tools/provision` in the VM will install them.


Troubleshooting
- If you do not see frontend changes:
  1. Ensure you built frontend assets (inside VM if using Vagrant): `pnpm install && pnpm build`
  2. Restart the dev server: `pkill -f tools/run-dev.py || true` then `./tools/run-dev.py`
  3. Hard-refresh the browser (Ctrl/Cmd+Shift+R)
  4. Check run-dev.py terminal output for build errors and browser console for JS errors.

Contact / next steps
- See `Implementation.md` for an implementation summary and direct file links for the
