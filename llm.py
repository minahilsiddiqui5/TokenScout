from groq import Groq

class LLMClient:
    def __init__(self, api_key, ledger):
        self.client = Groq(api_key=api_key)
        self.ledger = ledger

    def complete(self, prompt, model, step, max_tokens=800):
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
        )
        usage = response.usage
        # har call ka hisaab khud ledger mein daal do
        self.ledger.record(step, model, usage.prompt_tokens, usage.completion_tokens)
        return response.choices[0].message.content


# Test ke liye
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from ledger import CostLedger

    load_dotenv()
    ledger = CostLedger(budget_usd=0.01)
    llm = LLMClient(api_key=os.getenv("GROQ_API_KEY"), ledger=ledger)

    answer = llm.complete(
        "Explain prompt caching in one sentence.",
        model="llama-3.1-8b-instant",
        step="test",
    )
    print(answer)
    ledger.summary()