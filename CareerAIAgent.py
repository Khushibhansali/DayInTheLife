#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from openai import OpenAI
import json
from typing import List, Dict, Optional
from datetime import datetime

class BaseAgent:
    """Base class for all specialized agents"""
    def __init__(self, client: OpenAI, model: str, role: str):
        self.client = client
        self.model = model
        self.role = role
        self.memory: List[Dict] = []

    def think_and_act(self, prompt: str, context: Dict = None) -> Dict:
        """ReAct pattern: Reason → Act → Observe"""
        messages = [
            {"role": "system", "content": self.get_system_prompt()},
            {"role": "user", "content": self._format_prompt(prompt, context)}
        ]

        response = self._call_model(messages)

        return {
            "agent": self.role,
            "reasoning": response.get("reasoning", ""),
            "action": response.get("content", ""),
            "timestamp": datetime.now().isoformat()
        }

    def _call_model(self, messages: List[Dict]) -> Dict:
        """Internal model call with reasoning extraction"""
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            top_p=0.95,
            max_tokens=1024,
            stream=True,
            extra_body={
                "min_thinking_tokens": 256,
                "max_thinking_tokens": 512
            }
        )

        reasoning = ""
        content = ""

        for chunk in completion:
            r = getattr(chunk.choices[0].delta, "reasoning_content", None)
            if r:
                reasoning += r
            if chunk.choices[0].delta.content:
                content += chunk.choices[0].delta.content

        return {"reasoning": reasoning, "content": content}

    def get_system_prompt(self) -> str:
        raise NotImplementedError

    def _format_prompt(self, prompt: str, context: Dict = None) -> str:
        if context:
            return f"Context: {json.dumps(context)}\n\nTask: {prompt}"
        return prompt


class CareerResearchAgent(BaseAgent):
    """Researches career details and determines what information is needed"""
    def get_system_prompt(self) -> str:
        return """You are a Career Research Agent. Your job:
1. DECIDE if you have enough information about the career to create realistic scenarios
2. If NOT, identify WHAT specific information you need (typical day, common challenges, required skills, tools used)
3. Output your decision and reasoning

Use /think to analyze what's known vs needed. Output JSON:
{"needs_research": true/false, "missing_info": [...], "known_info": {...}}"""


class ScenarioDesignerAgent(BaseAgent):
    """Designs realistic, challenging career scenarios"""
    def get_system_prompt(self) -> str:
        return """You are a Scenario Designer Agent. Create realistic, challenging scenarios for career simulations.

For each scenario, include:
- Realistic problem/situation
- 3-4 decision options with trade-offs
- Hidden complexity that reveals career realities

Use /think to ensure authenticity. Output JSON:
{"scenario": "...", "options": [...], "learning_goal": "..."}"""


class EvaluationAgent(BaseAgent):
    """Evaluates user decisions and determines consequences"""
    def get_system_prompt(self) -> str:
        return """You are an Evaluation Agent. Analyze user decisions in career scenarios.

Consider:
- Immediate consequences
- Long-term implications
- What professionals would actually do
- Skills demonstrated (or lacking)

Use /think to reason about realistic outcomes. Output JSON:
{"consequence": "...", "skills_used": [...], "professional_insight": "..."}"""


class NarratorAgent(BaseAgent):
    """Synthesizes information into engaging narrative"""
    def get_system_prompt(self) -> str:
        return """You are a Narrator Agent. Transform scenario data into immersive storytelling.

Make it feel real and engaging while being educational. Keep responses 2-3 paragraphs.
Use /think to craft compelling narrative that teaches."""


