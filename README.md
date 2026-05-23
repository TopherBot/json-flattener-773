# json‑flattener

A **single‑file** Python utility that:

* Accepts JSON from **stdin**, a **file**, or a **URL**.
* Flattens nested objects into dot‑notation keys (e.g. `{"a":{"b":1}` → `a.b: 1`).
* Optionally **unflattens** back to the original structure.
* Provides colour‑coded output for readability.

## Installation

```bash
# From source
pip install .
# Or using the compiled binary (optional, see GitHub Releases)
curl -Lo json-flattener https://github.com/your‑user/json-flattener/releases/latest/download/json-flattener && chmod +x json-flattener && ./json-flattener --help
```

## Usage

```bash
# From a file
json-flattener -f data.json

# From stdin
cat data.json | json-flattener

# From a URL
json-flattener -u https://example.com/data.json

# Unflatten back
json-flattener -u https://example.com/flat.json --unflatten
```

## Development

```bash
# Set up the dev environment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest
```

## CI / Release Workflow

* **Tests** – `pytest` with coverage > 90%.
* **Installability** – `pip install .` on a clean Ubuntu runner.
* **Release** – Tag‑based GitHub Actions automatically build a self‑contained binary with `pyinstaller` and publish to GitHub Releases.

---

*If the repository name `json-flattener` is already taken, the fallback name will be `json‑flattener‑cli`.*
