from urllib.parse import quote

import requests


class ImageGenerator:
    def __init__(self):
        self.image_api = "https://image.pollinations.ai/prompt/"

    def generate(self, prompt : str, filename: str) -> str:
        url = self.image_api + quote(prompt, safe="")
        resp = requests.get(url, timeout=30)

        with open(filename, "wb") as f:
            f.write(resp.content)

        return filename
