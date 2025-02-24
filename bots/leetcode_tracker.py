from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import requests, os, discord
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("LEETCODE_BOT_TOKEN")
if not TOKEN:
    print("ERROR: LEETCODE_BOT_TOKEN is not set or is invalid.")
else:
    print(f"Token successfully loaded: {TOKEN[:5]}...")
CHANNEL_ID = os.getenv("LEETCODE_CHANNEL_ID")

client = discord.Client(intents=discord.Intents.default())
scheduler = AsyncIOScheduler()


def fetch_daily_problem():
    '''
    Fetches LeetCode daily problem
    :return: Message to place in chat
    '''
    logger.info("Fetching the daily LeetCode problem...")
    url = "https://leetcode.com/graphql"
    query = {
        "query": """
            query dailyCodingChallenge {
              activeDailyCodingChallengeQuestion {
                date
                question {
                  title
                  difficulty
                }
              }
            }
            """
    }
    post_response = requests.post(url, json=query)
    print(post_response.text)
    if post_response.ok:
        res_json = post_response.json()
        daily_challenge = res_json['data']['activeDailyCodingChallengeQuestion']
        problem_name = daily_challenge['question']['title']
        problem_dif= daily_challenge['question']['difficulty']
        problem_date = datetime.strptime(daily_challenge['date'], "%Y-%m-%d").strftime("%b %d, %Y")
        logger.info(f"Successfully fetched daily problem: {problem_name}")
        return f"**---------- ({str.upper(problem_dif)}) {problem_name} | {problem_date} ----------**"


# "async" since Discord API operations must be asynchronous
async def post_daily_problem():
    '''
    Posts message in discord channel
    :return: None
    '''

    logger.info("Preparing to post the daily problem...")
    # Setting channel and message to send
    channel = client.get_channel(int(CHANNEL_ID))
    message = fetch_daily_problem()
    await channel.send(message)
    logger.info("Successfully posted the daily problem to Discord.")
    await client.close()


def setup_bot():
    '''
    Sets up bot by scheduling its tasks and defining events
    :return: client and token value
    '''

    logger.info("Setting up the LeetCode tracker bot...")

    # Schedule message for 5AM
    @scheduler.scheduled_job('cron', hour='1', minute='0')
    async def scheduled_task():
        logger.info("Scheduled task triggered: Fetching and posting daily problem...")
        await post_daily_problem()

    @client.event
    # Needed to notify when Bot has logged into discord
    async def on_ready():
        # Print when connected and start the scheduler above
        print(f"Logged in as {client.user}")
        print(f"Connected to Discord channel ID: {CHANNEL_ID}")
        scheduler.start()

    return client, TOKEN