# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

---

My domain is student reviews of Computer Science professors at San Jose State University. This knowledge is valuable because students often want to know what professors are like before enrolling, including teaching style, grading difficulty, workload, exam format, assignment expectations, and feedback quality. Official course catalogs describe the classes, but they do not show what students actually experience in those classes.

This information is hard to find through official channels because student experiences are spread across unofficial sources such as Rate My Professors reviews. Students often need to compare multiple professors before registration, but the information is unstructured, inconsistent, and time-consuming to search manually. My system will make this professor-review knowledge searchable through natural-language questions.


## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #  | Source             | Description                                                   | URL or location                       |
| -- | ------------------ | ------------------------------------------------------------- | ------------------------------------- |
| 1  | Rate My Professors | Student reviews for David Taylor, SJSU Computer Science       | `data/raw/rmp_david_taylor.txt`       |
| 2  | Rate My Professors | Student reviews for Navrati Saxena, SJSU Computer Science     | `data/raw/rmp_navrati_saxena.txt`     |
| 3  | Rate My Professors | Student reviews for Melody Moh, SJSU Computer Science         | `data/raw/rmp_melody_moh.txt`         |
| 4  | Rate My Professors | Student reviews for Teng Moh, SJSU Computer Science           | `data/raw/rmp_teng_moh.txt`           |
| 5  | Rate My Professors | Student reviews for Chris Pollett, SJSU Computer Science      | `data/raw/rmp_chris_pollett.txt`      |
| 6  | Rate My Professors | Student reviews for Katerina Potika, SJSU Computer Science    | `data/raw/rmp_katerina_potika.txt`    |
| 7  | Rate My Professors | Student reviews for Saptarshi Sengupta, SJSU Computer Science | `data/raw/rmp_saptarshi_sengupta.txt` |
| 8  | Rate My Professors | Student reviews for Mark Stamp, SJSU Computer Science         | `data/raw/rmp_mark_stamp.txt`         |
| 9  | Rate My Professors | Student reviews for Leonard Wesley, SJSU Computer Science     | `data/raw/rmp_leonard_wesley.txt`     |
| 10 | Rate My Professors | Student reviews for Mike Wu, SJSU Computer Science            | `data/raw/rmp_mike_wu.txt`            |

Each raw document will contain the professor name, school, department, source URL, date collected, and copied student review text. I will aim to collect 3–5 useful reviews per professor so that the system has enough information to answer questions about teaching style, workload, exams, grading, helpfulness, and course difficulty.

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 700 characters

**Overlap:** 100 characters

**Reasoning:**

Because my documents are mostly short professor reviews, I will use small-to-medium chunks of about 700 characters with around 100 characters of overlap. This should keep each chunk focused on one professor, course, or student opinion while still preserving enough context to understand the review. I will avoid very large chunks because they may mix unrelated opinions about different professors, and I will avoid very small chunks because they may separate claims from the professor name, course name, or review context.

I will include source metadata with each chunk, including the source filename and chunk index. This matters because every generated answer must include source attribution. If I find during testing that chunks are too short and retrieval returns vague fragments, I will increase the chunk size. If chunks combine too many unrelated reviews, I will reduce the chunk size or switch to paragraph-based chunking.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->


**Embedding model:** `all-MiniLM-L6-v2` through `sentence-transformers`

**Top-k:** 5 chunks per query

**Production tradeoff reflection:**

I will use the `all-MiniLM-L6-v2` embedding model because it runs locally, is free, does not require an API key, and is lightweight enough for this class project. I will store the chunk embeddings in ChromaDB and retrieve the top 5 most similar chunks for each user question.

If I were deploying this system for real students, I would compare embedding models based on retrieval accuracy, latency, cost, context length, and ability to handle informal student language. A larger or newer embedding model might retrieve more accurate results, especially for vague questions or review slang, but it could be slower or more expensive. I would also consider whether the model handles multilingual reviews, abbreviations, professor nicknames, and course numbers well.

---


## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->


| # | Question                                                              | Expected answer                                                                                                                                                                                    |
| - | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | What do students say about David Taylor's teaching style?             | The answer should summarize the specific teaching-style comments found in `rmp_david_taylor.txt`, such as whether students describe him as clear, confusing, lecture-heavy, helpful, or difficult. |
| 2 | What do students say about Navrati Saxena's workload or assignments?  | The answer should describe the workload or assignment expectations mentioned in `rmp_navrati_saxena.txt`, using only the collected reviews.                                                        |
| 3 | Which professor is described as having difficult exams?               | The answer should identify one or more professors whose collected reviews specifically mention difficult exams, and cite the matching source file.                                                 |
| 4 | Which professor is described as helpful or supportive?                | The answer should identify a professor whose reviews mention helpfulness, office hours, responsiveness, or support, and cite the matching source file.                                             |
| 5 | What do students say about Mark Stamp's grading or course difficulty? | The answer should summarize the grading or difficulty comments found in `rmp_mark_stamp.txt`, without adding outside knowledge.                                                                    |

