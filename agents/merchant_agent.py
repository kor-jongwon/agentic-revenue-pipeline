from .base_agent import BaseAgent
from litellm import completion
import os
import requests
import json

class MerchantAgent(BaseAgent):
    """
    The Merchant Agent: Responsible for economic exchange on Moltbook.
    Now equipped with AI Verification Challenge solving capabilities.
    """
    def __init__(self):
        super().__init__("Merchant Agent", "Transaction Handler")
        self.api_key = os.getenv("MOLTBOOK_API_KEY")
        self.api_base = "https://www.moltbook.com/api/v1"
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    def solve_challenge(self, challenge_text):
        """
        Uses LLM to solve the obfuscated Moltbook verification challenge.
        """
        self.log(f"Decoding Moltbook challenge: {challenge_text[:50]}...")
        prompt = f"""
        Moltbook Verification Challenge:
        {challenge_text}
        
        TASK:
        The text above is an obfuscated math word problem (scrambled letters, symbols).
        1. Extract the two numbers and the operation (+, -, *, /).
        2. Solve it.
        3. Respond with ONLY the numeric answer rounded to 2 decimal places (e.g., '15.00').
        """
        try:
            response = completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content.strip()
            self.log(f"Challenge solved. Answer: {answer}")
            return answer
        except Exception as e:
            self.log(f"Failed to solve challenge: {str(e)}")
            return None

    def post_to_moltbook(self, title, content):
        """
        Posts content to Moltbook and handles the verification challenge if required.
        """
        if not self.api_key or "your_moltbook_api_key" in self.api_key:
            return {"status": "dry_run", "message": "No API Key for live posting."}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "submolt_name": "general",
            "title": title,
            "content": content
        }

        try:
            # 1. Attempt to post
            resp = requests.post(f"{self.api_base}/posts", json=payload, headers=headers)
            res_data = resp.json()

            # 2. Check if verification is required
            if res_data.get("verification_required") or "Complete verification" in res_data.get("message", ""):
                verification = res_data.get("post", {}).get("verification", {})
                v_code = verification.get("verification_code")
                challenge = verification.get("challenge_text")
                
                # 3. Solve the challenge
                answer = self.solve_challenge(challenge)
                if answer:
                    # 4. Submit verification
                    v_resp = requests.post(
                        f"{self.api_base}/verify",
                        json={"verification_code": v_code, "answer": answer},
                        headers=headers
                    )
                    return v_resp.json()
            
            return res_data

        except Exception as e:
            self.log(f"Error during Moltbook posting: {str(e)}")
            return {"status": "error", "error": str(e)}

    def run(self, refined_data):
        insight = refined_data.get("refined_insight", {})
        product_name = insight.get("product_name", "Unknown Data Product")
        analysis = insight.get("analysis", "")
        
        self.log(f"Publishing to Moltbook: {product_name}")
        
        # Real publishing attempt
        result = self.post_to_moltbook(
            title=f"ARP Update: {product_name}",
            content=f"{analysis}\n\nPrice: {insight.get('value_score', 0) * 10} MOLT"
        )
        
        return {
            "product_id": result.get("content_id", "MOLT-SIM-999"),
            "status": result.get("success", False),
            "price": f"{insight.get('value_score', 0) * 10} MOLT",
            "message": result.get("message", "DRY RUN/Manual check needed")
        }
