class ImageSearchMcp < Formula
  desc "MCP image search server for Unsplash, Pexels, and Pixabay"
  homepage "https://github.com/serbyte-development/image-search-mcp"
  url "https://github.com/serbyte-development/image-search-mcp/archive/693b459273727e9b2f30aa00d3bc5779099a5e08.tar.gz"
  version "1.0.0"
  sha256 "dc49fe6ad5729e9836ca80c6cca06b2487b3354c299c1c2aadd909a926c643cf"
  license "MIT"

  depends_on "pipx"

  def install
    pipx = Formula["pipx"].opt_bin/"pipx"
    (bin/"image-search-mcp").write <<~SH
      #!/bin/bash
      export PIPX_DEFAULT_BACKEND=pip
      exec "#{pipx}" run --quiet --spec "git+https://github.com/serbyte-development/image-search-mcp.git@693b459273727e9b2f30aa00d3bc5779099a5e08" image-search-mcp "$@"
    SH
  end

  test do
    assert_predicate bin/"image-search-mcp", :executable?
    assert_match "pipx", (bin/"image-search-mcp").read
  end
end
