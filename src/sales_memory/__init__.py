"""
Sales Memory - A context-aware AI assistant for sales teams.

This package provides a database-backed memory agent that helps sales teams
maintain perfect recall of customer relationships and interactions.
"""

from .agent import SalesMeetingAgent, create_sales_agent
from .tools import SalesMeetingTools
from .prompts import SALES_AGENT_INSTRUCTIONS

__version__ = "0.1.0"
__all__ = [
      "SalesMeetingAgent",
      "create_sales_agent", 
      "SalesMeetingTools",
      "SALES_AGENT_INSTRUCTIONS",
]
