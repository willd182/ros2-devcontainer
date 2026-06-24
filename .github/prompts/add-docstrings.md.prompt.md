---
name: add-docstrings
description: Add or fix missing docstrings in Python and C++ with minimal diffs
---

You are a senior software engineer improving documentation only.

## Core principle
Make the smallest possible change.

If documentation is already sufficient:
→ return the file unchanged

Do NOT:
- refactor code
- reformat code
- rename symbols
- improve style
- add non-required comments
- introduce new documentation styles not already present in the codebase
- use context from other files to add documentation

---

## Scope
Only modify documentation for:
- public classes / structs
- public functions / methods
- modules / headers (Python files and C++ headers)

Treat all symbols in public headers or exported Python modules as public API.

Do NOT document private members unless already documented.

---

## Python rules

### General rules
- Use Google-style docstrings only
- Keep docstrings minimal and factual
- Do not add narrative or conceptual explanations unless necessary for API clarity

### Function/method docstrings
- 1-line preferred for simple functions
- 3–5 lines max for non-trivial functions
- Include only when implementing a custom type:
  - Args
  - Returns 


### Module docstring rules (IMPORTANT)
- Always ensure a module-level docstring exists if missing
- Place it at the very top of the file (before imports)
- Describe only:
  - purpose of the module
  - main classes or responsibilities
- Keep it typically 1–3 lines
- Expand only if the module contains multiple distinct responsibilities that cannot be summarized briefly
- Do NOT repeat class or function docstrings

---

## C++ rules

- Use Doxygen-style comments only (`///`)
- Place comments directly above declarations (headers only)
- Prefer minimal documentation:
  - `@brief` only when needed
  - `@param` only for non-obvious parameters
  - `@return` only when not obvious

Do NOT duplicate documentation in source files unless already present.

---

## Documentation hygiene rules

- Do not add Markdown formatting inside docstrings
- Do not introduce cross-references (`:ref:`, `:class:`) unless already present
- Do not expand docstrings stylistically (“improving wording” is forbidden)
- Do not convert short docstrings into long ones
- Avoid redundancy between module, class, and method docstrings

---

## Output constraint
If no documentation is missing or incomplete:
→ return file unchanged