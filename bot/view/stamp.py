from discord.ui import select, View, Select
from discord import Interaction, InputTextStyle, File, SelectOption
from model import stamp


class StampSelect(Select):
    def __init__(self, guild_id: int) -> None:
        super().__init__(
            placeholder="スタンプを選択してね",
            options=stamp.get_select_option_by_guild_id(guild_id=guild_id)
        )

    async def callback(self, interaction: Interaction):
        value = self.values[0]
        await interaction.response.send_message(content=stamp.get_stamp(value).url)


class StampView(View):
    def __init__(self, guild_id: int):
        super().__init__()
        self.add_item(StampSelect(guild_id=guild_id))
