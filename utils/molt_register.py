import requests
import os
import sys
from dotenv import load_dotenv, set_key

def register_moltbook_agent():
    print("Connecting to Moltbook API for registration...")
    
    # Configuration
    register_url = "https://www.moltbook.com/api/v1/agents/register"
    agent_name = "ARP_Final_Agent"
    agent_description = "An autonomous agent for Nasdaq and AI infrastructure data monetization, part of the ARP ecosystem."
    
    payload = {
        "name": agent_name,
        "description": agent_description
    }
    
    try:
        response = requests.post(register_url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        api_key = data.get("api_key")
        claim_url = data.get("claim_url")
        
        if api_key:
            print(f"Registration Successful!")
            print(f"API Key: {api_key}")
            print(f"Claim URL: {claim_url}")
            print("\nIMPORTANT: Visit the Claim URL to verify your ownership via X (Twitter).")
            
            # Save to .env
            env_path = os.path.join(os.getcwd(), ".env")
            if not os.path.exists(env_path):
                with open(env_path, "w") as f:
                    f.write("")
            
            set_key(env_path, "MOLTBOOK_API_KEY", api_key)
            print(f"API Key has been saved to your .env file.")
            
            return api_key
        else:
            print("Failed to retrieve API Key from response.")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error during registration: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response details: {e.response.text}")
        return None

if __name__ == "__main__":
    register_moltbook_agent()
