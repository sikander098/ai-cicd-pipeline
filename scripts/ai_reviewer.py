#!/usr/bin/env python3
import os
import sys
import argparse
import requests
import json

def analyze_code_with_gemini(diff_content, api_key):
    """Send code diff to Google Gemini for analysis"""
    
    prompt = f"""You are an expert Senior DevOps Engineer and Code Reviewer. 
Your task is to analyze the following code diff from a Pull Request.

Focus on:
1. 🛡️ **Security Vulnerabilities** (hardcoded secrets, injection, permissions)
2. 🚀 **Performance Issues** (n+1 queries, memory leaks, inefficient loops)
3. 🧹 **Code Quality** (anti-patterns, readability, SOLID principles)
4. 🐛 **Potential Bugs** (race conditions, edge cases)

Provide the output in GitHub-flavored Markdown. 
Start with a summary table (Pass/Fail/Warn).
Then list specific findings with line numbers if possible.

Code Diff:
```
{diff_content}
```
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 2048
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        if "candidates" in data and len(data["candidates"]) > 0:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            if "promptFeedback" in data:
                return f"❌ Gemini blocked content: {data['promptFeedback']}"
            return "❌ Gemini returned no content. Check API limits or diff size."
            
    except Exception as e:
        return f"❌ AI Review failed: {str(e)}"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--diff", required=True, help="Path to diff file")
    parser.add_argument("--output", required=True, help="Output file")
    args = parser.parse_args()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not set")
        sys.exit(1)
    
    try:
        with open(args.diff, 'r', encoding='utf-8') as f:
            diff_content = f.read()
    except UnicodeDecodeError:
        # Fallback for non-utf8 files
        with open(args.diff, 'r', encoding='latin-1') as f:
            diff_content = f.read()
    
    # Limit diff size (Gemini Flash has large context, but let's be safe (~100k chars))
    if len(diff_content) > 100000:
        diff_content = diff_content[:100000] + "\n... (truncated diff due to size)"
    
    print(f"🤖 Sending {len(diff_content)} chars to Gemini...")
    review = analyze_code_with_gemini(diff_content, api_key)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(review)
    
    print(f"✅ AI review saved to {args.output}")

if __name__ == "__main__":
    main()
