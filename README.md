# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate


## Retrieval Test Results

### Retrieval Test 1

**Query:**
What do students say about Katerina Potika's teaching style?

**Top returned chunks:**

1. Source: `rmp_katerina_potika.txt`, chunk 1, distance: 0.627
2. Source: `rmp_katerina_potika.txt`, chunk 0, distance: 0.677

**Why the chunks are relevant:**
The top two chunks are both from Katerina Potika's review document. They directly mention her teaching style, including that the class is lecture-focused, sometimes boring, that she is passionate about Social Networks, and that her PowerPoints may not be very thorough.

**Retrieval judgment:**
Relevant for the top two chunks. The lower-ranked chunks were less useful because they came from other professors.

### Retrieval Test 2

**Query:**  
What do students say about Navrati Saxena's exams?

**Top returned chunks:**  
1. Source: `rmp_navrati_saxena.txt`, chunk 0, distance: 0.620  
2. Source: `rmp_navrati_saxena.txt`, chunk 1, distance: 0.763  
3. Source: `rmp_katerina_potika.txt`, chunk 1, distance: 1.145  

**Why the chunks are relevant:**  
The top returned chunk is directly relevant because it is from Navrati Saxena's review file and specifically says that her exams are manageable, especially if students study the content and attend SI sessions. The second chunk is partially relevant because it is also from Navrati Saxena's file and mentions that SI sessions helped, but it does not directly discuss exams. The third chunk is not relevant because it is about Katerina Potika, not Navrati Saxena.

**Retrieval judgment:**  
Partially relevant. The most important chunk was ranked first and directly answered the question, but one unrelated chunk appeared in the top 3.

### Retrieval Test 3

**Query:**  
Which professor does not respond to emails?

**Top returned chunks:**  
1. Source: `rmp_teng_moh.txt`, chunk 1, distance: 1.041  
2. Source: `rmp_teng_moh.txt`, chunk 0, distance: 1.201  
3. Source: `rmp_mike_wu.txt`, chunk 0, distance: 1.215  

**Why the chunks are relevant:**  
The top two chunks are relevant because both are from Teng Moh's review document and both specifically mention that he does not respond to emails. The third chunk is partially related to the email topic, but it is about Mike Wu being responsive to emails, so it does not answer the question directly.

**Retrieval judgment:**  
Relevant for the top two chunks. The retrieval system correctly ranked the Teng Moh reviews first, but the third chunk shows that semantic search also retrieved an opposite example because it contained similar email-related wording.
---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
