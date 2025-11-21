import socket
import time

def run_dns_test(test_def: dict) -> dict:
    hostname = test_def["hostname"]
    test_id = test_def.get("id", hostname)
    max_ms = test_def.get("max_lookup_ms", 1000)

    start = time.perf_counter()
    try:
        resolved_ip = socket.gethostbyname(hostname)
        elapsed_ms = (time.perf_counter() - start) * 1000

        passed = elapsed_ms <= max_ms
        error = None if passed else f"lookup {elapsed_ms:.2f} ms > limit {max_ms} ms"

        result = {
            "id": test_id,
            "type": "dns",
            "hostname": hostname,
            "resolved_ip": resolved_ip,
            "lookup_ms": round(elapsed_ms, 2),
            "max_lookup_ms": max_ms,
            "passed": passed,
            "error": error
        }

        if result.get("error") is None:
            result.pop("error")

        return result

    except Exception as e:
        elapsed_ms = (time.perf_counter() - start) * 1000
        return {
            "id": test_id,
            "type": "dns",
            "hostname": hostname,
            "resolved_ip": None,
            "lookup_ms": round(elapsed_ms, 2),
            "max_lookup_ms": max_ms,
            "passed": False,
            "error": str(e)
        }
