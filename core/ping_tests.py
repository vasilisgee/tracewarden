import subprocess
import platform

def run_ping_test(test_def: dict) -> dict:
    target = test_def["target"]
    test_id = test_def.get("id", target)

    if platform.system().lower() == "windows":
        cmd = ["ping", "-n", "1", "-w", "1000", target]
    else:
        cmd = ["ping", "-c", "1", "-W", "1", target]

    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=5
        )

        reachable = (completed.returncode == 0)

        result = {
            "id": test_id,
            "type": "ping",
            "target": target,
            "passed": reachable,
            "error": None if not reachable else None
        }

        if result.get("error") is None:
            result.pop("error")

        return result

    except Exception as e:
        return {
            "id": test_id,
            "type": "ping",
            "target": target,
            "passed": False,
            "error": str(e)
        }
