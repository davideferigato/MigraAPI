# Security Policy

## Supported Versions

Only the latest commit on `main` is supported (this is a demonstration project).

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not** open a public issue.

Send a private email to: **davide.ferigato@example.com** (replace with real email).

We will acknowledge receipt within **48 hours** and aim to resolve within **14 days**.

## Best Practices for Users

- **Always inspect third-party skills** before installation – especially `allowed-tools` and scripts.
- **Run `scanner.py` in a sandbox** if scanning untrusted code (e.g., container or isolated VM).
- **Never commit secrets** – `.gitignore` excludes `.env`, `*.key`, and `*.pem` by default.
- **Use `allowed-tools`** – this skill restricts scanner to `Read`, `Grep`, `Glob` only.

## Disclosure Policy

We follow a **coordinated disclosure** process:
1. Reporter sends details privately.
2. Maintainers confirm and address the issue.
3. A fix is prepared and tested.
4. Public disclosure with credits after fix is released.

## Acknowledgements

We thank the community for helping keep MigraAPI secure. Security researchers are welcome to responsibly disclose findings.
