import subprocess
import tempfile
import os

def execute_code(code: str, timeout: int = 10) -> dict:
    # Write code to a temp file
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py",
        delete=False, encoding="utf-8"
    ) as f:
        f.write(code)
        tmp_path = f.name

    try:
        result = subprocess.run(
            ["python", tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Code execution timed out after 10 seconds",
            "returncode": -1,
        }
    finally:
        os.unlink(tmp_path)