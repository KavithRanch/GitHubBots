import asyncio
import logging
from bots.leetcode_tracker import setup_bot as setup_leetcode_tracker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    try:
        logger.info("Starting bot manager...")
        # Initialize bots by storing their respective clients and tokens
        leetcode_client, leetcode_token = setup_leetcode_tracker()

        # Run all bots concurrently loop.create_task(bot_client.start(bot_token))
        loop = asyncio.get_event_loop()
        loop.create_task(leetcode_client.start(leetcode_token))
        logger.info("LeetCode tracker bot started successfully.")
        loop.run_forever()
    except Exception as e:
        logger.error("An error occurred in the bot manager", exc_info=True)
    finally:
        logger.info("Shutting down bot manager...")


if __name__ == "__main__":
    main()

