# USDC Auto Transfer on Base

This project automates a weekly USDC transfer from a source wallet to a target wallet on the Base Network using Python, cron, and Telegram alerts.

## Setup

1. Clone the repository
2. Create a `.env` file from `.env.example`
3. Set up a cron job to run `main.py` weekly

## Cron Example

```bash
0 10 * * 1 /usr/bin/python3 /path/to/project/src/main.py >> /path/to/project/logs/transfer.log 2>&1
```

## Environment Variables

Check `.env.example` for required variables.

## Run Locally

```bash
pip install -r requirements.txt
python src/main.py
```
