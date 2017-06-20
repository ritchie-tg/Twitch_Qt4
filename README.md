# Twitch_Qt4 (v0.2)
**Notice: Twitch_Qt4 is currently in early developemnt. But if you wish to test it, I'd appreciate your feedback.**

## Description:
Twitch_Qt4 is a desktop application developed for *Linux*, using *Python 2* and *PyQt4*, that assists with the viewing of live streams that are hosted on Twitch.tv. This app will pull a list of the streams you follow using Twitch's official Kraken API, then interface *streamlink* to your preferred media player such as *VLC*. Twitch_Qt4 is a lightweight application that is intended to avoid the resource usage or connection issues that can otherwise occur while watching Twitch.tv within a browser.
<hr>
<p align="center">
  <img src="https://github.com/datguy-dev/Twitch_Qt4/blob/master/assets/desc.png" title="Main Window">
</p>
<hr>

## How To:
### 1. Install Dependencies:
  * [streamlink](https://streamlink.github.io/install.html)
  * [VLC](https://wiki.videolan.org/Documentation:Installing_VLC/)
  * Python2 (no additional packages needed)
  * PyQt4 (python-qt4)
  
### 2. Get Twitch.tv Client-ID and Oauth keys:
   * [Client ID](https://blog.twitch.tv/client-id-required-for-kraken-api-calls-afbb8e95f843)
   * [Oauth /w **user_read AND chat_login** permissions](http://twitchapps.com/tokengen/)
   * Optional: Install Chatty IRC client.
      1. [Download Chatty](http://chatty.github.io/#download)
      2. Extract the archive and move the files to the chatty folder in Twitch_Qt4/chatty
      (If doesn't load, update & use Java 8 JRE or later. Login and authorize via Chatty)
<p align="center">
  <img src="https://github.com/datguy-dev/Twitch_Qt4/blob/master/assets/chatty.png" title="Main Window">
</p>      
   
### 3. Run: python2 /path/to/Twitch_Qt4.py

### 4. Open the options and enter your Client-ID and Oauth tokens
   - Quality: Select the desired quality of the stream.
   - Cache: Number of seconds to cache' the stream. This can provide a more reliable stream on slower connections.
   - Height Adjust: Enter a number to set the vertical length of the app window. (use negatives for smaller.)
   - Notifications: If ticked, pops up like Notify-Send are used to announce changes to the list of live streamers available.
   - Chatty: Open a Chatty IRC window or tab when launching a stream. This is configured to run in a single instance mode i.e one window, many tabs. Requires additional installation steps.

<hr>

<p align="center">
  <img src="https://github.com/datguy-dev/Twitch_Qt4/blob/master/assets/optionsv2.png" title="Options Window">
</p>

<hr>
