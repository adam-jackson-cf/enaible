# Product Requirements Document (PRD): visualdb Explorer Board Prototype

## 1. Overview

- Brief: visualdb is a desktop web prototype that lets technology strategists compose a single visual board by pasting source URLs (YouTube, X posts, or web articles) and arranging them alongside free-form notes without storing any upstream content.
- Goals:
  - Validate a minimal explorer board that persists layout and supports mixed note/embed blocks.
  - Demonstrate frictionless URL ingestion for the three priority sources (YouTube, X, general webpages).
  - Deliver a monochromatic, minimal interface aligned with the OpenAI-inspired brand aesthetic.
- Non-Goals:
  - Multi-user collaboration or authentication.
  - Analytics instrumentation or data persistence beyond layout metadata.
  - Mobile, tablet, or responsive breakpoints beyond desktop baseline.

## 2. Personas

- Priya Shah — CTO, Mid-Sized SaaS

  - Goals: Monitor emerging frameworks, synthesize insights for quarterly strategy.
  - Pain Points: Fragmented tabs across research platforms, manual curation of screenshots or notes.
  - Screen Patterns: { primary: [S-001], secondary: [], admin: [] }

- Dr. Luis Moreno — Lead Research Scientist

  - Goals: Aggregate academic articles, videos, and commentary for grant proposals.
  - Pain Points: Time lost converting sources into presentable summaries, inconsistent formatting.
  - Screen Patterns: { primary: [S-001], secondary: [], admin: [] }

- Avery Kim — Product Manager, Innovation Team
  - Goals: Build visual briefs that combine competitive intel with product notes.
  - Pain Points: Context switching between note apps and embedded media, difficulty keeping layouts updated.
  - Screen Patterns: { primary: [S-001], secondary: [], admin: [] }

## 3. Scope (MoSCoW)

### Must Have

- [F-001] Explorer Canvas & Layout Persistence — Single-board workspace that allows placement, movement, and deletion of content blocks while persisting their x/y positions for the current session.
- [F-002] Note Blocks — Rich-text blocks with Notion-like affordances (basic formatting, headers, bullet/number lists) that can be created, edited in place, and resized.
- [F-003] External Source Embeds — Create an embed block by pasting a supported URL (YouTube video, X post, or general webpage) with lightweight preview metadata and optional login prompt handoff.

### Should Have

- [F-004] Board Reset Control — Single action to clear all blocks and return the canvas to an empty state during a session.

### Could Have

- [F-005] Alignment Guides — Subtle snap or guide lines to aid positioning of blocks along common axes.

### Won't Have

- [F-006] Authentication & Multi-User Workspaces — Account creation, shared boards, or role management are explicitly out of scope for this prototype.

## 4. Screen Architecture

- Primary Screens: [S-001 Explorer Board]
- Secondary Screens: []
- Admin/Settings: []
- Navigation Model: Single-screen canvas with persistent top toolbar; no global navigation or nested routes in the prototype.

## 5. Key User Flows

- [FL-001] Capture External Resource

  - Trigger: User pastes a supported URL into the board.
  - Preconditions: Session initialized with empty or existing canvas; clipboard contains YouTube, X, or web article URL.
  - Steps:
    1. User invokes add action (toolbar or keyboard shortcut) and pastes URL.
    2. System validates URL against supported domains.
    3. System generates an embed block with preview metadata and places it at default coordinates.
    4. User repositions and resizes embed block as needed.
  - Alternate Paths: If URL requires platform login, user is directed to authenticate in new tab; embed block displays placeholder until access is granted.
  - Postconditions: Embed block stored with URL reference and current x/y coordinates within session storage.

- [FL-002] Create and Organize Note Blocks

  - Trigger: User selects “Add Note” from toolbar or uses keyboard shortcut.
  - Preconditions: Explorer board loaded and writable.
  - Steps:
    1. System places a blank note block at default coordinates.
    2. User enters text and applies basic formatting inline.
    3. User drags note block to desired position and optionally resizes.
  - Alternate Paths: User deletes note block via context menu or keyboard command.
  - Postconditions: Note text and positioning metadata persisted for the active session.

- [FL-003] Reset Board
  - Trigger: User selects “Reset Board” control.
  - Preconditions: Active session contains one or more blocks.
  - Steps:
    1. System prompts user to confirm irreversible reset.
    2. Upon confirmation, system clears all stored blocks and layout metadata.
    3. Canvas returns to initial empty state.
  - Alternate Paths: User cancels confirmation and board remains unchanged.
  - Postconditions: Session storage cleared; UI reflects empty canvas.

## 6. UX/UI Requirements

- Design Principles: Minimalist monochromatic palette, high clarity of primary actions, maintain generous whitespace, emphasize content over chrome.
- Accessibility (WCAG): Prototype adheres to basic keyboard focus states and readable typography; full WCAG conformance deferred to future iterations.
- Interaction Patterns: Drag-and-drop block movement, inline text editing, modal confirmation for destructive actions, unobtrusive empty-state prompt for first-time use.
- Content & Tone: No system copy beyond labels/tooltips; maintain neutral, utility-focused language when required.

## 7. Data & Analytics

- Core Entities: BoardSession, NoteBlock, EmbedBlock.
- Events to Track: None instrumented in prototype; logging deferred.
- KPIs: Qualitative usability feedback from pilot users; time-to-assemble baseline board target under 5 minutes.

## 8. Non-Functional Requirements

- Performance: Initial board load under 1s with fewer than 20 blocks; embed render latency acceptable within 2s after URL paste.
- Reliability: Session storage must retain block state until browser tab closes; reset action must fully clear state.
- Privacy: Only store target URLs and positioning metadata locally; do not cache remote content.
- Security: No authentication; ensure pasted URLs are sanitized to prevent script injection in embed previews.

## 9. Acceptance Criteria (per feature)

- [F-001] Explorer Canvas & Layout Persistence

  - Given an active session, when a user repositions a block, then the block retains its coordinates after a page refresh within the same session.
  - Given multiple blocks on the canvas, when a user deletes one, then remaining blocks maintain their stored positions.
  - Given the canvas is empty, when the page loads, then the default grid/background renders within 1s.

- [F-002] Note Blocks

  - Given the board is loaded, when a user invokes “Add Note,” then a text-editable block appears with focus ready for typing.
  - Given text is entered, when the user applies bold or bullet formatting, then the note renders formatting instantly.
  - Given a note block exists, when the user resizes it, then text reflows without clipping.

- [F-003] External Source Embeds

  - Given a supported URL is pasted, when validation passes, then an embed preview appears with source title/thumbnail.
  - Given an unsupported URL is pasted, when validation fails, then the system displays a clear error and no block is created.
  - Given an embed exists, when its position changes, then the new coordinates persist for the session.

- [F-004] Board Reset Control

  - Given blocks exist, when the user confirms reset, then all blocks disappear and session storage clears.
  - Given the reset dialog appears, when the user cancels, then the board remains unchanged.
  - Given the board was reset, when the user adds a new block, then it behaves as if the session started fresh.

- [F-005] Alignment Guides
  - Given two blocks are dragged near alignment thresholds, when snapping is enabled, then a guide appears and blocks snap within a 4px tolerance.
  - Given alignment guides are available, when a user drags rapidly, then the guides remain non-intrusive and do not lag the interaction.

## 10. Risks & Assumptions

- Risks: Embed previews may break if source platforms adjust embed APIs; lack of authentication limits personalization; no accessibility work may slow stakeholder adoption later.
- Assumptions: Users operate within a single browser session; target sources allow client-side embedding; stakeholders accept deferring accessibility and analytics until after POC validation.
