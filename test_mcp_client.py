#!/usr/bin/env python3
"""End-to-end smoke test using the MCP v2 client in process."""

import asyncio

from dotenv import load_dotenv
from mcp.client import Client

from image_search_mcp import ImageSearchServer


def _tool_payload(result):
    """Return Image Search MCP's structured tool payload."""
    structured = result.structured_content or {}
    return structured.get("result", structured)


async def main():
    """Exercise discovery, tools, provider routing, and the help resource."""
    load_dotenv()
    server = ImageSearchServer()

    async with Client(server.mcp) as client:
        print(f"Protocol: {client.protocol_version}")

        tools = await client.list_tools()
        print(f"Tools: {[tool.name for tool in tools.tools]}")

        search = await client.call_tool(
            "search_stock_images",
            {
                "query": "mountain landscape",
                "providers": ["pexels"],
                "per_page": 1,
            },
        )
        search_payload = _tool_payload(search)
        images = search_payload.get("results", [])
        assert images, "Pexels search returned no images"
        assert search_payload.get("providers") == ["pexels"]
        assert {image["source"] for image in images} == {"Pexels"}
        print(f"Search: {images[0]['id']} from {images[0]['source']}")

        details = await client.call_tool(
            "get_image_details",
            {"image_id": images[0]["id"]},
        )
        details_payload = _tool_payload(details)
        assert details_payload.get("source") == "Pexels"
        print(f"Details: {details_payload['id']}")

        resources = await client.list_resources()
        uris = [str(resource.uri) for resource in resources.resources]
        assert "stock-images://help" in uris

        help_result = await client.read_resource("stock-images://help")
        assert help_result.contents
        print("Help resource: OK")


if __name__ == "__main__":
    asyncio.run(main())
