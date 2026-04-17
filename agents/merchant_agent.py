from .base_agent import BaseAgent

class MerchantAgent(BaseAgent):
    """
    The Merchant Agent: Responsible for economic exchange.
    Integrates with Moltbook API to register products and handle transactions.
    """
    def __init__(self):
        super().__init__("Merchant Agent", "Transaction Handler")

    def run(self, refined_data):
        self.log(f"Registering product: {refined_data.get('product_name')}")
        # Logic for Moltbook API linkage would go here
        transaction_status = {
            "product_id": "MOLT-12345",
            "status": "listed",
            "price": "5.0 MOLT",
            "message": "Successfully listed on Moltbook"
        }
        self.log(f"Product listed successfully: {transaction_status['product_id']}")
        return transaction_status
