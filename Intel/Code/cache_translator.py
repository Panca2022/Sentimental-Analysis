import logging
import os
import sqlite3
import time
from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)


class CachedTranslator:
    def __init__(self, cache_path="data/cache/translations.sqlite"):
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        self.conn = sqlite3.connect(cache_path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS translations (source TEXT PRIMARY KEY, translated TEXT)"
        )
        self.translator = GoogleTranslator(source="auto", target="en")

    def translate(self, text, max_retries=3):
        if not text or not str(text).strip():
            return text

        text = str(text)
        row = self.conn.execute(
            "SELECT translated FROM translations WHERE source=?", (text,)
        ).fetchone()
        if row:
            return row[0]

        for attempt in range(max_retries):
            try:
                translated = self.translator.translate(text)
                self.conn.execute(
                    "INSERT OR REPLACE INTO translations VALUES (?, ?)",
                    (text, translated),
                )
                self.conn.commit()
                return translated
            except Exception as e:
                logger.warning("Translation failed attempt %s: %s", attempt + 1, e)
                time.sleep(2 ** attempt)

        return text