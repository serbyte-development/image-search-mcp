"""Vercel ASGI entrypoint for the public image search MCP server."""

import os

from mcp.server.transport_security import TransportSecuritySettings
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from image_search_mcp import ImageSearchServer


def _env_list(name, defaults):
    raw_value = os.getenv(name)
    if not raw_value:
        return defaults

    return [item.strip() for item in raw_value.split(",") if item.strip()]


server = ImageSearchServer()
transport_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=True,
    allowed_hosts=_env_list(
        "IMAGE_SEARCH_MCP_ALLOWED_HOSTS",
        [
            "stocky-mcp.vercel.app",
            "127.0.0.1:*",
            "localhost:*",
        ],
    ),
    allowed_origins=_env_list(
        "IMAGE_SEARCH_MCP_ALLOWED_ORIGINS",
        [
            "https://chatgpt.com",
            "https://chat.openai.com",
            "https://platform.openai.com",
            "http://127.0.0.1:*",
            "http://localhost:*",
        ],
    ),
)
app = server.mcp.streamable_http_app(
    stateless_http=True,
    json_response=True,
    transport_security=transport_security,
)


async def health(_request):
    return JSONResponse({
        "name": "image-search-mcp",
        "transport": "streamable-http",
        "mcp_endpoint": "/mcp",
        "auth": "none",
    })


async def reject_mcp_get(_request):
    """Disable the optional long-lived SSE stream on serverless Vercel."""
    return Response(status_code=405, headers={"Allow": "POST"})


app.routes.insert(0, Route("/mcp", reject_mcp_get, methods=["GET"]))
app.routes.insert(0, Route("/", health, methods=["GET"]))
