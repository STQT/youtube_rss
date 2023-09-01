import os

from dotenv import load_dotenv

load_dotenv()

YOUTUBE_RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id="

BOT_DEBUG = os.getenv("BOT_DEBUG", default=False)
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CRON_TASK_INTERVAL_MINUTES = os.getenv("CRON_TASK_INTERVAL_MINUTES")
if BOT_TOKEN is False:
    import sentry_sdk

    SENTRY_DSN = os.getenv("SENTRY_DSN")
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[],
    )
