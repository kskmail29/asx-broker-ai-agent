import os
import uvicorn
from agno.agent import Agent
from agno.os import AgentOS
from agno.models.anthropic import Claude
from agno.tools.yfinance import YFinanceTools

agent = Agent(
    name="ASX Alpha Broker",
    id="asx-alpha-broker",
    model=Claude(id="claude-sonnet-4-6"),
    tools=[YFinanceTools()],
    instructions=[
        "You are a senior ASX analyst.",
        "Always append .AX to Australian stock tickers.",
        "Provide insights on volume and RSI when possible."
    ],
    markdown=True
)

agent_os = AgentOS(agents=[agent])
app = agent_os.get_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
