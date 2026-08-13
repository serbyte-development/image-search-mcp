# MCP Image Search Server for Unsplash, Pexels & Pixabay

[![CI](https://github.com/Serbyte-Development/image-search-mcp/actions/workflows/python-lint.yml/badge.svg)](https://github.com/Serbyte-Development/image-search-mcp/actions/workflows/python-lint.yml)
[![CodeQL](https://github.com/Serbyte-Development/image-search-mcp/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Serbyte-Development/image-search-mcp/actions/workflows/codeql-analysis.yml)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![MCP Python SDK 2.x](https://img.shields.io/badge/MCP%20Python%20SDK-2.x-5A45FF)](https://github.com/modelcontextprotocol/python-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Image Search MCP** is a Model Context Protocol server for searching **Unsplash, Pexels, and Pixabay** from one MCP client. Search one provider or all configured providers concurrently, return normalized image metadata, inspect image details, and download results.

Use it as an **Unsplash MCP server**, **Pexels MCP server**, **Pixabay MCP server**, or one unified **MCP image search** tool.

<p align="center">
  <img src="images/landscape-mountains.jpg" alt="Stock image result available through the MCP image search server" width="800">
</p>

## Features

- Search Unsplash, Pexels, and Pixabay through one MCP server
- Query multiple configured providers concurrently
- Filter searches to specific providers
- Normalize results into one consistent image schema
- Fetch detailed metadata for individual images
- Download images or return base64 image data
- Run locally over MCP or deploy with Streamable HTTP
- Fail clearly when a requested provider is invalid or not configured

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/Serbyte-Development/image-search-mcp.git
cd image-search-mcp

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Get provider API keys

Configure one or more of these environment variables:

```text
PEXELS_API_KEY
UNSPLASH_ACCESS_KEY
PIXABAY_API_KEY
```

API keys are available from:

- Pexels: https://www.pexels.com/api/
- Unsplash: https://unsplash.com/developers
- Pixabay: https://pixabay.com/api/docs/

You only need keys for the providers you want to use.

### 3. Add the MCP server to your client

```json
{
  "mcpServers": {
    "image-search": {
      "command": "/absolute/path/to/image-search-mcp/.venv/bin/python",
      "args": [
        "/absolute/path/to/image-search-mcp/image_search_mcp.py"
      ],
      "env": {
        "PEXELS_API_KEY": "your_pexels_key",
        "UNSPLASH_ACCESS_KEY": "your_unsplash_key",
        "PIXABAY_API_KEY": "your_pixabay_key"
      }
    }
  }
}
```

Restart your MCP client after saving the configuration.

## MCP Tools

### `search_stock_images`

Search one or more configured providers.

Parameters:

- `query` - search query
- `providers` - optional list containing `pexels`, `unsplash`, and/or `pixabay`
- `per_page` - results per provider, clamped to 1-50
- `page` - page number
- `sort_by` - `relevant` or `newest`
- `include_attribution` - include provider attribution links when available

Example:

```json
{
  "query": "modern office interior",
  "providers": ["unsplash", "pexels"],
  "per_page": 10
}
```

### `get_image_details`

Fetch detailed metadata for a provider-prefixed image ID such as `pexels_123456`.

### `download_image`

Download an image by ID. Supported size values are `thumbnail`, `small`, `medium`, `large`, and `original`.

If `output_path` is omitted, the tool returns base64 image data instead of writing a file.

## Result Format

Search results are normalized across providers and include fields such as:

```json
{
  "id": "pexels_123456",
  "title": "Example image",
  "url": "https://...",
  "thumbnail": "https://...",
  "width": 1920,
  "height": 1080,
  "photographer": "Photographer Name",
  "source": "Pexels",
  "license": "Provider license",
  "tags": []
}
```

## Run from the CLI

Install the local command:

```bash
pip install -e .
```

Then run:

```bash
image-search-mcp
```

## Deploy with Streamable HTTP

`app.py` exposes a stateless Streamable HTTP MCP endpoint suitable for Vercel.

Set your provider API keys in the deployment environment, deploy the repository, then connect MCP clients to:

```text
https://your-project.vercel.app/mcp
```

The example deployment does not add authentication. If you expose an MCP endpoint publicly, add appropriate access controls or expect requests to consume your provider API quotas.

Optional transport security settings:

```text
IMAGE_SEARCH_MCP_ALLOWED_HOSTS
IMAGE_SEARCH_MCP_ALLOWED_ORIGINS
```

Both accept comma-separated values.

## Development

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run lint, type checks, and unit tests:

```bash
make check PYTHON=.venv/bin/python
```

The repository also runs CI and CodeQL on pushes and pull requests to `main`.

## Image Licensing

This project is MIT licensed, but images returned by the providers are governed by each provider's own current license and API terms. Review the applicable provider terms before using downloaded content in production.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## License

MIT - see [LICENSE](LICENSE).
