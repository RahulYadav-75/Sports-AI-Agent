# 🏆 AI-Powered Sports Engagement Content Agent

An AI-powered sports content generation agent that creates **fresh, engaging, factually grounded, and Instagram-ready sports content**.

The system uses **Web Search + ChromaDB + LLMs** to generate multiple interactive formats instead of relying only on traditional MCQs.

## 🚀 Live Demo

**Streamlit App:**
https://sports-ai-agent-aqqjkcnrt6ksse9hapkp6x.streamlit.app/

---

## 📌 Project Overview

Traditional sports social-media content is often limited to news, highlights, and repetitive questions.

This project solves that problem by generating different types of interactive sports content that can be directly used with Instagram's native text and sticker features.

The agent supports:

* Multiple Choice Questions
* True / False challenges
* This-or-That opinion polls
* Fill-in-the-Blank questions
* Guess-the-Number challenges

The system combines **fresh web information** with **historical sports knowledge stored in ChromaDB** to reduce hallucinations and improve factual accuracy.

---

## 🎯 Objectives

The main objectives of this project are:

* Generate engaging sports content automatically.
* Support multiple sports and difficulty levels.
* Use Web Search for recent and fast-changing sports facts.
* Use ChromaDB for stable and historical sports knowledge.
* Ground factual answers in retrieved information.
* Provide source citations.
* Generate 4–5 content items per request.
* Support mixed content types.
* Allow individual and full-batch regeneration.
* Prevent duplicate questions.
* Provide a simple content-generation dashboard.

---

## ✨ Key Features

### 🏏 Multi-Sport Support

Users can select different sports such as:

* Cricket
* Football
* Tennis
* Badminton
* Basketball
* And other supported sports

### 🎯 Difficulty Levels

* Easy
* Medium
* Hard

### 📝 Five Content Formats

#### 1. Multiple Choice Question

Generates:

* Sport
* Difficulty
* Question
* Four options
* Correct answer
* Short explanation

Example:

```text
Who won the 2023 Cricket World Cup?

A. India
B. Australia
C. England
D. New Zealand

Correct Answer: B. Australia
```

#### 2. True / False

Generates:

* Statement
* Correct answer
* Short explanation

#### 3. This-or-That Poll

Designed specifically for opinion and engagement.

Example:

```text
Messi or Ronaldo — who is the better dribbler?

🟢 Messi
🔵 Ronaldo
```

There is **no correct answer** because it is an opinion-based poll.

#### 4. Fill in the Blank

Generates a sentence with a blank and four answer options.

```text
India won the Cricket World Cup in ____.

A. 2007
B. 2011
C. 2015
D. 2019

Correct Answer: B. 2011
```

#### 5. Guess the Number

Generates:

* Question
* Target number
* Acceptable tolerance
* Explanation

Example:

```text
How many Grand Slam singles titles has Serena Williams won?

Target: 23
Tolerance: ±1
```

---

## 🤖 AI Agent Architecture

```text
                    ┌─────────────────────┐
                    │    Streamlit UI     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Sports AI Agent  │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐         ┌─────────────────┐
        │   Tavily Web    │         │    ChromaDB     │
        │     Search      │         │ Historical Facts│
        └────────┬────────┘         └────────┬────────┘
                 │                           │
                 └─────────────┬─────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Retrieved Context   │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Type-Specific Prompt│
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │        LLM          │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Schema Validation   │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Duplicate Check     │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Instagram-Ready     │
                    │ Sports Content      │
                    └─────────────────────┘
```

---

## 🔍 Retrieval System

The project uses a hybrid retrieval approach.

### 🌐 Web Search

Tavily is used to retrieve:

* Recent match results
* Current sports information
* Tournament outcomes
* Recent records
* Transfers
* Fast-changing facts

### 🧠 ChromaDB

ChromaDB stores stable and historical sports facts.

Example stored facts:

```text
Australia won the 2023 Cricket World Cup.

India won the 2011 Cricket World Cup.

Brazil has won the FIFA World Cup five times.

Argentina won the FIFA World Cup in 2022.

Serena Williams won 23 Grand Slam singles titles.
```

### 🔗 Combined Context

The agent combines:

```text
Web Search Information
+
Historical ChromaDB Knowledge
```

and provides the retrieved context to the LLM.

---

## 🛡️ Accuracy & Hallucination Reduction

Factual content is grounded using retrieved information.

The system:

1. Searches the web.
2. Searches ChromaDB.
3. Combines retrieved information.
4. Sends the context to the LLM.
5. Generates structured content.
6. Validates the generated output.
7. Provides source information where applicable.

Opinion polls are treated differently because they intentionally have **no correct answer**.

---

## 📦 Batch Generation

The agent can generate **4–5 items in a single request**.

Example:

```text
1. MCQ
2. True / False
3. This-or-That Poll
4. Fill in the Blank
5. Guess the Number
```

