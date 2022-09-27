# Shuttle Tracker Tracker

Status tracker of the Shuttle Tracker. The script constantly calls the specified backend endpoint at a set time interval, and sends out a Discord alert if the API failed to respond after N failures.

## Running

Rename `template.env.txt` to `.env` and fill out the following configurable options:

| Name | Description |
| ---- | ----- |
| DISCORD_WEBHOOK_URL | Discord webhook URL for the bot to send out the message |
| PING_URL | Target URL for the bot to health check the server |
| MAX_FAIL | Maximum consecutive failures before a failure message is triggered |
| SCRAPE_INTERVAL | Time interval (seconds) for the bot to make a request to the PING_URL |

Assuming `python3` and all related packages were installed, the entry point of the program is simply `main.py`.

Or run ShuttleTrackerBot using the `pm2` proccess manager:
```
pm2 start ecosystem.config.js
```
