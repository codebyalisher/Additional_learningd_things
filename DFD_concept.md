**little bit examples with hint and flow diagram**
want the output to always look like this:

**OVERALL FUNCTIONALITY**

```python
What the feature does
What data it works on
What structure holds the data
```

**STEPS**

**Step-by-step execution order**

**CODE CALLING STRUCTURE**

```python
Function A calls Function B

Function B prepares data

Function C executes action

With parameters shown
```
**DATA HOLDER / STRUCTURE**

```python
A class or object that stores intermediate data

FLOW DIRECTION

Top → Bottom execution

Bottom → Top return
```
<br>
This is implementation-thinkingFEATURE: Send Notifications  <br>

═══════════════════════════════════════════════════════════════<br>
**1. OVERALL CONCEPT** <br>
═══════════════════════════════════════════════════════════════<br>
We need to SEND NOTIFICATIONS → for USERS/TEAMS/DEPTS/COMPANIES → by COLLECTING TARGETS AND CREATING SINGLE DB RECORD <br>

═══════════════════════════════════════════════════════════════<br>
**2. STEPS** <br>
═══════════════════════════════════════════════════════════════ <br>
1. Receive event trigger (task updated, ticket created, etc.)-->this will call the send notification function and send notification will call the collect targets by passing the inputs which are being passed to the send notification from the route/front end or query.
2. Collect all target recipients (users, teams, depts, companies)-->this will be using the strcutre or defined dtype whatever dtype we wll define 
3. Apply flags (include_managers=True, etc.)
4. Create single notification record with all targets in arrays -->here this function wll be using our data that we have collected using our structure or function using the strcture <br>

═══════════════════════════════════════════════════════════════<br>
**3. CODE CALLING STRUCTURE** <br>
═══════════════════════════════════════════════════════════════ <br>
from top to bottom and for bottom to top to understand clearly our logic<br>
task_routes.py (Entry)<br>
    │ <br>
    │ calls with: (db, task, current_user, assignees)<br>
    ▼ <br>
NotificationTargets() ← Data holder class <br>
    │ <br>
    │ methods: add_user(id), add_team(id), add_assignees(list) <br>
    ▼ <br>
collect_targets(db, current_user_id, owner_id, creator_id, assignees, flags...) <br>
    │ <br>
    │ returns: NotificationTargets (populated) <br>
    ▼ <br>
create_notification_sync(db, type, targets, data, task_id, company_id) <br>
    │ <br>
    │ input: NotificationTargets + notification metadata <br>
    ▼ <br>
Notification record in DB (single row with arrays <br>

```md
# Reusable Prompt — Data-First Build Standard

Approach this work using a data-first thinking standard. Before writing or designing any code, fully understand the data the feature deals with: its source, its shape, how it flows, and what it means. Code is only the vehicle for moving and reshaping data — once the data is understood, the structure of the code should fall out naturally.

## Step 1 — Understand the source data

- Where does the data come from?  
  API, DB, stream, file, queue, user input, another service

- What is its raw format and shape?  
  Capture a real concrete example before starting.

- Is it streamed or batched?
- Ordered or unordered?
- Idempotent or not?
- Can it be lost, duplicated, delayed, or arrive partially?
- What is the volume and frequency?

## Step 2 — Understand the target shape

- What do downstream consumers actually need?  
  UI, DB write, cache update, another service, response payload

- What fields are required vs optional?
- What is the right level of abstraction?
  - Should the consumer know the origin?
  - Or should it see a clean domain type?

- Sketch the target shape with a concrete example before writing any class or function.

## Step 3 — List the transformations between source and target

- Parse / decode raw input into structured form
- Validate inputs and reject what doesn’t belong
- Filter out events / rows / records that aren’t relevant
- Reshape fields:
  - rename
  - compute derived values
  - normalize

- Enrich with related data:
  - lookups
  - joins
  - cached metadata

- Route / fan out / aggregate
- Persist or hand off

Each transformation should become one well-named function, class, or method — never a single mega-function that does several stages at once.

## Step 4 — Decide where state lives

- State that must survive process restarts → persistent storage  
  DB, Redis, file

- State that must survive only this run → in-memory cache
- State that lives only for one event → local variables

Choose storage based on how long the data must last, not on what feels convenient.

## Step 5 — Plan for failure as a data problem

- What if the source goes away mid-flow?
- What if a downstream consumer is slow, missing, or crashes?
- What if a previous run left stale state behind?
- What if the same event is delivered twice?

For each failure, define how the data survives, resumes, or gets safely dropped without corruption.

## Step 6 — Only then, design components

Map answers to structure:

- Boundary types and contracts → dataclasses, Pydantic models, schemas
- Source → consumer translators → decoder / parser / mapper classes
- Expensive lookups → cache classes
- Multiple downstream consumers → router / dispatcher / event bus
- Shared business rules → service classes / utils modules
- Long-running orchestration → coordinator class with a clear lifecycle
- State that persists → small dedicated persistence helpers

## Step 7 — Build in safe increments

Build in the order that lets you prove correctness at each step:

1. Print or log the raw input. Confirm it arrives in the expected shape.
2. Decode / parse it into a structured type. Confirm one example end-to-end.
3. Apply filters and transformations on real data. Confirm with edge cases.
4. Hook in consumers: handlers, DB writes, responses. Confirm side effects fire.
5. Add persistence / state. Restart the process and confirm correct resumption.
6. Add reconnect / retry / timeout logic. Force failures and confirm recovery.
7. Add hardening:
   - validation
   - idempotency
   - safety valves
   - observability

## Working Rules

- Never start with “let me write a class.” Start with “what does the data look like.”
- Never design abstractions before the data shape is fully understood.
- Prefer many small components, each tied to one data shape change.
- Prefer Pydantic / typed models over manual parsing helpers when possible.
- Keep transformations pure where they can be — no DB or IO inside a decoder/mapper.
- Keep coordination thin — the top-level orchestrator should read like the data flow itself.
- Reserve persistence only for state that genuinely must outlive the process.
- Treat error handling as part of the data flow, not as an afterthought.

## Report Back With

- The raw input shape with a real example
- The target output shape with a real example
- The list of transformation stages between them
- Which components own which stage
- Where state lives and why
- What failure modes are handled and how the data survives them
```
