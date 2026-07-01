# MigraAPI Documentation

Welcome to the **MigraAPI** documentation.

MigraAPI is a demonstration project that implements **Claude Agent Skills** and **Subagents** (Anthropic) to automate migration from a deprecated API to a new API in Python and JavaScript codebases.

## Quick links

- [GitHub Repository](https://github.com/davideferigato/MigraAPI)
- [Architecture Overview](architecture.md)
- [Subagents Design](subagents.md)
- [Contributing Guide](contributing.md)

## What you'll find here

- **Architecture**: Progressive disclosure, orchestrator pattern, parallel execution.
- **Subagents**: How to create scanner, rewriter, validator subagents with structured outputs.
- **Contributing**: Guidelines for extending the project.

## Get started

Clone the repository and run the demo:

```bash
git clone https://github.com/davideferigato/MigraAPI
cd MigraAPI
./demo-script.sh
```

For real usage with Claude Code, see the [main README](../README.md).

---
*Built with Anthropic's Agent Skills & Subagents*
