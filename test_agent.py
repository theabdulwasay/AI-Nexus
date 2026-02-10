from main import AgenticAIAssistant
import time

print("Initializing Agent...")
try:
    agent = AgenticAIAssistant()
    print("Agent initialized.")
except Exception as e:
    print(f"FAILED to initialize agent: {e}")
    exit(1)

queries = [
    "Hi",
    "Where is Paris?",
    "What time is it?",
    "List files in tools",
    "Calculate \"15 * 24 + 100\""
]

print("\nRunning Queries...")
for q in queries:
    print(f"\nQUERY: {q}")
    try:
        res = agent.process_query(q)
        print(f"RESPONSE: {res['response']}")
        print(f"PLAN STEP: {res['plan'][0]['action']} -> {res['plan'][0]['parameters']}")
        print(f"EXEC STATUS: {res['execution_results'][0]['status']}")
    except Exception as e:
        print(f"FAILED query '{q}': {e}")
        import traceback
        traceback.print_exc()

print("\nTesting Persistence...")
agent.memory.add_interaction("user", "TEST_PERSISTENCE_MARKER")
agent.memory._save_to_disk()

print("Creating new agent instance...")
agent2 = AgenticAIAssistant()
history = agent2.get_conversation_history()
found = any("TEST_PERSISTENCE_MARKER" in x["content"] for x in history)
if found:
    print("PERSISTENCE SUCCESS: Marked interaction found in new instance.")
else:
    print("PERSISTENCE FAILED: Marked interaction NOT found.")
