import re
from urllib.parse import quote

import requests


class Rephraser:
    def __init__(self):
        self.text_api = "https://text.pollinations.ai/"

    def rewrite(self, text: str, style: str) -> str:
        prompt = (
                f"Переформулируй текст, сделай его в стиле «{style}» и сохрани смысл. "
                "Требования к результату (обычный Markdown, parse_mode=\"Markdown\" в aiogram):\n"
                "1. Разбей на несколько абзацев.\n"
                "2. Используй преимущественно жирный как *...*, а курсив как _..._ только при необходимости.\n"
                "3. В ответе пришли только на русском языке только текст поста без каких-либо лишних комментариев или пояснений.\n"
                "4. Не вставляй никаких ссылок или элементов, напоминающих ссылки на другие источники.\n\n"
                "Исходный текст:\n\n"
                + text
        )
        while True:
            url = self.text_api + quote(prompt, safe="")
            resp = requests.get(url, timeout=30)
            text = resp.text.strip()
            if len(text.split("---")) == 1 and len(text)>100:
                break
        text = text.replace("**", "*")
        text = re.sub(r"@\S+\b", "", text).strip()
        # "\b" -> [a-zA-Z0-9_]
        return text

    def generate_image_prompt(self, text: str, image_style: str) -> str:
        prompt = (
            f"{image_style}. На основе текста: «{text}» "
            "— короткий лаконичный промт для генерации изображения. "
            "В ответе пришли только промт без каких-либо лишних комментариев или пояснений."
        )
        url = self.text_api + quote(prompt, safe="")
        resp = requests.get(url, timeout=30)
        return resp.text.strip()
