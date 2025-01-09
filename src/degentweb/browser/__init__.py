from dataclasses import dataclass
from pathlib import Path

from playwright.async_api import BrowserContext, async_playwright

from degentweb.types import Fn, Fut


@dataclass
class BrowserOpts:
    """Singleton browser-related options."""

    ui: bool = False
    slow_mo_ms: int = 200


browser_opts = BrowserOpts()


async def in_default_context[T](
    user_data_dir: str | Path,
    downloads_path: str | Path,
    task: Fn[[BrowserContext], Fut[T]],
):
    """Run a task in a browser context with default configuration."""
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            args=[
                "--disable-site-isolation-trials",  # Make `eval` work
            ],
            bypass_csp=True,  # Make `eval` work
            devtools=browser_opts.ui,
            downloads_path=downloads_path,
            headless=not browser_opts.ui,
            screen={
                "width": 1920,
                "height": 1080,
            },
            slow_mo=browser_opts.slow_mo_ms if browser_opts.ui else None,
            # TODO: New contact webpage.
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            + " WebMeasure/1.0 (https://webresearch.eecs.umich.edu/overview-of-web-measurements/)",
        )
        result = await task(context)
        await context.close()
        return result
