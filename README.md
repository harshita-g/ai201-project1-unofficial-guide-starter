# The Unofficial Guide — Project 1

## Domain

My system covers student reviews of Computer Science professors at San Jose State University. This knowledge is valuable because students often want to understand what professors are like before enrolling, including teaching style, workload, grading difficulty, exam style, assignment expectations, and helpfulness.

This information is hard to find through official university channels because official course catalogs describe course topics, but they do not describe actual student experiences. Student reviews are spread across unofficial websites and are written in unstructured text, so a RAG system can help make this information easier to search and summarize.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|------------------|
| 1 | Rate My Professors — David Taylor | Professor review text file | `documents/raw/rmp_david_taylor.txt` |
| 2 | Rate My Professors — Navrati Saxena | Professor review text file | `documents/raw/rmp_navrati_saxena.txt` |
| 3 | Rate My Professors — Melody Moh | Professor review text file | `documents/raw/rmp_melody_moh.txt` |
| 4 | Rate My Professors — Teng Moh | Professor review text file | `documents/raw/rmp_teng_moh.txt` |
| 5 | Rate My Professors — Chris Pollett | Professor review text file | `documents/raw/rmp_chris_pollett.txt` |
| 6 | Rate My Professors — Katerina Potika | Professor review text file | `documents/raw/rmp_katerina_potika.txt` |
| 7 | Rate My Professors — Saptarshi Sengupta | Professor review text file | `documents/raw/rmp_saptarshi_sengupta.txt` |
| 8 | Rate My Professors — Mark Stamp | Professor review text file | `documents/raw/rmp_mark_stamp.txt` |
| 9 | Rate My Professors — Leonard Wesley | Professor review text file | `documents/raw/rmp_leonard_wesley.txt` |
| 10 | Rate My Professors — Mike Wu | Professor review text file | `documents/raw/rmp_mike_wu.txt` |

Each file contains copied student review text from Rate My Professors, along with professor name, school, department, source URL, date collected, course information, rating, difficulty, tags, and review text.

---

## Document Ingestion and Preprocessing

The ingestion pipeline reads `.txt` files from `documents/raw`, cleans the text, and writes cleaned versions to `documents/clean`. The cleaning step removes extra whitespace, blank lines, and formatting artifacts while preserving useful source information such as professor name, course, rating, difficulty, tags, source URL, and the actual review text.

The pipeline keeps source information in the text and also stores source metadata later during chunking. This makes it possible for generated answers to cite the original professor review file and chunk number.

---

## Sample Chunks

### Sample Chunk 1

**Source:** `rmp_katerina_potika.txt`, chunk 1

```text
Professor: Katerina Potika
Source URL: https://www.ratemyprofessors.com/professor/2099184

Review 2:
Course: CS176
Rating: 2
Difficulty: 4
Tags: None
Review text:
Really lecture focused, takes participation with pollev and class is kind of boring. Homework assignments that are confusing/already coded for you? Not a huge fan of her but the class is doable, only recommend if you have a heavy interest. She's a nice enough person, just not a great teacher imo.
```

### Sample Chunk 2

**Source:** `rmp_katerina_potika.txt`, chunk 0

```text
Professor: Katerina Potika
Source URL: https://www.ratemyprofessors.com/professor/2099184

Review 1:
Course: CS176
Rating: 5
Difficulty: 3
Tags: None
Review text:
Potika is one of the few professor I would like to sit down and have a coffee with. She's very passionate about Social Networks and her passion can be felt. She can crack a few good jokes as well. My only criticism would be her power points are not very thorough.
```

### Sample Chunk 3

**Source:** `rmp_navrati_saxena.txt`, chunk 0

```text
Professor: Navrati Saxena
Source URL: https://www.ratemyprofessors.com/professor/2626481

Review 1:
Course: CS146
Rating: 5
Difficulty: 2
Tags: None
Review text:
Prof Saxena is one of the sweetest, most caring professors I've had. She genuinely cares about her students, and is quite funny. The classes are fun to attend, and she teaches really well. The exams are manageable, especially if you study the content and attend the SI sessions. Would highly recommend taking her class.
```

