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


