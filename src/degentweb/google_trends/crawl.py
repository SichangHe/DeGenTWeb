"""Crawl Google Trends.
Reference:
<https://github.com/dballinari/GoogleTrends-Scraper/blob/5845c481b47db0ea584b06dcbd1bbd80b4dcd63d/src/GoogleTrendsScraper.py>
"""

import asyncio
import os
import traceback
from dataclasses import dataclass
from datetime import datetime
from typing import Final

from playwright.async_api import BrowserContext

from degentweb import include_file
from degentweb.browser import browser_opts, in_default_context
from degentweb.google_trends import SEARCH_REGIONS, SEARCH_TERM_CATEGORIES
from degentweb.logging import init_logger_w_env_level

BASE_URL: Final = "https://trends.google.com/trends/explore"
DATE_FORMAT: Final = "%Y-%m-%d"
USER_DATA_DIR: Final = "target/browser/user_data"
DOWNLOADS_PATH: Final = "target/browser/downloads"

logger = init_logger_w_env_level(__name__)


def create_url(
    start: datetime,
    end: datetime,
    region: str | None = None,
    category: int | None = None,
):
    """URL for Google Trends."""
    geo = f"geo={region}&" if region is not None else ""
    cat = f"cat={category}&" if category is not None else ""
    date = f"date={start.strftime(DATE_FORMAT)}%20{end.strftime(DATE_FORMAT)}"
    return f"{BASE_URL}?{cat}{date}&{geo}"


@dataclass
class SearchEntry:
    """Search topic or query entry of Google Trends."""

    name: str
    """Name of the search topic or query text."""
    classification: str | None
    """Classification of search topic (e.g. "Company"), or null for query."""
    interest: int
    """Relative interest score from 1 to 100."""
    href: str
    """URL to the entry's Google Trends page."""


async def crawl_trends(url: str, context: BrowserContext):
    """Crawl Google Trends at `url` for topics and queries."""
    page = await context.new_page()
    try:
        await page.goto(url, wait_until="networkidle")
        topics_and_queries_or_err: dict[str, str | list] = await page.evaluate(
            include_file(__file__, "inject.js")
        )

        if (err := topics_and_queries_or_err.get("err")) is not None:
            assert type(err) is str
            raise Exception(err)
        topics, queries = (
            topics_and_queries_or_err["topics"],
            topics_and_queries_or_err["queries"],
        )
        assert type(topics) is list, topics_and_queries_or_err
        assert type(queries) is list, topics_and_queries_or_err
        topics_entries = [SearchEntry(**topic) for topic in topics]
        queries_entries = [SearchEntry(**query) for query in queries]
        await page.close()
    except Exception as err:
        if browser_opts.ui:
            await page.pause()
        raise err
    await asyncio.sleep(10)
    return topics_entries, queries_entries


async def do_main(context: BrowserContext):
    region_category_pairs = [
        (region, category)
        for region in SEARCH_REGIONS
        for category in [k for k in SEARCH_TERM_CATEGORIES.keys() if k != 0]
    ]
    failed_region_category: dict[tuple[str, int], tuple[Exception, str]] = {}
    # NOTE: Currently, the date range is hardcoded to be 2024.
    start = datetime(2024, 1, 1)
    end = datetime(2024, 12, 31)
    for region, category in region_category_pairs:
        try:
            url = create_url(start, end, region, category)
            topics, queries = await crawl_trends(url, context)
            # TODO: Save to database instead.
            print(
                f"region={region}, category={category}, topics={topics}, queries={queries}"
            )
        except Exception as err:
            stack_trace = traceback.format_exc()
            logger.error(
                f"Failed: region={region}, category={category}, err={err}, stack_trace={stack_trace}"
            )
            failed_region_category[(region, category)] = (err, stack_trace)
    if failed_region_category:
        logger.error(f"Failed region-category pairs: {failed_region_category}")
    # TODO: Recurs on topics href to find more topics & queries.


async def main():
    # TODO: Parse args for opts.
    # browser_opts.ui = True
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    os.makedirs(DOWNLOADS_PATH, exist_ok=True)
    await in_default_context(USER_DATA_DIR, DOWNLOADS_PATH, do_main)


asyncio.run(main()) if __name__ == "__main__" else None