The system can also mix different content types in one batch.

---

## 🔄 Regeneration

Users can:

* Regenerate an individual item.
* Regenerate the complete batch.

This allows content creators to quickly replace an unwanted question without regenerating everything.

---

## 🚫 Duplicate Prevention

The system checks previously generated content to reduce repeated questions.

The duplicate-prevention flow is:

```text
New Content
     ↓
Normalize Text
     ↓
Compare With Previous Content
     ↓
Duplicate?
   /      \
 Yes       No
 ↓          ↓
Reject     Save
```

This helps maintain content freshness across repeated sessions.

---

## 💾 Persistent History

Generated content can be stored locally so that previous generated content remains available after restarting the application.

This history is also used for duplicate prevention.

---

## 💬 Sports AI Q&A

The application can also provide a direct sports Q&A experience.

Users can ask questions such as:

```text
Who won the latest India vs England match?

Who has won the most Grand Slam titles?

When did Argentina last win the FIFA World Cup?
```

The system can retrieve information using:

```text
User Question
      ↓
Tavily Web Search
      +
ChromaDB
      ↓
Retrieved Context
      ↓
LLM
      ↓
Grounded Answer
      ↓
Sources
```

---

## 🧰 Technology Stack

| Technology                | Purpose                      |
| ------------------------- | ---------------------------- |
| Python                    | Core programming             |
| Streamlit                 | Web dashboard                |
| Gemini                    | LLM                          |
| LangChain                 | LLM integration              |
| Tavily                    | Web search                   |
| ChromaDB                  | Vector database              |
| Pydantic                  | Structured output validation |
| python-dotenv             | Environment variables        |
| GitHub                    | Version control              |
| Streamlit Community Cloud | Deployment                   |

---

## 📂 Project Structure

```text
sports-ai-agent/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── agent/
│   └── ...
│
├── retrieval/
│   └── chroma_db.py
│
├── tools/
│   └── ...
│
└── assets/
    └── ...
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd sports-ai-agent
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### Important

Never upload `.env` to GitHub.

Your `.gitignore` should contain:

```text
.env
venv/
__pycache__/
*.pyc
chroma_db/
.streamlit/secrets.toml
```

---

## ▶️ Run Locally

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will normally open at:

```text
http://localhost:8501
```

---

## ☁️ Streamlit Community Cloud Deployment

The application is deployed using Streamlit Community Cloud.

Streamlit supports GitHub-based deployment and installs Python dependencies from `requirements.txt`.

For deployment:

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new app.
4. Select the GitHub repository.
5. Select the `main` branch.
6. Set the main file to `app.py`.
7. Add API keys under Streamlit Secrets.
8. Deploy the application.

Example secrets:

```toml
GOOGLE_API_KEY = "your_google_api_key"
TAVILY_API_KEY = "your_tavily_api_key"
```

---

## 📊 Assignment Requirements

| Requirement             | Status |
| ----------------------- | ------ |
| Sport Selection         | ✅      |
| Difficulty Selection    | ✅      |
| MCQ                     | ✅      |
| True / False            | ✅      |
| This-or-That Poll       | ✅      |
| Fill in the Blank       | ✅      |
| Guess the Number        | ✅      |
| Mixed Batch             | ✅      |
| 4–5 Items               | ✅      |
| Web Search              | ✅      |
| ChromaDB                | ✅      |
| Source Citations        | ✅      |
| Structured Output       | ✅      |
| Individual Regeneration | ✅      |
| Full Batch Regeneration | ✅      |
| 429 Error Handling      | ✅      |
| Duplicate Prevention    | ✅      |
| Persistent History      | ✅      |
| Streamlit Deployment    | ✅      |

---

## 🌟 Unique Selling Point

The main USP of this project is its **multi-format sports engagement generation**.

Instead of generating only MCQs, the agent intelligently supports:

```text
MCQ
+
True / False
+
Opinion Poll
+
Fill in the Blank
+
Guess the Number
```

Combined with **fresh web retrieval + historical vector knowledge + schema validation + duplicate prevention**, the system is designed for sports creators who need varied and reusable engagement content.

---

## 🔮 Future Improvements

* More sports and leagues
* Better semantic duplicate detection
* Multi-language content generation
* Social media scheduling
* Content performance analytics
* Automatic hashtag generation
* Instagram content calendar
* Advanced sports APIs
* User accounts and personalized history
* Engagement prediction for generated posts

---

## 👨‍💻 Author

**Rahul Yadav**

B.Tech — Computer Science & Engineering (Data Science)

### Project

**AI-Powered Sports Engagement Content Agent**

### Live Demo

https://sports-ai-agent-aqqjkcnrt6ksse9hapkp6x.streamlit.app/

---

## 📜 License

This project is developed for educational, internship, and portfolio purposes.
