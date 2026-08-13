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
2. Clone the repository into a sensible local tools directory. If it already exists, reuse it rather than cloning a second copy.
3. Create a Python virtual environment with Python 3.10 or newer and install the project:

   ```bash
   python -m venv .venv
   .venv/bin/python -m pip install -e .
   ```

   On Windows, use `.venv\\Scripts\\python.exe` instead.

4. Ask the user for whichever provider API keys they want to use. At least one provider must be configured:

   - `PEXELS_API_KEY`
   - `UNSPLASH_ACCESS_KEY`
   - `PIXABAY_API_KEY`

   Never print, commit, or expose secret values.

5. Configure the user's MCP client to launch `image_search_mcp.py` with the virtual-environment Python and pass the provider keys as environment variables. Use absolute paths.

   Example configuration shape:

   ```json
   {
     "mcpServers": {
       "image-search": {
         "command": "/absolute/path/to/image-search-mcp/.venv/bin/python",
         "args": ["/absolute/path/to/image-search-mcp/image_search_mcp.py"],
         "env": {
           "PEXELS_API_KEY": "...",
           "UNSPLASH_ACCESS_KEY": "...",
           "PIXABAY_API_KEY": "..."
         }
       }
     }
   }
   ```

   Only include keys the user actually configured.

6. Restart or reload the MCP client if required.
7. Verify the server by listing MCP tools. Expected tools:

   - `search_stock_images`
   - `get_image_details`
   - `download_image`

8. Run one small image search against a configured provider to confirm end-to-end functionality.

## Rules

- Prefer performing the installation directly when shell and filesystem access are available instead of only giving instructions.
- Do not overwrite an existing MCP configuration. Merge the new server entry into it.
- Preserve unrelated user configuration.
- Do not store API keys in the repository.
- If the user's MCP client has a native install command or a different configuration format, adapt the configuration to that client rather than forcing the JSON example above.
