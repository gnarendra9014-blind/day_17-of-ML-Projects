import os
from fixer import analyze_bugs, fix_code
from executor import execute_code

MAX_ATTEMPTS = 3

def run_agent(code: str, filename: str):
    print(f"\n{'='*60}")
    print(f"AUTONOMOUS BUG FIXER — {filename}")
    print(f"{'='*60}")

    # Step 1: Analyze bugs
    print("\nAnalyzing code for bugs...")
    analysis = analyze_bugs(code)
    print(f"Found {analysis['bug_count']} bugs (Severity: {analysis['severity']})")
    for i, bug in enumerate(analysis["bugs"]):
        print(f"  BUG {i+1}: {bug}")

    # Step 2: Test original code first
    print("\nTesting original code...")
    original_result = execute_code(code)
    if original_result["success"]:
        print("Original code runs fine! No fixes needed.")
        return
    print(f"Original code failed: {original_result['stderr'][:100]}")

    # Step 3: Fix and retry loop
    current_code = code
    current_error = original_result["stderr"]

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\nAttempt {attempt}/{MAX_ATTEMPTS} — Generating fix...")
        fixed_code = fix_code(current_code, current_error, attempt)
        print("Fix generated. Testing fixed code...")

        result = execute_code(fixed_code)
        if result["success"]:
            print(f"\nSUCCESS! Fixed on attempt {attempt}!")
            print(f"Output: {result['stdout']}")
            print("\nFIXED CODE:")
            print("-"*40)
            print(fixed_code)
            print("-"*40)
            return
        else:
            print(f"Still failing: {result['stderr'][:100]}")
            current_code = fixed_code
            current_error = result["stderr"]

    print("\nMax attempts reached. Could not fix automatically.")

def main():
    print("\n=== Autonomous Bug Fixer Agent ===")
    print("1. Fix a specific file")
    print("2. Run all sample bugs")
    choice = input("\nChoose (1 or 2): ").strip()

    if choice == "1":
        path = input("Enter file path: ").strip().strip('"').strip("'")
        if not os.path.exists(path):
            print(f"Error: Path '{path}' not found.")
            return
        if not os.path.isfile(path):
            print(f"Error: '{path}' is a directory, not a file.")
            return
            
        with open(path) as f:
            code = f.read()
        run_agent(code, os.path.basename(path))
    else:
        for fname in ["bug1.py", "bug2.py", "bug3.py"]:
            path = os.path.join("buggy_samples", fname)
            if os.path.exists(path):
                with open(path) as f:
                    code = f.read()
                run_agent(code, fname)

if __name__ == "__main__":
    main()