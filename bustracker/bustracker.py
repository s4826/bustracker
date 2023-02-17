"""Bustracker app, main entry point"""

from app import create_app

app = create_app("postgres_config")
