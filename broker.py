import os
import json
import uvicorn
from datetime import datetime
from urllib.parse import parse_qs

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from agno.agent import Agent
from agno.os import AgentOS
from agno.models.anthropic import Claude
from agno.tools.yfinance import YFinanceTools

# --- LOGGING SETUP ---
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)


class PromptLogger(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "POST" and "/runs" in request.url.path:
            body_bytes = await request.body()
            try:
                message = json.loads(body_bytes).get("message", "")
            except Exception:
                message = parse_qs(body_bytes.decode("utf-8", errors="replace")).get("message", [""])[0]

            if message:
                log_path = os.path.join(LOG_DIR, f"prompts_{datetime.now().strftime('%Y-%m-%d')}.log")
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now().isoformat()}] {request.url.path}\n")
                    f.write(f"PROMPT: {message}\n")
                    f.write("-" * 80 + "\n")

        return await call_next(request)


# --- BROKER AGENT ---
broker = Agent(
    name="Global Alpha Broker",
    id="global-alpha-broker",
    model=Claude(id="claude-sonnet-4-6", max_tokens=1500),
    tools=[YFinanceTools()],
    instructions=[
        "You are a senior broker covering ASX, NSE India, and US markets.",
        "Ticker rules: ASX/Australian → append .AX | India/NSE → append .NS | US/NYSE/NASDAQ → no suffix. Multiple markets: analyse each. Ambiguous market: ask user.",
        "For each ticker: fetch price, volume, 52W high/low, P/E, RSI, analyst recommendations, and latest news.",
        "Score each stock /10 on Momentum (RSI, price trend, volume), Fundamentals (P/E, analyst ratings), and News Sentiment. Composite: Momentum 40%, Fundamentals 35%, Sentiment 25%. Rank all.",
        "Output a markdown report: 1) Market detected 2) Data table (ticker, price, volume, RSI, P/E) 3) News sentiment per ticker 4) Scored rankings table 5) BUY/HOLD/SELL per ticker with High/Medium/Low confidence.",
    ],
    markdown=True,
)

agent_os = AgentOS(agents=[broker])
app = agent_os.get_app()
app.add_middleware(PromptLogger)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
