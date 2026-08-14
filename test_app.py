import os
import unittest
from unittest.mock import patch

from app import _default_allowed_hosts


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


if __name__ == "__main__":
    unittest.main()
