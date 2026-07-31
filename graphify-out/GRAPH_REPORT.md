# Graph Report - /home/rama/Projects/ARK-I  (2026-07-31)

## Corpus Check
- Corpus is ~5,054 words - fits in a single context window. You may not need a graph.

## Summary
- 173 nodes · 326 edges · 12 communities (8 shown, 4 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 36 edges (avg confidence: 0.58)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Tool Schemas|Tool Schemas]]
- [[_COMMUNITY_ARK Core Engine|ARK Core Engine]]
- [[_COMMUNITY_Shared Tools & Controller|Shared Tools & Controller]]
- [[_COMMUNITY_Chat Engine & Sub-Models|Chat Engine & Sub-Models]]
- [[_COMMUNITY_Readme Documentation|Readme Documentation]]
- [[_COMMUNITY_Schedule & Sukoon Tools|Schedule & Sukoon Tools]]
- [[_COMMUNITY_Experts & Schedules|Experts & Schedules]]
- [[_COMMUNITY_Main Tools & Slack|Main Tools & Slack]]
- [[_COMMUNITY_Events Tools|Events Tools]]
- [[_COMMUNITY_EventsGPT Prompt|EventsGPT Prompt]]
- [[_COMMUNITY_ExpertsGPT Prompt|ExpertsGPT Prompt]]

## God Nodes (most connected - your core abstractions)
1. `GetCurrentTime` - 23 edges
2. `CommonTools` - 16 edges
3. `ARK` - 15 edges
4. `MainTools` - 14 edges
5. `EventsTools` - 11 edges
6. `ExpertsTools` - 10 edges
7. `SchedulesTools` - 10 edges
8. `Chat` - 9 edges
9. `SukoonTools` - 9 edges
10. `Controller` - 8 edges

## Surprising Connections (you probably didn't know these)
- `ARKResource` --uses--> `ARK`  [INFERRED]
  app.py → index.py
- `EventsTools` --uses--> `CommonTools`  [INFERRED]
  models/eventsGPT/tools.py → models/common.py
- `ExpertsTools` --uses--> `CommonTools`  [INFERRED]
  models/expertsGPT/tools.py → models/common.py
- `MainTools` --uses--> `CommonTools`  [INFERRED]
  models/main/tools.py → models/common.py
- `SchedulesTools` --uses--> `CommonTools`  [INFERRED]
  models/schedulesGPT/tools.py → models/common.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Hierarchical Model Architecture (MainGPT delegates to specialized sub-models)** — readme_main_model, readme_controller, readme_expertsgpt, readme_schedulesgpt, readme_sukoongpt, readme_eventsgpt, readme_partnersgpt, readme_usergpt [EXTRACTED 1.00]
- **Inter-Model Communication Flow (sub-models invoke each other via Controller)** — readme_controller, readme_schedulesgpt, readme_expertsgpt, readme_sukoongpt, readme_eventsgpt [EXTRACTED 1.00]

## Communities (12 total, 4 thin omitted)

### Community 0 - "Tool Schemas"
Cohesion: 0.18
Nodes (20): BaseModel, GetCurrentTime, GetEventDetails, GetUserRegisteredEvents, GetSarathiSchedules, GetSlots, ExpertsAssistant, GetPreviousCalls (+12 more)

### Community 1 - "ARK Core Engine"
Cohesion: 0.15
Nodes (6): ARKResource, ARK, Input, MainPrompt, Resource, Response

### Community 2 - "Shared Tools & Controller"
Cohesion: 0.17
Nodes (4): datetime, CommonTools, PartnersPrompt, PartnersTools

### Community 3 - "Chat Engine & Sub-Models"
Cohesion: 0.15
Nodes (4): Chat, Model, SukoonPrompt, UserPrompt

### Community 4 - "Readme Documentation"
Cohesion: 0.12
Nodes (20): REST Endpoint POST /ark, ARK-I (Adaptive Resource Kernel - Implementation), Chat Engine (chat/__init__.py), Controller (models/controller.py), EventsGPT (Events and Meetups), ExpertsGPT (Sarathi Expert Management), Flask API Server (app.py, run.py), Function Calling Mechanism with Structured Schemas (+12 more)

### Community 6 - "Experts & Schedules"
Cohesion: 0.21
Nodes (3): ExpertsTools, SchedulesPrompt, Output

### Community 7 - "Main Tools & Slack"
Cohesion: 0.24
Nodes (3): Controller, SlackManager, MainTools

## Knowledge Gaps
- **6 isolated node(s):** `PartnersGPT (Partner Organizations)`, `UserGPT (Conversation Context Analysis)`, `REST Endpoint POST /ark`, `WhatsApp Business API Integration`, `Slack Notifications` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CommonTools` connect `Shared Tools & Controller` to `Events Tools`, `Schedule & Sukoon Tools`, `Experts & Schedules`, `Main Tools & Slack`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Why does `MainTools` connect `Main Tools & Slack` to `Events Tools`, `ARK Core Engine`, `Shared Tools & Controller`, `Schedule & Sukoon Tools`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `GetCurrentTime` (e.g. with `GetEventDetails` and `GetUserRegisteredEvents`) actually correct?**
  _`GetCurrentTime` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `CommonTools` (e.g. with `EventsTools` and `ExpertsTools`) actually correct?**
  _`CommonTools` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `MainTools` (e.g. with `CommonTools` and `Controller`) actually correct?**
  _`MainTools` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `PartnersGPT (Partner Organizations)`, `UserGPT (Conversation Context Analysis)`, `REST Endpoint POST /ark` to the rest of the system?**
  _9 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ARK Core Engine` be split into smaller, more focused modules?**
  _Cohesion score 0.14624505928853754 - nodes in this community are weakly interconnected._