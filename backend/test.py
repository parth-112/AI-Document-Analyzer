from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings

# 1. Load the environment variables
load_dotenv()

# 2. Check if the code can actually see the key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERROR: Could not find OPENAI_API_KEY in the environment.")
    exit()
else:
    # Print just the first few characters to verify it loaded correctly
    print(f"✅ Found API Key starting with: {api_key[:7]}...")

# 3. Try to hit the OpenAI server
print("Attempting to connect to OpenAI...")
try:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Try embedding a single simple word
    vector = embeddings.embed_query("hello")

    print("✅ SUCCESS! Received a response from OpenAI.")
    print(f"Vector length (dimensions): {len(vector)}")
    print(f"First 3 values: {vector[:3]}")

except Exception as e:
    print("\n❌ FAILED TO CONNECT TO OPENAI:")
    print(str(e))
