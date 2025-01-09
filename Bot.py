import discord
from discord.ext import commands
import speech_recognition as sr
import os
from pydub import AudioSegment

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and before.channel != after.channel:
        voice_channel = after.channel
        voice_client = await voice_channel.connect()

        # Записываем аудио
        audio_filename = f"{member.id}.wav"
        voice_client.start_recording(discord.Sink(encoding='wav'), record_audio, stop=lambda: False)

        def record_audio(sink, *args):
            sink.vc.stop_recording()
            sink.vc.cleanup()
            sink.audio_data(sink.get_data()).save(audio_filename)

            # Конвертируем аудио в формат, подходящий для распознавания
            audio = AudioSegment.from_wav(audio_filename)
            audio.export(audio_filename, format="wav")

            # Распознаем речь
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_filename) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language='ru-RU')
                    if 'привет' in text.lower():
                        asyncio.run_coroutine_threadsafe(member.move_to(None), bot.loop)  # Кикаем пользователя с голосового канала
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")

            # Удаляем временный аудиофайл
            os.remove(audio_filename)

bot.run('BOT_TOKEN')
