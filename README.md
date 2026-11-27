# negative
An Open-Source Minecraft Launcher alternative to TLauncher/SKLauncher

You can play Minecraft for free with this, as we provide the option to start Minecraft in offline-mode without authentication.  
You can play in singleplayer, or join "cracked" servers (servers that have specifically disabled online-mode authentication)

## How to run
clone  
`git clone https://github.com/utkrstht/negative`  

get in folder  
`cd negative`  

install deps (you need python 3.11+)
`pip install -r requirements.txt`

run  
`python src/main.py`

## How to play
You can go into the Releases tab and select a binary for your operating system (Linux and Windows builds available)  
You load into an offline-mode account.

The launcher can launch almost all Minecraft versions.

## Launcher information
The current game directory is named `.minecrafttest` (`%APPDATA%/.minecrafttest` for windows, `/home/<user>/.minecrafttest` for linux) so as to not corrupt my real minecraft installation.  

You can find logs for the launcher in `.negative/logs`, the launcher log is `launcher.log` and minecraft log is `minecraft.log`  

The Java runtimes are in `.negative/java/<java_ver>`. If the manifest does not provide a Java version, we default to using Java 8 because that only happens in pretty old versions. If we are unable to get just the JRE, we download the entire JDK. Adoptium (our default Java vendor) does not have native builds for MacOS, so we switch vendors if the user is on MacOS

## User Interfaces
GUI interface is WIP! coming soon!

A TUI is planned.

## Contributing
Good luck