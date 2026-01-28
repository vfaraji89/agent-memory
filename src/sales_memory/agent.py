"""
Prixs Client Memory Agent

Context-aware AI assistant for insurance agents at Prixs, Istanbul.
Manages client relationships with persistent database memory.
"""

from typing import Optional
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.db.sqlite import SqliteDb

from .tools import InsuranceTools
from .prompts import INSURANCE_AGENT_INSTRUCTIONS


def create_insurance_agent(
          db_url: Optional[str] = None,
          use_sqlite: bool = False,
          sqlite_path: str = "prixs_memory.db",
          num_history_runs: int = 5,
          enable_session_summaries: bool = True,
) -> Agent:
          """
              Create Prixs insurance agent with persistent database storage.

                      Args:
                              db_url: PostgreSQL connection string
                                      use_sqlite: Use SQLite for development
                                              sqlite_path: Path to SQLite database
                                                      num_history_runs: Previous interactions to include in context
                                                              enable_session_summaries: Auto-summarize long conversations

                                                                      Returns:
                                                                              Configured Agent with database memory and insurance tools
                                                                                  """

    if use_sqlite:
                  db = SqliteDb(db_file=sqlite_path)
else:
              if not db_url:
                                raise ValueError("db_url required when not using SQLite")
                            db = PostgresDb(db_url=db_url)

    agent = Agent(
                  name="PrixsInsuranceAgent",
                  db=db,
                  add_history_to_context=True,
                  num_history_runs=num_history_runs,
                  enable_session_summaries=enable_session_summaries,
                  tools=[InsuranceTools()],
                  instructions=INSURANCE_AGENT_INSTRUCTIONS,
                  markdown=True,
    )

    return agent


class PrixsInsuranceAgent:
          """
              Insurance agent assistant for Prixs.

                      Features:
                          - Pre-meeting client briefings
                              - Post-meeting interaction logging
                                  - Policy renewal tracking
                                      - Client relationship monitoring
                                          """

    def __init__(
                  self,
                  db_url: Optional[str] = None,
                  use_sqlite: bool = False,
                  sqlite_path: str = "prixs_memory.db",
    ):
                  self.agent = create_insurance_agent(
                                    db_url=db_url,
                                    use_sqlite=use_sqlite,
                                    sqlite_path=sqlite_path,
                  )

    def get_client_brief(
                  self,
                  client_name: str,
                  agent_id: Optional[str] = None,
    ) -> str:
                  """
                          Generate pre-meeting briefing for a client.

                                          Args:
                                                      client_name: Client's full name
                                                                  agent_id: Insurance agent's ID

                                                                                  Returns:
                                                                                              Formatted briefing with policies, history, and opportunities
                                                                                                      """
                  prompt = f"Meeting with {client_name} coming up. Give me a briefing."
                  session_id = f"brief_{agent_id}_{client_name}".lower().replace(" ", "_")

        response = self.agent.run(prompt, session_id=session_id)
        return response.content

    def log_interaction(
                  self,
                  client_name: str,
                  notes: str,
                  agent_id: Optional[str] = None,
    ) -> str:
                  """
                          Log a client interaction and extract insights.

                                          Args:
                                                      client_name: Client's full name
                                                                  notes: Free-form meeting notes
                                                                              agent_id: Insurance agent's ID

                                                                                              Returns:
                                                                                                          Confirmation with extracted data and next steps
                                                                                                                  """
                  prompt = f"""Log this interaction with {client_name}:

          {notes}

          Extract key information, identify opportunities, and suggest next steps."""

        session_id = f"log_{agent_id}_{client_name}".lower().replace(" ", "_")

        response = self.agent.run(prompt, session_id=session_id)
        return response.content

    def get_renewals(
                  self,
                  days_ahead: int = 30,
                  agent_id: Optional[str] = None,
    ) -> str:
                  """
                          Get policies expiring soon.

                                          Args:
                                                      days_ahead: Days to look ahead
                                                                  agent_id: Filter by specific agent

                                                                                  Returns:
                                                                                              List of expiring policies with client details
                                                                                                      """
                  prompt = f"Which policies expire in the next {days_ahead} days?"
                  session_id = f"renewals_{agent_id or 'all'}"

        response = self.agent.run(prompt, session_id=session_id)
        return response.content

    def get_inactive_clients(
                  self,
                  days_threshold: int = 60,
    ) -> str:
                  """
                          Find clients without recent contact.

                                          Args:
                                                      days_threshold: Days without contact to flag

                                                                      Returns:
                                                                                  At-risk client relationships
                                                                                          """
                  prompt = f"Which clients haven't been contacted in {days_threshold}+ days?"

        response = self.agent.run(prompt, session_id="inactive_clients")
        return response.content


if __name__ == "__main__":
          # Development setup
          agent = PrixsInsuranceAgent(use_sqlite=True)

    # Example: Pre-meeting brief
    brief = agent.get_client_brief(
                  client_name="Mehmet Yilmaz",
                  agent_id="ahmet_demir"
    )
    print(brief)
