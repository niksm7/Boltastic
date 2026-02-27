"""
Boltastic MCP Server: single tool ui_analysis_tool.
Visits nova-web login and home pages, captures screenshots, sends query + images to Gemini for analysis.
"""

import os
import asyncio
import logging
import tempfile
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP
import google.generativeai as genai
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("boltastic-ui-analysis-mcp")

logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

LOGIN_URL = "https://niksm7.github.io/nova-web/login"
HOME_URL = "https://niksm7.github.io/nova-web/"


def _get_gemini_model():
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Set GOOGLE_API_KEY or GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


async def _screenshot_url(url: str, viewport: dict) -> Optional[bytes]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page(viewport=viewport)
            await page.goto(url, wait_until="networkidle", timeout=15000)
            await asyncio.sleep(1)
            shot = await page.screenshot(full_page=True)
            return shot
        finally:
            await browser.close()
    return None


def _call_gemini(prompt: str, image_paths: list) -> str:
    model = _get_gemini_model()
    parts = [prompt]
    for path in image_paths:
        parts.append(genai.upload_file(path, mime_type="image/png"))
    response = model.generate_content(parts)
    return (response.text or "").strip() or "No analysis returned from the model."


@mcp.tool()
async def ui_analysis_tool(query_or_issue: str) -> dict:
    """
    Analyze the Nova Web UI for a given query or issue.
    Visits the login and home pages, captures screenshots, and uses Gemini to summarize
    what the issue could be and possible fixes.
    """
    query_or_issue = (query_or_issue or "").strip()
    if not query_or_issue:
        return {
            "success": False,
            "error": "query_or_issue is required",
            "summary": None,
            "possible_fix": None,
        }

    screenshots = []
    viewport = {"width": 1280, "height": 720}

    try:
        login_bytes = await _screenshot_url(LOGIN_URL, viewport)
        if login_bytes:
            screenshots.append(("Login page", login_bytes))
        home_bytes = await _screenshot_url(HOME_URL, viewport)
        if home_bytes:
            screenshots.append(("Home page", home_bytes))
    except Exception as e:
        logger.exception("Screenshot failed")
        return {
            "success": False,
            "error": str(e),
            "summary": None,
            "possible_fix": None,
        }

    if not screenshots:
        return {
            "success": False,
            "error": "Could not capture any screenshots",
            "summary": None,
            "possible_fix": None,
        }

    try:
        _get_gemini_model()
    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
            "summary": None,
            "possible_fix": None,
        }

    prompt = (
        f"User query or reported issue:\n{query_or_issue}\n\n"
        "The following images are screenshots of the Nova Web app (login page and main page). "
        "Analyze the UI in these screenshots in the context of the user's query/issue. "
        "Respond with:\n"
        "1. **Summary**: What the issue could be (or what you observe).\n"
        "2. **Possible fix**: Concrete steps or changes to fix or address the issue.\n"
        "Keep the response concise and actionable."
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        image_paths = []
        for i, (label, img_bytes) in enumerate(screenshots):
            path = Path(tmpdir) / f"screenshot_{i}.png"
            path.write_bytes(img_bytes)
            image_paths.append(str(path))
        try:
            loop = asyncio.get_event_loop()
            text = await loop.run_in_executor(
                None, lambda: _call_gemini(prompt, image_paths)
            )
            return {
                "success": True,
                "error": None,
                "summary": text,
                "possible_fix": None,
                "pages_analyzed": [label for label, _ in screenshots],
            }
        except Exception as e:
            logger.exception("Gemini call failed")
            return {
                "success": False,
                "error": str(e),
                "summary": None,
                "possible_fix": None,
            }


if __name__ == "__main__":
    logger.info(f"🚀 MCP server started on port {os.getenv('PORT', 8080)}")
    asyncio.run(
        mcp.run_async(
            transport="http",
            host="0.0.0.0",
            port=os.getenv("PORT", 8080),
        )
    )