# Discord-soundbox
A soundbox bot for discord. You just have to create your samples database, and it's *almost* ready to work. Here is the procedure to setup your soundbox.

# Requirements :

- Language :
  - python 3.X
 
- Modules :
  - discord
  - PyNaCl (Used by discord.py btu not built-in, so you have to install manually)
  - asyncio (built-in)
  - os (built-in)
  - json (built-in)
 
- Installations :
  - discord : In CMD, type : `py -m pip install discord`
  - PyNaCl : In CMD, type : `py -m pip install PyNaCl`
  - You have to install ffmpeg following [this tutorial](http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/).
  - Create a bot account and invite it on your serveur following this  [great tutorial](https://www.writebots.com/discord-bot-token/).
    - The bot needs folloing permissions : `view channels, connect, speak, send messages, manage messages`


# Settings :
  Once you've created and invited your bot on your serveur, setup the discord-soundbox. It's the purpose of the 'settings.json' file, open it and change parameters to personnalise the bot.
**__Parameters :__**
- samples_dir : Put here the directory where your samples (.mp3 format !) are located. ⚠️ If you forgot to create this directory, an error will occure !
- prefix : You can change here the prefix before bot commands. Default prefix is '!' (Example : `!samples`).
- ffmpeg_path : Put here the path to the 'ffmpeg.exe' file you downloaded earlier. ⚠️ Without this information, the discord-soundbox is unable to find the .exe by itself. So an error will occure !
- token : Put here your bot's token.
- forbidden chans : Put here all the ID's of forbidden channels (separated by a ','). Then the soundbox will not be authorised to speak in these voice channels.

# Now you can use it !

⚠️ You have to be connected to a voice channel (that musn't be in forbidden channels ^^) to use the soundbox, else you will get an error !

🔊 You have to create a file to store your samples database. The samples must be in '.mp3' format and have simle names. The 'sample name' i talk about later in this document is the filename of the sample without th '.mp3'. It will be used to select the sample you want to play.

**__Commands :__**
- `!play sample_name` : discord-soundbox connect to your voice_channel and play the selected sample.
- `!samples` : If you don't remember the available samples, you can show their list with this command.
  
