import nltk
from discord.ext import commands
from nltk.sentiment import SentimentIntensityAnalyzer

from Plugin import AutomataPlugin

nltk.downloader.download("vader_lexicon")


class SentimentAnalysis(AutomataPlugin):
    """NLTK Sentiment Analyzer"""

    sia = SentimentIntensityAnalyzer()

    @commands.command()
    async def sentiment(self, ctx, *, argument=None):
        """Replies with the sentiment of the sentence"""

        message_to_reply_to = ctx.message
        message_to_be_scored = argument

        if argument is None and ctx.message.reference is None:
            historical_messages = await ctx.channel.history(limit=2).flatten()
            message_to_reply_to = historical_messages[1]
            message_to_be_scored = message_to_reply_to.content

        elif argument is None and ctx.message.reference is not None:
            message_to_reply_to = await ctx.fetch_message(
                ctx.message.reference.message_id
            )
            message_to_be_scored = message_to_reply_to.content

        sentiment_text = ""
        output_template = "<@{author}>: This text is **{sentiment_text}**."
        compound_score = self.sia.polarity_scores(message_to_be_scored)["compound"]
        absolute_score = abs(compound_score)

        if absolute_score == 0:
            sentiment_text = "absolutely neutral"
        elif 0.01 < absolute_score < 0.25:
            sentiment_text = "slightly "
        elif 0.25 <= absolute_score < 0.50:
            sentiment_text = "somewhat "
        elif 0.50 <= absolute_score < 0.75:
            sentiment_text = ""
        elif 0.75 <= absolute_score < 0.90:
            sentiment_text = "mostly "
        elif 0.90 <= absolute_score < 1.00:
            sentiment_text = "overwhelmingly "
        elif absolute_score == 1.00:
            sentiment_text = "absolutely "

        if compound_score < 0:
            sentiment_text += "negative"
        elif compound_score > 0:
            sentiment_text += "positive"

        output = output_template.format(
            author=ctx.message.author.id, sentiment_text=sentiment_text
        )
        await message_to_reply_to.reply(output)
