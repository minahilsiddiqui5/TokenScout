# Prices for each model, in US dollars per 1 million tokens.
# (Groq is free, but we pretend it costs money so we build cost-discipline.)
# input = price for what we send, output = price for what the model replies.
PRICING = {
    "llama-3.1-8b-instant":    {"input": 0.05, "output": 0.08},
    "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
}


# A class is like a blueprint. This one is a "money tracker" for the agent.
class CostLedger:

    # Runs once when we create a ledger. We give it a budget to start with.
    def __init__(self, budget_usd):
        self.budget_usd = budget_usd   # the spending limit
        self.entries = []              # an empty list to store every call's record

    # Call this after every AI call to log its cost.
    def record(self, step, model, prompt_tokens, completion_tokens):
        # Get this model's price (or 0 if the model isn't in our list)
        rates = PRICING.get(model, {"input": 0, "output": 0})

        # Cost = (input tokens / 1 million) * input price
        #      + (output tokens / 1 million) * output price
        cost = (prompt_tokens / 1_000_000) * rates["input"] + \
               (completion_tokens / 1_000_000) * rates["output"]

        # Save a small record of this call into our list
        self.entries.append({
            "step": step,                                   # name of the step
            "model": model,                                 # which model was used
            "tokens": prompt_tokens + completion_tokens,    # total tokens
            "cost": cost,                                   # how much it cost
        })
        return cost   # give the cost back

    # Add up the cost of every entry = total spent so far
    def spent(self):
        return sum(e["cost"] for e in self.entries)

    # Budget minus what we've spent = how much money is left
    def remaining(self):
        return self.budget_usd - self.spent()

    # The "brake": is there enough money left for one more step?
    def can_afford(self, estimated_cost):
        return self.remaining() >= estimated_cost

    # Print a nice table of all entries + the total
    def summary(self):
        print("\n--- COST LEDGER ---")
        for e in self.entries:
            print(f"{e['step']:10} | {e['model']:25} | {e['tokens']:5} tokens | ${e['cost']:.6f}")
        print(f"TOTAL: ${self.spent():.6f} kharch / ${self.budget_usd:.4f} budget")


# Test only — runs when you run this file directly
if __name__ == "__main__":
    ledger = CostLedger(budget_usd=0.01)                       # make a ledger with $0.01 budget
    ledger.record("plan",  "llama-3.1-8b-instant",    300, 150)   # fake cheap call
    ledger.record("draft", "llama-3.3-70b-versatile", 1500, 800)  # fake expensive call
    ledger.summary()                                            # show the table
    print("Aur $0.005 afford kar sakte hain?", ledger.can_afford(0.005))  # ask the brake