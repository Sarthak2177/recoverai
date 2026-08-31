# 🚀 RecoverAI

**Razorpay Buildathon Submission — Track 03: AI Revenue Recovery & Agentic Commerce**

RecoverAI is an autonomous, state-driven agent designed to recover failed payments, abandoned carts, and lapsed subscriptions using a strict, auditable LangGraph architecture.

## 🏆 Why RecoverAI? (Hitting the Judging Criteria)

Most AI agents are dangerous. They give an LLM an API key and hope it doesn\'t hallucinate a financial transaction. RecoverAI takes a completely different approach designed for enterprise-grade compliance:

1. **AI Judgment (The \'Restraint\' Principle):** RecoverAI uses a 6-node LangGraph state machine. **Only 2 nodes (Diagnosis & Strategy) use the Gemini LLM.** The actual Execution and Verification nodes are **100% deterministic Python code**. AI handles the reasoning; code handles the money.
2. **Build Quality (The Immutable Audit Trail):** Every transition in the State Machine generates an immutable AuditEntry. Our real-time dashboard streams exactly *why* a decision was made, explicitly badging actions as ✨ AI JUDGMENT or ⚙️ RULE.
3. **Problem Taste (Real Integration):** We don\'t just generate text. When the agent decides to offer a discount for an abandoned cart, it directly hits the **official Razorpay Python SDK** to generate a live Payment Link.
4. **Failure Recovery (Graceful Degradation):** What happens if the Gemini API times out or rate limits are hit? RecoverAI catches the exception and instantly falls back to a deterministic, rule-based recovery strategy. The agent never crashes.

## ⚙️ Architecture

The system is built on **LangGraph** (State Machine), **FastAPI** (Backend + Server-Sent Events), and **Vanilla JS/CSS** (Real-time Dashboard). 

**The 6 Nodes:**
1. Detector (Rule): Ingests the failed transaction.
2. Diagnoser (AI): Analyzes the root cause using Gemini.
3. Interventor (AI): Maps the cause to a specific recovery strategy.
4. Executor (Rule): Fires the Razorpay API / Webhooks.
5. Verifier (Rule): Checks if the action succeeded.
6. Reporter (Rule): Finalizes the state.

## 🚀 How to Run Locally

1. **Install dependencies:**
   `ash
   pip install -r requirements.txt
   `
2. **Set up API Keys:**
   Rename .env.example to .env and add your **Gemini API Key** and **Razorpay Test Keys**.
3. **Run the Demo:**
   `ash
   python run_demo.py
   `
   *(This automatically generates 200 synthetic failed transactions and starts the real-time dashboard on http://localhost:8000)*

## 💡 Built By
**Sarthak** for the Razorpay Buildathon.
