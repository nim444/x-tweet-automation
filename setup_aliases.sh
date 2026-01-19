#!/bin/bash
# Setup shell aliases for X Tweet Automation

PROJECT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo ""
echo "Add these aliases to your ~/.zshrc:"
echo ""
echo "# X Tweet Automation"
echo "alias xw='cd $PROJECT_PATH && uv run main.py'"
echo "alias xt='cd $PROJECT_PATH && uv run manage_tweets.py'"
echo ""
echo "Then run: source ~/.zshrc"
echo ""
