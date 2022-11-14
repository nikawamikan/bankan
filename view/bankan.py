from discord.ui import Modal, InputText
from discord import Interaction, InputTextStyle, File
from lib.imgen import BaseImages


class MessageInput(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            InputText(
                label="言わせたい事入力しよう",
                placeholder="私に何言わせたいんですか？",
                style=InputTextStyle.long,
                max_length=300,
                required=True,
            ),
            *args,
            **kwargs,
        )

    async def callback(self, interaction: Interaction):
        message = self.children[0].value
        file: File = await BaseImages.get_imege(key="bankan", message=message)
        await interaction.response.send_message(file=file)
