from backend.ai import CleanerChain
from backend.test_data.load_test_data import load_test_data

from dotenv import load_dotenv
import os

load_dotenv()


def test_cleaner():
    cleaner = CleanerChain(api_key=os.getenv("GOOGLE_API_KEY"))
    text = load_test_data()
    cleaned_text = cleaner.run(text).get("cleaned_text").get("cleaned_text")
    print(cleaned_text)
    with open("cleaned_text.txt", "w") as file:
        file.write(cleaned_text)


if __name__ == "__main__":
    test_cleaner()
