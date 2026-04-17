import time
import json
import os

class PipelineMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.total_cycles = 0
        self.success_count = 0
        self.total_value_generated = 0.0
        self.logs_path = "transaction_logs.json"
        self.snapshot_dir = "data_snapshots"
        
        if not os.path.exists(self.snapshot_dir):
            os.makedirs(self.snapshot_dir)

    def record_cycle(self, success, value=0.0, product_id=None, raw_data=None, refined_insight=None):
        self.total_cycles += 1
        timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
        json_timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        
        if success:
            self.success_count += 1
            self.total_value_generated += value
            
            # Save a detailed snapshot of this cycle
            snapshot = {
                "cycle": self.total_cycles,
                "timestamp": json_timestamp,
                "product_id": product_id,
                "raw_data": raw_data,
                "refined_insight": refined_insight
            }
            snapshot_file = os.path.join(self.snapshot_dir, f"snapshot_{timestamp}.json")
            with open(snapshot_file, "w", encoding="utf-8") as f:
                json.dump(snapshot, f, indent=4, ensure_ascii=False)

        log_entry = {
            "timestamp": json_timestamp,
            "success": success,
            "value": value,
            "product_id": product_id,
            "snapshot_file": f"snapshot_{timestamp}.json" if success else None
        }
        
        self._save_log(log_entry)

    def _save_log(self, entry):
        logs = []
        if os.path.exists(self.logs_path):
            try:
                with open(self.logs_path, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            except:
                logs = []
        
        logs.append(entry)
        logs = logs[-100:]
        
        with open(self.logs_path, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=4, ensure_ascii=False)
