# snips-tv-programm
SNIPS TV Programm

# Credits
At the moment all data is provided by www.tvspielfilm.de

This app is a speech representation of their rss feeds located at:
- http://www.tvspielfilm.de/tv-programm/rss/jetzt.xml
- http://www.tvspielfilm.de/tv-programm/rss/heute2200.xml
- http://www.tvspielfilm.de/tv-programm/rss/heute2015.xml

# Usage
Just install the app in your snips console.

The programm responds to the intends:
- Philipp:whatsOnTV {channel|time}

Tells the show on the requested channels during the given timeslot.
If there is no channel given, or when it is explicitly requested, it will list the shows for all favorite channels.
If there is no time given, it will tell the current show

- Philipp:addFavouriteChannel {channel}

Add one channel to the favourite list. The favourites are maintained in a local file.

- Philipp:removeFavouriteChannel {channel}

Remove one channel from the favourite list. The favourites are maintained in a local file.


# Planned features (feel free to request more)
Reminders:
- Create reminders for a specific show
- Create reminders for every time a show is live

Use different data source for more specific requests:
- Next occurance of a show: When will X be shown the next time { on channel Y }
- Specific requests with free timeframes: What will air on channel X at Y o'clock next thursday

Integration with television: send and receive MQTT messages with my TV-App Interface
- rec.: what show is that? (current channel on TV)
- rec.: how long will the show take? (remaining time of show on current channel)
- send: (after question: what's running now?) -> take me to that channel

Screen integration: Send out MQTT containing the data to display stuff on a smart screen
- show favorite list
- show programm info (with details and img?)
- receive input: remove(add?) favourite
