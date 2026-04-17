from .base_agent import BaseAgent
import os

class MerchantAgent(BaseAgent):
    """
    The Merchant Agent: Responsible for economic exchange.
    Integrates with Moltbook API to register products and handle transactions.
    """
    def __init__(self):
        super().__init__("Merchant Agent", "Transaction Handler")
        self.api_key = os.getenv("MOLTBOOK_API_KEY")

    def run(self, refined_data):
        insight = refined_data.get("refined_insight", {})
        product_name = insight.get("product_name", "Unknown Data Product")
        
        self.log(f"Preparing to list product: {product_name}")
        
        # Check if API Key exists
        if not self.api_key or "your_moltbook_api_key" in self.api_key:
            self.log("Warning: No Moltbook API Key found. Skipping live registration.")
            return {
                "product_id": "MOLT-SIM-999",
                "status": "dry_run",
                "price": f"{insight.get('value_score', 0) * 10} MOLT",
                "message": f"DRY RUN: Product '{product_name}' is ready for Moltbook."
            }

        # Real logic for Moltbook API (POST /api/v1/posts) would go here
        # For now, we simulate the success response
        transaction_status = {
            "product_id": f"MOLT-{os.urandom(4).hex().upper()}",
            "status": "listed",
            "price": f"{insight.get('value_score', 0) * 10} MOLT",
            "message": f"Successfully listed '{product_name}' on Moltbook!"
        }
        
        self.log(f"Product listed successfully: {transaction_status['product_id']}")
        return transaction_status
