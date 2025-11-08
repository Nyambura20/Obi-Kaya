import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔍 Testing SalesGenius AI Agent Setup...\n")
print("=" * 60)

# Test 1: Check Python version
print("\n1️⃣  Checking Python version...")
python_version = sys.version_info
if python_version.major >= 3 and python_version.minor >= 8:
    print(f"   ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
else:
    print(f"   ❌ Python {python_version.major}.{python_version.minor} (need 3.8+)")
    sys.exit(1)

# Test 2: Check environment variables
print("\n2️⃣  Checking environment variables...")
api_key = os.getenv("GOOGLE_API_KEY")
if api_key and api_key != "your_google_api_key_here":
    print(f"   ✅ GOOGLE_API_KEY is set ({api_key[:10]}...)")
else:
    print("   ❌ GOOGLE_API_KEY is not set or is placeholder")
    print("   👉 Get your API key: https://aistudio.google.com/app/apikey")
    print("   👉 Add it to your .env file")
    sys.exit(1)

# Test 3: Check required packages
print("\n3️⃣  Checking required packages...")
required_packages = {
    "google.adk.agents": "google-adk",
    "google.genai": "google-genai",
    "dotenv": "python-dotenv"
}

missing_packages = []
for module, package in required_packages.items():
    try:
        __import__(module)
        print(f"   ✅ {package}")
    except ImportError:
        print(f"   ❌ {package}")
        missing_packages.append(package)

if missing_packages:
    print(f"\n   ❌ Missing packages: {', '.join(missing_packages)}")
    print("   👉 Run: pip install -r requirements.txt")
    sys.exit(1)

# Test 4: Try to import the agent
print("\n4️⃣  Checking agent module...")
try:
    from obi_kaya_agent import agent
    print("   ✅ Agent module loaded successfully")
    print(f"   ✅ Agent name: {agent.root_agent.name}")
    print(f"   ✅ Agent has {len(agent.root_agent.tools)} tools configured")
except Exception as e:
    print(f"   ❌ Failed to load agent: {str(e)}")
    sys.exit(1)

# Test 5: Test a simple tool
print("\n5️⃣  Testing a tool (answer_sales_question)...")
try:
    result = agent.answer_sales_question(
        question="What is MEDDIC sales methodology?",
        context="Training new sales rep"
    )
    if result.get("status") == "success":
        print("   ✅ Tool executed successfully")
        answer_preview = result.get("answer", "")[:150]
        print(f"   📝 Answer preview: {answer_preview}...")
    else:
        print(f"   ❌ Tool failed: {result.get('message')}")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Tool test failed: {str(e)}")
    sys.exit(1)

# All tests passed!
print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED!")
print("=" * 60)
print("\n🎉 Your SalesGenius AI Agent is ready to use!")
print("\n📝 Next steps:")
print("   1. Run locally: adk web")
print("   2. Open http://localhost:8080 in your browser")
print("   3. Test with sample data from ./sample_data/")
print("   4. Deploy to Cloud Run: bash deploy.sh")
print("\n" + "=" * 60)
