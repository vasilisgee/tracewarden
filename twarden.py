import json
import time
from core.http_tests import run_http_test
from core.ping_tests import run_ping_test
from core.dns_tests import run_dns_test
from utils.reporting import generate_html_report, save_results_json

CONFIG_PATH = "config.json"
RESULTS_PATH = "results.json"
REPORT_PATH = "report.html"


def load_config(path: str = CONFIG_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_tests(config: dict) -> list[dict]:
    tests = config.get("tests", [])
    print(f"Running {len(tests)} tests...")
    results: list[dict] = []

    for test in tests:
        t_type = test.get("type")

        if t_type == "http":
            result = run_http_test(test)
        elif t_type == "ping":
            result = run_ping_test(test)
        elif t_type == "dns":
            result = run_dns_test(test)
        else:
            result = {
                "id": test.get("id", "unknown"),
                "type": t_type,
                "passed": False,
                "error": f"Unsupported type: {t_type}"
            }

        results.append(result)

        symbol = "✔" if result.get("passed") else "✖"
        status_text = "PASS" if result.get("passed") else "FAIL"
        print(f"{symbol} {result.get('id')}: {status_text}")

    return results


def main() -> None:
    print("\n=== TraceWarden v1 - Network Reporting Tool ===\n")
    config = load_config(CONFIG_PATH)
    results = run_tests(config)
    save_results_json(results, RESULTS_PATH)
    generate_html_report(results, REPORT_PATH)
    print(f"\nResults saved to {RESULTS_PATH}")
    print(f"HTML report saved to {REPORT_PATH}")


if __name__ == "__main__":
    main()
