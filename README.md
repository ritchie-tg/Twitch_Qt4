# Twitch_Qt4 (v0.1)
**Notice: Twitch_Qt4 is currently in a pre-alpha stage. It is missing features, expect bugs, thecode is not fully commented, etc. But if you wish to test it, we'd be glad to hear your feedback.**

## Description:
Twitch_Qt4 is a desktop application developed for *Linux*, using *Python 2* and *PyQt4*, that assists with the viewing of live streams that are hosted on Twitch.tv. This app will pull a list of the streams you follow using Twitch's offical Kraken API, then interface *streamlink* to your preferred media player such as *VLC*. Twitch_Qt4 is a lightweight application that is intended to avoid the resource usage or connection issues that can otherwise occur while watching Twitch.tv within a browser.

<hr>

<p align="center">
  <img src="https://github.com/datguy-dev/Twitch_Qt4/blob/master/assets/UI.png" title="Main Window">
</p>

<hr>

## How To:
### 1. Install Dependencies:
  * streamlink (ex: sudo apt-get install streamlink or pacman -S streamlink)
  * VLC (see streamLib.Livestreamer() to customize the player or change abs. path)
  * Python2 (imports should all be built-in packages)
  * PyQt4
  
### 2. Get Twitch.tv Client-ID and Oauth keys:
   * [Client ID](https://blog.twitch.tv/client-id-required-for-kraken-api-calls-afbb8e95f843)
   * [Oauth /w **user_read** permissions](http://twitchapps.com/tokengen/)
   
### 3. Run: python2 /path/to/Twitch_Qt4-master.py

### 4. Open the options and enter your Client-ID and Oauth
   - Quality: Select the desired quality of the stream.
   - Cache: Number of seconds to catch the stream. This can provide a more reliable stream on slower connections.
   - Height Adjust: Enter a number to set the hegith of the app window. (negative for smaller)

<hr>

<p align="center">
  <img src="https://github.com/datguy-dev/Twitch_Qt4/blob/master/assets/options.png" title="Options Window">
</p>

<hr>

Thanks for checking out my first repo and my first attempt at a GUI in Python...
