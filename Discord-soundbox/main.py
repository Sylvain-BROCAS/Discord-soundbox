from discord.ext import commands, tasks
from discord.utils import get
import discord
import asyncio
from os import listdir, chdir
from os.path import join
import json

# Install FFMPEG : http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/
# Install PyNaCl : In Cmd ==> >>>py -m pip instal PyNaCl

# Open settings
with open("settings.json", "r") as f:
    settings = json.load(f)

# Get the forbiden channels ID's
forbidden_chans = [i for i in settings["forbidden_chans"].split(",")]

client = commands.Bot(settings["prefix"])

def slct_sample(command):
    """ Select a sample of '/samples' directory  from a command """
    slctd_sample = None
    for sample in listdir(settings["samples_dir"]): # Look for the MP3 file
        if command in sample: # If file found in /samples, select it
            slctd_sample = sample
    return slctd_sample

@client.event
async def on_ready():
    print(f"Logged in as {client} ...")

@client.command()
async def play(ctx, *args, channel: discord.VoiceChannel=None):
    """
    Connect to a voice channel
    This command also handles moving the bot to different channels.

    Params:
    - *args : list of eventuals arguments passed with the 'play' key word. This must contain one and only one argument to work.
    - channel: discord.VoiceChannel [Optional]
        The channel to connect to. If a channel is not specified, an attempt to join the voice channel you are in
        will be made.
    This function was adapted from here : https://stackoverflow.com/questions/53604339/how-do-i-make-my-discord-py-bot-play-mp3-in-voice-channel
    """

    print("------------- Trying to play a sample ... -------------")

    if "soundbox" in [y.name.lower() for y in ctx.author.roles]:

        # Verifiy that only 1 argument was passed and the sample is avalaible
        if len(args) == 1 and slct_sample(args[0]) != None:
            command = args[0] # Get the command
            print(">>> The command is correct")

            audio_source =join(settings["samples_dir"],slct_sample(command))

            # Try to grab the user's voice channel
            if not channel:
                try:
                    channel = ctx.author.voice.channel
                except AttributeError:
                    # raise InvalidVoiceChannel
                    print('No channel to join. Please either specify a valid channel or join one.')
            print(">>> Channel selected : ",channel,"  - Id : ",channel.id)

            # verify that the target channel is not in forbidden channels
            if str(channel.id) in forbidden_chans:
                print(">>> Error : Don't have the permission to talk in this channel !")
                await ctx.send(">>> Error : Don't have the permission to talk in this channel !")
            else:
                vc = ctx.voice_client # Get the voice client
                print(">>> Voice client : ",vc)

        
                # If already connected to a voice channel, verify that soundbox is in the same channel than the user
                if vc:
                    if vc.channel.id == channel.id:
                        pass
                    try:
                        # Else, ove to the new channel
                        await vc.move_to(channel)
                    except asyncio.TimeoutError:
                        # raise VoiceConnectionError
                        print(f'Moving to channel: <{channel}> timed out.')
                else:
                    try:
                        # If not connected, try to connect to the user's channel
                        await channel.connect()
                    except asyncio.TimeoutError:
                        # raise VoiceConnectionError
                        print(f'Connecting to channel: <{channel}> timed out.')
                    
                conn_vc = ctx.voice_client # Get the voice client after connection
                print(">>> Conn_vc : ",conn_vc)

                #await ctx.send(f'Connected to: **{channel}**') # Display where soundbox just connected

                try:
                    conn_vc.play(discord.FFmpegPCMAudio(executable = settings["ffmpeg_path"], source = audio_source)) # Play the mp3 file
                    print(f">>> Played {command} ")
                    played_msg = await ctx.send(f">>> Played {command} ")
                    if bool(settings["delete_msg_after"]):
                        asyncio.sleep(settings["delay"]) # If the option 'delete messages' is activated, wait for a given delay
                        await ctx.message.delete() # Delete command message
                        await played_msg.delete() # Delete played song message
                except Exception as e:
                    print(f">>> Can't play the audio file ...\n--> {e}")
                    await ctx.send(">>> Can't play the audio file ...")
        else :
            print(">>> Error : Invalid command !")
            await ctx.send(">>> Error : Invalid command !\n*- Ensure you have passed only one argument.\n- If you want to get the avalaible samples, type `!samples`.*")
            pass
    else:
        print(">>> This user isn not allowed to use soundbox")
        await ctx.send(">>> You are not allowed to use Discord-soundbox")

@client.command()
async def samples(ctx):
    """ On '!samples" message, display the list of availables samples"""

    msg = ">>> __**List of available samples :**__"
    for f in listdir(settings["samples_dir"]):
        msg += f'\n\t{f[:-4]} ;' # Display each filename (remove the '.mp3')
    print(msg)
    await ctx.send(msg)

@client.command()
async def disconnect(ctx):
    """Disconnects the bot on command '!disconnect'."""
    server = ctx.message.guild.voice_client
    await server.disconnect()

client.run(settings["token"])
