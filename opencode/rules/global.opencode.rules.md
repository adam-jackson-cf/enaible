# General coding rules

## **CRITICAL** Must follow Design Principles

### General Principles

- **NEVER implement backward compatibility** never refactor code to handle its new objective AND its legacy objective, all legacy code should be removed.
- **NEVER create fallbacks** we never build fallback mechanisms, our code should be designed to work as intended without fallbacks.
- **NEVER over engineer** only action what the user has requested, if you dont have approval for an action you must ask the user.
- **ALWAYS minimise complexity** keep code Cyclomatic Complexity under 10
- **ALWAYS prefer established libraries over bespoke code** only produce bespoke code if no established library - **ALWAYS use appropriate symbol naming when refactoring code**: When refactoring do not add prefixes/suffixes like "Refactored", "Updated", "New", or "V2" to symbol names to indicate changes.

### SOLID Principles - Architectural Shaping (with Examples)

#### Single Responsibility

- **ALWAYS** give every module/class/function exactly one clear responsibility — Example: keep `InvoiceFormatter` focused on string formatting; move PDF generation to `InvoicePdfBuilder`.
- **NEVER** bundle unrelated behaviors in a single unit — Example: if `UserController` handles profile edits and billing, split billing into `BillingController`.
- **ALWAYS** extract shared logic when the same behavior appears 3+ times — Example: move repeated “normalize phone number” snippets into `sanitize_phone_number()`.

#### Open/Closed

- **ALWAYS** design abstractions so new behavior is added via extension, not edits — Example: add `StripePaymentProcessor` that implements `PaymentProcessor` rather than changing `PaypalPaymentProcessor`.
- **NEVER** edit a stable component just to introduce a variant — Example: don’t rewrite `DiscountCalculator`; introduce `SeasonalDiscountCalculator` that plugs into the same interface.
- **ALWAYS** protect core contracts with tests before restructuring — Example: lock in `ShippingCostService`’s public API with tests, then add `ExpressShippingStrategy`.

#### Liskov Substitution

- **ALWAYS** ensure any subtype can replace its base without changing observable behavior — Example: `CachingConfigLoader` must return the same config shape as `ConfigLoader`.
- **NEVER** narrow preconditions or widen postconditions in overrides — Example: if `FileStorage.save()` accepts any file-like object, `S3Storage.save()` must accept the same, not only file paths.
- **ALWAYS** preserve exception semantics across the hierarchy — Example: if `Queue.dequeue()` raises `QueueEmptyError`, `PriorityQueue.dequeue()` must raise the same error.

#### Interface Segregation

- **ALWAYS** offer clients the smallest interface they need — Example: split `ReportingService` into `ReportBuilder` and `ReportPublisher` so consumers depend only on `ReportBuilder`.
- **NEVER** force consumers to import methods they’ll never call — Example: if `NotificationClient` exposes `send_sms()` and `send_email()` but a caller only emails, provide `EmailSender` instead.
- **ALWAYS** document each interface’s audience and responsibility — Example: mark `AuditTrailWriter` as “used solely by compliance logging” to prevent general-purpose reuse.

#### Dependency Inversion

- **ALWAYS** depend on abstractions and inject collaborators — Example: have `OrderService` receive a `PaymentProcessor` in its constructor rather than instantiating `StripePaymentProcessor` directly.
- **NEVER** let high-level policies import low-level modules — Example: keep `AnalyticsController` from importing `psycopg2`; depend on an `EventRepository` interface.
- **ALWAYS** centralize wiring in composition roots or factories — Example: configure bindings in `app_container.py`, leaving `InventoryService` free of framework-specific setup.

### DRY Principles - Implementation Hygiene (with Examples)

- **ALWAYS** extract repeated behavior into a single reusable unit as soon as duplication appears — Example: consolidate three separate "calculate tax and tip" snippets into a single `compute_order_totals()` helper used by checkout, refunds, and reporting.
- **NEVER** copy‑paste code to meet a deadline; refactor the shared logic before adding new cases — Example: instead of duplicating the email confirmation workflow for SMS, move the common "compose confirmation payload" steps into `build_confirmation_payload()` and reuse it for both channels.
- **ALWAYS** reconcile parallel knowledge sources so there’s a single source of truth — Example: migrate duplicated validation rules from both `signup_form.validate()` and `user_service.create_user()` into a central `UserValidator`, then delete the scattered checks.
- **NEVER** let configuration or constants drift across files — Example: pull repeated "30-minute session timeout" literals into `SESSION_TIMEOUT_MINUTES` inside `settings.py` and reference it everywhere.

## **CRITICAL** Must follow Behaviour Rules - how you must carry out actions

### Research Approach

- **ALWAYS**: Read the entire contents of a source of information or context for your current task objective
- **ALWAYS**: Read the entire class, symbols or function you intend to change

### Security Requirements

- **NEVER**: commit secrets, API keys, or credentials to version control
- **NEVER**: expose sensitive information like api keys, secrets or credentials in any log or database entries

### Prohibited Reward Hacking

- **NEVER** use placeholders, mocking, hardcoded values, or stub implementations outside test contexts
- **NEVER** suppress, bypass, handle with defaults, or work around quality gate failures, errors, or test failures
- **NEVER** alter, disable, suppress, add permissive variants to, or conditionally bypass quality gates or tests
- **NEVER** comment out, conditionally disable, rename to avoid calling, or move to unreachable locations any failing code
- **NEVER** delegate prohibited behaviors to external services, configuration files, or separate modules
- **NEVER** bypass, skip or change a task if it fails without the users permission
- **NEVER** implement fallback modes or temporary strategys to meet task requirements
- **NEVER** bypass quality gates by using `--skip` or `--no-verify`

---
