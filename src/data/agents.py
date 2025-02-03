from pathlib import Path

SUMMARIZE_ARTICLE_AGENT = (Path(__file__).parent / "prompt.md").read_text()
