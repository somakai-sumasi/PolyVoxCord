import discord
from typing import List

class SelectView(discord.ui.View):
    def __init__(self, items: List[dict], callback_func):
        """抽象化したdiscord.ui.Select作成を呼び出し

        Parameters
        ----------
        items : List[dict]
            選択項目
        callback_func : function
            コールバック時呼び出し関数
        """
        super().__init__()
        self.add_item(Select(items, callback_func))


class Select(discord.ui.Select):
    def __init__(self, items: List[dict], callback_func):
        """discord.ui.Select作成を抽象化

        Parameters
        ----------
        items : List[dict]
            選択項目
        callback_func : function
            コールバック時呼び出し関数
        """

        self.callback_func = callback_func
        options = []
        for item in items:
            options.append(
                discord.SelectOption(
                    label=item["label"],
                    value=item["value"],
                    description=item["description"],
                )
            )

        super().__init__(placeholder="", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await self.callback_func(self, interaction)
