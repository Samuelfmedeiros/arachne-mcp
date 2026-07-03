# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | ✅ Active development |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it privately.

**Do not open a public GitHub issue.** Instead, send an email to the maintainer or open a private security advisory at:
https://github.com/Samuelfmedeiros/arachne-mcp/security/advisories

Please include:
- Description of the vulnerability
- Steps to reproduce
- Affected versions
- Potential impact

You should receive a response within 48 hours. If the issue is confirmed, a fix will be released as soon as possible, and you will be credited in the release notes.

## Security Best Practices

- **API keys** are read from environment variables, never hardcoded
- Input validation is performed on all user-supplied data
- Dependencies are scanned regularly via Dependabot
- Secrets are excluded from version control via `.env` and `.gitignore`
