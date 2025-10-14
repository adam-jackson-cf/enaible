# visualdb Proof of Concept Research

## 1. Goals

Establish a viable toolkit for the visualdb explorer board prototype that:

- Delivers an extensible whiteboard surface aligned with the PRD.
- Supports URL-driven embeddings for YouTube videos, X posts, and generic webpages without persisting source content.
- Minimizes bespoke infrastructure by leaning on open-source components and provider SDKs.

## 2. Whiteboard Library Scan

| Option                                | License                            | Highlights                                                                                                                                                           | Key Gaps                                                                                                                 |
| ------------------------------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Excalidraw (`@excalidraw/excalidraw`) | MIT                                | Mature React canvas, infinite board, embeddable component with plugin APIs; self-host assets and extend via custom UI. citeturn0search6turn4search2turn4search3 | Default hand-drawn styling—require theming to hit monochrome aesthetic.                                                  |
| tldraw SDK                            | Business Source (source-available) | Polished UX, native multiplayer & snapping; requires license key in production builds. citeturn0search5                                                           | Non-permissive license complicates open prototype demos; vendor lock-in risk.                                            |
| React Flow (`@xyflow/react`)          | MIT                                | Node/edge editor with hooks, Tailwind-friendly; great for structured graphs. citeturn0search0turn0search8                                                        | Oriented around connections, so replicating free-form whiteboard takes extra effort (e.g., custom node for every block). |

**Recommendation:** Fork Excalidraw as the canvas foundation. It already ships as a React component compatible with Bun/Vite, supports custom elements, and remains permissively licensed for future commercialization. citeturn4search2turn4search3

## 3. URL Embed Strategies

### 3.1 YouTube

- Continue with the official IFrame Player API: construct `https://www.youtube.com/embed/<id>?enablejsapi=1&origin=<host>` so we can programmatically resize and react to playback events. citeturn1search0turn1search2
- Respect YouTube’s 200px minimum player size and surface a fallback card if the video is geo-blocked. citeturn1search0

### 3.2 X (Twitter) Posts

- Use the `twttr.widgets.createTweet` factory once `https://platform.twitter.com/widgets.js` is loaded; accepts Tweet IDs and renders authenticated views when user cookies exist. citeturn2search1turn2search4
- Normalise pasted `x.com` URLs to `twitter.com` for compatibility—community reports confirm widgets.js still rejects the rebranded domain. citeturn2search5
- Offer a degraded metadata card if embeds fail (private accounts, deleted posts).

### 3.3 Generic Webpages

- Attempt sandboxed iframes (`allow-scripts allow-same-origin allow-popups`) for hosts permitting embedding.
- Detect `X-Frame-Options` / `Content-Security-Policy: frame-ancestors` blocks and show a link-style card instead of proxying content, keeping “no storage” intact. citeturn1search1turn1search3
- Avoid bypass services (e.g., Webfuse) for the POC to honour the requirement not to store or rewrite third-party data. citeturn1search5

## 4. Session Model & State

- Store blocks in client-side state (Zustand) persisted to `sessionStorage`: `{ id, type, url, position, size, metadata }`.
- Do not cache remote HTML/media; rely on provider iframes to fetch live content, which keeps us out of data retention scope.

## 5. Authentication & Cookies

- Provider iframes will leverage existing first-party cookies. Google’s July 2024 policy shift means third-party cookies remain available, so logged-in embeds continue to function. citeturn3search0turn3news12
- Monitor Chrome’s Privacy Sandbox updates; fenced frames and cookie restrictions are postponed until at least 2026, but the roadmap may change. citeturn5search4turn5search7

## 6. Alternatives to Standard IFrames

- **Fenced frames / Controlled frames:** Emerging Chrome features designed for privacy-preserving embeds, but current guidance indicates Chrome will not mandate fenced frames before 2026 and they still carry security vulnerabilities (CVE-2025-0441). citeturn5search4turn5search5turn5search6
- **Headless fetch & render:** Would require storing parsed content (violates PRD constraint) and handling provider auth flows—defer.

## 7. Security Considerations

- Sanitize URLs before injecting into iframes to mitigate XSS.
- Keep provider SDKs (YouTube, X widgets) pinned and monitored for advisories.
- If adopting experimental frame tech later, track Chrome CVEs like 2025-0441 that exposed fenced frame info leaks. citeturn5search5turn5search6

## 8. Recommended Architecture Sketch

1. **Canvas Layer:** Excalidraw embedded component; custom `EmbedBlock` element type renders provider iframe or fallback card.
2. **Paste Pipeline:** URL normalizer → classifier (YouTube, X, Web) → block factory.
3. **State:** Zustand store synchronizing blocks to sessionStorage, exposing undo/redo for board actions.
4. **Embed Manager:** Shared utility handling iframe creation, provider script loading, and teardown.
5. **Theming:** Override Excalidraw’s styles (CSS vars) to achieve monochrome OpenAI aesthetic.

## 9. Next Steps

1. Spike Excalidraw integration and customise the toolbar to “Add Note” / “Add URL” actions.
2. Implement URL classification + embed manager with provider-specific handlers.
3. Validate embeds behind corporate SSO to ensure cookie passthrough works for each provider.
4. Draft fallback card design for unsupported hosts; confirm usability with stakeholders.

## 10. Open Questions

- Do we need offline support for notes if embeds fail to load (e.g., travel scenarios)?
- Should we log anonymised embed errors for debugging, or remain strictly non-logging per proof-of-concept scope?
