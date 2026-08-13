# Contributing

Contributions to Image Search MCP are welcome.

## Development setup

```bash
git clone https://github.com/Serbyte-Development/image-search-mcp.git
cd image-search-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Before opening a pull request

Run the full local check:

```bash
make check PYTHON=.venv/bin/python
```

For provider changes, keep the normalized `ImageResult` contract stable unless the change intentionally updates that public shape. Never commit API keys, provider credentials, downloaded private assets, or local `.env` files.

## Pull requests

Keep each pull request focused. Include a concise description of the problem, the implementation, and how you verified it. Add or update tests when behavior changes.

By contributing, you agree that your contribution is licensed under the repository's MIT License.

