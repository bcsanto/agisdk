"""
Debug script to see agent's thinking process
"""
import asyncio
import json

from agi_agents.qwen.qwen import QwenAgent
from arena import RunHarness


class DebugQwenAgent(QwenAgent):
    """QwenAgent with debug logging"""

    async def step(self, browser, state):
        """Execute one agent step with debug output"""
        print("\n" + "="*80)
        print(f"STEP {state.step}")
        print("="*80)

        # Call parent step but capture messages
        screenshot = await self._take_screenshot_cdp(browser)
        messages = await self.build_messages(state, screenshot)

        print("\n📨 MESSAGES SENT TO MODEL:")
        print("-"*80)
        for i, msg in enumerate(messages):
            print(f"\n[Message {i}] Role: {msg['role']}")
            content = msg.get('content', '')
            if isinstance(content, str):
                # Truncate long content
                if len(content) > 500:
                    print(f"Content (truncated): {content[:500]}...")
                else:
                    print(f"Content: {content}")
            elif isinstance(content, list):
                print(f"Content: [Mixed content with {len(content)} parts]")
                for part in content:
                    if isinstance(part, dict):
                        if part.get('type') == 'image_url':
                            print("  - Image")
                        elif part.get('type') == 'text':
                            print(f"  - Text: {part.get('text', '')[:100]}")

        # Now call parent to get actual result
        original_state = await super().step(browser, state)

        print("\n🤖 AGENT RESPONSE:")
        print("-"*80)
        if state.messages and state.messages[-1].get('role') == 'assistant':
            print(state.messages[-1].get('content', ''))

        print("\n✅ TOOL RESULTS:")
        print("-"*80)
        if len(state.messages) >= 2 and state.messages[-1].get('role') == 'user':
            print(state.messages[-1].get('content', ''))

        print("\n" + "="*80 + "\n")

        return original_state


async def main():
    # Create debug agent
    agent = DebugQwenAgent()

    # Run just the networkin-13 task
    harness = RunHarness(
        agent=agent,
        tasks=['src/benchmarks/hackathon/tasks/networkin-13.json'],
        parallel=1,
        sample_count=1,
        max_steps=15,  # Limit steps for debugging
        headless=False,  # Watch the browser!
    )

    print("\n🔍 STARTING DEBUG SESSION")
    print("Watch the browser window to see what the agent is doing")
    print("="*80 + "\n")

    await harness.run()


if __name__ == "__main__":
    asyncio.run(main())
