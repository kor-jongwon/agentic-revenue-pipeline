from .base_agent import BaseAgent
from crawl4ai import AsyncWebCrawler
import json
import time
import asyncio

class OracleAgent(BaseAgent):
    """
    The Oracle Agent: Responsible for data ingestion.
    Now using AsyncWebCrawler from Crawl4AI for modern, markdown-based data collection.
    """
    def __init__(self):
        super().__init__("Oracle Agent", "Modern Data Ingestor")
        self.target_url = "https://www.google.com/finance/quote/IREN:NASDAQ"

    async def _async_crawl(self):
        """
        Asynchronously crawl the target URL using AsyncWebCrawler.
        """
        async with AsyncWebCrawler() as crawler:
            # We use 'markdown' as it's the most agentic format for LLMs
            result = await crawler.arun(url=self.target_url)
            return result

    def run(self):
        self.log(f"Starting Agentic Crawling from {self.target_url} using Crawl4AI")
        
        try:
            # Running the async crawler in a synchronous context
            result = asyncio.run(self._async_crawl())
            
            if not result.success:
                raise Exception(f"Crawl failed: {result.error_message}")

            markdown_content = result.markdown
            self.log("Successfully crawled page and converted to Markdown.")
            
            data = {
                "symbol": "IREN",
                "name": "Iris Energy Limited",
                "raw_markdown": markdown_content[:500] + "...",
                "source": "Google Finance via Crawl4AI",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "status": "success",
                "full_content_length": len(markdown_content)
            }
            
            return data

        except Exception as e:
            self.log(f"Error during agentic crawling: {str(e)}")
            return {
                "symbol": "IREN",
                "status": "error",
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
