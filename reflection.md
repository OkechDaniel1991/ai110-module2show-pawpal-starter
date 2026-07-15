# PawPal+ Project Reflection

## 1. System Design
The 3 core actions a user hsould be able to perform are: A user should be able to add the owner's name, available care window, and one or more pets. A user should be able to create a pet care tasks. A user should be able to generate and review a daily care plan.  

**a. Initial design**

- Briefly describe your initial UML design.
  Response: The design splits into three layers or packages; the data layer has Owner, Pet, Task entities, and Priority and Recurrence enums. An Owner owns pets, a Pet has tasks, and those are composition relationships, as a Task doesn't exist without a Pet. 
  The Scheduler entity reads an Owner and produces a plan. The Scheduler entity holds the algorithm--reading the Owner and producing the plan. Keeping the Scheduler separate means scheduling can be changed without touching the data classes. The output is Plan, which records three things: what got scheduled, what goit skpped, and a list of reasons. The reasons hold the explanation of choices made. 

**b. Design changes**

- Did your design change during implementation?
Potential bottleneck: Plan.skipped and Plan.reasons are parallel lists. This can become fragile because the skipped task and its reason must always stay aligned by index. A cleaner later design would be a small SkippedTask dataclass or skipped: list[tuple[Task, str]].

- If yes, describe at least one change and why you made it.

Changes: Instead of skipped: list[Task], reasons: list[str],
I'll use: class SkippedTask:
            task: Task
            reason: str

Then, skipped: list[SkippedTask]

The reason is that this will avoid keeping two separate lists in sync.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