### Sample Chunk 4

**Source:** `rmp_teng_moh.txt`, chunk 1

```text
Professor: Teng Moh
Source URL: https://www.ratemyprofessors.com/professor/660443

Review 2:
Course: CS190
Rating: 1
Difficulty: 2
Tags: None
Review text:
The rudest professor at SJSU. Does not care about the students; does not respond to emails. Unethical and unprofessional behaviors. Unfortunately, he has a monopoly for CS 190 class.
```

### Sample Chunk 5

**Source:** `rmp_chris_pollett.txt`, chunk 0

```text
Professor: Chris Pollett
Source URL: https://www.ratemyprofessors.com/professor/214943

Review 1:
Course: CS174
Rating: 3
Difficulty: 4
Tags: None
Review text:
His slides are helpful since it shows code examples but has a lot of information. His HW are challenging but you can work in a group for them.
```

---

## Chunking Strategy

**Chunk size:**  
Originally planned: about 700 characters.  
Final approach: review-based chunks, where each individual review becomes one chunk.

**Overlap:**  
Originally planned: 100 characters.  
Final approach: no overlap, because chunks are split by review boundaries instead of fixed character boundaries.

**Why these choices fit my documents:**  
My documents are short professor review files, and each file contains two student reviews for one professor. At first, I used fixed-size character chunking, but some chunks started in the middle of words or sentences. This made chunks less readable and less self-contained. I changed the implementation to split documents by review sections such as `Review 1:` and `Review 2:`.

This review-based strategy works better for my corpus because each review usually contains a complete student opinion about a professor's teaching style, workload, grading, exams, or helpfulness. Each chunk also includes the professor name and source URL so that retrieval results remain easy to attribute.

Before chunking, I cleaned the raw text by removing extra whitespace, empty lines, and formatting artifacts. I stored the cleaned versions in `documents/clean`.

**Final chunk count:**  
20 chunks after switching to review-based chunking.

---

## Embedding Model

**Model used:**  
`all-MiniLM-L6-v2` through `sentence-transformers`

**Production tradeoff reflection:**  
I used `all-MiniLM-L6-v2` because it is lightweight, runs locally, does not require a paid API key, and is recommended for this project. It is a good fit for a small course project because the dataset is small and the documents are short professor reviews.

If I were deploying this system for real students, I would compare embedding models based on retrieval accuracy, latency, cost, context length, and ability to handle informal student language. A more powerful embedding model might perform better on vague queries, slang, abbreviations, course numbers, or professor nicknames, but it could be slower or more expensive. I would also consider whether the model supports multilingual text and whether an API-hosted model is worth the tradeoff compared to a local model.

---

## Vector Store and Retrieval

I used ChromaDB as the local vector store. The embedding pipeline reads `documents/chunks.jsonl`, embeds every chunk using `all-MiniLM-L6-v2`, and stores each chunk in a persistent ChromaDB collection named `unofficial_guide`.

Each stored record includes:

- chunk text
- source filename
- chunk index

The retrieval function embeds the user's query and returns the top matching chunks using semantic similarity search. I originally tested top-k = 5, but some lower-ranked chunks were less relevant, so I reduced the default retrieval setting to top-k = 3 for generation.

---

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

## Grounded Generation

**System prompt grounding instruction:**

The system sends retrieved chunks to Groq's `llama-3.3-70b-versatile` model and instructs the model to answer only from the retrieved source context. The prompt includes this grounding instruction:

```text
You are a grounded question-answering assistant for student reviews of SJSU Computer Science professors.

Use only the source context below to answer the user's question.

Rules:
1. Do not use outside knowledge.
2. Do not guess or infer beyond the provided reviews.
3. If the source context does not contain enough information, say:
   "I don't have enough information from the provided documents to answer that."
4. Mention the relevant source filename in your answer.
```

