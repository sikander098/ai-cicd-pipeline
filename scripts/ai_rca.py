#!/usr/bin/env python3
import os
import sys
import argparse
import requests
import json

def analyze_logs_with_gemini(log_content, api_key):
    """Send build logs to Google Gemini for Root Cause Analysis"""
    
    prompt = f"""You are an expert DevOps Engineer and Build Troubleshooter. 
Your task is to analyze the following CI/CD build log failure.

Focus on:
1. 🔴 **Identify the Root Cause** (Syntax error, Missing dependency, Test failure, Timeout)
2. 🔧 **Suggest a Specific Fix** (Exact command to run, Code change needed)
3. 📚 **Explain the Error** (Why did it happen?)

Provide the output in GitHub-flavored Markdown. 
Start with a **tl;dr** summary.
Then provide the detailed analysis.

Build Logs:
```
{log_content}
```
"""

    model = "qwen2.5-coder:7b"
    url = "http://localhost:11434/api/generate"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Ollama API Format
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 2048
        }
    }
    
    import time

    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload)
            
            response.raise_for_status()
            
            data = response.json()
            if "response" in data:
                return data["response"]
            else:
                return "❌ Ollama returned no content."
                
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⚠️ Error: {str(e)}. Retrying...")
                time.sleep(retry_delay)
                continue
            return f"❌ AI RCA failed: {str(e)}"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--logs", required=True, help="Path to log file")
    parser.add_argument("--output", required=True, help="Output file")
    args = parser.parse_args()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not set")
        sys.exit(1)
    
    try:
        with open(args.logs, 'r', encoding='utf-8') as f:
            log_content = f.read()
    except UnicodeDecodeError:
        with open(args.logs, 'r', encoding='latin-1') as f:
            log_content = f.read()
    
    # Limit log size (Gemini Flash has large context, but let's be safe (~100k chars))
    # For logs, we often want the END of the file where the error is
    if len(log_content) > 100000:
        print("⚠️ Logs too large, truncating to last 100k chars...")
        log_content = "... (truncated)\n" + log_content[-100000:]
    
    print(f"🤖 Sending {len(log_content)} chars to Gemini for RCA...")
    analysis = analyze_logs_with_gemini(log_content, api_key)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(analysis)
    
    print(f"✅ AI RCA saved to {args.output}")

if __name__ == "__main__":
    main()
