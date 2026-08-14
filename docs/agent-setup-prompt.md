# Agent Setup Prompt

Copy this prompt into a coding agent or AI assistant:

```text
Install and connect Serbyte Development's Image Search MCP from:
https://github.com/Serbyte-Development/image-search-mcp

Detect my operating system and MCP client. Prefer the simplest packaged local install:
- Homebrew: brew install Serbyte-Development/tap/image-search-mcp
- Otherwise: pipx install --backend pip git+https://github.com/Serbyte-Development/image-search-mcp.git

Ask me which provider API keys I want to configure. At least one is required:
PEXELS_API_KEY, UNSPLASH_ACCESS_KEY, PIXABAY_API_KEY.

For a local MCP client, configure stdio using the `image-search-mcp` command and pass only the provider keys I supply as environment variables.

If my client requires a remote MCP endpoint, help me deploy my own copy to Vercel from the repository, add my provider keys as Vercel environment variables, and connect the client to https://<my-project>.vercel.app/mcp. Do not use the maintainer's deployment.

Do not print, commit, or store my API keys in the repository. Preserve existing MCP configuration. Restart/reload the client if needed, verify the tools are visible, and run one small image search to confirm the connection. If I self-host remotely, remind me the default endpoint has no authentication and requests use my provider API quota.
```

Expected tools:

- `search_stock_images`
- `get_image_details`
- `download_image`
