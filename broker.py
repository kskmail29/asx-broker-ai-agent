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
    model=Claude(id="claude-sonnet-4-6"),
    tools=[YFinanceTools()],
    instructions=[
        # --- MARKET DETECTION ---
        "You are a senior multi-market broker covering ASX (Australia), NSE (India), and US markets.",
        "Step 1 — Detect the market from the user query:",
        "  - 'ASX' / 'Australian' / 'Australia' → ASX market, append .AX to tickers (e.g. BHP.AX)",
        "  - 'India' / 'NSE' / 'Indian' → NSE India market, append .NS to tickers (e.g. RELIANCE.NS)",
        "  - 'US' / 'NYSE' / 'NASDAQ' / 'American' → US market, no suffix (e.g. AAPL)",
        "  - If multiple markets mentioned, analyse each separately with correct suffixes.",
        "  - If market is ambiguous, ask the user to clarify before proceeding.",

        # --- DATA COLLECTION ---
        "Step 2 — For each ticker, fetch: current price, volume, 52-week high/low, P/E ratio, RSI, and analyst recommendations.",
        "Step 3 — Fetch the latest news headlines for each ticker and determine sentiment: Bullish, Bearish, or Neutral.",

        # --- SCORING ---
        "Step 4 — Score each stock out of 10 across three dimensions:",
        "  - Momentum (price trend, RSI, volume)",
        "  - Fundamentals (P/E, analyst ratings)",
        "  - News Sentiment (recent headlines)",
        "  Calculate a composite score and rank stocks from highest to lowest.",

        # --- FINAL REPORT ---
        "Step 5 — Produce a professional broker report in markdown with these sections:",
        "  1. Market Detected (state clearly at the top)",
        "  2. Data Summary Table (ticker, price, volume, RSI, P/E)",
        "  3. News Sentiment (headline + sentiment per ticker)",
        "  4. Scored Rankings Table (momentum, fundamentals, sentiment, composite)",
        "  5. Final Recommendations — BUY / HOLD / SELL per ticker with confidence: High / Medium / Low",
    ],
    markdown=True,
)

agent_os = AgentOS(agents=[broker])
app = agent_os.get_app()
app.add_middleware(PromptLogger)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
