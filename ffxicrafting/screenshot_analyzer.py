import pytesseract
import re
import pandas as pd
import statistics
import os
from PIL import Image


class ScreenshotAnalyzer:
    def __init__(self, item_name) -> None:
        self.item_name = item_name

    def get_avg_price_and_frequency(self, stack):
        if stack:
            path = "auction_screenshots/{}_stack.png".format(self.item_name)
        else:
            path = "auction_screenshots/{}.png".format(self.item_name)

        # If file doesn't exist, return None for price and frequency
        if not os.path.isfile(path):
            return None, None

        timestamp_strings, prices = self.extract_data(path)

        # No timestamps or prices were found in the screenshot, return None for both
        if not timestamp_strings or not prices:
            return None, None

        avg_price = statistics.fmean(prices)
        sales_frequency = self.calculate_sales_frequency(timestamp_strings)

        return avg_price, sales_frequency

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

    @staticmethod
    def calculate_sales_frequency(timestamp_strings):
        # Convert to datetime
        timestamps = pd.to_datetime(timestamp_strings, format="%m/%d/%Y, %I:%M:%S %p")

        # Sort timestamps
        timestamps = timestamps.sort_values()

        # Calculate time differences
        time_diffs = timestamps.diff().dropna()

        # Average time difference
        avg_time_diff = time_diffs.mean()

        # Convert average time differences to frequency (sales per day)
        avg_time_diff_seconds = avg_time_diff.total_seconds()
        return 86400 / avg_time_diff_seconds if avg_time_diff_seconds != 0 else None


analyzer = ScreenshotAnalyzer("red_hot_cracker")
data = analyzer.get_price_and_frequency(stack=False)
print(data)
