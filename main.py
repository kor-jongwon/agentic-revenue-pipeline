from agents.oracle_agent import OracleAgent
from agents.refiner_agent import RefinerAgent
from agents.merchant_agent import MerchantAgent

def run_pipeline():
    print("🚀 Starting Agentic Revenue Pipeline (ARP)...")
    
    # 1. Oracle: Collect Data
    oracle = OracleAgent()
    raw_data = oracle.run()
    
    # 2. Refiner: Evaluate Data
    refiner = RefinerAgent()
    refined_data = refiner.run(raw_data)
    
    # 3. Merchant: List Data
    merchant = MerchantAgent()
    result = merchant.run(refined_data)
    
    print("\n✅ Pipeline Cycle Completed.")
    print(f"Summary: {result['message']} - ID: {result['product_id']}")

if __name__ == "__main__":
    run_pipeline()
