from urllib.parse import quote

import requests
from PIL import Image


class ImageGenerator:
    def __init__(self):
        self.image_api = "https://image.pollinations.ai/prompt/"

    def generate(self, prompt : str, filename: str) -> str:
        url = self.image_api + quote(prompt, safe="")
        resp = requests.get(url, timeout=30)

        with open(filename, "wb") as f:
            f.write(resp.content)

        with Image.open(filename) as img:
            width, height = img.size
            new_height = height - 60
            cropped = img.crop((0, 0, width, new_height))
            cropped.save(filename)

        return filename
