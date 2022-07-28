from typing import List
from discord import Embed, Message
from Music.VulkanBot import VulkanBot
from Parallelism.ProcessInfo import ProcessInfo
from Config.Configs import VConfigs
from Config.Messages import Messages
from Music.Song import Song
from Config.Embeds import VEmbeds
from UI.Views.PlayerView import PlayerView


class MessagesController:
    def __init__(self, bot: VulkanBot) -> None:
        self.__bot = bot
        self.__previousMessages = []
        self.__configs = VConfigs()
        self.__messages = Messages()
        self.__embeds = VEmbeds()

    async def sendNowPlaying(self, processInfo: ProcessInfo, song: Song) -> None:
        # Get the lock of the playlist
        print('Entrei')
        playlistLock = processInfo.getLock()
        playlist = processInfo.getPlaylist()
        with playlistLock:
            print('A')
            if playlist.isLoopingOne():
                title = self.__messages.ONE_SONG_LOOPING
            else:
                title = self.__messages.SONG_PLAYING

            embed = self.__embeds.SONG_INFO(song.info, title)
            view = PlayerView(self.__bot)
            channel = processInfo.getTextChannel()

            await self.__deletePreviousNPMessages()
            await channel.send(embed=embed, view=view)
            self.__previousMessages.append(await self.__getSendedMessage())

    async def __deletePreviousNPMessages(self) -> None:
        for message in self.__previousMessages:
            try:
                await message.delete()
            except:
                pass
        self.__previousMessages.clear()

    async def __getSendedMessage(self) -> Message:
        stringToIdentify = 'Uploader:'
        last_messages: List[Message] = await self.__textChannel.history(limit=5).flatten()

        for message in last_messages:
            try:
                if message.author == self.__bot.user:
                    if len(message.embeds) > 0:
                        embed: Embed = message.embeds[0]
                        if len(embed.fields) > 0:
                            if embed.fields[0].name == stringToIdentify:
                                return message

            except Exception as e:
                print(f'DEVELOPER NOTE -> Error cleaning messages {e}')
                continue
