#!/usr/bin/env python3
"""
Daily Journal Bot - Automatically creates and commits daily journal entries to GitHub.
"""
import os
import datetime
import logging
from pathlib import Path
import git
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("journal_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("journal_bot")

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_EMAIL = os.getenv("GITHUB_EMAIL")
REPO_PATH = os.path.dirname(os.path.abspath(__file__))

JOURNAL_PROMPTS = [
    "What went well today?",
    "What could have gone better?",
    "What am I grateful for today?",
    "What did I learn today?",
    "What's one thing I want to focus on tomorrow?",
    "What was the best part of my day?",
    "What challenged me today?",
    "How did I take care of myself today?",
    "What's something I accomplished today?",
    "What's something I'm looking forward to?"
]

def setup_repo():
    """Initialize the repository if it doesn't exist."""
    try:
        if not os.path.isdir(os.path.join(REPO_PATH, '.git')):
            logger.info("Initializing git repository...")
            repo = git.Repo.init(REPO_PATH)
            
            with repo.config_writer() as git_config:
                git_config.set_value('user', 'name', GITHUB_USERNAME)
                git_config.set_value('user', 'email', GITHUB_EMAIL)
                
            readme_path = os.path.join(REPO_PATH, 'README.md')
            if not os.path.exists(readme_path):
                with open(readme_path, 'w') as f:
                    f.write("# Daily Journal\n\nThis repository contains my daily journal entries, automatically committed by my journal bot.")
                repo.git.add('README.md')
                repo.git.commit('-m', 'Initial commit: Add README')
                logger.info("Created README and made initial commit")
        
        return git.Repo(REPO_PATH)
    except Exception as e:
        logger.error(f"Error setting up repository: {e}")
        return None

def create_journal_entry():
    """Create a new journal entry for today."""
    today = datetime.datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    year_str = today.strftime('%Y')
    month_name = today.strftime('%B').lower()
    month_year = f"{month_name}-{year_str}"  
    day_number = today.strftime('%d')
    
    journals_dir = os.path.join(REPO_PATH, 'journals')
    if not os.path.exists(journals_dir):
        os.makedirs(journals_dir)
        logger.info(f"Created journals directory at {journals_dir}")
    
    # Create month-year directory 
    month_dir = os.path.join(journals_dir, month_year)
    if not os.path.exists(month_dir):
        os.makedirs(month_dir)
        logger.info(f"Created month directory at {month_dir}")
    
    # Create day-specific directory
    day_dir = os.path.join(month_dir, day_number)
    if not os.path.exists(day_dir):
        os.makedirs(day_dir)
        logger.info(f"Created day directory at {day_dir}")
    
    file_path = os.path.join(day_dir, f"{date_str}.md")
    
    if os.path.exists(file_path) and os.path.getmtime(file_path) >= today.replace(hour=0, minute=0, second=0, microsecond=0).timestamp():
        logger.info(f"Journal entry for {date_str} already exists. Skipping creation.")
        return file_path
    
    # Ask for user input instead of using random prompts
    print("\n===== Journal Entry Prompts =====")
    print("You can choose from the following prompts or enter your own:")
    for i, prompt in enumerate(JOURNAL_PROMPTS, 1):
        print(f"{i}. {prompt}")
    
    print("\nEnter up to 3 prompt numbers or type your own prompts.")
    print("Enter 'done' when finished.")
    
    selected_prompts = []
    count = 1
    
    while count <= 3:
        user_input = input(f"Prompt {count} (or 'done' to finish): ").strip()
        
        if user_input.lower() == 'done':
            break
        
        if user_input.isdigit() and 1 <= int(user_input) <= len(JOURNAL_PROMPTS):
            selected_prompts.append(JOURNAL_PROMPTS[int(user_input) - 1])
            count += 1
        elif user_input:
            selected_prompts.append(user_input)
            count += 1
    
    content = f"# Journal Entry: {date_str}\n\n"
    
    for prompt in selected_prompts:
        content += f"## {prompt}\n\n_Write your thoughts here..._\n\n"
    
    content += f"\nCreated automatically by Journal Bot on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    logger.info(f"Created journal entry: {file_path}")
    return file_path

def commit_to_github():
    """Commit the latest journal entry to GitHub."""
    try:
        repo = setup_repo()
        if not repo:
            return False
        
        entry_path = create_journal_entry()
        
        repo_path = Path(repo.working_dir)
        relative_path = Path(entry_path).relative_to(repo_path)
        
        repo.git.add(str(relative_path))
        
        if not repo.git.diff('--staged'):
            logger.info("No changes to commit")
            return False
        
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        commit_message = f"Add journal entry for {today}"
        repo.git.commit('-m', commit_message)
        
        # Push to remote if configured
        if "origin" in [remote.name for remote in repo.remotes]:
            logger.info("Pushing changes to remote repository...")
            repo.git.push('origin', 'main')
        else:
            logger.info("No remote repository configured. Skipping push.")
            logger.info("To push manually, set up a remote repository and run: git push -u origin main")
        
        logger.info(f"Successfully committed journal entry for {today}")
        return True
    except Exception as e:
        logger.error(f"Error committing to GitHub: {e}")
        return False

def run_journal_bot():
    """Main function to execute the journal bot."""
    logger.info("Running journal bot...")
    success = commit_to_github()
    if success:
        logger.info("Journal bot completed successfully!")
    else:
        logger.error("Journal bot failed to complete.")


if __name__ == "__main__":
    run_journal_bot()