**How source attribution is surfaced in the response:**  
Each retrieved chunk includes source metadata from the chunking and vector store steps. The generation code formats each retrieved chunk with a label such as `rmp_teng_moh.txt, chunk 1`. The Gradio interface displays the answer and a separate source list so users can see which source files and chunks were used.

**Out-of-scope handling:**  
When asked `Which SJSU dining hall is best?`, the system responded that it did not have enough information from the provided documents. This is the desired behavior because the document collection only contains Computer Science professor reviews, not dining hall information.

---

## Query Interface

The system uses a Gradio web interface. The user enters a natural-language question in the input box. The app returns a grounded answer and a separate list of retrieved source chunks.

**Input field:**  
A textbox where the user types a question about SJSU Computer Science professor reviews.

**Output fields:**

1. Answer generated from retrieved context
2. Retrieved source list showing source filename and chunk number

### Sample Interaction

**Question:**  
Which professor does not respond to emails?

**Answer:**  
The reviews identify Teng Moh as a professor who does not respond to emails. One review says he “does not respond to emails regarding questions about the class,” and another says he “does not respond to emails.” Source: `rmp_teng_moh.txt`.

**Sources:**

- `rmp_teng_moh.txt`, chunk 1
- `rmp_teng_moh.txt`, chunk 0

---

## Example Responses

### Example Response 1

**Question:**  
Which professor does not respond to emails?

**Answer:**  
According to the provided reviews in `rmp_teng_moh.txt`, Professor Teng Moh does not respond to emails. This is mentioned in both Review 1 and Review 2 for the CS190 course.

**Retrieved sources:**

- `rmp_teng_moh.txt`, chunk 1
- `rmp_teng_moh.txt`, chunk 0
- `rmp_mike_wu.txt`, chunk 0

### Example Response 2

**Question:**  
What do students say about Navrati Saxena's exams?

**Answer:**  
According to the reviews in `rmp_navrati_saxena.txt`, students say that Professor Navrati Saxena's exams are manageable, especially if students study the content and attend the SI sessions. There is no other information about her exams in the provided source context.

**Retrieved sources:**

- `rmp_navrati_saxena.txt`, chunk 0
- `rmp_navrati_saxena.txt`, chunk 1
- `rmp_katerina_potika.txt`, chunk 1

### Out-of-Scope Example

**Question:**  
Which SJSU dining hall is best?

**Answer:**  
I don't have enough information from the provided documents to answer that. The provided source context only contains reviews of SJSU Computer Science professors and does not mention SJSU dining halls.

---

## Evaluation Report

| # | Question | Expected answer | System response summarized | Retrieval quality | Response accuracy |
|---|----------|-----------------|----------------------------|-------------------|-------------------|
| 1 | What do students say about Katerina Potika's teaching style? | Students have mixed opinions. One review says she is passionate about Social Networks but her PowerPoints are not thorough. Another says the class is lecture-focused, kind of boring, and homework can be confusing. | The system summarized both reviews and said students have mixed opinions: she is passionate, but the class can be lecture-focused and boring, and her slides may not be thorough. | Relevant | Accurate |
| 2 | What do students say about Navrati Saxena's exams? | The reviews say her exams are manageable if students study the content and attend SI sessions. | The system said her exams are manageable, especially with studying and SI sessions, and noted that there was no other exam-specific information. | Partially relevant | Accurate |
| 3 | Which professor does not respond to emails? | Teng Moh is described as not responding to emails. | The system identified Teng Moh and cited `rmp_teng_moh.txt`, where both reviews mention that he does not respond to emails. | Relevant | Accurate |
| 4 | Which professor has challenging homework? | Chris Pollett is explicitly described as having challenging homework. | The system identified Chris Pollett and quoted that his homework is challenging. It also mentioned less relevant retrieved context from Leonard Wesley and David Taylor. | Partially relevant | Accurate |
| 5 | Which professor is described as caring or helpful? | Mike Wu, Navrati Saxena, and David Taylor are described as caring or helpful in the retrieved reviews. | The system identified Mike Wu, Navrati Saxena, and David Taylor as caring or helpful and cited their review files. | Relevant | Accurate |

