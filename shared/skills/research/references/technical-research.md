# Purpose

Research technical topics, analyze implementations, and evaluate solutions using structured methodologies.

## Deterministic Logging

Log each retained source with `scripts/research_execute.py source` and associate it with a question ID.

## Documentation Research Patterns

### Source Priority Order

1. **Official documentation**: Creator/maintainer docs, API references (check release notes or changelog to confirm recency; run @WEB_FETCH where needed)
2. **GitHub repositories**: High-star repos, recent activity, good maintenance (record commit hashes and retrieval dates)
3. **Technical blogs**: Recognized industry experts, engineering blogs from established companies (verify publish date; refresh searches for anything >12 months old unless foundational)
4. **Academic sources**: Conference papers, technical books (note conference year or edition)
5. **Community resources**: Stack Overflow, Reddit (supplementary; capture thread URLs and timestamps)

### Documentation Assessment

For each source, evaluate:

- Completeness of coverage
- Currency (last update date) and whether fresh searches uncovered newer revisions
- Quality of examples
- Community contributions and corrections
- Known gaps or outdated sections

## Code Analysis Approaches

### Repository Evaluation

- **Activity metrics**: Commit frequency, issue response time, release cadence
- **Community health**: Contributors, stars, forks, open issues ratio
- **Code quality**: Test coverage, documentation, lint compliance
- **Architecture**: Directory structure, separation of concerns, dependencies

### Pattern Identification

- Design patterns in use (factory, observer, strategy, etc.)
- Architectural patterns (MVC, microservices, event-driven)
- Error handling approaches
- Testing strategies
- Performance optimization techniques

## Implementation Comparison Framework

| Criterion          | Option A | Option B | Option C |
| ------------------ | -------- | -------- | -------- |
| Maturity           |          |          |          |
| Performance        |          |          |          |
| Ease of use        |          |          |          |
| Documentation      |          |          |          |
| Community support  |          |          |          |
| License            |          |          |          |
| Maintenance status |          |          |          |

### Evaluation Criteria

- **Maturity**: Version stability, production usage, breaking change history
- **Performance**: Benchmarks, scalability characteristics, resource requirements
- **Developer experience**: Learning curve, documentation quality, tooling
- **Ecosystem**: Integrations, plugins, community extensions
- **Long-term viability**: Funding, governance, adoption trajectory

## Architecture Decision Extraction

### ADR Components

For each significant architectural decision found:

- **Context**: What problem or requirement prompted this?
- **Decision**: What approach was chosen?
- **Rationale**: Why was this approach selected?
- **Consequences**: What trade-offs result from this decision?
- **Alternatives**: What other options were considered?

## Best Practices Research

### Collection Framework

For each major concept or technique:

- Clear definition and explanation
- Usage examples (not full implementations)
- Common pitfalls and anti-patterns
- Performance considerations
- Security implications

### Validation Approach

- Cross-reference multiple authoritative sources
- Check for version-specific applicability
- Note conflicting recommendations
- Identify consensus best practices

## Output Structure

### Technical Research Report

1. **Getting Started**: Installation, setup, minimal example
2. **Core Concepts**: Key abstractions, architecture overview
3. **Best Practices**: Industry standards, recommended patterns
4. **Common Patterns**: Practical examples for typical use cases
5. **Troubleshooting**: Common errors, debugging techniques
6. **Comparison**: Trade-offs between alternatives (if applicable)
