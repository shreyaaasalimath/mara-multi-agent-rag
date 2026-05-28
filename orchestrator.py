import anthropic
import json
import re
import time
import uuid
from datetime import datetime
from agents.finance_agent import FinanceAgent
from agents.research_agent import ResearchAgent
from agents.legal_agent import LegalAgent
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

class Orchestrator:
    def __init__(self):
        print("Initializing MARA System...")
        self.agents = {
            "finance": FinanceAgent(),
            "research": ResearchAgent(),
            "legal": LegalAgent(),
        }
        self.audit_log = []
        self.conversation_history = []
        self.session_id = str(uuid.uuid4())[:8]
        print(f"Session {self.session_id} ready.")

    def route(self, query):
        history_context = ""
        if self.conversation_history:
            history_context = "Recent:\n" + "\n".join(
                [f"Q: {h['query']}" for h in self.conversation_history[-2:]]
            ) + "\n\n"

        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=150,
            messages=[{"role": "user", "content": f"""{history_context}Route this query to the right specialist agents.

Agents:
- finance: stocks, markets, revenue, earnings, crypto, economics, investing, companies, money
- research: AI, machine learning, science, technology, papers, algorithms, physics, biology
- legal: laws, contracts, regulations, GDPR, privacy, employment, IP, compliance, rights

Query: {query}

Return ONLY this JSON:
{{"agents": ["finance"], "reasoning": "one sentence"}}
JSON:"""}]
        )

        raw = msg.content[0].text.strip()
        try:
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            parsed = json.loads(match.group()) if match else {}
            agents = [a for a in parsed.get("agents", []) if a in self.agents]
            reasoning = parsed.get("reasoning", "")
        except Exception:
            agents = list(self.agents.keys())
            reasoning = "Calling all agents"

        if not agents:
            agents = ["finance"]
        return agents, reasoning

    def synthesize(self, query, agent_responses):
        if len(agent_responses) == 1:
            r = agent_responses[0]
            return {
                "answer": r["answer"],
                "synthesis_method": "single_agent_direct",
                "confidence": r["confidence"],
            }

        combined = "\n\n".join([
            f"=== {r['domain'].upper()} ===\n{r['answer']}"
            for r in agent_responses
        ])
        avg_conf = round(sum(r["confidence"] for r in agent_responses) / len(agent_responses))

        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1000,
            system="Synthesize these specialist answers into one clear comprehensive response. Label insights with [Finance], [Research], or [Legal] tags. Be thorough and direct.",
            messages=[{"role": "user", "content": f"Question: {query}\n\nAnswers:\n{combined}\n\nSynthesized answer:"}]
        )

        return {
            "answer": msg.content[0].text,
            "synthesis_method": "multi_agent_synthesis",
            "confidence": max(90, avg_conf),
        }

    def run(self, query):
        run_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().isoformat()
        start = time.time()

        agents_to_call, routing_reasoning = self.route(query)
        agent_responses = [self.agents[a].answer(query, use_memory=True) for a in agents_to_call]
        synthesis = self.synthesize(query, agent_responses)

        total_latency = round(time.time() - start, 2)
        total_tokens = sum(r.get("tokens_used", 0) for r in agent_responses)

        result = {
            "run_id": run_id,
            "session_id": self.session_id,
            "timestamp": timestamp,
            "query": query,
            "routing_reasoning": routing_reasoning,
            "agents_called": agents_to_call,
            "agent_responses": agent_responses,
            "final_answer": synthesis["answer"],
            "synthesis_method": synthesis["synthesis_method"],
            "overall_confidence": synthesis["confidence"],
            "total_latency_sec": total_latency,
            "total_tokens": total_tokens,
        }

        self.audit_log.append({
            "run_id": run_id,
            "timestamp": timestamp,
            "query": query,
            "agents": agents_to_call,
            "latency": total_latency,
            "tokens": total_tokens,
            "confidence": synthesis["confidence"],
        })

        self.conversation_history.append({
            "query": query,
            "answer": synthesis["answer"],
            "agents": agents_to_call,
        })

        return result

    def get_session_stats(self):
        if not self.audit_log:
            return {}
        return {
            "total_queries": len(self.audit_log),
            "avg_latency": round(sum(r["latency"] for r in self.audit_log) / len(self.audit_log), 2),
            "total_tokens": sum(r["tokens"] for r in self.audit_log),
            "avg_confidence": round(sum(r["confidence"] for r in self.audit_log) / len(self.audit_log)),
            "agent_usage": {
                name: sum(1 for r in self.audit_log if name in r["agents"])
                for name in self.agents
            },
        }

    def clear_conversation(self):
        self.conversation_history = []
        for agent in self.agents.values():
            agent.clear_memory()
