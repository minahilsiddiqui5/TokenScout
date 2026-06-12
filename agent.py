import json
from search import web_search
from llm import LLMClient
from ledger import CostLedger

FAST_MODEL = "llama-3.1-8b-instant"
SMART_MODEL = "llama-3.3-70b-versatile"

class ResearchAgent:
    def __init__(self, llm, ledger, num_questions=4):
        self.llm = llm
        self.ledger = ledger
        self.num_questions = num_questions
        self.findings = []

    def plan(self, topic):
        print(f"\n PLAN — '{topic}' ko research sawaalon mein todna")
        prompt = (
            f'Return ONLY a JSON object with one key "questions" containing '
            f'{self.num_questions} specific research questions about the topic. '
            f'No other text.\n\nTopic: {topic}'
        )
        raw = self.llm.complete(prompt, model=FAST_MODEL, step="plan", max_tokens=300)
        try:
            cleaned = raw.replace("```json", "").replace("```", "").strip()
            questions = json.loads(cleaned).get("questions", [])
        except Exception:
            questions = [topic]
        for q in questions:
            print(f"   • {q}")
        return questions

    def research(self, questions):
        print("\n RESEARCH — har sawaal pe search + key points")
        for q in questions:
            results = web_search(q, max_results=4)
            context = "\n".join(f"- {r['title']}: {r['snippet']}" for r in results)
            prompt = (
                f"From these search results, list the 3-4 most important facts "
                f"for the question. Be brief.\n\nQuestion: {q}\n\nResults:\n{context}"
            )
            finding = self.llm.complete(prompt, model=FAST_MODEL, step="extract", max_tokens=400)
            self.findings.append(f"### {q}\n{finding}")
            print(f"   searched: {q[:50]}")

    def draft(self, topic):
        print("\n DRAFT — sab findings se report (strong model)")
        body = "\n\n".join(self.findings)
        prompt = (
            f"Write a clear research briefing on '{topic}' using ONLY these "
            f"findings. Use markdown headings.\n\nFindings:\n{body}"
        )
        return self.llm.complete(prompt, model=SMART_MODEL, step="draft", max_tokens=1000)

    def critique(self, topic, report):
        print("\n CRITIQUE — agent apni hi report ke gaps dhoondta hai")
        prompt = (
            f'Review this research briefing and find the most important gaps. '
            f'Return ONLY a JSON object with key "gaps": a list of up to 2 '
            f'follow-up research questions to fix them. If it is already solid, '
            f'return an empty list.\n\nTopic: {topic}\n\nBriefing:\n{report}'
        )
        raw = self.llm.complete(prompt, model=SMART_MODEL, step="critique", max_tokens=300)
        try:
            cleaned = raw.replace("```json", "").replace("```", "").strip()
            gaps = json.loads(cleaned).get("gaps", [])
        except Exception:
            gaps = []
        for g in gaps:
            print(f"   ↳ gap: {g}")
        return gaps

    def run(self, topic, reflection_rounds=1):
        questions = self.plan(topic)
        self.research(questions)
        report = self.draft(topic)

        for r in range(reflection_rounds):
            if not self.ledger.can_afford(0.002):
                print("\n [budget] reflection ke liye paisa kam — yahin rukte hain")
                break
            gaps = self.critique(topic, report)
            if not gaps:
                print("   report mukammal lag rahi hai — aur khodne ki zaroorat nahi")
                break
            print(f"\n REFINE — round {r+1}: {len(gaps)} gap(s) pe dobara research")
            self.research(gaps)
            report = self.draft(topic)
        return report