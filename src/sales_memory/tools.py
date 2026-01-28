"""
Sales Meeting Tools

Custom tools for the Sales Meeting Memory Agent that interact with
the customer database to retrieve and store relationship data.
"""

import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from uuid import uuid4

from agno.tools import Toolkit, tool


class SalesMeetingTools(Toolkit):
      """
          Tools for managing customer relationships and sales interactions.

                  These tools allow the agent to:
                      - Query customer and contact information
                          - Log new interactions
                              - Create and update insights
                                  - Analyze relationship patterns
                                      """

    def __init__(self, db_connection=None):
              super().__init__(name="sales_meeting_tools")
              self.db = db_connection

    @tool
    def get_customer_context(
              self,
              customer_name: str,
              include_interactions: bool = True,
              interaction_limit: int = 5,
    ) -> str:
              """
                      Retrieve comprehensive context for a customer.

                                      Args:
                                                  customer_name: Company name to look up
                                                              include_interactions: Include recent interaction history
                                                                          interaction_limit: Max number of interactions to return

                                                                                          Returns:
                                                                                                      JSON string with customer data, contacts, and recent interactions
                                                                                                              """
              # In production, this would query the actual database
              # This is a demonstration of the tool interface

        query = """
                SELECT 
                            c.id, c.company_name, c.industry, c.company_size, c.annual_revenue,
                                        json_agg(DISTINCT jsonb_build_object(
                                                        'name', ct.name,
                                                                        'title', ct.title,
                                                                                        'email', ct.email,
                                                                                                        'is_decision_maker', ct.is_decision_maker
                                                                                                                    )) as contacts
                                                                                                                            FROM customers c
                                                                                                                                    LEFT JOIN contacts ct ON ct.customer_id = c.id
                                                                                                                                            WHERE LOWER(c.company_name) LIKE LOWER(%s)
                                                                                                                                                    GROUP BY c.id
                                                                                                                                                            """

        # Simulated response for demonstration
        context = {
                      "customer": {
                                        "name": customer_name,
                                        "industry": "Technology",
                                        "size": "500-1000 employees",
                                        "status": "Active Opportunity"
                      },
                      "contacts": [
                                        {
                                                              "name": "Sarah Chen",
                                                              "title": "VP Engineering",
                                                              "is_decision_maker": True,
                                                              "last_contact": "2025-01-10"
                                        }
                      ],
                      "recent_interactions": [
                                        {
                                                              "type": "demo",
                                                              "date": "2025-01-10",
                                                              "summary": "Product demo for engineering team",
                                                              "sentiment": "positive",
                                                              "key_topics": ["integration", "pricing", "timeline"]
                                        }
                      ],
                      "insights": [
                                        {
                                                              "type": "opportunity",
                                                              "text": "Budget approved for Q1 purchase",
                                                              "confidence": 0.85
                                        },
                                        {
                                                              "type": "risk",
                                                              "text": "Also evaluating Competitor X",
                                                              "confidence": 0.70
                                        }
                      ]
        }

        return json.dumps(context, indent=2)

    @tool
    def log_interaction(
              self,
              customer_name: str,
              contact_name: str,
              interaction_type: str,
              summary: str,
              key_topics: List[str],
              sentiment: str = "neutral",
              next_steps: Optional[str] = None,
              competitor_mentions: Optional[List[str]] = None,
              objections_raised: Optional[List[str]] = None,
    ) -> str:
              """
                      Log a new interaction with a customer.

                                      Args:
                                                  customer_name: Company name
                                                              contact_name: Name of the contact spoken with
                                                                          interaction_type: Type of interaction (call, email, meeting, demo)
                                                                                      summary: Brief summary of the interaction
                                                                                                  key_topics: List of topics discussed
                                                                                                              sentiment: Overall sentiment (positive, neutral, concerned)
                                                                                                                          next_steps: Agreed next steps
                                                                                                                                      competitor_mentions: Any competitors mentioned
                                                                                                                                                  objections_raised: Any objections or concerns raised
                                                                                                                                                          
                                                                                                                                                                  Returns:
                                                                                                                                                                              Confirmation message with interaction ID
                                                                                                                                                                                      """
              interaction_id = str(uuid4())[:8]

        # In production, this would insert into the database
              insert_query = """
                      INSERT INTO interactions (
                                  id, customer_id, contact_id, interaction_type, occurred_at,
                                              summary, key_topics, sentiment, next_steps,
                                                          competitor_mentions, objections_raised
                                                                  ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                                                          """

        result = {
                      "status": "logged",
                      "interaction_id": interaction_id,
                      "customer": customer_name,
                      "contact": contact_name,
                      "type": interaction_type,
                      "timestamp": datetime.now().isoformat(),
                      "topics_recorded": key_topics,
                      "insights_extracted": []
        }

        # Auto-extract insights from the interaction
        if objections_raised:
                      for objection in objections_raised:
                                        result["insights_extracted"].append({
                                                              "type": "objection",
                                                              "text": objection
                                        })

                  if competitor_mentions:
                                for competitor in competitor_mentions:
                                                  result["insights_extracted"].append({
                                                                        "type": "competitive_intel",
                                                                        "text": f"Customer mentioned {competitor}"
                                                  })

                            return json.dumps(result, indent=2)

    @tool
    def create_contact(
              self,
              customer_name: str,
              contact_name: str,
              title: Optional[str] = None,
              email: Optional[str] = None,
              is_decision_maker: bool = False,
              notes: Optional[str] = None,
    ) -> str:
              """
                      Create a new contact for a customer.

                                      Args:
                                                  customer_name: Company name
                                                              contact_name: Full name of the contact
                                                                          title: Job title
                                                                                      email: Email address
                                                                                                  is_decision_maker: Whether this person can make purchasing decisions
                                                                                                              notes: Any additional notes about the contact
                                                                                                                      
                                                                                                                              Returns:
                                                                                                                                          Confirmation with new contact ID
                                                                                                                                                  """
              contact_id = str(uuid4())[:8]

        result = {
                      "status": "created",
                      "contact_id": contact_id,
                      "customer": customer_name,
                      "contact": {
                                        "name": contact_name,
                                        "title": title,
                                        "email": email,
                                        "is_decision_maker": is_decision_maker,
                                        "notes": notes
                      },
                      "created_at": datetime.now().isoformat()
        }

        return json.dumps(result, indent=2)

    @tool
    def add_insight(
              self,
              customer_name: str,
              insight_type: str,
              insight_text: str,
              confidence: float = 0.8,
              expires_days: Optional[int] = None,
    ) -> str:
              """
                      Add a new insight about a customer.

                                      Args:
                                                  customer_name: Company name
                                                              insight_type: Type of insight (risk, opportunity, preference, competitive)
                                                                          insight_text: The insight itself
                                                                                      confidence: Confidence level (0.0 to 1.0)
                                                                                                  expires_days: Days until this insight should be considered stale
                                                                                                          
                                                                                                                  Returns:
                                                                                                                              Confirmation with insight ID
                                                                                                                                      """
              insight_id = str(uuid4())[:8]

        expires_at = None
        if expires_days:
                      expires_at = (datetime.now() + timedelta(days=expires_days)).isoformat()

        result = {
                      "status": "added",
                      "insight_id": insight_id,
                      "customer": customer_name,
                      "insight": {
                                        "type": insight_type,
                                        "text": insight_text,
                                        "confidence": confidence,
                                        "expires_at": expires_at
                      },
                      "created_at": datetime.now().isoformat()
        }

        return json.dumps(result, indent=2)

    @tool
    def get_stale_relationships(
              self,
              days_threshold: int = 30,
              min_opportunity_value: Optional[float] = None,
    ) -> str:
              """
                      Find customers that haven't been contacted recently.

                                      Args:
                                                  days_threshold: Days without contact to flag as stale
                                                              min_opportunity_value: Only include opportunities above this value

                                                                              Returns:
                                                                                          List of at-risk customer relationships
                                                                                                  """
              # In production, this would query the database
              query = """
                      SELECT 
                                  c.company_name,
                                              c.industry,
                                                          MAX(i.occurred_at) as last_interaction,
                                                                      COUNT(i.id) as total_interactions,
                                                                                  json_agg(DISTINCT ct.name) as contacts
                                                                                          FROM customers c
                                                                                                  LEFT JOIN interactions i ON i.customer_id = c.id
                                                                                                          LEFT JOIN contacts ct ON ct.customer_id = c.id
                                                                                                                  GROUP BY c.id
                                                                                                                          HAVING MAX(i.occurred_at) < NOW() - INTERVAL '%s days'
                                                                                                                                  ORDER BY MAX(i.occurred_at) DESC
                                                                                                                                          """

        # Simulated response
        stale_relationships = [
                      {
                                        "customer": "TechCorp Inc",
                                        "last_contact": "2024-12-15",
                                        "days_since_contact": 44,
                                        "opportunity_value": 75000,
                                        "primary_contact": "Mike Johnson",
                                        "recommendation": "Schedule check-in call - was interested in Q1 purchase"
                      },
                      {
                                        "customer": "Global Solutions",
                                        "last_contact": "2024-12-20",
                                        "days_since_contact": 39,
                                        "opportunity_value": 120000,
                                        "primary_contact": "Lisa Park",
                                        "recommendation": "Follow up on proposal sent before holiday break"
                      }
        ]

        return json.dumps({
                      "threshold_days": days_threshold,
                      "at_risk_count": len(stale_relationships),
                      "relationships": stale_relationships
        }, indent=2)

    @tool
    def analyze_objection_patterns(
              self,
              time_period_days: int = 90,
              deal_outcome: Optional[str] = None,
    ) -> str:
              """
                      Analyze patterns in objections raised by customers.

                                      Args:
                                                  time_period_days: Days to look back
                                                              deal_outcome: Filter by outcome (won, lost, open)

                                                                              Returns:
                                                                                          Analysis of objection patterns with recommendations
                                                                                                  """
              # In production, this would aggregate from the database
              query = """
                      SELECT 
                                  objection,
                                              COUNT(*) as frequency,
                                                          COUNT(CASE WHEN deal_outcome = 'won' THEN 1 END) as won_after,
                                                                      COUNT(CASE WHEN deal_outcome = 'lost' THEN 1 END) as lost_after
                                                                              FROM interactions i
                                                                                      CROSS JOIN LATERAL jsonb_array_elements_text(i.objections_raised) as objection
                                                                                              WHERE i.occurred_at > NOW() - INTERVAL '%s days'
                                                                                                      GROUP BY objection
                                                                                                              ORDER BY frequency DESC
                                                                                                                      """

        # Simulated analysis
        analysis = {
                      "period": f"Last {time_period_days} days",
                      "total_objections_recorded": 47,
                      "patterns": [
                                        {
                                                              "objection": "Price too high",
                                                              "frequency": 15,
                                                              "win_rate_after": 0.40,
                                                              "recommendation": "Lead with ROI calculator and case studies showing 3x return"
                                        },
                                        {
                                                              "objection": "Integration complexity",
                                                              "frequency": 12,
                                                              "win_rate_after": 0.58,
                                                              "recommendation": "Offer implementation support package and timeline guarantees"
                                        },
                                        {
                                                              "objection": "Need more features",
                                                              "frequency": 8,
                                                              "win_rate_after": 0.25,
                                                              "recommendation": "Share product roadmap and consider design partnership"
                                        },
                                        {
                                                              "objection": "Evaluating competitors",
                                                              "frequency": 7,
                                                              "win_rate_after": 0.57,
                                                              "recommendation": "Focus on differentiation and offer extended trial"
                                        }
                      ]
        }

        return json.dumps(analysis, indent=2)

    @tool
    def get_interaction_timeline(
              self,
              customer_name: str,
              limit: int = 20,
    ) -> str:
              """
                      Get chronological timeline of all interactions with a customer.

                                      Args:
                                                  customer_name: Company name
                                                              limit: Maximum interactions to return

                                                                              Returns:
                                                                                          Chronological list of interactions
                                                                                                  """
              # Simulated timeline
              timeline = {
                            "customer": customer_name,
                            "total_interactions": 8,
                            "first_contact": "2024-09-15",
                            "timeline": [
                                              {
                                                                    "date": "2024-09-15",
                                                                    "type": "email",
                                                                    "contact": "Sarah Chen",
                                                                    "summary": "Initial outreach - showed interest in enterprise features",
                                                                    "rep": "John Smith"
                                              },
                                              {
                                                                    "date": "2024-09-22",
                                                                    "type": "call",
                                                                    "contact": "Sarah Chen",
                                                                    "summary": "Discovery call - discussed pain points with current solution",
                                                                    "rep": "John Smith"
                                              },
                                              {
                                                                    "date": "2024-10-05",
                                                                    "type": "demo",
                                                                    "contact": "Sarah Chen, Mike Lee (CTO)",
                                                                    "summary": "Full product demo - positive reception, questions about Oracle integration",
                                                                    "rep": "John Smith"
                                              },
                                              {
                                                                    "date": "2024-10-20",
                                                                    "type": "meeting",
                                                                    "contact": "Sarah Chen",
                                                                    "summary": "Technical deep-dive on integration capabilities",
                                                                    "rep": "John Smith, Emily Davis (SE)"
                                              },
                                              {
                                                                    "date": "2024-11-10",
                                                                    "type": "email",
                                                                    "contact": "Sarah Chen",
                                                                    "summary": "Sent proposal and pricing",
                                                                    "rep": "John Smith"
                                              },
                                              {
                                                                    "date": "2024-12-01",
                                                                    "type": "call",
                                                                    "contact": "Sarah Chen",
                                                                    "summary": "Budget discussion - approved for Q1, need legal review",
                                                                    "rep": "John Smith"
                                              },
                                              {
                                                                    "date": "2025-01-10",
                                                                    "type": "meeting",
                                                                    "contact": "Sarah Chen, John from IT",
                                                                    "summary": "Final demo with IT team, data residency concerns raised",
                                                                    "rep": "John Smith"
                                              }
                            ]
              }

        return json.dumps(timeline, indent=2)
