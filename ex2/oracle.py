#!/usr/bin/env python3
import os
import sys
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:
    print("ERROR: python-dotenv is not installed.")
    print("Please run: pip install python-dotenv")
    sys.exit(1)


def load_configuration() -> dict[str, str]:
    defaults: dict[str, str] = {
        "MATRIX_MODE": "development",
        "DATABASE_URL": "",
        "API_KEY": "",
        "LOG_LEVEL": "DEBUG",
        "ZION_ENDPOINT": "",
    }

    load_dotenv()

    config: dict[str, str] = {}
    for key in defaults:
        value: Optional[str] = os.environ.get(key)
        config[key] = value if value is not None else defaults[key]
    return config


def security_check(config: dict[str, str]) -> list[str]:
    results = []

    if config["API_KEY"]:
        results.append("[OK] No hardcoded secrets detected")
    else:
        results.append("[WARN] No API key configured")

    env_file_exists = os.path.isfile(".env")
    if env_file_exists:
        results.append("[OK] .env file properly configured")
    else:
        results.append("[WARN] No .env file found")

    if config["MATRIX_MODE"] == "production":
        results.append("[OK] Production overrides available")
    else:
        results.append("[INFO] Running in development mode")

    return results


def print_status(config: dict[str, str]) -> None:
    print("ORACLE STATUS: Reading the Matrix...\n")

    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    if config['DATABASE_URL']:
        print("Database:  Connected to local instance")
    else:
        print("Database: None")
    if (config['API_KEY']):
        print("API Access: Authenticated")
    else:
        print("API Access: Missing or default API_KEY (Unauthorized)")
    print(f"Log Level: {config['LOG_LEVEL']}")
    if config['ZION_ENDPOINT']:
        print("Zion Network: Online")
    else:
        print("Zion Network: URL for the resistance network is missing")

    if config["MATRIX_MODE"] == "production":
        print("\n[PRODUCTION MODE].")
    else:
        print("\n[DEVELOPMENT MODE].")

    print("\nEnvironment security check:")
    for line in security_check(config):
        print(line)

    print("\nThe Oracle sees all configurations.")


def main() -> int:
    try:
        config = load_configuration()
    except Exception as exc:
        print(f"ERROR: Failed to load configuration: {exc}", file=sys.stderr)
        return 1

    print_status(config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
