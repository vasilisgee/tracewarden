import time
import requests

def run_http_test(test_def: dict) -> dict:
    url = test_def["url"]
    expected_status = test_def.get("expected_status", 200)
    max_ms = test_def.get("max_response_ms", 1000)
    test_id = test_def.get("id", url)

    start = time.perf_counter()
    try:
        response = requests.get(url, timeout=5)
        elapsed_ms = (time.perf_counter() - start) * 1000

        status_ok = response.status_code == expected_status
        time_ok = elapsed_ms <= max_ms
        passed = bool(status_ok and time_ok)

        reason_parts = []
        if not status_ok:
            reason_parts.append(f"expected status {expected_status}, got {response.status_code}")
        if not time_ok:
            reason_parts.append(f"response time {elapsed_ms:.2f} ms exceeded limit {max_ms} ms")
        error = "; ".join(reason_parts) if reason_parts else None

        result = {
            "id": test_id,
            "type": "http",
            "url": url,
            "expected_status": expected_status,
            "max_response_ms": max_ms,
            "status_code": response.status_code,
            "response_ms": round(elapsed_ms, 2),
            "content_length": len(response.content),
            "passed": passed,
            "error": error,
        }
        
        if result.get("error") is None:
            result.pop("error")

        return result
    
    except Exception as e:
        return {
            "id": test_id,
            "type": "http",
            "url": url,
            "expected_status": expected_status,
            "max_response_ms": max_ms,
            "status_code": None,
            "response_ms": None,
            "content_length": None,
            "passed": False,
            "error": str(e),
        }
