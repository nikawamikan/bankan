from discord.ui import Modal, InputText
from discord import Interaction, InputTextStyle, File, Member, Role
from model import image
from typing import Union

Colors = image.Colors


class MessageInput(Modal):
    def __init__(self, base_image: image.BaseImages, mention: Union[Member, Role], * args, **kwargs) -> None:
        super().__init__(
            InputText(
                label="言わせたい事入力しよう",
                placeholder="私に何言わせたいんですか？",
                style=InputTextStyle.long,
                max_length=200,
                required=True,
            ),
            *args,
            **kwargs,
        )
        self.base_image = base_image
        self.mention = mention

    async def callback(self, interaction: Interaction):
        message = self.children[0].value
        self.base_image.message = message
        file: File = await self.base_image.get_discord_file()
        if self.mention == None:
            await interaction.response.send_message(file=file)
        else:
            await interaction.response.send_message(content=self.mention.mention, file=file)
