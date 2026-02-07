# Prixs Client Memory Agent

Context-aware AI assistant for insurance agents at Prixs, Istanbul.

**For:** As ACME Company Insurance teams managing health, auto, home, and life policies across Turkey.

---

## Problem

Insurance agents manage hundreds of client relationships. Context gets lost.

- Agent scrambles through emails, spreadsheets, and notes before client meetings
  - "What policy did we discuss last time?"
  - "Did they have concerns about premium pricing?"
  - "What's their family situation for life insurance?"
  - **Result:** Clients repeat themselves. Agents miss upsell opportunities. Knowledge walks out when agents leave.

---

## Solution

AI agent with persistent memory that knows your clients better than any individual agent could.

### Workflow

```
1. Agent has meeting with Mehmet Yilmaz in 30 minutes
                    |
2. System retrieves ALL context:
   - Policy history (health, auto, home)
   - Previous claims and renewals
   - Family members and coverage needs
   - Last 5 interactions
                    |
3. Pre-meeting brief generated:
   "Mehmet Yilmaz - Besiktas
    Current: Health + Auto policies
    Renewal: Auto policy expires Feb 15
    Opportunity: Recently married, needs life insurance
    Risk: Complained about premium increase last call"
                    |
4. After meeting, agent logs notes
   System extracts structured data
                    |
5. Memory persists - any agent has full context
```

### Value

| Without Memory | With Memory Agent |
|----------------|-------------------|
| Each conversation starts cold | Every interaction builds context |
| Knowledge in agent's head | Knowledge in your database |
| New agents start from zero | New agents inherit full history |
| Can't analyze patterns | "Why do clients churn after renewal?" |

---

## Architecture

```
+----------------------------------------------------------+
|                    PRIXS INFRASTRUCTURE                   |
+----------------------------------------------------------+
|                                                           |
|   Gmail          Google Calendar       Google Drive       |
|   Integration    Integration           (Documents)        |
|       |               |                    |              |
|       +---------------+--------------------+              |
|                       |                                   |
|              +------------------+                         |
|              |  Memory Agent    |                         |
|              |     (Agno)       |                         |
|              +--------+---------+                         |
|                       |                                   |
|         +-------------+-------------+                     |
|         |             |             |                     |
|    Clients       Interactions    Policies                 |
|    Table         Table           Table                    |
|         |             |             |                     |
|         +-------------+-------------+                     |
|                       |                                   |
|              +--------+---------+                         |
|              |   PostgreSQL     |                         |
|              +------------------+                         |
|                                                           |
+----------------------------------------------------------+
```

---

## Quick Start

```bash
pip install agno psycopg2-binary google-auth google-api-python-client
```

```python
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from prixs_memory import InsuranceTools

db = PostgresDb(db_url="postgresql://user:pass@localhost:5432/prixs_memory")

agent = Agent(
    db=db,
    add_history_to_context=True,
    num_history_runs=5,
    tools=[InsuranceTools()],
    instructions="You are Prixs insurance assistant. Help agents prepare for client meetings and log interactions."
)

# Pre-meeting briefing
response = agent.run(
    "Meeting with Mehmet Yilmaz in 30 minutes. Brief me.",
    session_id="ahmet_demir_meeting_yilmaz"
)
```


- Store policy documents
- Link contracts to client records
- Version tracking for proposals

---

## Benefits

- Full context control - you decide what the AI sees
- Zero vendor lock-in - your client data stays yours
- Query with SQL - build dashboards, run analytics
- Compliance ready - data residency in Turkey
- Self-learning - track which briefs led to closed policies

---

## Project Structure

```
agent-memory/
├── README.md
├── requirements.txt
├── src/
│   └── prixs_memory/
│       ├── __init__.py
│       ├── agent.py
│       ├── tools.py
│       └── prompts.py
├── migrations/
│   └── 001_initial_schema.sql
└── examples/
    ├── pre_meeting_brief.py
    └── renewal_tracking.py
```

---

## License

MIT

