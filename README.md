# Twitter Auto-Follow Script

## Overview

This script was created to automatically manage followers on Twitter. It follows the followers of targeted accounts, unfollows users who don't follow back, and handles errors such as hitting Twitter's rate limits. The script runs within a specified time frame each day, and logs its activity for monitoring purposes.

## Disclaimer

**Note:** This script was coded when I was around 14 or 15 years old. It is far from perfect and might not run anymore due to changes in Twitter's API and policies. Additionally, I discourage you from using this script as it goes against Twitter's guidelines and could result in your account being penalized.

## Background Story

When I was young, I managed a Telegram channel where I posted Amazon offers daily, using a bot I coded. To expand my reach, I wanted to use Twitter as another communication channel to promote these offers. However, my profile had very few followers, so I created this script to attract followers by following the followers of similar accounts that published offers. The idea was to get their attention, have them follow my page, and then unfollow them.

## Script Functionality

### Features
- **Network Check:** Ensures there is an active network connection before starting.
- **Follower Management:** 
  - Follows followers of specified target accounts.
  - Unfollows users who don't follow back.
  - Unfollows all users (excluding whitelisted ones).
- **Error Handling:** Manages rate limits and other potential errors.
- **Logging:** Logs activities and errors for monitoring purposes.
- **Configurable Working Hours:** Runs within a specified time frame each day.

### How It Works
1. **Network Check:** The script first checks if there is a network connection.
2. **Configuration:** Loads configuration settings from a `config.json` file.
3. **Authorization:** Authenticates with Twitter using credentials provided in the config file.
4. **Main Loop:** Runs continuously within the specified working hours, performing follow and unfollow actions.

## Configuration

The script requires a `config.json` file with the following structure:

```json
{
    "auth": {
        "screen_name": "your_twitter_handle",
        "CONSUMER_KEY": "your_consumer_key",
        "CONSUMER_SECRET": "your_consumer_secret",
        "ACCESS_TOKEN": "your_access_token",
        "ACCESS_SECRET": "your_access_secret"
    },
    "debug": true,
    "time_zone": "your_time_zone",
    "start_time": "09:00",
    "end_time": "17:00",
    "targets": ["target_account_1", "target_account_2"],
    "whitelisted_accounts": ["whitelisted_account_1", "whitelisted_account_2"],
    "blacklisted": ["blacklisted_account_1", "blacklisted_account_2"]
}
```

### Key Configuration Fields
- **auth:** Contains Twitter API credentials.
- **debug:** Enables or disables debug mode.
- **time_zone:** Specifies the time zone for working hours.
- **start_time and end_time:** Define the working hours.
- **targets:** List of Twitter accounts whose followers you want to follow.
- **whitelisted_accounts:** Accounts that should never be unfollowed.
- **blacklisted:** Accounts that should never be followed.

## Important Note

This script was a quick hack to gain followers and is not a good practice. Using such scripts can lead to your Twitter account being suspended or banned. Engage with your audience in a genuine and meaningful way instead of using automated methods to inflate your follower count.

## Running the Script

Ensure you have the required Python libraries installed, such as `tweepy` and `pytz`. Run the script using Python:

```bash
python crazy-twitter.py
```

## Conclusion

This script was an attempt to solve a problem using automation, but it is not an ideal or ethical solution. If you are looking to grow your social media presence, focus on creating valuable content and engaging with your audience genuinely.