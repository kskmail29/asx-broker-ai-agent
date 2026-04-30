from agno.agent import Agent
from agno.os import AgentOS
from agno.models.anthropic import Claude
from agno.tools.yfinance import YFinanceTools

# 1. Define your agent logic
agent = Agent(
    name="ASX Alpha Broker",
    model=Claude(id="claude-sonnet-4-6"),
    tools=[YFinanceTools()],
    instructions=[
        "You are a senior ASX analyst.",
        "Always append .AX to Australian stock tickers.",
        "Provide insights on volume and RSI when possible."
    ],
    markdown=True
)

# 2. Wrap the agent in AgentOS to enable the Agno features (UI, monitoring, etc.)
agent_os = AgentOS(agents=[agent])

# 3. This is the crucial fix: use the .get_app() method
app = agent_os.get_app()
