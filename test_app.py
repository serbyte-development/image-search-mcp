import os
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from mcp.client import Client

from app import _default_allowed_hosts
from image_search_mcp import ImageSearchServer, _server_icons


class VercelHostConfigurationTests(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "VERCEL_PROJECT_PRODUCTION_URL": "image-search.example.com",
            "VERCEL_URL": "image-search-preview.vercel.app",
            "VERCEL_BRANCH_URL": "image-search-git-main.vercel.app",
        },
        clear=False,
    )
    def test_vercel_hosts_are_added_to_default_allowlist(self):
        self.assertEqual(
            _default_allowed_hosts(),
            [
                "127.0.0.1:*",
                "localhost:*",
                "image-search.example.com",
                "image-search-preview.vercel.app",
                "image-search-git-main.vercel.app",
            ],
        )


class ServerIconTests(unittest.IsolatedAsyncioTestCase):
    async def test_initialize_exposes_server_icons(self):
        with patch.dict(
            os.environ, {"VERCEL_PROJECT_PRODUCTION_URL": "stocky-mcp.vercel.app"}
        ):
            server = ImageSearchServer()

        async with Client(server.mcp) as client:
            self.assertIsNotNone(client.server_info)
            self.assertEqual(
                [icon.src for icon in client.server_info.icons],
                [
                    "https://stocky-mcp.vercel.app/icon.png",
                    "https://stocky-mcp.vercel.app/icon.webp",
                ],
            )

    def test_self_hosted_vercel_icon_urls(self):
        with patch.dict(
            os.environ, {"VERCEL_PROJECT_PRODUCTION_URL": "my-stocky.vercel.app"}
        ):
            self.assertEqual(
                [icon.src for icon in _server_icons()],
                [
                    "https://my-stocky.vercel.app/icon.png",
                    "https://my-stocky.vercel.app/icon.webp",
                ],
            )

    def test_registry_icon_metadata_points_to_static_assets(self):
        root = Path(__file__).parent
        registry = json.loads((root / "server.json").read_text())
        for icon in registry["icons"]:
            self.assertTrue((root / "public" / Path(icon["src"]).name).is_file())


if __name__ == "__main__":
    unittest.main()
