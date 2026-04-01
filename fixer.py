import os, re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_bugs(code: str) -> dict:
    prompt = f"""You are an expert Python debugger.
Analyze this code and identify all bugs.

Code:
{code}

Reply in EXACTLY this format:
BUG_COUNT: [number]
BUG_1: [description of first bug]
BUG_2: [description of second bug if exists]
SEVERITY: HIGH or MEDIUM or LOW"""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    return parse_analysis(res.choices[0].message.content)

def fix_code(code: str, error: str, attempt: int) -> str:
    prompt = f"""You are an expert Python developer.
Fix ALL bugs in this code. Attempt {attempt}.

Original code:
{code}

Error when running:
{error}

Return ONLY the fixed Python code with no explanation.
Do not include markdown code blocks.
Just return the raw Python code."""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )
    fixed = res.choices[0].message.content.strip()
    # Remove markdown code blocks if present
    fixed = re.sub(r'```python\n?', '', fixed)
    fixed = re.sub(r'```\n?', '', fixed)
    return fixed.strip()

def parse_analysis(text: str) -> dict:
    result = {"bug_count": 0, "bugs": [], "severity": "LOW"}
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("BUG_COUNT:"):
            nums = re.findall(r"\d+", line)
            if nums: result["bug_count"] = int(nums[0])
        elif re.match(r"BUG_\d+:", line):
            bug = line.split(":", 1)[-1].strip()
            if bug: result["bugs"].append(bug)
        elif line.startswith("SEVERITY:"):
            if "HIGH" in line: result["severity"] = "HIGH"
            elif "MEDIUM" in line: result["severity"] = "MEDIUM"
    return result