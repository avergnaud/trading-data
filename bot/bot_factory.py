from bot.macd_stochrsi_bot import MacdStochRsiBot
from bot.six_ema_atr_stochrsi_bot import Ema6AtrStochRsiBot
from bot.ema28_48_stochrsi_bot import Ema2848StochRsiBot
from bot.ichimoku_ema50_stochrsi_bot import IchimokuEma50StochRsiBot
from bot.sma200_600_bot import Sma200600Bot
from bot.supertrend3_ema90_stochrsi_bot import Supertrend3Ema90StochRsiBot


def get_all_bot_names():
    return [
        Ema6AtrStochRsiBot.NAME,
        Ema2848StochRsiBot.NAME,
        IchimokuEma50StochRsiBot.NAME,
        Sma200600Bot.NAME,
        Supertrend3Ema90StochRsiBot.NAME,
        MacdStochRsiBot.NAME
    ]


def get_bot_by_name(name):
    match name:
        case Ema6AtrStochRsiBot.NAME:
            return Ema6AtrStochRsiBot()
        case Ema2848StochRsiBot.NAME:
            return Ema2848StochRsiBot()
        case IchimokuEma50StochRsiBot.NAME:
            return IchimokuEma50StochRsiBot()
        case Sma200600Bot.NAME:
            return Sma200600Bot()
        case Supertrend3Ema90StochRsiBot.NAME:
            return Supertrend3Ema90StochRsiBot()
        case MacdStochRsiBot.NAME:
            return MacdStochRsiBot()
        case _:
            # Anything not matched by the above
            print(f"No bot found for {name}")
            return None


if __name__ == "__main__":
    some_bot = get_bot_by_name(Ema6AtrStochRsiBot.NAME)
    print(some_bot.description())
