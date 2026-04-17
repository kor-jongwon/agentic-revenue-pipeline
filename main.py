import os
import time
import signal
import sys
from dotenv import load_dotenv
from agents.oracle_agent import OracleAgent
from agents.refiner_agent import RefinerAgent
from agents.merchant_agent import MerchantAgent
from core.monitor import PipelineMonitor

# Load environment variables
load_dotenv()

monitor = PipelineMonitor()

def handle_exit(sig, frame):
    print("\n👋 Gracefully shutting down ARP Pipeline...")
    summary = monitor.get_summary()
    print(f"📊 Final Stats: {summary}")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)

def run_pipeline_cycle():
    print(f"\n🔄 [Cycle #{monitor.total_cycles + 1}] Starting...")
    
    try:
        # 1. Oracle: Collect Data
        oracle = OracleAgent()
        raw_data = oracle.run()
        if raw_data.get("status") == "error":
            raise Exception(f"Oracle failed: {raw_data.get('error')}")
        
        # 2. Refiner: Evaluate Data
        refiner = RefinerAgent()
        refined_data = refiner.run(raw_data)
        if refined_data.get("status") == "error":
            raise Exception("Refiner failed to analyze data")
            
        # 3. Merchant: List Data
        merchant = MerchantAgent()
        result = merchant.run(refined_data)
        
        # Record Success
        value = float(result.get("price", "0").split()[0])
        monitor.record_cycle(
            success=True, 
            value=value, 
            product_id=result.get("product_id"),
            raw_data=raw_data,
            refined_insight=refined_data.get("refined_insight")
        )
        
        print("\n" + "="*50)
        print("✅ Cycle Completed Successfully.")
        print(f"💰 Status: {result['message']}")
        print(f"📦 Product ID: {result['product_id']}")
        print(f"💵 Price: {result['price']}")
        print("="*50)

    except Exception as e:
        print(f"❌ Cycle Failed: {str(e)}")
        monitor.record_cycle(False)

def main():
    print("🚀 Agentic Revenue Pipeline (ARP) is Live!")
    interval = int(os.getenv("POLLING_INTERVAL", 3600))
    
    while True:
        run_pipeline_cycle()
        
        summary = monitor.get_summary()
        print(f"📊 Live Monitor: {summary}")
        
        print(f"😴 Sleeping for {interval} seconds...")
        time.sleep(interval)

if __name__ == "__main__":
    main()
