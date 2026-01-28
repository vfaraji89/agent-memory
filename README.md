# 🧠 Sales Meeting Memory Agent

> A context-aware AI assistant that gives your sales team perfect recall of every customer interaction.
>
> **Built for:** Mid-size companies (500+ employees) who need their sales teams to walk into every meeting fully prepared.
>
> ---
>
> ## The Problem
>
> Your company has 500 employees. Your sales team talks to hundreds of customers every week. But here's what happens:
>
> **Before a meeting:**
> - Sales rep scrambles through Salesforce, emails, Slack, and notes
> - - "Wait, what did we discuss last time?"
>   - - "Did they have concerns about pricing or implementation?"
>     - - "Who else from their team was involved?"
>      
>       - **The result:**
>       - - Customers repeat themselves (and get frustrated)
>         - - Sales reps miss context that could close deals
>           - - Institutional knowledge lives in individual heads, not systems
>             - - When reps leave, customer relationships walk out the door
>              
>               - **The root cause:** Your CRM stores data, but it doesn't surface context. And your AI tools? They don't remember anything between sessions.
>              
>               - ---
>
> ## The Solution: Sales Meeting Memory Agent
>
> An AI agent with **persistent memory** that knows your customers better than any individual rep could.
>
> ### How It Works
>
> ```
> ┌─────────────────────────────────────────────────────────────┐
> │                    SALES REP WORKFLOW                        │
> ├─────────────────────────────────────────────────────────────┤
> │                                                              │
> │  1. Rep has meeting with Acme Corp in 30 minutes            │
> │                     ↓                                        │
> │  2. Agent retrieves ALL context from database:               │
> │     • Last 5 interactions (calls, emails, meetings)          │
> │     • Key stakeholders and their roles                       │
> │     • Open issues and concerns raised                        │
> │     • Purchase history and contract details                  │
> │     • Competitor mentions and alternatives discussed         │
> │                     ↓                                        │
> │  3. Agent generates pre-meeting brief:                       │
> │     "Acme Corp - Sarah Chen (VP Engineering)                 │
> │      Last contact: 3 weeks ago, demo of Enterprise tier      │
> │      Hot button: Integration with their legacy Oracle DB     │
> │      Risk: Also evaluating Competitor X                      │
> │      Opportunity: Budget approved for Q1"                    │
> │                     ↓                                        │
> │  4. After meeting, rep logs notes                            │
> │     Agent extracts and stores structured data                │
> │                     ↓                                        │
> │  5. Memory persists → Next rep has full context              │
> │                                                              │
> └─────────────────────────────────────────────────────────────┘
> ```
>
> ### Why Database-Backed Memory Matters
>
> | Without Memory | With Memory Agent |
> |----------------|-------------------|
> | Each conversation starts cold | Every interaction builds on the last |
> | Context lives in rep's head | Context lives in your database |
> | New reps start from zero | New reps inherit full history |
> | Can't analyze patterns | "Which objections kill deals?" |
> | Vendor lock-in for data | You own your customer data |
>
> ---
>
> ## Architecture
>
> ```
> ┌──────────────────────────────────────────────────────────────┐
> │                     YOUR INFRASTRUCTURE                       │
> ├──────────────────────────────────────────────────────────────┤
> │                                                               │
> │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
> │  │   Slack     │    │   Email     │    │  Calendar   │       │
> │  │  Integration│    │  Integration│    │ Integration │       │
> │  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘       │
> │         │                  │                  │               │
> │         └──────────────────┼──────────────────┘               │
> │                            ↓                                  │
> │                   ┌─────────────────┐                         │
> │                   │  Memory Agent   │                         │
> │                   │    (Agno)       │                         │
> │                   └────────┬────────┘                         │
> │                            │                                  │
> │              ┌─────────────┼─────────────┐                    │
> │              ↓             ↓             ↓                    │
> │     ┌─────────────┐ ┌─────────────┐ ┌─────────────┐          │
> │     │  Customers  │ │Interactions │ │  Insights   │          │
> │     │   Table     │ │   Table     │ │   Table     │          │
> │     └─────────────┘ └─────────────┘ └─────────────┘          │
> │                            │                                  │
> │                   ┌────────┴────────┐                         │
> │                   │   PostgreSQL    │                         │
> │                   │  (Your Database)│                         │
> │                   └─────────────────┘                         │
> │                                                               │
> └──────────────────────────────────────────────────────────────┘
> ```
>
> ---
>
> ## Quick Start
>
> ### Installation
>
> ```bash
> pip install agno psycopg2-binary
> ```
>
> ### Basic Usage
>
> ```python
> from agno.agent import Agent
> from agno.db.postgres import PostgresDb
> from sales_memory import SalesMeetingTools
>
> # Connect to your database
> db = PostgresDb(db_url="postgresql://user:pass@localhost:5432/sales_memory")
>
> # Create the memory-enabled agent
> agent = Agent(
>     db=db,
>     add_history_to_context=True,
>     num_history_runs=5,
>     tools=[SalesMeetingTools()],
>     instructions="""
>     You are a sales meeting assistant with access to our customer database.
>     Before any meeting, retrieve relevant customer context.
>     After meetings, help structure and store new information.
>     """
> )
>
> # Pre-meeting briefing
> response = agent.run(
>     "I have a meeting with Sarah Chen from Acme Corp in 30 minutes. Brief me.",
>     session_id="rep_john_meeting_acme"
> )
> ```
>
> ---
>
> ## Database Schema
>
> ### Customers Table
> ```sql
> CREATE TABLE customers (
>     id UUID PRIMARY KEY,
>     company_name VARCHAR(255) NOT NULL,
>     industry VARCHAR(100),
>     company_size VARCHAR(50),
>     annual_revenue DECIMAL,
>     created_at TIMESTAMP DEFAULT NOW(),
>     updated_at TIMESTAMP DEFAULT NOW()
> );
> ```
>
> ### Contacts Table
> ```sql
> CREATE TABLE contacts (
>     id UUID PRIMARY KEY,
>     customer_id UUID REFERENCES customers(id),
>     name VARCHAR(255) NOT NULL,
>     title VARCHAR(255),
>     email VARCHAR(255),
>     phone VARCHAR(50),
>     is_decision_maker BOOLEAN DEFAULT FALSE,
>     communication_preference VARCHAR(50),
>     notes TEXT,
>     created_at TIMESTAMP DEFAULT NOW()
> );
> ```
>
> ### Interactions Table
> ```sql
> CREATE TABLE interactions (
>     id UUID PRIMARY KEY,
>     customer_id UUID REFERENCES customers(id),
>     contact_id UUID REFERENCES contacts(id),
>     sales_rep_id UUID,
>     interaction_type VARCHAR(50), -- 'call', 'email', 'meeting', 'demo'
>     occurred_at TIMESTAMP,
>     summary TEXT,
>     key_topics JSONB,           -- ['pricing', 'integration', 'timeline']
>     sentiment VARCHAR(20),       -- 'positive', 'neutral', 'concerned'
>     next_steps TEXT,
>     competitor_mentions JSONB,   -- ['Competitor X', 'Competitor Y']
>     objections_raised JSONB,     -- ['price too high', 'integration concerns']
>     created_at TIMESTAMP DEFAULT NOW()
> );
> ```
>
> ### Customer Insights Table
> ```sql
> CREATE TABLE customer_insights (
>     id UUID PRIMARY KEY,
>     customer_id UUID REFERENCES customers(id),
>     insight_type VARCHAR(50),    -- 'risk', 'opportunity', 'preference'
>     insight TEXT,
>     confidence DECIMAL,
>     source_interaction_id UUID REFERENCES interactions(id),
>     created_at TIMESTAMP DEFAULT NOW(),
>     expires_at TIMESTAMP         -- Some insights become stale
> );
> ```
>
> ---
>
> ## Key Features
>
> ### 1. Pre-Meeting Briefings
> ```python
> # The agent retrieves and synthesizes all relevant context
> briefing = agent.run(
>     "Brief me for my 2pm meeting with Acme Corp",
>     session_id="meeting_prep_acme"
> )
>
> # Output:
> # "## Acme Corp - Meeting Brief
> #
> #  **Key Contact:** Sarah Chen, VP Engineering
> #  **Last Interaction:** Demo call 3 weeks ago
> #  **Deal Stage:** Evaluation
> #  **Budget:** $150K approved for Q1
> #
> #  **What They Care About:**
> #  - Integration with Oracle DB (mentioned 3x)
> #  - SOC2 compliance requirements
> #
> #  **Risks:**
> #  - Also evaluating Competitor X
> #  - Previous concern about implementation timeline
> #
> #  **Recommended Talking Points:**
> #  1. Address Oracle integration with case study
> #  2. Share SOC2 certification docs
> #  3. Propose phased implementation to address timeline concerns"
> ```
>
> ### 2. Post-Meeting Logging
> ```python
> # After the meeting, the agent extracts structured data
> agent.run(
>     """Log this meeting: Met with Sarah and her team (John from IT was new).
>     They're ready to move forward but need legal review. Main concern is
>     data residency - they need EU hosting. Sarah mentioned they have to
>     decide by end of month because their current contract expires.""",
>     session_id="meeting_log_acme"
> )
>
> # Agent automatically:
> # - Creates new contact record for John
> # - Logs interaction with structured topics
> # - Creates insight: "Risk - EU data residency requirement"
> # - Creates insight: "Opportunity - Contract expiry creating urgency"
> # - Sets follow-up reminder for legal docs
> ```
>
> ### 3. Relationship Health Monitoring
> ```python
> # Identify at-risk relationships
> at_risk = agent.run(
>     "Which customers haven't we contacted in 30+ days that have open opportunities?",
>     session_id="relationship_health"
> )
> ```
>
> ### 4. Pattern Analysis
> ```python
> # Learn from your data
> patterns = agent.run(
>     "What are the most common objections in deals we lost last quarter?",
>     session_id="loss_analysis"
> )
> ```
>
> ---
>
> ## Why Own Your Database?
>
> From the article that inspired this project:
>
> > "The industry has normalized storing our data in someone else's database... We're paying twice: once for the API call, again for storage and egress."
> >
> > **With this approach:**
> >
> > ✅ **Full context control** - Decide exactly what goes into the AI's context window
> > ✅ **Zero vendor lock-in** - Your customer data stays in your infrastructure
> > ✅ **Query with SQL** - Build dashboards, run analytics, export anytime
> > ✅ **Self-learning loops** - Track which briefings led to closed deals
> > ✅ **Compliance friendly** - Data residency requirements? No problem.
> >
> > ---
> >
> > ## Project Structure
> >
> > ```
> > agent-memory/
> > ├── README.md
> > ├── requirements.txt
> > ├── setup.py
> > ├── src/
> > │   └── sales_memory/
> > │       ├── __init__.py
> > │       ├── agent.py          # Main agent configuration
> > │       ├── tools.py          # Custom tools for sales operations
> > │       ├── schema.py         # Database models
> > │       └── prompts.py        # System prompts and templates
> > ├── migrations/
> > │   └── 001_initial_schema.sql
> > ├── examples/
> > │   ├── pre_meeting_brief.py
> > │   ├── post_meeting_log.py
> > │   └── relationship_analysis.py
> > └── tests/
> >     └── test_agent.py
> > ```
> >
> > ---
> >
> > ## Contributing
> >
> > This project demonstrates database-backed agent memory for sales use cases. Contributions welcome!
> >
> > ---
> >
> > ## License
> >
> > MIT
> >
> > ---
> >
> > ## Inspired By
> >
> > - [Agents Need a Database](https://www.agno.com/blog/agents-need-a-database) - The case for owning your agent's state
> > - - [Agno](https://github.com/agno-agi/agno) - Open-source infrastructure for agents
