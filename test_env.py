import feedparser
from newspaper import Article
from pydantic import BaseModel

def test_imports():
    print("✅ All imports successful!")
    
    # Test News Parsing
    url = "https://news.google.com/rss/search?q=Trustpair"
    feed = feedparser.parse(url)
    print(f"✅ feedparser is working. Found {len(feed.entries)} entries.")
    
    # Test Pydantic
    class TestModel(BaseModel):
        test_field: str
    
    data = TestModel(test_field="Environment is healthy")
    print(f"✅ Pydantic is working. Data: {data.test_field}")
    print("🚀 You are ready to run the full agent!")

if __name__ == "__main__":
    test_imports()