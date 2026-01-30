## Feature 1 — Message Recap (LLM recap of unread messages)

What it does
- Collects the canonical unread message ids from Zulip's global unread state and posts them to a server endpoint that returns an LLM-generated HTML recap plus per-message anchors. Unread recap shows the summary of the unread messages, and references part serves the link for those unread message. 

Key files / symbols
- Server LLM recap generator: [`generate_message_recap`](zerver/lib/ai.py) — [zerver/lib/ai.py](zerver/lib/ai.py)
- Frontend trigger & UI: [`show_unread_recap`](web/src/recap.ts) — [web/src/recap.ts](web/src/recap.ts)
- Unread canonical source used: [`get_all_msg_ids`](web/src/unread.ts) — [web/src/unread.ts](web/src/unread.ts)
- Frontend entry ensures the module runs: [web/src/index.ts](web/src/index.ts)

How links to original messages are created
- Frontend receives the server response that includes message references (message id + anchor snippet). The UI uses Zulip message anchors that jump to the message in the client (a URL like `/#narrow/near/<message_id>` or the client’s message anchor), so clicking a reference navigates the user to the original message. See link assembly and modal rendering in [web/src/recap.ts](web/src/recap.ts) (see [`show_unread_recap`](web/src/recap.ts)).

Notes on safety
- Server sanitizes LLM output with bleach in [`generate_message_recap`](zerver/lib/ai.py) to allow only a small safe set of tags/attributes before embedding recap HTML in the client.
- Hide the api-key into environment variable to keep it safe.

Youtube Link: https://www.youtube.com/watch?v=S9U81diCwcI (private video which could only viewed by @andrew.cmu.edu email)
---

## Feature 2 — Topic Title Improver (low-cost drift detection + suggestion)

What it does
 From the moment the server starts up, when the server side receives three messages, it will package and send them to the model. After 3 stream message is successfully sent (in the actual production environment, the parameters can be adjusted to be larger as the situation requires. The three pieces of information are for the convenience of testing), the client may call a backend endpoint with the sent message id and current topic. The backend runs fast heuristics and only calls the LLM when heuristics indicate possible drift. If the LLM returns a suggestion, the client shows a small non-blocking dialog with "Apply" actions.

Key files / symbols
- LLM helper for suggestions: [`suggest_topic_title`](zerver/lib/ai.py) — [zerver/lib/ai.py](zerver/lib/ai.py)
- Server view with heuristics + fetch context: [`suggest_topic_title_backend`](zerver/views/topic_improver.py) — [zerver/views/topic_improver.py](zerver/views/topic_improver.py)
- Frontend helper that triggers the endpoint: [`maybe_request_topic_suggestion`](web/src/topic_improver.ts) — [web/src/topic_improver.ts](web/src/topic_improver.ts)
- Integration point to call after send success: [web/src/transmit.ts](web/src/transmit.ts) (place the call into the send-success handler)

Cost / latency / scalability decisions
- Frontend throttling: the client implements a short cooldown (e.g. one request per user per 10s) before sending another suggestion request to reduce duplicate calls. See throttle logic in [web/src/topic_improver.ts](web/src/topic_improver.ts).
- Backend cheap heuristics: the server performs quick rule checks before calling the LLM:
  - minimum number of recent messages
  - minimum average message length (content density)
  - percentage of recent messages referencing current title
  These heuristics are implemented in [zerver/views/topic_improver.py](zerver/views/topic_improver.py) and avoid LLM calls when drift is unlikely.
- Context bounds: when the LLM is called, the backend sends only a bounded recent context (e.g., latest 10–30 messages, each truncated) to limit tokens and latency. See `suggest_topic_title` in [zerver/lib/ai.py](zerver/lib/ai.py) which truncates and uses a low-cost model by default.
- Model selection & token caps: `suggest_topic_title` uses a lower-cost model (e.g. `gpt-3.5-turbo`) and tight `max_tokens` to keep cost and latency down — see model selection and `max_tokens` in [zerver/lib/ai.py](zerver/lib/ai.py).

UX & integration
- Non-blocking UX: the frontend displays a small dialog with the suggested title and  "Apply" to rename topic. See [web/src/topic_improver.ts](web/src/topic_improver.ts).
- Trigger location: call [`maybe_request_topic_suggestion`](web/src/topic_improver.ts) immediately after a successful stream message send (hook from [web/src/transmit.ts](web/src/transmit.ts)) so the suggestion appears while the sender still has context.
- Server-side gating: the endpoint can be feature-flagged / rate-limited (recommended) so organizations can opt in or 
limit usage.

Youtube Link: https://www.youtube.com/watch?v=xD0FzcyPcNg (private video which could only viewed by @andrew.cmu.edu email)

## Frontend wiring summary

- Entry point import: [web/src/index.ts](web/src/index.ts) imports the modules so side effects (sidebar mounting and topic-improver inclusion) run as part of the bundle.
- Sidebar button / Recap UI: [web/src/recap.ts](web/src/recap.ts) mounts the "Recap unread" UI entry and implements [`show_unread_recap`](web/src/recap.ts) which:
  - reads unread IDs from [`get_all_msg_ids`](web/src/unread.ts),
  - posts them to `/json/ai/message_recap`,
  - displays the returned HTML recap and clickable message anchors in a dialog.
- Topic-improver client: [web/src/topic_improver.ts](web/src/topic_improver.ts) performs client throttling and posts `{message_id, current_title}` to `/json/ai/suggest_topic_title` (server view in [zerver/views/topic_improver.py](zerver/views/topic_improver.py)), then surfaces the suggestion to the user.