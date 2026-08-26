from utils.history import (get_recent_history,save_item)
from retrieval.chroma_db import search_chroma
from retrieval.web_search import search_sports
from retrieval.web_search import get_sports_context
import streamlit as st
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
load_dotenv()
st.set_page_config(
    page_title="Sports AI Agent",    
    layout="centered"
)
st.sidebar.subheader("AI Agent")
st.sidebar.success("Web Search: Active")
st.sidebar.success("ChromaDB: Active")
st.sidebar.success("Schema Validation: Active")
st.sidebar.info("Opinion Polls: No fact-checking")


# Schemas

class MCQ(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str

class TrueFalse(BaseModel):
    statement: str
    correct_answer: str
    explanation: str

class Poll(BaseModel):
    prompt: str
    options: list[str] = Field(min_length=2, max_length=2)

class FillBlank(BaseModel):
    sentence: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str

class GuessNumber(BaseModel):
    question: str
    target_number: int
    tolerance: int
    explanation: str

# LLM

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.8,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Generation Functions


def generate_mcq(sport, difficulty):
    structured = llm.with_structured_output(MCQ)
    query = f"{sport} important statistics records history recent results"
    search_results = search_sports(
        query,
        max_results=5
    )
    chroma_results = search_chroma(
        query,
        n_results=3
    )
    web_context = "\n\n".join(
        [
            f"WEB SOURCE: {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Information: {r['content']}"
            for r in search_results
        ]
    )
    chroma_context = "\n\n".join(
        [
            f"HISTORICAL KNOWLEDGE: {fact}"
            for fact in chroma_results
        ]
    )
    context = f"""
WEB SEARCH INFORMATION:
{web_context}
HISTORICAL KNOWLEDGE FROM CHROMADB:
{chroma_context}
"""
    previous_questions = get_recent_history(20)
    previous_text = "\n".join(
    f"- {q}"
    for q in previous_questions
    )
    prompt = f"""
Create a {difficulty} difficulty {sport} multiple-choice question.

Use ONLY the information from the context below.

Requirements:
- Exactly 4 options
- Exactly 1 correct answer
- The question must be factually correct
- Give a short explanation
- Make it interesting for Instagram
- Do not invent facts
- Do not repeat previous questions

PREVIOUSLY GENERATED CONTENT:

{previous_text}
CONTEXT:
{context}
"""
    result = structured.invoke(prompt)
    save_item(result.question)
    return result, search_results


def generate_true_false(sport, difficulty):
    structured = llm.with_structured_output(TrueFalse)
    query = f"{sport} important records statistics history recent results"
    context, sources = get_sports_context(query)
    prompt = f"""
Create a {difficulty} difficulty True/False question about {sport}.
Use ONLY the information from the context.
Requirements:
- One factual statement
- Answer must be True or False
- Give a short explanation
- Do not invent facts

CONTEXT:

{context}
"""
    result = structured.invoke(prompt)
    return result, sources


def generate_poll(sport):
    structured = llm.with_structured_output(Poll)
    prompt = f"""
    Create a fun Instagram This-or-That poll about {sport}.
    Requirements:
    - Pure opinion
    - No correct answer
    - Exactly 2 options
    - Make it engaging for sports fans
    """
    return structured.invoke(prompt)


def generate_fill_blank(sport, difficulty):
    structured = llm.with_structured_output(FillBlank)
    query = f"{sport} important statistics records history players tournaments"
    context, sources = get_sports_context(query)
    prompt = f"""
Create a {difficulty} difficulty fill-in-the-blank question
about {sport}.
Use ONLY the information from the context.
Requirements:
- One blank
- Exactly 4 answer options
- Exactly 1 correct answer
- Factually accurate
- Short explanation
- Do not invent facts

CONTEXT:
{context}
"""
    result = structured.invoke(prompt)
    return result, sources


def generate_guess_number(sport, difficulty):
    structured = llm.with_structured_output(GuessNumber)
    query = f"{sport} player statistics records scores runs goals points"
    context, sources = get_sports_context(query)
    prompt = f"""
Create a {difficulty} difficulty Guess-the-Number question
about {sport}.
Use ONLY the information from the context.
Requirements:
- The target must be a real numeric sports statistic
- Give the exact target number
- Give an acceptable tolerance
- Give a short explanation
- Do not invent facts

CONTEXT:
{context}
"""
    result = structured.invoke(prompt)
    return result, sources


def ask_sports_question(question):
    # 1. Search web for fresh information
    web_context = get_sports_context(question)
    # 2. Search ChromaDB for historical knowledge
    vector_context = get_sports_context(question)
    # 3. Combine retrieved information
    context = f"""
    Web Search Context:
    {web_context}
    ChromaDB Context:
    {vector_context}
    """
    # 4. Ask LLM using grounded context
    prompt = f"""
    Answer the user's sports question using ONLY the
    retrieved context below.
    If the information is not available, say that clearly.
    User Question:
    {question}
    Retrieved Context:
    {context}
    Give a short, accurate answer.
    """
    response = llm.invoke(prompt)
    return response.content

# UI

st.title("Sports AI Engagement Agent")
st.write(
    "AI-powered sports content generator for Instagram."
)
sport = st.selectbox(
    "Select Sport",
    [
        "Cricket",
        "Football",
        "Tennis",
        "Badminton",
        "Basketball"
    ]
)

difficulty = st.selectbox(
    "Difficulty",
    ["Easy", "Medium", "Hard"]
)

content_type = st.selectbox(
    "Content Type",
    [   "Mixed",
        "MCQ",
        "True / False",
        "This-or-That Poll",
        "Fill in the Blank",
        "Guess the Number"
    ]
)
count = st.slider(
    "Number of Items",
    min_value=1,
    max_value=5,
    value=5
)

# Content Generation functions


def generate_item(item_type, sport, difficulty):
    if item_type == "MCQ":
        result, sources = generate_mcq(
            sport,
            difficulty
        )
        return {
            "type": item_type,
            "result": result,
            "sources": sources
        }
    elif item_type == "True / False":
        result, sources = generate_true_false(
            sport,
            difficulty
        )
        return {
            "type": item_type,
            "result": result,
            "sources": sources
        }
    elif item_type == "This-or-That Poll":
        result = generate_poll(sport)
        return {
            "type": item_type,
            "result": result,
            "sources": []
        }
    elif item_type == "Fill in the Blank":
        result, sources = generate_fill_blank(
            sport,
            difficulty
        )
        return {
            "type": item_type,
            "result": result,
            "sources": sources
        }
    elif item_type == "Guess the Number":
        result, sources = generate_guess_number(
            sport,
            difficulty
        )
        return {
            "type": item_type,
            "result": result,
            "sources": sources
        }



# Generate button

if st.button("Generate Content"):
    with st.spinner("Creating content..."):
        try:
            content_types = [
                "MCQ",
                "True / False",
                "This-or-That Poll",
                "Fill in the Blank",
                "Guess the Number"
            ]
            # Mixed = different types
            if content_type == "Mixed":
                selected_types = content_types[:count]
            # Single type = generate multiple items
            else:
                selected_types = [
                    content_type
                    for _ in range(count)
                ]
            generated_items = []
            for item_type in selected_types:
                item = generate_item(
                    item_type,
                    sport,
                    difficulty
                )
                generated_items.append(item)
            st.session_state.generated_items = generated_items
            st.success(
                f"Generated {len(generated_items)} items!"
            )
        except Exception as e:
            st.error(
                f"Something went wrong: {e}"
            )


# Display Generated Content

if "generated_items" in st.session_state:
    items = st.session_state.generated_items
    st.divider()
    st.header("Generated Sports Content")
    for index, item in enumerate(items):
        item_type = item["type"]
        result = item["result"]
        sources = item["sources"]
        st.divider()


        
        # MCQ        
        if item_type == "MCQ":
            st.subheader(
                f"MCQ #{index + 1}"
            )
            st.write(
                f"**Question:** {result.question}"
            )
            for i, option in enumerate(result.options):
                st.write(
                    f"{chr(65+i)}. {option}"
                )
            st.success(
                f"Correct Answer: {result.correct_answer}"
            )
            st.info(
                f"{result.explanation}"
            )
        
        # TRUE / FALSE        
        elif item_type == "True / False":
            st.subheader(
                f"True / False #{index + 1}"
            )
            st.write(
                f"**Statement:** {result.statement}"
            )
            st.success(
                f"Answer: {result.correct_answer}"
            )
            st.info(
                f"{result.explanation}"
            )
        
        # POLL
        
        elif item_type == "This-or-That Poll":
            st.subheader(
                f"This-or-That Poll #{index + 1}"
            )
            st.write(
                f"**{result.prompt}**"
            )
            st.write(
                f"{result.options[0]}"
            )
            st.write(
                f"{result.options[1]}"
            )
            st.caption(
                "Opinion-based — No correct answer"
            )


    
        # FILL BLANK
        elif item_type == "Fill in the Blank":
            st.subheader(
                f"Fill in the Blank #{index + 1}"
            )
            st.write(
                f"**{result.sentence}**"
            )
            for i, option in enumerate(result.options):
                st.write(
                    f"{chr(65+i)}. {option}"
                )
            st.success(
                f"Correct Answer: {result.correct_answer}"
            )
            st.info(
                f"{result.explanation}"
            )
        
        # GUESS NUMBER
        elif item_type == "Guess the Number":
            st.subheader(
                f"Guess the Number #{index + 1}"
            )
            st.write(
                f"**{result.question}**"
            )
            st.write(
                f"Target Number: {result.target_number}"
            )
            st.write(
                f"Accepted tolerance: ±{result.tolerance}"
            )
            st.info(
                f"{result.explanation}"
            )


        
        # SOURCES       
        if sources:
            st.caption("Sources")
            for source in sources:
                st.write(
                    f"[{source['title']}]({source['url']})"
                )
        
        # INDIVIDUAL REGENERATE
        if st.button(
            f"🔄 Regenerate {item_type}",
            key=f"regenerate_{index}"
        ):
            with st.spinner(
                f"Regenerating {item_type}..."
            ):
                try:
                    new_item = generate_item(
                        item_type,
                        sport,
                        difficulty
                    )
                    st.session_state.generated_items[index] = new_item
                    st.rerun()
                except Exception as e:
                    st.error(
                        f"Regeneration failed: {e}"
                    )



# REGENERATE FULL BATCH


if "generated_items" in st.session_state:
    st.divider()
    if st.button(
        "Regenerate Full Batch"
    ):
        with st.spinner(
            "Regenerating full batch..."
        ):
            try:
                new_items = []
                for old_item in st.session_state.generated_items:
                    new_item = generate_item(
                        old_item["type"],
                        sport,
                        difficulty
                    )
                    new_items.append(new_item)
                st.session_state.generated_items = new_items
                st.rerun()
            except Exception as e:
                error_message = str(e)
                if "RESOURCE_EXHAUSTED" in error_message or "429" in error_message:
                    st.warning(
            "Gemini API quota is exhausted. "
            "Please try again after the quota resets."
        )
                else:
                        st.error(
                            f"Batch regeneration failed: {e}"
        )
st.sidebar.divider()
st.divider()
st.subheader("Ask Sports AI")
user_question = st.text_input(
    "Ask any sports-related question",
    placeholder="Example: Who won the latest India vs England match?"
)
if st.button("Ask AI", use_container_width=True):
    if not user_question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching and generating answer..."):
            try:
                answer = ask_sports_question(user_question)
                st.markdown("### Answer")
                st.write(answer)
            except Exception as e:
                st.error(f"Unable to answer: {e}")

