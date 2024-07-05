def load_system_prompt():
    """load system prompt"""
    system_prompt = """Answer the following questions based on the story below"""

    story = """**Title**: The Mysterious Guest

**Main Character**: Emily, a curious and somewhat cautious event planner.

**Supporting Characters**:
- **Sarah**: Emily's best friend and confidante.
- **John**: Emily's colleague, who is known for his practical jokes.
- **Mrs. Wallace**: An elderly and wise neighbor.
- **Tom**: A new and mysterious visitor in town.

### Scenario 1: The Arrival

**Dialogue**:
- **Sarah**: "Have you heard about the new guy, Tom? Everyone says he might be a famous actor."
- **Emily**: "Really? That’s exciting, but why would someone famous come here without notice?"
- **John**: "Maybe he’s just looking for some peace and quiet?"
- **Emily**: "Perhaps, but it's odd. I'm intrigued."

### Scenario 2: The Meeting

**Dialogue**:
- **Emily** (to Mrs. Wallace): "I’ve organized this small get-together to welcome Tom. I hope he’s as interesting as the rumors suggest."
- **Mrs. Wallace**: "It’s always good to welcome someone with open arms. But remember, people sometimes are not who we think they are."
- **Emily**: "I’ll keep that in mind. I’m just a bit nervous about the whole thing."

### Scenario 3: The Confusion

**Dialogue**:
- **Tom**: "Thank you for the warm welcome, Emily. It’s nice to see such hospitality."
- **Emily**: "We’re glad to have you here. So, what brings you to our town?"
- **Tom**: "Just some quiet time away from the city’s chaos."
- **Emily** (thinking): "He doesn’t act like a celebrity. Maybe I was wrong."

### Scenario 4: The Revelation

**Dialogue**:
- **John**: "I have to confess something, Emily. I started the celebrity rumor about Tom as a joke. He’s just a regular guy."
- **Emily**: "What? Why would you do that, John?"
- **John**: "I thought it’d be funny. I didn’t expect it to go this far."
- **Emily**: "This changes everything. I need to apologize to Tom for the misunderstanding."

### Scenario 5: The Resolution

**Dialogue**:
- **Emily**: "Tom, I owe you an apology. There was a misunderstanding, and I thought you were someone you’re not."
- **Tom**: "That’s quite alright, Emily. I appreciated the warm welcome regardless."
- **Emily**: "I’m glad to hear that. Perhaps we can start over, just as two people getting to know each other?"
- **Tom**: "I’d like that."
"""
    questions = """Scenario 1: The Arrival
Questions
1.What is Emily's initial belief about Tom?

A) Tom is a regular visitor
B) Tom may be a famous actor
C) Tom is a friend of Sarah
D) Tom is John’s relative

2.What emotion does Emily experience upon hearing about Tom?

A) Indifference
B) Confusion
C) Excitement
D) Fear

3.How does Emily's belief about Tom being potentially famous influence her emotion?

A) It makes her nervous
B) It excites her
C) It disappoints her
D) It calms her

Scenario 2: The Meeting
Questions
4.What intention does Emily express about the meeting with Tom?

A) To confront him about his identity
B) To welcome him warmly
C) To ignore the rumors
D) To find out why he is in town

5.How does Emily's emotion from Scenario 1 (excitement) evolve in this scenario?

A) It turns into disappointment
B) It remains stable
C) It changes to nervousness
D) It becomes fear

6.What causes the change in Emily’s emotion from excitement to nervousness?

A) John’s skepticism
B) Mrs. Wallace's warning
C) Sarah’s reassurance
D) Tom’s arrival

Scenario 3: The Confusion
Questions
7.What action does Emily take based on her previous intentions?

A) She cancels the meeting
B) She hosts the welcome event
C) She confronts Tom about the rumors
D) She apologizes immediately

8.How does Emily's belief about Tom change in this scenario?

A) She believes more strongly that he is famous
B) She starts doubting he is a celebrity
C) She confirms he is just a regular visitor
D) She believes he is hiding something

9.What influence does Tom's demeanor have on Emily's belief?

A) It reinforces her original belief
B) It has no effect
C) It makes her doubt her initial belief
D) It confirms all rumors

Scenario 4: The Revelation
Questions
10.What is Emily's emotional response to John’s confession?

A) Happiness
B) Anger
C) Relief
D) Frustration

11.How does the revelation about the joke affect Emily's intention?

A) She intends to continue believing John
B) She intends to end her friendship with John
C) She intends to apologize to Tom
D) She decides to leave the town

12.Which sequence correctly represents how Emily’s emotions led to her intentions?

A) Excitement → Nervousness → Doubt → Frustration → Apology
B) Confusion → Excitement → Doubt → Anger → Reconciliation
C) Curiosity → Fear → Suspicion → Disappointment → Resolution
D) Interest → Anxiety → Confusion → Frustration → Apology

Scenario 5: The Resolution
Questions
13.What action does Emily take based on her intention from Scenario 4?

A) She apologizes to Tom
B) She confronts John
C) She leaves the town
D) She ignores Tom"""

    full_prompt = f"{system_prompt}\n{story}\n{questions}"
    return full_prompt
