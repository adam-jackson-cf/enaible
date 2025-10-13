**CRITICAL** You must follow and apply the below ways of working to your current task(s)

**Purpose**: Minimal intrusion code changes with comprehensive system understanding and surgical precision

### Core Principles:

- Understand system context completely before making any changes
- Minimize code footprint while achieving the objective
- Preserve existing system behavior where not conflicting with task requirements
- Map all inputs and outputs clearly before implementation
- Implement single-purpose solutions without fallback mechanisms
- Maintain descriptive naming without process-referential artifacts

### System Analysis Requirements:

**Context Mapping Standards**:

- Identify all affected components and their boundaries
- Map data flow through the system for affected areas
- Understand existing interfaces and their contracts
- Document current behavior that must be preserved

**Dependency Analysis**:

- Trace all upstream dependencies that provide inputs
- Identify all downstream consumers of outputs
- Map integration points and external system connections
- Assess impact radius of proposed changes

### Implementation Standards:

**Surgical Precision Approach**:

- Target the smallest possible code area that achieves the objective
- Preserve existing symbol names wherever possible
- Make changes at the most specific scope necessary
- Avoid broad refactoring unless directly required for the task

**Naming Requirements**:

- New symbols must be descriptive of their purpose, not the change process
- NEVER use suffixes like `-refactored`, `-fixed`, `-updated`, `-new`, `-v2`
- Preserve existing naming conventions and patterns
- Choose names that reflect business purpose and functionality

**Implementation Prohibitions**:

- NEVER implement fallback mechanisms or backward compatibility layers
- NEVER create dual-purpose code that serves both old and new requirements
- NEVER add conditional logic to handle legacy behavior
- Code must serve only the single intended purpose of the task

### Change Implementation Process:

1. **Analysis Phase**: Map current system behavior and identify minimal change points
2. **Design Phase**: Choose the least intrusive approach that achieves the objective
3. **Implementation Phase**: Make surgical changes with preserved naming and no fallbacks
4. **Validation Phase**: Verify the change achieves the objective without unintended side effects

### Validation Criteria:

**Impact Assessment**:

- Confirm changes are limited to the minimum necessary scope
- Verify no unintended behavior changes in unrelated system areas
- Ensure all existing interfaces continue to function as expected
- Validate that naming follows descriptive, non-process patterns

**Change Verification**:

- Test that the objective is fully achieved
- Confirm no fallback or compatibility code exists
- Verify clean, purpose-driven implementation
- Ensure system integration points remain stable
