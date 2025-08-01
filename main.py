import discord
import tweepy

DISCORD_BOT_TOKEN = "MTQwMDQ4NzQ2NTk0MDQyMjc2Nw.GhGGD8.itZ1h5CFoFDek8Buait7jeHC_M_mq_qx1CL75k"
TWITTER_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAACBy3QEAAAAAs50taaMduHIQC%2F2eqcwbV9QeCNM%3D0X0UXoT9RnEZ5bYb52LDK3Sj55i6NLVWL3ZMIrFJU3KiUosZvN"

TARGET_CHANNEL_ID = 1400498671531065555

twitter_client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

QUERY = "#賞金付き lang:ja -is:reply"

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user in message.mentions:
        channel = client.get_channel(TARGET_CHANNEL_ID)
        if channel is None:
            await message.channel.send("指定のチャンネルが見つかりません。")
            return

        await message.channel.send("#賞金付き のツイートを取得中…少々お待ちください。")

        try:
            tweets = twitter_client.search_recent_tweets(query=QUERY, max_results=10, tweet_fields=["author_id","created_at"])
            if not tweets.data:
                await channel.send("最近の#賞金付きツイートが見つかりませんでした。")
                return

            response = "最新の#賞金付きツイート（最大5件）:\n"
            for tweet in tweets.data[:5]:
                url = f"https://twitter.com/i/web/status/{tweet.id}"
                response += f"- {url}\n"

            await channel.send(response)

        except Exception as e:
            await channel.send(f"エラーが発生しました: {e}")

client.run(DISCORD_BOT_TOKEN)
