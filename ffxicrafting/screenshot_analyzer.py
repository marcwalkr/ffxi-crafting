import pytesseract
import re
from PIL import Image


class ScreenshotAnalyzer:
    def __init__(self, item_name) -> None:
        self.item_name = item_name

    def get_single_data(self):
        single_path = "auction_screenshots/{}.png".format(self.item_name)
        return self.extract_data(single_path)

    def get_stack_data(self):
        stack_path = "auction_screenshots/{}_stack.png".format(self.item_name)
        return self.extract_data(stack_path)

    @staticmethod
    def extract_data(path):
        # Load the screenshot of the price history
        original_image = Image.open(path)

        # Resize the image
        resized_image = original_image.resize((original_image.width * 4, original_image.height * 4))

        # Perform OCR on the image
        text = pytesseract.image_to_string(resized_image)

        # Collect timestamps and prices
        timestamps = []
        prices = []

        lines = text.split("\n")
        for line in lines:
            # Extract timestamp if it exists
            timestamp_pattern = r"\b\d{1,2}/\d{1,2}/\d{4}, \d{1,2}:\d{2}:\d{2} (AM|PM)\b"
            timestamp_match = re.search(timestamp_pattern, line)
            if timestamp_match:
                timestamp = timestamp_match.group()
                timestamps.append(timestamp)

            # Extract price if it exists
            price_pattern = r"\b(\d{1,3}(?:,\d{3})*)g\b"
            price_match = re.search(price_pattern, line)
            if price_match:
                price_str = price_match.group(1)
                price_str = price_str.replace(",", "")  # Remove commas
                price_int = int(price_str)
                prices.append(price_int)

        return timestamps, prices
