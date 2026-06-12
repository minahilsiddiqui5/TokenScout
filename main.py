import argparse
import os
from datetime import datetime
from dotenv import load_dotenv

from ledger import CostLedger
from llm import LLMClient
from agent import ResearchAgent


def main():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("GROQ_API_KEY nahi mili — .env file check karo.")
        return

    parser = argparse.ArgumentParser(description="TokenScout — budget-aware research agent")
    parser.add_argument("topic", nargs="+", help="research topic")
    parser.add_argument("--budget", type=float, default=0.02, help="max spend in USD")
    parser.add_argument("--rounds", type=int, default=1, help="self-critique rounds")
    args = parser.parse_args()

    topic = " ".join(args.topic)

    ledger = CostLedger(budget_usd=args.budget)
    llm = LLMClient(api_key=api_key, ledger=ledger)
    agent = ResearchAgent(llm, ledger)

    print(f"\n=== TokenScout ===\nTopic : {topic}\nBudget: ${args.budget:.4f}\n" + "-" * 40)

    report = agent.run(topic, reflection_rounds=args.rounds)

    print("\n========== REPORT ==========\n")
    print(report)
    ledger.summary()

    filename = f"report_{datetime.now():%Y%m%d_%H%M%S}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {topic}\n\n{report}\n")
    print(f"\nReport saved: {filename}")


if __name__ == "__main__":
    main()