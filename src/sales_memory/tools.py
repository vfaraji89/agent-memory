"""
Insurance Tools for Prixs Client Memory Agent

Database interaction tools for managing client relationships,
policies, and interactions.
"""

import json
from datetime import datetime, timedelta
from typing import Optional, List
from uuid import uuid4

from agno.tools import Toolkit, tool


class InsuranceTools(Toolkit):
          """
              Tools for Prixs insurance operations.

                      Capabilities:
                          - Query client and policy information
                              - Log interactions
                                  - Track renewals
                                      - Monitor relationship health
                                          """

    def __init__(self, db_connection=None):
                  super().__init__(name="insurance_tools")
                  self.db = db_connection

    @tool
    def get_client_context(
                  self,
                  client_name: str,
                  include_policies: bool = True,
                  include_interactions: bool = True,
    ) -> str:
                  """
                          Retrieve client context for meeting preparation.

                                          Args:
                                                      client_name: Client's full name
                                                                  include_policies: Include policy details
                                                                              include_interactions: Include interaction history

                                                                                              Returns:
                                                                                                          JSON with client data, policies, and recent interactions
                                                                                                                  """
                  # Simulated response for demonstration
                  context = {
                      "client": {
                          "name": client_name,
                          "tc_kimlik": "12345678901",
                          "phone": "+90 532 XXX XX XX",
                          "district": "Besiktas",
                          "city": "Istanbul"
                      },
                      "policies": [
                          {
                              "type": "health",
                              "policy_number": "SAG-2024-0012",
                              "premium": 12500,
                              "status": "active",
                              "expires": "2025-03-15"
                          },
                          {
                              "type": "auto",
                              "policy_number": "KAS-2024-0089",
                              "premium": 4200,
                              "vehicle": "Toyota Corolla 2020",
                              "status": "active",
                              "expires": "2025-02-15"
                          }
                      ],
                      "recent_interactions": [
                          {
                              "date": "2025-01-10",
                              "type": "call",
                              "agent": "Ahmet Demir",
                              "summary": "Discussed auto policy renewal, mentioned premium increase concern"
                          }
                      ],
                      "opportunities": [
                          {"type": "life", "reason": "Recently married, no life coverage"},
                          {"type": "home", "reason": "Bought apartment last year"}
                      ]
                  }

        return json.dumps(context, indent=2, ensure_ascii=False)

    @tool
    def log_interaction(
                  self,
                  client_name: str,
                  interaction_type: str,
                  summary: str,
                  topics: List[str],
                  next_steps: Optional[str] = None,
    ) -> str:
                  """
                          Log a client interaction.

                                          Args:
                                                      client_name: Client's full name
                                                                  interaction_type: Type (call, email, meeting, whatsapp)
                                                                              summary: Brief summary
                                                                                          topics: Topics discussed
                                                                                                      next_steps: Agreed follow-ups
                                                                                                              
                                                                                                                      Returns:
                                                                                                                                  Confirmation with interaction ID
                                                                                                                                          """
                  interaction_id = str(uuid4())[:8]

        result = {
                          "status": "logged",
                          "interaction_id": interaction_id,
                          "client": client_name,
                          "type": interaction_type,
                          "timestamp": datetime.now().isoformat(),
                          "topics_recorded": topics,
                          "next_steps": next_steps
        }

        return json.dumps(result, indent=2, ensure_ascii=False)

    @tool
    def get_expiring_policies(
                  self,
                  days_ahead: int = 30,
    ) -> str:
                  """
                          Get policies expiring within specified days.

                                          Args:
                                                      days_ahead: Days to look ahead

                                                                      Returns:
                                                                                  List of expiring policies with client details
                                                                                          """
                  # Simulated response
                  expiring = [
                                    {
                                                          "client": "Mehmet Yilmaz",
                                                          "phone": "+90 532 111 22 33",
                                                          "policy_type": "auto",
                                                          "policy_number": "KAS-2024-0089",
                                                          "expires": "2025-02-15",
                                                          "premium": 4200,
                                                          "days_remaining": 18
                                    },
                                    {
                                                          "client": "Fatma Ozturk",
                                                          "phone": "+90 533 444 55 66",
                                                          "policy_type": "health",
                                                          "policy_number": "SAG-2024-0156",
                                                          "expires": "2025-02-20",
                                                          "premium": 8900,
                                                          "days_remaining": 23
                                    }
                  ]

        return json.dumps({
                          "days_ahead": days_ahead,
                          "count": len(expiring),
                          "policies": expiring
        }, indent=2, ensure_ascii=False)

    @tool
    def get_inactive_clients(
                  self,
                  days_threshold: int = 60,
    ) -> str:
                  """
                          Find clients without recent contact.

                                          Args:
                                                      days_threshold: Days without contact to flag

                                                                      Returns:
                                                                                  List of inactive client relationships
                                                                                          """
                  # Simulated response
                  inactive = [
                                    {
                                                          "client": "Ali Koc",
                                                          "last_contact": "2024-11-15",
                                                          "days_since": 74,
                                                          "policies": ["health", "auto"],
                                                          "total_premium": 18500,
                                                          "recommendation": "Schedule renewal check-in"
                                    },
                                    {
                                                          "client": "Zeynep Aksoy",
                                                          "last_contact": "2024-11-28",
                                                          "days_since": 61,
                                                          "policies": ["health"],
                                                          "total_premium": 9200,
                                                          "recommendation": "Follow up on life insurance interest"
                                    }
                  ]

        return json.dumps({
                          "threshold_days": days_threshold,
                          "count": len(inactive),
                          "clients": inactive
        }, indent=2, ensure_ascii=False)

    @tool
    def add_policy_note(
                  self,
                  client_name: str,
                  note_type: str,
                  note_text: str,
    ) -> str:
                  """
                          Add a note to client record.

                                          Args:
                                                      client_name: Client's full name
                                                                  note_type: Type (opportunity, risk, preference)
                                                                              note_text: Note content

                                                                                              Returns:
                                                                                                          Confirmation with note ID
                                                                                                                  """
                  note_id = str(uuid4())[:8]

        result = {
                          "status": "added",
                          "note_id": note_id,
                          "client": client_name,
                          "type": note_type,
                          "text": note_text,
                          "created_at": datetime.now().isoformat()
        }

        return json.dumps(result, indent=2, ensure_ascii=False)