These questions are specific enough to evaluate because each answer should be traceable to one or more collected review files. After I collect the actual review text, I will update the expected answers with more precise ground-truth statements based on the documents.
---  

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->


1. **Noisy or inconsistent review text:**
   Rate My Professors reviews may contain slang, incomplete sentences, emotional opinions, repeated phrases, or comments that mention multiple topics at once. This could make chunking and retrieval less accurate because a single review might discuss exams, workload, grading, and personality together.

2. **Missing or weak source attribution:**
   The system must cite which document an answer came from. If I do not preserve source metadata during chunking and embedding, the generated answer may not be properly grounded. To avoid this, every chunk will include metadata such as source filename and chunk index.

3. **Off-topic retrieval:**
   A user may ask about one professor, but semantic search might retrieve chunks about a different professor if the review language is similar. To reduce this risk, each raw document and chunk should include the professor name clearly.

4. **Insufficient information for some questions:**
   Some professors may have fewer useful reviews or reviews that do not mention specific topics like exams or feedback. In those cases, the system should say it does not have enough information instead of guessing.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

```text
Raw Professor Review Files
data/raw/*.txt
        |
        v
Document Ingestion
Python file loading with pathlib
        |
        v
Cleaning / Preprocessing
Remove empty lines, extra whitespace, HTML artifacts, and irrelevant copied text
        |
        v
Chunking
Custom Python chunk_text() function
Chunk size: 700 characters
Overlap: 100 characters
        |
        v
Embedding
sentence-transformers
Model: all-MiniLM-L6-v2
        |
        v
Vector Store
ChromaDB persistent local database
Stores chunk text + metadata
        |
        v
Retrieval
Semantic similarity search
Top-k = 5
        |
        v
Generation
Groq LLM: llama-3.3-70b-versatile
Prompt instructs model to answer only from retrieved context
        |
        v
Query Interface
Gradio web app
User enters question
System returns grounded answer + source list
```

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->


**Milestone 3 — Ingestion and chunking:**

I plan to use ChatGPT or GitHub Copilot to help write the ingestion and chunking scripts. I will give the AI tool my Documents section, Chunking Strategy section, and Architecture section. I will ask it to create Python code that loads `.txt` files from `data/raw`, cleans the text, splits each document into 700-character chunks with 100-character overlap, and saves chunks with metadata such as source filename and chunk index.

I will verify the output by printing at least 5 random chunks and checking that they are readable, substantive, and self-contained. I will also check that each chunk has the correct source filename attached. If the chunks are too short, too long, or missing professor context, I will revise the chunking code and update this planning document if my strategy changes.

**Milestone 4 — Embedding and retrieval:**

I plan to use ChatGPT or Copilot to help implement the embedding and retrieval code. I will provide the AI tool my Retrieval Approach section and Architecture diagram. I will ask it to write code that loads `data/chunks.jsonl`, embeds each chunk using `all-MiniLM-L6-v2`, stores the embeddings and metadata in ChromaDB, and creates a retrieval function that returns the top 5 chunks for a user query.

I will verify the retrieval code by running at least 3 evaluation questions before adding generation. I will inspect the returned chunks, source filenames, chunk indexes, and distance scores. If the retrieved chunks are unrelated or come from the wrong professor, I will debug the chunk text, metadata, or chunking strategy before moving on.

**Milestone 5 — Generation and interface:**

I plan to use ChatGPT or Copilot to help create the grounded generation function and Gradio interface. I will give the AI tool my grounding requirement, Retrieval Approach section, and Architecture diagram. I will ask it to create a function that sends retrieved chunks to Groq's `llama-3.3-70b-versatile` model and instructs the model to answer only from the provided context. I will also ask it to create a simple Gradio app with one input box for the user question and two output boxes: one for the answer and one for the source list.

I will verify the output by testing questions that are covered by my documents and questions that are not covered. For covered questions, the answer should cite the retrieved source files. For uncovered questions, the system should say it does not have enough information instead of making up an answer. I will also check that source attribution is included programmatically, not only left up to the LLM.

