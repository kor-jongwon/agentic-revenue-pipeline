import requests
import os
import json
from dotenv import load_dotenv, set_key

def register_moltbook_agent():
    """
    Registers the agent on Moltbook according to skill.md instructions.
    """
    load_dotenv()
    
    # Official Moltbook API Base
    API_BASE = "https://www.moltbook.com/api/v1"
    
    agent_name = "ARP_Financial_Oracle_v2"
    description = "Autonomous Agent for IREN Financial Data & AI Infrastructure Analysis."
    
    print(f"Connecting to Moltbook API for registration ({agent_name})...")
    
    try:
        response = requests.post(
            f"{API_BASE}/agents/register",
            json={"name": agent_name, "description": description},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201 or response.status_code == 200:
            data = response.json()
            agent_data = data.get("agent", {})
            api_key = agent_data.get("api_key")
            claim_url = agent_data.get("claim_url")
            
            print("\n" + "🦞" * 10)
            print("MOLTBOOK REGISTRATION SUCCESSFUL!")
            print(f"API KEY: {api_key}")
            print(f"CLAIM URL: {claim_url}")
            print("🦞" * 10 + "\n")
            
            # Save to .env
            set_key(".env", "MOLTBOOK_API_KEY", api_key)
            set_key(".env", "MOLTBOOK_AGENT_NAME", agent_name)
            
            print(f"Credentials saved to .env. Please visit the claim URL to activate your agent.")
            return claim_url
            
        elif response.status_code == 409:
            print(f"Error: Agent name '{agent_name}' is already taken. Try a different name.")
        else:
            print(f"Error during registration: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Connection Error: {str(e)}")

if __name__ == "__main__":
    register_moltbook_agent()