class MultiAgentCareerSimulator:
    """Orchestrator for multi-agent career simulation"""
    def __init__(self, api_key: str):
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key
        )
        self.model = "nvidia/nvidia-nemotron-nano-9b-v2"

        # Initialize specialized agents
        self.research_agent = CareerResearchAgent(self.client, self.model, "Research")
        self.scenario_agent = ScenarioDesignerAgent(self.client, self.model, "Scenario Designer")
        self.evaluator = EvaluationAgent(self.client, self.model, "Evaluator")
        self.narrator = NarratorAgent(self.client, self.model, "Narrator")

        self.career_knowledge: Dict = {}
        self.simulation_state: Dict = {
            "time": "9:00 AM",
            "scenarios_completed": 0,
            "skills_demonstrated": [],
            "current_scenario": None
        }
        self.agent_log: List[Dict] = []

    def start_simulation(self, career: str) -> str:
        """Initialize simulation with agentic research workflow"""
        print(f"\n🤖 [Research Agent] Analyzing career: {career}...")

        # Step 1: Research Agent decides if it needs more info (Agentic RAG)
        research_result = self.research_agent.think_and_act(
            f"Do we have enough information to simulate a day as a {career}? What do we need to know?",
            {"career": career}
        )
        self.agent_log.append(research_result)
        print(f"   Reasoning: {research_result['reasoning'][:100]}...")

        # Parse research needs (in real implementation, this would trigger tool calls)
        self.career_knowledge = {
            "career": career,
            "researched": True,
            "typical_challenges": f"Common challenges for {career}",
            "tools": f"Tools used in {career}"
        }

        # Step 2: Scenario Designer creates first scenario
        print(f"\n🎨 [Scenario Designer] Creating opening scenario...")
        scenario_result = self.scenario_agent.think_and_act(
            f"Design an engaging opening scenario for a {career}'s day at 9 AM",
            self.career_knowledge
        )
        self.agent_log.append(scenario_result)

        # Step 3: Narrator makes it engaging
        print(f"\n📖 [Narrator] Crafting narrative...")
        narrative_result = self.narrator.think_and_act(
            f"Present this scenario engagingly: {scenario_result['action']}",
            {"career": career, "time": "9:00 AM"}
        )
        self.agent_log.append(narrative_result)

        self.simulation_state["current_scenario"] = scenario_result

        return narrative_result['action']

    def process_user_decision(self, user_choice: str) -> str:
        """ReAct loop: Evaluate → Generate consequence → Create next scenario"""
        print(f"\n⚖️ [Evaluator] Analyzing decision...")

        # Step 1: Evaluator analyzes the decision
        eval_result = self.evaluator.think_and_act(
            f"User chose: '{user_choice}'. Evaluate this decision.",
            {
                "scenario": self.simulation_state["current_scenario"],
                "career": self.career_knowledge["career"]
            }
        )
        self.agent_log.append(eval_result)
        print(f"   Reasoning: {eval_result['reasoning'][:100]}...")

        # Update simulation state based on evaluation
        try:
            eval_data = json.loads(eval_result['action'])
            self.simulation_state["skills_demonstrated"].extend(
                eval_data.get("skills_used", [])
            )
        except:
            pass

        # Step 2: Decide if we need a new scenario or continue current one
        print(f"\n🎨 [Scenario Designer] Planning next step...")
        self.simulation_state["scenarios_completed"] += 1
        self.simulation_state["time"] = self._advance_time()

        next_scenario = self.scenario_agent.think_and_act(
            f"Create next scenario based on the consequence of user's choice",
            {
                "previous_choice": user_choice,
                "consequence": eval_result['action'],
                "time": self.simulation_state["time"],
                "career": self.career_knowledge["career"]
            }
        )
        self.agent_log.append(next_scenario)

        # Step 3: Narrator weaves it together
        print(f"\n📖 [Narrator] Creating narrative...")
        narrative = self.narrator.think_and_act(
            f"Tell the story of what happened after their choice and introduce the new scenario",
            {
                "choice": user_choice,
                "consequence": eval_result['action'],
                "next_scenario": next_scenario['action']
            }
        )
        self.agent_log.append(narrative)

        self.simulation_state["current_scenario"] = next_scenario

        return narrative['action']

    def _advance_time(self) -> str:
        """Simple time progression"""
        times = ["9:00 AM", "10:30 AM", "12:00 PM", "2:00 PM", "4:00 PM", "5:30 PM"]
        idx = min(self.simulation_state["scenarios_completed"], len(times) - 1)
        return times[idx]

    def generate_summary(self) -> Dict:
        """Multi-agent summary generation"""
        print(f"\n📊 [All Agents] Generating summary...")

        # Each agent contributes to the summary
        eval_summary = self.evaluator.think_and_act(
            "Summarize the skills and decisions demonstrated",
            self.simulation_state
        )

        narrative_summary = self.narrator.think_and_act(
            "Create an engaging summary of the career day experience",
            {
                "state": self.simulation_state,
                "evaluation": eval_summary['action']
            }
        )

        return {
            "career": self.career_knowledge["career"],
            "scenarios_completed": self.simulation_state["scenarios_completed"],
            "skills": list(set(self.simulation_state["skills_demonstrated"])),
            "summary": narrative_summary['action'],
            "agent_interactions": len(self.agent_log)
        }

    def get_agent_log(self) -> List[Dict]:
        """Return full agent interaction log for evaluation/debugging"""
        return self.agent_log


# Multi-agent coordination
def main():
    API_KEY = ""

    simulator = MultiAgentCareerSimulator(API_KEY)

    print("=" * 70)
    print("🎯 MULTI-AGENT CAREER SIMULATION SYSTEM")
    print("   Powered by: Research → Design → Evaluate → Narrate Agents")
    print("=" * 70)

    career = input("\n🎬 What career would you like to experience? ")

    print("\n" + "=" * 70)
    print("🚀 AGENT COLLABORATION IN PROGRESS...")
    print("=" * 70)

    # Multi-agent startup sequence
    opening = simulator.start_simulation(career)

    print("\n" + "=" * 70)
    print("📱 YOUR CAREER DAY BEGINS:")
    print("=" * 70)
    print(opening)

    # Interactive loop with ReAct pattern
    while simulator.simulation_state["scenarios_completed"] < 5:
        print("\n" + "-" * 70)
        user_input = input("\n💬 What do you do? (or 'quit' to end): ").strip()

        if user_input.lower() in ['quit', 'exit', 'end']:
            break

        if not user_input:
            continue

        print("\n" + "=" * 70)
        print("🤖 AGENTS PROCESSING YOUR DECISION...")
        print("=" * 70)

        response = simulator.process_user_decision(user_input)

        print("\n" + "=" * 70)
        print("📱 WHAT HAPPENS NEXT:")
        print("=" * 70)
        print(response)

    # Generate multi-agent summary
    print("\n" + "=" * 70)
    print("🏆 CAREER DAY COMPLETE - GENERATING INSIGHTS...")
    print("=" * 70)

    summary = simulator.generate_summary()

    print(f"\n📊 SUMMARY:")
    print(f"   Career: {summary['career']}")
    print(f"   Scenarios Completed: {summary['scenarios_completed']}")
    print(f"   Skills Demonstrated: {', '.join(summary['skills'][:5])}")
    print(f"   Agent Interactions: {summary['agent_interactions']}")
    print(f"\n{summary['summary']}")

    # Show agent log (useful for hackathon demo)
    print(f"\n🔍 Agent Collaboration Log: {len(simulator.get_agent_log())} interactions")


if __name__ == "__main__":
    main()
