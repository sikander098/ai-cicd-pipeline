# AI-Powered CI/CD Pipeline & Code Reviewer
![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![Python](https://img.shields.io/badge/python-3.9%2B-blue) ![LLM](https://img.shields.io/badge/AI-Gemini%20%7C%20Groq-purple)

A self-healing, intelligent CI/CD pipeline architecture that integrates **Generative AI** into the software delivery lifecycle. It performs automated code reviews, detects security vulnerabilities (SAST), and provides Automated Root Cause Analysis (RCA) for build failures. Uses **Google Gemini 2.0 Flash** for high-speed inference.

> **Status:** Reference Implementation (Architecture Phase)

## 🚀 Key Features

### 🤖 Intelligent Code Reviewer
A Python-based agent that hooks into GitHub Pull Requests:
*   **Security Analysis:** Detects hardcoded secrets, injection flaws, and IAM permission risks.
*   **Performance Audits:** Identifies N+1 queries, memory leaks, and inefficient loops.
*   **Style Enforcer:** Checks for SOLID principles and maintainability.

### 🧠 Automated Root Cause Analysis (RCA)
*   **Log Parsing:** Automatically captures build failure logs from GitHub Actions.
*   **Contextual Remediation:** Feeds errors to the LLM (Gemini 2.0 / Groq) to generate specific fix code blocks.
*   **ChatOps:** Posts the fix directly to the PR comments.

### 📈 Predictive Scaling (Architecture)
*   **Traffic Forecasting:** Ingests historical metrics to predict resource usage.
*   **Dynamic Terraform:** (Roadmap) Adjusts `requests/limits` in Terraform plans prior to deployment based on predicted load.

---

## 🏗️ Architecture

```mermaid
graph TD
    User([Developer]) -->|Push Code| GH[GitHub Actions]
    
    subgraph "AI Pipeline"
        GH -->|Trigger| Agent[Python AI Agent]
        Agent -->|Diff Analysis| LLM{LLM Inference}
        LLM -->|Gemini 2.0 Flash| Google[Google AI]
        LLM -->|Llama 3 70b| Groq[Groq API]
    end
    
    subgraph "Outputs"
        Google -->|Review Comments| PR[Pull Request]
        Google -->|Fix Suggestion| Logs[Build Logs]
    end
    
    GH -->|Deploy| AWS[AWS EKS]
```

## 🛠️ Setup & Configuration

### Prerequisites
*   GitHub Repository with Actions enabled.
*   LLM API Key: **Google Gemini** (Default) or **Groq** (Low-Latency Mode).

### Installation
1.  **Workflows**: Copy `.github/workflows/ai-review.yml` to your repo.
2.  **Scripts**: Place `scripts/ai_reviewer.py` in your source.
3.  **Secrets**: Add `GOOGLE_API_KEY` (or `GROQ_API_KEY`) to GitHub Repository Secrets.

## 💻 Usage Example

### 1. Automated Security Audit
Just open a Pull Request. The Agent automatically scans the diff.

**Example Output:**

> **🤖 AI Code Review**
> 
> | Category | Status | Findings |
> |----------|--------|----------|
> | **Security** | ⚠️ High | Hardcoded API Key detected in `config.py` line 12. |
> | **Performance** | ✅ Pass | No bottlenecks detected. |
> 
> **Suggestion:**
> ```python
> - api_key = "sk-12345"
> + api_key = os.getenv("API_KEY")
> ```

## 🔮 Roadmap
*   **Vector DB Integration**: Store past code review feedback to prevent repeat errors.
*   **Predictive Scaling**: Implement the Terraform dynamic variable injection based on Prometheus metrics.

## 📄 License
MIT
