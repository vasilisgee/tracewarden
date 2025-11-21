import json
import time
from pathlib import Path

def save_results_json(results: list[dict], path: str = "results.json") -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

def compute_summary(results: list[dict]) -> dict:
    total = len(results)
    passed = sum(1 for r in results if r.get("passed"))
    failed = total - passed

    # HTTP times
    http_times = [
        r["response_ms"]
        for r in results
        if r.get("type") == "http" and r.get("response_ms") is not None
    ]
    avg_http = round(sum(http_times) / len(http_times), 2) if http_times else None

    # DNS lookup times
    dns_times = [
        r["lookup_ms"]
        for r in results
        if r.get("type") == "dns" and r.get("lookup_ms") is not None
    ]
    avg_dns = round(sum(dns_times) / len(dns_times), 2) if dns_times else None

    # Ping reachability 
    ping_total = sum(1 for r in results if r.get("type") == "ping")
    ping_passed = sum(
        1 for r in results
        if r.get("type") == "ping" and r.get("passed")
    )

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "avg_http_ms": avg_http,
        "avg_dns_ms": avg_dns,
        "ping_total": ping_total,
        "ping_passed": ping_passed,
    }


def generate_html_report(results: list[dict], path: str = "report.html") -> None:
    summary = compute_summary(results)
    summary = compute_summary(results)

    avg_http_text = (
        f"{summary['avg_http_ms']} ms" if summary['avg_http_ms'] is not None else "N/A"
    )
    avg_dns_text = (
        f"{summary['avg_dns_ms']} ms" if summary['avg_dns_ms'] is not None else "N/A"
    )
    ping_reach_text = (
        f"{summary['ping_passed']} / {summary['ping_total']}"
        if summary['ping_total'] > 0
        else "N/A"
    )


    rows = []
    for r in results:
        row_class = "pass" if r.get("passed") else "fail"
        if r.get("type") == "http":
            status_code = r.get("status_code")
            response_ms = r.get("response_ms")
            measured = f"status={status_code}, time={response_ms} ms"
        elif r.get("type") == "ping":
            measured = "reachable" if r.get("passed") else "unreachable"
        elif r.get("type") == "dns":
            resolved_ip = r.get("resolved_ip")
            lookup_ms = r.get("lookup_ms")
            measured = f"ip={resolved_ip}, lookup={lookup_ms} ms"
        else:
            measured = ""

        target_display = r.get("url") or r.get("target") or r.get("hostname", "")
        error_text = r.get("error") or ""

        rows.append(f"""
        <tr class="{row_class}">
            <td>{target_display}</td>
            <td>{r.get('type', '')}</td>
            <td>{measured}</td>
            <td>{"PASS" if r.get("passed") else "FAIL"}</td>
            <td>{error_text}</td>
        </tr>""")

    rows_html = "\n".join(rows)

    html = f"""<!DOCTYPE html>
<html>
<head>
<title>TraceWarden Report</title>
<link rel="stylesheet" href="static/styles.css">
</head>
<body>
<h1>TraceWarden – Network Report</h1>
<div class="meta">
    Generated at: {time.strftime("%d/%m/%Y - %H:%M")}
</div>
<div class="summary">
<div>Total: <span>{summary['total']}</span></div>
<div>Passed: <span>{summary['passed']}</span></div>
<div>Failed: <span>{summary['failed']}</span></div>
<div>Avg HTTP response: <span>{avg_http_text}</span></div>
<div>Avg DNS lookup: <span>{avg_dns_text}</span></div>
<div>Ping reachability: <span>{ping_reach_text} hosts</span></div>
</div>
<table>
<thead>
<tr>
<th>Target / URL</th><th>Type</th><th>Details</th><th>Result</th><th>Error Message</th>
</tr>
</thead>
<tbody>
{rows_html}
</tbody>
</table>
</body>
</html>"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    return path
