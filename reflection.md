# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

Three Core Actions User Should Be Able To Perform: 
- Register a pet, including adding care needs for the pet with frequency and priority.
- See a task list/daily schedule and be able to mark tasks complete.
- Be able to input your availability so tasks can be scheduled around your schedule but in a way the pet's priorities are taken care of.

Brainstorm of Main Objects: 
- Pet
- Task
- User's Schedule Items
- Day (Schedule)

Main Objects with Attributes + Methods
- Pet (Name, Species, Age, Care_Tasks) [UpdateAge, GetAllTasks, AddCareTask, RemoveCareTask]
- Task (Name, Type, Priority, Duration, Frequency, Time_Preference, Status) [AssignPriority, AssignDuration, AssignFrequency, AssignTimePreference, MarkComplete, MarkIncomplete]
- Owner (Name, Availability) [AddAvailability, GetFreeSlots]
- AvailabilityBlock (Label, Start_Time, End_Time, Frequency) [UpdateStart, UpdateEnd, AddFrequency]
- ScheduledTask (Task, Start_Time, End_Time, Is_Complete) [MarkComplete, UpdateStart, UpdateFinish]
- DayPlan (Date, Owner, Pet, Scheduled_Tasks) [AddTask, GetCompletionStatus, Display]
- Scheduler (Owner, Pet, Date, Day_Start, Day_End) [BuildSchedule, PrioritizeTasks, FindAvailableSlot, ExplainPlan]



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
