"""
Save screenshots from each step to see what the agent sees
"""
import asyncio
import os
from datetime import datetime

from agi_agents.qwen.qwen import QwenAgent
from arena import RunHarness


class ScreenshotSavingAgent(QwenAgent):
    """Agent that saves screenshots at each step"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screenshot_dir = f"debug_screenshots_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        print(f"📸 Saving screenshots to: {self.screenshot_dir}/")

    async def step(self, browser, state):
        # Take screenshot before step
        screenshot = await self._take_screenshot_cdp(browser)

        # Save to file
        screenshot_path = os.path.join(self.screenshot_dir, f"step_{state.step:03d}_before.jpg")
        with open(screenshot_path, 'wb') as f:
            f.write(screenshot)

        print(f"📸 Saved screenshot: {screenshot_path}")
        print(f"   URL: {browser.page.url}")
        print(f"   Viewport: {browser.width}x{browser.height}")

        # Do normal step
        result = await super().step(browser, state)

        return result


async def main():
    agent = ScreenshotSavingAgent()

    harness = RunHarness(
        agent=agent,
        tasks=['src/benchmarks/hackathon/tasks/networkin-13.json'],
        parallel=1,
        sample_count=1,
        max_steps=10,
        headless=True,
        width=1920,  # Make sure we see the full page
        height=1080,
    )

    await harness.run()
    print(f"\n✅ Screenshots saved! Check the folder to see what the agent saw.")


if __name__ == "__main__":
    asyncio.run(main())
