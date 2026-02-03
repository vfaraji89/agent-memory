# Prixs Client Memory Agent

Context-aware AI assistant for insurance agents at Prixs, Istanbul.

**For:** As ACME Company Insurance teams managing health, auto, home, and life policies across Turkey.

---

## Problem

Insurance agents manage hundreds of client relationships. Context gets lost.

- Agent scrambles through emails, spreadsheets, and notes before client meetings
- - "What policy did we discuss last time?"
  - - "Did they have concerns about premium pricing?"
    - - "What's their family situation for life insurance?"
     
      - **Result:** Clients repeat themselves. Agents miss upsell opportunities. Knowledge walks out when agents leave.
     
      - ---

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

      ---

      ## Database Schema

      ### Clients
      ```sql
      CREATE TABLE clients (
          id UUID PRIMARY KEY,
          name VARCHAR(255) NOT NULL,
          tc_kimlik VARCHAR(11),
          phone VARCHAR(20),
          email VARCHAR(255),
          address TEXT,
          district VARCHAR(100),
          city VARCHAR(100) DEFAULT 'Istanbul',
          created_at TIMESTAMP DEFAULT NOW()
      );
      ```

      ### Policies
      ```sql
      CREATE TABLE policies (
          id UUID PRIMARY KEY,
          client_id UUID REFERENCES clients(id),
          policy_type VARCHAR(50),  -- 'health', 'auto', 'home', 'life', 'travel'
          policy_number VARCHAR(100),
          premium_amount DECIMAL,
          start_date DATE,
          end_date DATE,
          status VARCHAR(20),  -- 'active', 'expired', 'cancelled'
          created_at TIMESTAMP DEFAULT NOW()
      );
      ```

      ### Interactions
      ```sql
      CREATE TABLE interactions (
          id UUID PRIMARY KEY,
          client_id UUID REFERENCES clients(id),
          agent_id UUID,
          interaction_type VARCHAR(50),  -- 'call', 'email', 'meeting', 'whatsapp'
          occurred_at TIMESTAMP,
          summary TEXT,
          topics JSONB,
          sentiment VARCHAR(20),
          next_steps TEXT,
          created_at TIMESTAMP DEFAULT NOW()
      );
      ```

      ---

      ## Key Features

      ### Pre-Meeting Brief
      ```python
      brief = agent.run(
          "Brief me for meeting with Ayse Kaya",
          session_id="meeting_prep_kaya"
      )

      # Output:
      # Ayse Kaya - Kadikoy
      #
      # Current Policies:
      # - Health (Family): 12,500 TL/year, renews March
      # - Auto (Toyota Corolla): 4,200 TL/year
      #
      # Recent Activity:
      # - Called 2 weeks ago about adding dental coverage
      # - Husband started new job, may need updated health plan
      #
      # Opportunities:
      # - Life insurance (2 children, no coverage)
      # - Home insurance (recently bought apartment)
      #
      # Talking Points:
      # 1. Follow up on dental coverage question
      # 2. Review health plan for husband's new employment
      # 3. Introduce life insurance options
      ```

      ### Post-Meeting Log
      ```python
      agent.run(
          """Log meeting with Ayse Kaya:
          Met at Kadikoy office. She wants to add dental to health policy.
          Husband Kemal now works at Garanti Bank. Need to update health plan.
          Interested in life insurance, asked for quote.
          Follow up next week with proposals.""",
          session_id="log_kaya"
      )
      ```

      ### Renewal Alerts
      ```python
      renewals = agent.run(
          "Which policies expire in the next 30 days?",
          session_id="renewal_check"
      )
      ```

      ---

      ## Google Workspace Integration

      ### Gmail
      - Auto-extract client interactions from emails
      - Log correspondence with timestamps
       - Track response rates
         
      ### Calendar
        -Sync meeting schedules
       - Auto-generate pre-meeting briefs
       -  Set renewal reminders
               
       - ### Drive
       - - Store policy documents
       - - Link contracts to client records
        - - Version tracking for proposals
                     
                      - ---

                      >
                      > **Benefits:**
 - Full context control - you decide what the AI sees
 - Zero vendor lock-in - your client data stays yours
 - Query with SQL - build dashboards, run analytics
 - Compliance ready - data residency in Turkey
 - Self-learning - track which briefs led to closed policies
   
                      > ## Project Structure
                      >
                      > ```
                      > agent-memory/
                      > ├── README.md
                      > ├── requirements.txt
                      > ├── src/
                      > │   └── prixs_memory/
                      > │       ├── __init__.py
                      > │       ├── agent.py
                      > │       ├── tools.py
                      > │       └── prompts.py
                      > ├── migrations/
                      > │   └── 001_initial_schema.sql
                      > └── examples/
                      >     ├── pre_meeting_brief.py
                      >     └── renewal_tracking.py
                      > ```
                      >
                      > ---
                      >
                      > ## License
                      >
                      > MIT
                      >
                      > ---
                      >
                      > ## References
                      >
                      > - [Agents Need a Database](https://www.agno.com/blog/agents-need-a-database)
                      > - - [Agno](https://github.com/agno-agi/agno)
