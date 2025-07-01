# Daily Journal GitHub Bot

A Python bot that automatically creates and commits daily journal entries to GitHub at a specified time each day.

## Features

- Creates daily markdown journal entries with random prompts
- Automatically commits entries to your GitHub repository
- Easy to customize with your own journal prompts

## Installation

1. Clone this repository:

```bash
git clone https://github.com/A-Shalchian/daily-journal.git
cd daily-journal
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project directory with your GitHub credentials:

```
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_USERNAME=your_github_username
GITHUB_EMAIL=your_github_email
```

To generate a GitHub Personal Access Token:
1. Go to GitHub → Settings → Developer Settings → Personal Access Tokens → Generate New Token
2. Give it a name and select the `repo` scope
3. Copy the generated token to your `.env` file

## Usage

### Run the bot immediately:

```bash
python journal_bot.py --run-now
```

### Schedule the bot to run daily at a specific time (default is 9:00 AM):

```bash
python journal_bot.py --schedule "09:00"
```

You can change the time to any 24-hour format, like "15:30" for 3:30 PM.

### Setting up as a scheduled task

#### Windows (Task Scheduler):

1. Open Task Scheduler
2. Create a new Basic Task
3. Name it "Daily Journal Bot"
4. Set trigger to Daily, at your preferred time
5. Action: Start a Program
6. Program/script: `pythonw.exe` (use full path if needed)
7. Add arguments: `C:\path\to\journal_bot.py`
8. Start in: `C:\path\to\daily-journal\`

## Customization

You can customize the journal prompts by editing the `JOURNAL_PROMPTS` list in `journal_bot.py`.

## Hosting Options

For continuous operation without keeping your computer on:

1. **GitHub Actions**: Set up a scheduled workflow
2. **Heroku**: Deploy with a scheduler add-on
3. **AWS Lambda**: Configure with CloudWatch scheduled events

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
