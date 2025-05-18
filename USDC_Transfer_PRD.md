
# PRD: Automated Weekly USDC Transfer on Base Network

## Overview

This product automates the transfer of USDC from a source wallet to a target wallet on the Base Network on a weekly schedule using a system cron job. It ensures secure execution, robust error handling, proper gas and balance validation, and alerts via Telegram bot on success or failure.

---

## Objective

- Automatically send a fixed amount of USDC from one wallet to another once per week.
- Ensure safe, repeatable execution via Linux cron.
- Provide operational transparency through logging and Telegram alerts.
- Facilitate future enhancements like batching or on-chain automation.

---

## Features

### 1. Scheduled Execution

- **Frequency**: Weekly
- **Tool**: Linux system `cron`
- **Example Schedule**: Every Monday at 10:00 AM

```bash
0 10 * * 1 /usr/bin/python3 /path/to/main.py >> /path/to/logs/transfer.log 2>&1
```

### 2. Blockchain Interaction

- **Network**: Base Mainnet (an Ethereum L2 built on the OP Stack)
- **Token**: USDC (ERC20-compliant)
- **USDC Contract Address**: `0xD9AAE9C67e9FCf4C3c118e7Dd048E0a8F1C0eCf2`
- **Smart Contract Methods Used**:
  - `transfer(address to, uint256 amount)`
  - `balanceOf(address owner)`
  - `decimals()`

### 3. Private Key Management

- The private key used to sign transactions must be securely stored:
  - `.env` for local/testing environments
  - Vault-based solution for production (e.g., AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault)
- **Never hardcode private keys** in the codebase.

### 4. Gas Fee Handling

- ETH (on Base) is required to cover gas fees.
- The script will:
  - Check ETH balance before attempting a transaction.
  - Abort if ETH balance is below a threshold (e.g., 0.0002 ETH).
  - Estimate gas using `w3.eth.gas_price` and manual limits.

### 5. Telegram Alerting

- On every run, the script will:
  - Send a success or failure message to a configured Telegram chat.
  - Include transaction hash or error details.
- Uses Telegram Bot API.
- Required `.env` variables:
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`

---

## Technical Stack

### Runtime

- Python 3.10+

### Python Dependencies

- `web3` – Blockchain interaction
- `python-dotenv` – Load `.env` files
- `requests` – Send Telegram messages
- `logging` – Log execution and errors

### Infrastructure

- Runs via `cron` on Linux server or Docker container.
- Uses any public RPC endpoint for Base:
  - [https://mainnet.base.org](https://mainnet.base.org)
  - Infura, Alchemy, or Ankr

---

## Configuration (`.env` File)

```env
BASE_RPC_URL=https://mainnet.base.org
PRIVATE_KEY=your_private_key
USDC_CONTRACT=0xD9AAE9C67e9FCf4C3c118e7Dd048E0a8F1C0eCf2
TARGET_WALLET=0xTargetWalletAddress
TRANSFER_AMOUNT=100

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

---

## Execution Flow

1. Load environment variables using `dotenv`.
2. Initialize `Web3` and load the wallet from the private key.
3. Load USDC ERC20 contract using ABI.
4. Validate:
   - **USDC balance** ≥ transfer amount
   - **ETH balance** ≥ gas threshold
5. Build and sign a `transfer()` transaction.
6. Send transaction and wait for receipt.
7. Log the result (success/failure, timestamp, TX hash).
8. Send Telegram alert with outcome.

---

## Error Handling and Alerts

### Scenarios & Responses

- **Insufficient USDC**:
  - Abort
  - Log warning
  - Telegram alert: ❗ Insufficient USDC

- **Insufficient ETH**:
  - Abort
  - Log error
  - Telegram alert: ❗ Insufficient ETH for gas

- **Transaction Rejected**:
  - Retry once (optional)
  - Log error and notify

- **Unhandled Exception**:
  - Catch and log stack trace
  - Send Telegram alert with traceback summary

---

## Deliverables

- `src/main.py`: Main transfer script.
- `src/utils.py`: Balance checking, gas estimation, transaction helpers.
- `src/telegram.py`: Telegram alert sender.
- `src/abi.py`: Minimal ERC20 ABI definition.
- `.env.example`: Sample config file.
- `README.md`: Setup guide and usage instructions.
- `logs/transfer.log`: Auto-generated output file.
- `requirements.txt`: All required dependencies.
- `Dockerfile` (optional): Containerize the script.
- `USDC_Transfer_PRD.md`: This document.

---

## Future Enhancements

- Batch transfers from CSV or JSON.
- Google Sheets integration for wallet management.
- Admin web UI for status tracking and control.
- Integration with on-chain automation (Gelato, Chainlink Keepers).
- Encrypted vault for private key access.
- Slack/Discord alerting options.
- Monitoring dashboard (Grafana + Loki or UptimeRobot).

---

## Ownership

- **Product Owner**: [Your Name]
- **Developer**: [Developer Name]
- **Review Date**: [YYYY-MM-DD]
- **Version**: 1.0.0

---
