import os
import logging
from dotenv import load_dotenv
from web3 import Web3
from telegram import send_telegram_message
from utils import get_token_balance, check_eth_balance, get_token_contract, send_usdc

# Setup logging
logging.basicConfig(filename='./logs/transfer.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

# Load environment variables
RPC_URL = os.getenv("BASE_RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
USDC_CONTRACT = os.getenv("USDC_CONTRACT")
TARGET_WALLET = os.getenv("TARGET_WALLET")
TRANSFER_AMOUNT = float(os.getenv("TRANSFER_AMOUNT"))

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
wallet_address = account.address

def main():
    try:
        usdc = get_token_contract(w3, USDC_CONTRACT)
        balance = get_token_balance(usdc, wallet_address)
        if balance < TRANSFER_AMOUNT:
            msg = f"❗ Insufficient USDC. Balance: {balance}, Required: {TRANSFER_AMOUNT}"
            logging.warning(msg)
            send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, msg)
            return

        if not check_eth_balance(w3, wallet_address):
            msg = "❗ Insufficient ETH for gas"
            logging.error(msg)
            send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, msg)
            return

        tx_hash = send_usdc(w3, account, usdc, TARGET_WALLET, TRANSFER_AMOUNT)
        msg = f"✅ USDC Transfer successful. TX Hash: {tx_hash}"
        logging.info(msg)
        send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, msg)

    except Exception as e:
        msg = f"❌ Transfer failed: {str(e)}"
        logging.exception(msg)
        send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, msg)

if __name__ == "__main__":
    main()
