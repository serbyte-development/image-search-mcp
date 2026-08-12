"""Focused unit tests for Stocky's provider selection and search manager."""

import asyncio
import unittest

from stocky_mcp import ImageResult, StockImageManager, StockImageProvider


class FakeProvider(StockImageProvider):
    """Provider test double that can coordinate concurrent searches."""

    def __init__(self, source, prefix, shared=None, expected_starts=0):
        super().__init__("test-key")
        self.source = source
        self.prefix = prefix
        self.shared = shared
        self.expected_starts = expected_starts

    async def search(self, query, per_page=20, page=1, **kwargs):
        if self.shared is not None:
            self.shared["started"] += 1
            if self.shared["started"] == self.expected_starts:
                self.shared["ready"].set()
            await asyncio.wait_for(self.shared["ready"].wait(), timeout=0.5)

        return [
            ImageResult(
                id=f"{self.prefix}_{index}",
                title=query,
                description=query,
                url=f"https://example.com/{self.prefix}/{index}",
                thumbnail=f"https://example.com/{self.prefix}/{index}/thumb",
                width=100,
                height=100,
                photographer="Tester",
                photographer_url=None,
                source=self.source,
                license="test",
            )
            for index in range(per_page)
        ]

    async def get_details(self, image_id):
        return None


class StockImageManagerTests(unittest.IsolatedAsyncioTestCase):
    def manager_with_all_providers(self):
        manager = StockImageManager()
        manager.providers = {
            "pexels": FakeProvider("Pexels", "pexels"),
            "unsplash": FakeProvider("Unsplash", "unsplash"),
            "pixabay": FakeProvider("Pixabay", "pixabay"),
        }
        return manager

    async def test_requested_provider_is_enforced_case_insensitively(self):
        manager = self.manager_with_all_providers()

        result = await manager.search("mountains", [" PEXELS "], per_page=2)

        self.assertEqual(result["providers"], ["pexels"])
        self.assertEqual(list(result["results"]), ["pexels"])
        self.assertEqual(
            {image.source for image in result["results"]["pexels"]},
            {"Pexels"},
        )

    async def test_unknown_provider_is_not_silently_ignored(self):
        manager = self.manager_with_all_providers()

        result = await manager.search("mountains", ["pexels", "bogus"])

        self.assertIn("error", result)
        self.assertIn("bogus", result["error"])

    async def test_unconfigured_provider_is_an_error(self):
        manager = self.manager_with_all_providers()
        del manager.providers["pixabay"]

        result = await manager.search("mountains", ["pixabay"])

        self.assertIn("error", result)
        self.assertIn("not configured", result["error"])

    async def test_duplicate_provider_names_are_deduplicated(self):
        manager = self.manager_with_all_providers()

        result = await manager.search(
            "mountains", ["Pexels", "pexels", "PEXELS"], per_page=1
        )

        self.assertEqual(result["providers"], ["pexels"])
        self.assertEqual(len(result["results"]["pexels"]), 1)

    async def test_provider_searches_start_concurrently(self):
        shared = {"started": 0, "ready": asyncio.Event()}
        manager = StockImageManager()
        manager.providers = {
            "pexels": FakeProvider("Pexels", "pexels", shared, 3),
            "unsplash": FakeProvider("Unsplash", "unsplash", shared, 3),
            "pixabay": FakeProvider("Pixabay", "pixabay", shared, 3),
        }

        result = await manager.search("mountains", per_page=1)

        self.assertNotIn("error", result)
        self.assertEqual(shared["started"], 3)
        self.assertEqual(set(result["results"]), set(manager.providers))


if __name__ == "__main__":
    unittest.main()