**Retrieval quality labels:** Relevant / Partially relevant / Off-target  
**Response accuracy labels:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed or partially failed:**  
What do students say about Navrati Saxena's exams?

**What the system returned:**  
The system correctly retrieved the most important chunk from `rmp_navrati_saxena.txt`, which says that her exams are manageable if students study and attend SI sessions. However, the third retrieved chunk came from `rmp_katerina_potika.txt`, which was unrelated to Navrati Saxena's exams.

**Root cause tied to a specific pipeline stage:**  
This issue happened during the retrieval stage. The semantic search matched general teaching and course-experience language, so it retrieved a chunk about another professor even though the query named Navrati Saxena. The top result was correct, but the lower-ranked result was not useful.

**What I would change to fix it:**  
I would add metadata filtering by professor name when the query explicitly includes a professor. For example, if the question contains “Navrati Saxena,” the system should filter retrieved chunks to only sources related to that professor before passing context to the LLM. I would also keep top-k small, such as top-k = 3, to reduce unrelated context.

---

## Spec Reflection

**One way the spec helped me during implementation:**  
The planning spec helped me organize the system before writing code. Because I had already decided on the domain, document structure, embedding model, vector store, and retrieval strategy, it was easier to build each stage step by step instead of trying to implement the full RAG system at once. The architecture diagram also helped clarify how raw review files would move through ingestion, cleaning, chunking, embedding, retrieval, and generation.

**One way my implementation diverged from the spec, and why:**  
My original spec planned to use 700-character chunks with 100-character overlap. During testing, I noticed that fixed-size chunking sometimes split reviews in the middle of words or sentences, which made chunks less readable and less useful. I changed the implementation to review-based chunking because my documents are structured around `Review 1:` and `Review 2:` sections. This better matched the actual document format and produced cleaner chunks.

---

## AI Usage

### Instance 1

- **What I gave the AI:** I gave ChatGPT my project domain, professor-review document format, and `planning.md` structure. I asked it to help fill out the planning file based on the assignment requirements.
- **What it produced:** It produced a completed `planning.md` draft with sections for domain, documents, chunking strategy, retrieval approach, evaluation plan, anticipated challenges, architecture, and AI tool plan.
- **What I changed or overrode:** I changed the document plan to use 10 professor review files instead of mixing Rate My Professors and Reddit sources, because using one consistent document type made the project cleaner.

### Instance 2

- **What I gave the AI:** I showed ChatGPT my chunking output, including examples where chunks started in the middle of words or sentences.
- **What it produced:** It suggested replacing fixed-size character chunking with review-based chunking that splits documents by `Review 1:` and `Review 2:`.
- **What I changed or overrode:** I updated `src/chunk.py` to use review-based splitting instead of fixed 700-character chunks. This improved chunk readability and made retrieval results easier to interpret.

### Instance 3

- **What I gave the AI:** I gave ChatGPT my retrieval output for the query “What do students say about Katerina Potika's teaching style?”
- **What it produced:** It analyzed the retrieval results and identified that the top two chunks were relevant, while lower-ranked chunks from other professors were less useful.
- **What I changed or overrode:** I decided to reduce the default retrieval value from top-k = 5 to top-k = 3 so the LLM receives fewer unrelated chunks during generation.

---

## Demo Video Checklist

The demo video should show:

- The Gradio app running
- At least three different questions answered with source citations visible
- One query where retrieval works well, such as “Which professor does not respond to emails?”
- One query where the system struggles or partially fails, such as a professor-specific query that retrieves one unrelated chunk
- A brief walkthrough of this evaluation report
