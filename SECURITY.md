# 🔐 Security Policy for Agent Performance Monitor

## Overview

Security is a top priority for Agent Performance Monitor. This document outlines our security practices and how to report vulnerabilities.

## Supported Versions

| Version | Supported          | Release Date |
|---------|-------------------|---------------|
| 0.1.x   | ✅ Yes            | 2024-06-15   |
| 0.0.x   | ❌ No             | EOL          |

## Security Best Practices

### 1. Environment Variables & Secrets

**NEVER commit secrets to version control:**

```bash
# ✅ DO: Use .env.example with placeholder values
# ❌ DON'T: Commit actual .env files with real secrets
# ✅ DO: Use environment variable substitution in production
# ❌ DON'T: Hardcode API keys in source code
```

**Files that MUST be in .gitignore:**
- `.env` - Local environment variables
- `.env.local` - Local overrides
- `.env.*.local` - Environment-specific secrets
- `secrets.json` - JSON secrets
- `*.pem`, `*.key`, `*.cert` - SSL certificates and keys

### 2. Database Security

**Connection Security:**
```python
# ✅ DO: Use connection pooling with SSL
# ✅ DO: Use strong passwords (minimum 16 characters, mixed case, numbers, symbols)
# ❌ DON'T: Use default credentials in production
# ✅ DO: Enable SSL/TLS for database connections
```

**Data Protection:**
- Sensitive data should be encrypted at rest
- Use parameterized queries to prevent SQL injection
- Implement row-level security where appropriate

### 3. API Security

**Authentication:**
```python
# ✅ DO: Use JWT tokens with secure signing
# ✅ DO: Implement rate limiting on all endpoints
# ✅ DO: Use HTTPS only in production
# ❌ DON'T: Pass credentials in URLs
# ✅ DO: Implement token expiration
# ✅ DO: Support token refresh with rotation
```

**Authorization:**
```python
# ✅ DO: Implement role-based access control (RBAC)
# ✅ DO: Validate permissions on every endpoint
# ❌ DON'T: Trust client-side permission checks
# ✅ DO: Log authorization failures
```

### 4. Input Validation

```python
# ✅ DO: Validate all input (type, length, format)
# ✅ DO: Use Pydantic models for request validation
# ❌ DON'T: Trust client input
# ✅ DO: Sanitize output to prevent XSS
# ✅ DO: Implement rate limiting per user
```

### 5. Logging & Monitoring

**What to LOG:**
- Authentication attempts (success and failure)
- Authorization failures
- Data access patterns
- Configuration changes
- API errors and exceptions

**What NOT to LOG:**
- ❌ API keys or tokens
- ❌ Passwords or sensitive credentials
- ❌ Personal identification information (PII)
- ❌ Credit card numbers
- ❌ Full request/response bodies containing secrets

```python
# ✅ DO: Log sanitized error messages
logger.warning(f"API key validation failed for user {user_id}")

# ❌ DON'T: Log actual secrets
# logger.debug(f"API key: {api_key}")  # NEVER DO THIS
```

### 6. Dependencies & Vulnerabilities

**Keep Dependencies Updated:**
```bash
# Check for vulnerabilities
pip install safety
safety check

# Audit dependencies
pip install pip-audit
pip-audit

# Update requirements regularly
pip-compile --upgrade requirements.txt
```

**Supply Chain Security:**
- Only use packages from trusted sources
- Pin exact versions for production
- Review dependency licenses
- Monitor for security advisories

### 7. Secrets Management

**Development:**
```bash
# Use .env.example (committed)
# Copy to .env and fill with your values (NOT committed)
cp .env.example .env
# Edit .env with your local values
```

**Production:**
```bash
# DO NOT use .env files
# Use a secrets manager:
# - AWS Secrets Manager
# - Azure Key Vault
# - HashiCorp Vault
# - Google Secret Manager
# - Kubernetes Secrets (with encryption)
```

**Best Practices:**
- Rotate secrets regularly
- Use unique secrets for each environment
- Implement audit logging for secret access
- Never include secrets in error messages
- Use short-lived credentials when possible

## Reporting Security Vulnerabilities

### Private Disclosure

If you discover a security vulnerability, please email: `security@apm.dev`

**Include:**
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)
- Your contact information

### Responsible Disclosure Timeline

1. **Initial Report**: Send to security@apm.dev
2. **Acknowledgment**: We will acknowledge within 24 hours
3. **Investigation**: We will investigate within 72 hours
4. **Fix Development**: We will develop a fix (timeline depends on severity)
5. **Release**: We will release a patch
6. **Disclosure**: We will publish a security advisory

### Vulnerability Severity Levels

| Severity | CVSS Score | Timeline | Example |
|----------|-----------|----------|----------|
| Critical | 9.0-10.0  | 24 hours | Authentication bypass |
| High     | 7.0-8.9   | 72 hours | Privilege escalation |
| Medium   | 4.0-6.9   | 1 week   | Information disclosure |
| Low      | 0.1-3.9   | 2 weeks  | Minor bug |

## Security Checklist for Contributors

Before submitting a Pull Request:

- [ ] No secrets or credentials in code
- [ ] No hardcoded API keys
- [ ] All user input is validated
- [ ] SQL queries use parameterized statements
- [ ] Passwords are hashed (bcrypt, argon2, etc.)
- [ ] Error messages don't leak sensitive information
- [ ] Logging doesn't include secrets
- [ ] Dependencies are up to date
- [ ] No debug code or print statements in production code
- [ ] Tests include security test cases
- [ ] Documentation includes security best practices

## Security Headers

All API responses should include security headers:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
```

## CORS Configuration

Configure CORS carefully:

```python
# ✅ DO: Specify exact origins in production
CORS_ALLOWED_ORIGINS = ["https://apm.yourdomain.com"]

# ❌ DON'T: Allow all origins
# CORS_ALLOWED_ORIGINS = ["*"]
```

## SSL/TLS

**Production Requirements:**
- [ ] Use HTTPS only
- [ ] Use TLS 1.2 or higher
- [ ] Use strong cipher suites
- [ ] Implement HSTS
- [ ] Use valid SSL certificates
- [ ] Automate certificate renewal

## Database Security

**PostgreSQL Hardening:**
```sql
-- ✅ DO: Use strong passwords
-- ✅ DO: Limit connections
-- ✅ DO: Use SSL connections
-- ✅ DO: Implement row-level security
-- ❌ DON'T: Use superuser credentials for applications
```

## Compliance

This tool may need to comply with:
- GDPR (General Data Protection Regulation)
- CCPA (California Consumer Privacy Act)
- HIPAA (Health Insurance Portability and Accountability Act)
- SOC 2 (System and Organization Controls)

Please ensure your deployment adheres to applicable regulations.

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## Questions?

If you have security-related questions, please contact: `security@apm.dev`

---

**Last Updated**: 2024-06-15
**Version**: 1.0
