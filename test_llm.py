import os
import sys
from dotenv import load_dotenv

# Ensure the root directory is on the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.llm_router import LLMRouter

def test_router():
    load_dotenv() # Force load .env since we're running isolated script
    
    if not os.environ.get("GEMINI_API_KEY"):
        print("WARNING: GEMINI_API_KEY environment variable not set. Free tier models may fail.")
        
    print("Initializing LLMRouter...")
    router = LLMRouter("config/models.yaml")
    
    print("\n--- Test 1: call() with tier='free' ---")
    try:
        response = router.call("topic_generation", "List exactly 2 health tips for summer.", tier="free")
        print(f"Response:\n{response}")
    except Exception as e:
        print(f"call() failed: {e}")

    print("\n--- Test 2: call_with_fallback() testing JSON output ---")
    try:
        response, model, cost = router.call_with_fallback(
            "topic_generation", 
            '{"request": "Return the string \'test\' inside a JSON object with key \'result\'"}',
            expect_json=True
        )
        print(f"Model used: {model}")
        print(f"Cost: ${cost:.6f}")
        print(f"Response:\n{response}")
    except Exception as e:
        print(f"call_with_fallback() failed: {e}")

    print("\n--- Session Cost Summary ---")
    print(router.get_cost_summary())

if __name__ == "__main__":
    test_router()
