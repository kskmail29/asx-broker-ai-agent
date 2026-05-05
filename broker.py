import os
import uvicorn
from agno.agent import Agent
from agno.os import AgentOS
from agno.models.anthropic import Claude
from agno.tools.yfinance import YFinanceTools

# --- AGENT 1: DATA MINER ---
# Fetches raw price, volume, fundamentals and technical indicators
data_miner = Agent(
    name="Data Miner",
    id="data-miner",
    model=Claude(id="claude-sonnet-4-6"),
    tools=[YFinanceTools(
        stock_price=True,
        stock_fundamentals=True,
        analyst_recommendations=True,
        technical_indicators=True,
    )],
    instructions=[
        "You are a market data specialist covering ASX, NSE India, and US markets.",
        "Ticker suffix rules: ASX stocks → append .AX (e.g. BHP.AX), Indian NSE stocks → append .NS (e.g. RELIANCE.NS), US stocks → no suffix (e.g. AAPL).",
        "Always fetch: current price, volume, 52-week high/low, P/E ratio, and RSI.",
        "Return structured data only — no opinions or recommendations.",
    ],
    markdown=True,
)

# --- AGENT 2: NEWS ANALYST ---
# Fetches and scores news sentiment for given tickers
news_analyst = Agent(
    name="News Analyst",
    id="news-analyst",
    model=Claude(id="claude-sonnet-4-6"),
    tools=[YFinanceTools(stock_news=True)],
    instructions=[
        "You are a financial news analyst covering ASX, NSE India, and US markets.",
        "Ticker suffix rules: ASX → .AX, Indian NSE → .NS, US → no suffix.",
        "Fetch the latest 5 news items per ticker.",
        "For each ticker return: top headlines, overall sentiment (Bullish / Bearish / Neutral), and a one-line sentiment justification.",
        "Return structured news summaries only — no trading recommendations.",
    ],
    markdown=True,
)

# --- AGENT 3: STOCK SCORER ---
# Scores and ranks stocks based on data + news inputs
stock_scorer = Agent(
    name="Stock Scorer",
    id="stock-scorer",
    model=Claude(id="claude-sonnet-4-6"),
    instructions=[
        "You are a quantitative stock scoring engine.",
        "You receive data and news summaries from other agents.",
        "Score each stock out of 10 across three dimensions: Momentum, Fundamentals, and News Sentiment.",
        "Calculate a composite score (weighted average) and rank stocks from highest to lowest.",
        "Return a ranked table with individual dimension scores, composite score, and a one-line justification per stock.",
    ],
    markdown=True,
)

# --- AGENT 4: GLOBAL BROKER (COORDINATOR) ---
# Detects market, delegates to the three specialists, then delivers final recommendations
broker = Agent(
    name="Global Alpha Broker",
    id="global-alpha-broker",
    model=Claude(id="claude-sonnet-4-6"),
    team=[data_miner, news_analyst, stock_scorer],
    instructions=[
        "You are a senior multi-market broker covering ASX (Australia), NSE (India), and US markets.",
        "Follow these steps for every user query:",
        "Step 1 — Market Detection: identify the market from the query. Keywords: 'ASX'/'Australian'/'Australia' → ASX (.AX), 'India'/'NSE'/'Indian' → NSE India (.NS), 'US'/'NYSE'/'NASDAQ'/'American' → US (no suffix). If ambiguous, ask the user to clarify.",
        "Step 2 — Data: delegate to the Data Miner agent with the correctly suffixed tickers.",
        "Step 3 — News: delegate to the News Analyst agent for the same tickers.",
        "Step 4 — Scoring: pass the data and news outputs to the Stock Scorer agent.",
        "Step 5 — Final Report: synthesise all inputs into a professional broker report with: market detected, data summary table, news sentiment, ranked scores, and a final BUY / HOLD / SELL recommendation per ticker with a confidence level (High / Medium / Low).",
        "Always state the market being analysed at the top of the report.",
        "Format the entire output in clean markdown.",
    ],
    markdown=True,
)

agent_os = AgentOS(agents=[broker, data_miner, news_analyst, stock_scorer])
app = agent_os.get_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
