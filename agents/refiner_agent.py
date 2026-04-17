from .base_agent import BaseAgent
import os
import json
from litellm import completion

class RefinerAgent(BaseAgent):
    """
    The Refiner Agent: Responsible for value proposition.
    Evaluates the scarcity and value of collected Markdown data using AI insights.
    """
    def __init__(self):
        super().__init__("Refiner Agent", "AI Data Evaluator")
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini") # Default model

    def run(self, raw_data):
        self.log(f"Refining data for {raw_data.get('symbol')} using {self.model}")
        
        markdown_content = raw_data.get("raw_markdown", "")
        
        prompt = f"""
        You are a high-level financial data analyst for the Agentic Revenue Pipeline (ARP).
        Below is a raw markdown data collected from a financial source about {raw_data.get('symbol')}.
        
        ### RAW DATA:
        {markdown_content}
        
        ### TASK:
        1. Extract the current price and 24h change if visible.
        2. Analyze the significance of this data for AI infrastructure investors.
        3. Provide a 'Value Score' (0.0 to 1.0) based on how marketable this processed data would be.
        4. Generate a catchy product name for Moltbook.
        
        ### OUTPUT FORMAT (JSON ONLY):
        {{
            "extracted_price": "string",
            "extracted_change": "string",
            "analysis": "string",
            "value_score": float,
            "product_name": "string",
            "key_insight": "string"
        }}
        """

        try:
            # Check for API Key presence
            if not os.getenv("OPENAI_API_KEY") and not os.getenv("ANTHROPIC_API_KEY"):
                self.log("Warning: No LLM API Keys found in environment. Using simulated analysis.")
                return self._simulate_analysis(raw_data)

            response = completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            refined_json = json.loads(response.choices[0].message.content)
            self.log(f"AI Analysis complete. Value Score: {refined_json.get('value_score')}")
            
            return {
                "source": raw_data,
                "refined_insight": refined_json,
                "status": "success"
            }

        except Exception as e:
            self.log(f"Error during AI refining: {str(e)}")
            return self._simulate_analysis(raw_data)

    def _simulate_analysis(self, raw_data):
        """Fallback simulated analysis if AI call fails or no API keys."""
        return {
            "source": raw_data,
            "refined_insight": {
                "extracted_price": "Simulated $12.50",
                "extracted_change": "+2.4%",
                "analysis": "Data contains positive momentum for IREN AI growth.",
                "value_score": 0.85,
                "product_name": f"IREN_Alpha_{raw_data.get('symbol')}",
                "key_insight": "AI infrastructure demand is outpacing supply."
            },
            "status": "simulated"
        }
