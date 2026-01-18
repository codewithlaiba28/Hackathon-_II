try:
    from agents import Agent, Runner, set_tracing_disabled, set_default_openai_api
    print("agents core imported successfully")
except ImportError as e:
    print(f"FAILED to import agents core: {e}")

try:
    from agents.mcp import MCPServerStdio
    print("agents.mcp imported successfully")
except ImportError as e:
    print(f"FAILED to import agents.mcp: {e}")

try:
    from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
    print("agents.models.openai_chatcompletions imported successfully")
except ImportError as e:
    print(f"FAILED to import OpenAIChatCompletionsModel: {e}")
