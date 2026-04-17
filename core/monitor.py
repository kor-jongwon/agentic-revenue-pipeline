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

    def record_cycle(self, success, value=0.0, product_id=None):
        self.total_cycles += 1
        if success:
            self.success_count += 1
            self.total_value_generated += value

        log_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "success": success,
            "value": value,
            "product_id": product_id
        }
        
        self._save_log(log_entry)

    def _save_log(self, entry):
        logs = []
        if os.path.exists(self.logs_path):
            try:
                with open(self.logs_path, "r") as f:
                    logs = json.load(f)
            except:
                logs = []
        
        logs.append(entry)
        # Keep only last 100 logs
        logs = logs[-100:]
        
        with open(self.logs_path, "w") as f:
            json.dump(logs, f, indent=4)

    def get_summary(self):
        uptime = time.time() - self.start_time
        return {
            "uptime_seconds": round(uptime, 2),
            "total_cycles": self.total_cycles,
            "success_rate": f"{(self.success_count / self.total_cycles * 100):.1f}%" if self.total_cycles > 0 else "0%",
            "total_value_molt": round(self.total_value_generated, 2)
        }
