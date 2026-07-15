# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Terminal output from running `py main.py`:

```
Today's Schedule
================
8:00 AM - Mochi: Morning walk (30 min, daily)
9:00 AM - Luna: Breakfast feeding (10 min, daily)
6:30 PM - Mochi: Evening medication (5 min, daily)
```

## Testing PawPal+

```bash
python -m pytest
```

The automated tests verify the core PawPal+ system behaviors: task completion status, adding tasks to pets, sorting scheduled tasks in chronological order, handling tasks without scheduled times, filtering by pet and completion status, recurring daily and weekly tasks, non-recurring task behavior, conflict detection for duplicate times, and empty schedules for pets with no tasks.

Successful test run:

```
============================= test session starts =============================
platform win32 -- Python 3.13.14, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\danie\Downloads\Project PawPal+\ai110-module2show-pawpal-starter
configfile: pytest.ini
testpaths: tests
plugins: anyio-4.14.2
collected 12 items

tests\test_pawpal.py ............                                        [100%]

============================== warnings summary ===============================
..\..\..\AppData\Local\Programs\Python\Python313\Lib\site-packages\_pytest\cacheprovider.py:469
  C:\Users\danie\AppData\Local\Programs\Python\Python313\Lib\site-packages\_pytest\cacheprovider.py:469: PytestCacheWarning: could not create cache path C:\Users\danie\Downloads\Project PawPal+\ai110-module2show-pawpal-starter\.pytest_cache\v\cache\nodeids: [WinError 5] Access is denied: 'C:\\Users\\danie\\Downloads\\Project PawPal+\\ai110-module2show-pawpal-starter\\.pytest_cache\\v\\cache'
    config.cache.set("cache/nodeids", sorted(self.cached_nodeids))

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 12 passed, 1 warning in 0.04s ========================
```

Confidence Level: ★★★★☆ (4/5). The core scheduling logic is reliable based on the passing automated tests, with the remaining risk being that the suite focuses on system logic rather than full Streamlit UI behavior.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks by `scheduled_time` so the daily schedule prints from earliest to latest. Tasks without a time are placed at the end. |
| Filtering | `Scheduler.filter_tasks()` | Filters by completion status with `completed=True` or `completed=False`, and filters by pet name with `pet_name="Mochi"`. |
| Conflict handling | `Scheduler.detect_conflicts()` | Groups pending tasks by exact scheduled time and returns warning messages when two or more tasks share the same time. |
| Recurring tasks | `Task.next_due_date()`, `Scheduler.mark_task_complete()` | Uses `timedelta` to calculate the next daily or weekly due date, then creates a new pending task for the same pet. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
