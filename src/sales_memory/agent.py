"""
Sales Meeting Memory Agent

A context-aware AI assistant that gives sales teams perfect recall
of every customer interaction using persistent database memory.
"""

from typing import Optional
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.db.sqlite import SqliteDb

from .tools import SalesMeetingTools
from .prompts import SALES_AGENT_INSTRUCTIONS


def create_sales_agent(
      db_url: Optional[str] = None,
      use_sqlite: bool = False,
      sqlite_path: str = "sales_memory.db",
      num_history_runs: int = 5,
      enable_session_summaries: bool = True,
) -> Agent:
      """
          Create a sales meeting memory agent with persistent database storage.

                  Args:
                          db_url: PostgreSQL connection string (if not using SQLite)
                                  use_sqlite: Use SQLite instead of PostgreSQL (good for development)
                                          sqlite_path: Path to SQLite database file
                                                  num_history_runs: Number of previous interactions to include in context
                                                          enable_session_summaries: Auto-summarize long conversations

                                                                  Returns:
                                                                          Configured Agent with database memory and sales tools
                                                                              """

    # Choose database backend
      if use_sqlite:
                db = SqliteDb(db_file=sqlite_path)
else:
        if not db_url:
                      raise ValueError("db_url required when not using SQLite")
                  db = PostgresDb(db_url=db_url)

    # Create the agent with memory configuration
    agent = Agent(
              name="SalesMeetingAgent",
              db=db,
              add_history_to_context=True,
              num_history_runs=num_history_runs,
              enable_session_summaries=enable_session_summaries,
              tools=[SalesMeetingTools()],
              instructions=SALES_AGENT_INSTRUCTIONS,
              markdown=True,
    )

    return agent


class SalesMeetingAgent:
      """
          High-level wrapper for the Sales Meeting Memory Agent.

                  Provides convenient methods for common sales workflows:
                      - Pre-meeting briefings
                          - Post-meeting logging
                              - Customer insights
                                  - Relationship health monitoring
                                      """

    def __init__(
              self,
              db_url: Optional[str] = None,
              use_sqlite: bool = False,
              sqlite_path: str = "sales_memory.db",
    ):
              self.agent = create_sales_agent(
                            db_url=db_url,
                            use_sqlite=use_sqlite,
                            sqlite_path=sqlite_path,
              )

    def get_meeting_brief(
              self,
              customer_name: str,
              contact_name: Optional[str] = None,
              sales_rep_id: Optional[str] = None,
    ) -> str:
              """
                      Generate a pre-meeting briefing for a customer.

                                      Args:
                                                  customer_name: Company name
                                                              contact_name: Optional specific contact to focus on
                                                                          sales_rep_id: ID of the sales rep requesting the brief

                                                                                          Returns:
                                                                                                      Formatted meeting briefing with context and recommendations
                                                                                                              """
              prompt = f"I have a meeting with {customer_name}"
              if contact_name:
                            prompt += f" ({contact_name})"
                        prompt += " coming up. Give me a comprehensive briefing."

        session_id = f"brief_{sales_rep_id}_{customer_name}".lower().replace(" ", "_")

        response = self.agent.run(prompt, session_id=session_id)
        return response.content

    def log_meeting(
              self,
              customer_name: str,
              meeting_notes: str,
              sales_rep_id: Optional[str] = None,
    ) -> str:
              """
                      Log a meeting and extract structured insights.

                                      Args:
                                                  customer_name: Company name
                                                              meeting_notes: Free-form notes from the meeting
                                                                          sales_rep_id: ID of the sales rep logging the meeting

                                                                                          Returns:
                                                                                                      Confirmation with extracted insights and next steps
                                                                                                              """
        prompt = f"""Log this meeting with {customer_name}:

        {meeting_notes}

        Extract key information, create any new contacts mentioned, 
        identify risks and opportunities, and suggest next steps."""

        session_id = f"log_{sales_rep_id}_{customer_name}".lower().replace(" ", "_")

        response = self.agent.run(prompt, session_id=session_id)
        return response.content

    def get_at_risk_relationships(
              self,
              days_threshold: int = 30,
              sales_rep_id: Optional[str] = None,
    ) -> str:
              """
                      Identify customers that haven't been contacted recently.

                                      Args:
                                                  days_threshold: Days without contact to flag as at-risk
                                                              sales_rep_id: Optional filter for specific rep's customers

                                                                              Returns:
                                                                                          List of at-risk relationships with recommendations
                                                                                                  """
        prompt = f"""Which customers haven't been contacted in {days_threshold}+ days 
        that have open opportunities? Include recommendations for re-engagement."""

        session_id = f"health_check_{sales_rep_id or 'all'}"

        response = self.agent.run(prompt, session_id=session_id)
        return response.content

    def analyze_objections(
              self,
              time_period: str = "last quarter",
    ) -> str:
              """
                      Analyze common objections from lost or stalled deals.

                                      Args:
                                                  time_period: Time period to analyze

                                                                  Returns:
                                                                              Analysis of objection patterns with suggestions
                                                                                      """
        prompt = f"""Analyze the most common objections raised in deals from {time_period}.
        Group by category and provide suggestions for addressing each."""

        response = self.agent.run(prompt, session_id="objection_analysis")
        return response.content

    def get_customer_timeline(
              self,
              customer_name: str,
    ) -> str:
              """
                      Get complete interaction timeline for a customer.

                                      Args:
                                                  customer_name: Company name

                                                                  Returns:
                                                                              Chronological timeline of all interactions
                                                                                      """
        prompt = f"""Show me the complete interaction timeline for {customer_name}.
        Include all meetings, calls, emails, and key milestones."""

        session_id = f"timeline_{customer_name}".lower().replace(" ", "_")

        response = self.agent.run(prompt, session_id=session_id)
        return response.content


# Quick development setup
if __name__ == "__main__":
      # For local development, use SQLite
      agent = SalesMeetingAgent(use_sqlite=True)

    # Example: Get a meeting brief
    brief = agent.get_meeting_brief(
              customer_name="Acme Corp",
              contact_name="Sarah Chen",
              sales_rep_id="john_smith"
    )
    print(brief)
