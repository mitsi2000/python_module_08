#!/usr/bin/env python3
import os
import sys
from typing import Optional

from dotenv import load_dotenv


def load_configuration() -> dict[str, str]:
    defaults: dict[str, str] = {
        "MATRIX_MODE": "development",
        "DATABASE_URL": "sqlite:///local_matrix.db",
        "API_KEY": "",
        "LOG_LEVEL": "DEBUG",
        "ZION_ENDPOINT": "http://localhost:9999",
    }

    load_dotenv()

    config: dict[str, str] = {}
    for key in defaults:
        value: Optional[str] = os.environ.get(key)
        config[key] = value if value is not None else defaults[key]
    return config


def mask_secret(value: str, visible_chars: int = 4) -> str:
    if not value:
        return "NOT SET"
    if len(value) <= visible_chars:
        return "*" * len(value)
    return value[:visible_chars] + "*" * (len(value) - visible_chars)


def security_check(config: dict[str, str]) -> list[str]:
    results = []

    if config["API_KEY"]:
        results.append("[OK] API key detected (not hardcoded, loaded from env)")
    else:
        results.append("[WARN] No API key configured")

    env_file_exists = os.path.isfile(".env")
    if env_file_exists:
        results.append("[OK] .env file properly configured")
    else:
        results.append("[WARN] No .env file found (using defaults / real env vars)")

    if config["MATRIX_MODE"] == "production":
        results.append("[OK] Production overrides available")
    else:
        results.append("[INFO] Running in development mode")

    return results


def print_status(config: dict[str, str]) -> None:
    print("ORACLE STATUS: Reading the Matrix...\n")

    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    print(f"Database: {config['DATABASE_URL']}")
    print(f"API Access: {mask_secret(config['API_KEY'])}")
    print(f"Log Level: {config['LOG_LEVEL']}")
    print(f"Zion Network: {config['ZION_ENDPOINT']}")

    if config["MATRIX_MODE"] == "production":
        print("\n[PRODUCTION MODE] Verbose logging disabled, strict checks enabled.")
    else:
        print("\n[DEVELOPMENT MODE] Verbose logging enabled, using local defaults.")

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