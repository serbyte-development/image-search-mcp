---
name: install-image-search-mcp
description: Install and configure the Serbyte Image Search MCP server for Unsplash, Pexels, and Pixabay. Use when a user asks an AI coding agent to install this MCP, add it to an MCP client, configure provider API keys, or verify the installation.
---

# Install Image Search MCP

Repository: `https://github.com/Serbyte-Development/image-search-mcp`

## Goal

Install the MCP server locally, configure provider API keys, add it to the user's MCP client, and verify that the tools are available.

## Instructions

1. Determine the user's operating system and MCP client from context or local inspection when possible. Ask only if it cannot be determined.
2. Prefer a packaged install instead of cloning the repository:

   ```bash
   brew install Serbyte-Development/tap/image-search-mcp
   ```

   If Homebrew is unavailable or the formula has not been published yet, use:

   ```bash
   pipx install git+https://github.com/Serbyte-Development/image-search-mcp.git
   ```

   Fall back to cloning + a virtual environment only if neither packaged path is available.

3. Ask the user for whichever provider API keys they want to use. At least one provider must be configured:

   - `PEXELS_API_KEY`
   - `UNSPLASH_ACCESS_KEY`
   - `PIXABAY_API_KEY`

   Never print, commit, or expose secret values.

4. Configure the user's MCP client to launch the installed `image-search-mcp` command and pass the provider keys as environment variables.

   Example configuration shape:

   ```json
   {
     "mcpServers": {
       "image-search": {
         "command": "image-search-mcp",
         "env": {
           "PEXELS_API_KEY": "...",
           "UNSPLASH_ACCESS_KEY": "...",
           "PIXABAY_API_KEY": "..."
         }
       }
     }
   }
   ```

   Only include keys the user actually configured. If the client requires a remote MCP endpoint instead of stdio, help the user deploy their own copy to Vercel, configure the provider keys as Vercel environment variables, and connect to `https://<project>.vercel.app/mcp`. Do not use the maintainer's deployment. Verify the endpoint after deployment; if host validation returns HTTP 421, expose Vercel system environment variables or set `IMAGE_SEARCH_MCP_ALLOWED_HOSTS` to the deployment host.

5. Restart or reload the MCP client if required.
6. Verify the server by listing MCP tools. Expected tools:

   - `search_stock_images`
   - `get_image_details`
   - `download_image`

7. Run one small image search against a configured provider to confirm end-to-end functionality.

## Rules

- Prefer performing the installation directly when shell and filesystem access are available instead of only giving instructions.
- Do not overwrite an existing MCP configuration. Merge the new server entry into it.
- Preserve unrelated user configuration.
- Do not store API keys in the repository.
- If the user's MCP client has a native install command or a different configuration format, adapt the configuration to that client rather than forcing the JSON example above.
