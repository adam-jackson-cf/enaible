# Security Policy

## Supported Versions

| Version  | Supported          |
| -------- | ------------------ |
| Latest   | :white_check_mark: |
| < Latest | :x:                |

## Reporting a Vulnerability

Please report security vulnerabilities by emailing: **security@yourorganization.com**

### Response Times

- **Critical**: Within 24 hours
- **High**: Within 3 days
- **Medium/Low**: Within 1 week

## Automated Security Scanning

This repository uses comprehensive automated security scanning:

### 1. Continuous Monitoring

- **GitHub Dependabot**: Monitors for vulnerable dependencies
- **Automatic PRs**: Created immediately for security updates
- **Weekly Updates**: Regular dependency updates every Monday

### 2. CI/CD Validation

- **Package Manager Audits**: Security scans on every PR and push
- **Multi-Package Manager Support**: npm, yarn, pnpm, bun
- **Audit Level**: critical (blocks critical+ severity vulnerabilities)
- **Matrix Testing**: Node.js 18.x and 20.x versions

### 3. Dependency Pinning

- **Automatic Detection**: Identifies unpinned dependencies
- **Automated PRs**: Creates PRs to pin dependencies to exact versions
- **Security Benefits**: Prevents dependency confusion and ensures reproducible builds

## Severity Thresholds

### Build Blocking

- **info**: ALL vulnerabilities block builds
- **low**: Low+ severity vulnerabilities block builds
- **moderate**: Moderate+ severity vulnerabilities block builds _(default)_
- **high**: Only high and critical vulnerabilities block builds
- **critical**: Only critical vulnerabilities block builds

### Current Configuration

- **Audit Level**: `critical`
- **Weekly Scans**: Every Monday at 9 AM UTC
- **Automatic Pinning**: Enabled for unpinned dependencies

## False Positives

If you encounter false positives that are blocking development:

1. **Verify the vulnerability** is indeed a false positive
2. **Document the reasoning** for why it's not applicable
3. **Create an issue** to track the decision with justification
4. **Document in team/project security decisions** for future reference

## Security Best Practices

### For Contributors

- Keep dependencies up to date
- Review Dependabot PRs promptly
- Don't ignore security warnings
- Pin dependencies to exact versions
- Use `npm ci` instead of `npm install` in CI

### For Maintainers

- Review security PRs within 24 hours
- Merge critical security updates immediately
- Monitor security audit workflow results
- Update this policy as needed

## Workflow Configuration

The security workflow (`.github/workflows/package-audit.yml`) includes:

- **Triggers**: Push, PR, weekly schedule, manual dispatch
- **Package Managers**: Automatic detection and appropriate auditing
- **Reports**: Uploaded as artifacts with 30-day retention
- **PR Comments**: Automatic comments on security issues
- **Branch Protection**: Optional enforcement of security checks

## Emergency Procedures

### Critical Vulnerability Response

1. **Immediate Response**: Apply patches or workarounds within 24 hours
2. **Create Hotfix**: Deploy fix to production immediately
3. **Update Dependencies**: Merge security updates
4. **Verify Fix**: Ensure vulnerability is resolved
5. **Document**: Record incident and response in security log

---

_Last Updated: 2025-09-10_
_Security Workflow Version: 2.0_
