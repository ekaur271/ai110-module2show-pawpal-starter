# PawPal+ Project Reflection

## 1. System Design

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

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial brainstorm had 4 objects pet, task, user's schedule items and day or schedule. The idea was pet had to have an entity and each task needed one. I wanted to have the user's scheudle so that would be one and there should be like a day with all its items. After that I mainly just brainstormed basic items and then I talked to claude for a bit. Now its what you see above. The parenthesis are the attributes and the brackets are the methods to mostly set those attributes. 


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yeah but only once, I think I started with a very good setup so it didnt need much change. I think I mostly added the Day start and Day end to scheduler since that was also needed. This particular bottleneck was identified with the help of claude. 

---


## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

Basically we consider the owner's work schedule or busy time, each tasks time preference like morning, afternoon, evening and the priority of the task. Priority matters teh most since those items would be handled with more importance than work. So tasks like feeding or medication gets scheduled before teh lower priority tasks like grooming and stuff. Time preference comes after that to really fit to the app user's life and to make the map more useful overall. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff made is having the scheduler scan for open slots in 15 minute increments. This means that if there is a free window that starts at 8:05 it gets skipped. I feel like for pet care tasks precision of time isn't that essential and 15 minute chunks is ok. 

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
