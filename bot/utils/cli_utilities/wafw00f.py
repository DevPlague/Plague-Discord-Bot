import subprocess
import re

# opciones: -a, -T, --no-colors
TIMEOUT = 3     # Seconds
WAF_FOUND = re.compile(r"\[\+\] The site (https?://[^\s]+) is behind (.+?)(?: and/or (.+?))? WAF\.")
WAF_NOT_FOUND = re.compile(r"\[\-\]")
REQUESTS = re.compile(r"\[~\] Number of requests: \d+")


def wafw00f(url: str) -> None:
    """
    Runs the wafw00f tool to detect the presence of a Web Application Firewall (WAF)
    on the given URL.

    Args:
        `url`: The URL of the website to analyze.
    """
    proc = subprocess.run(["wafw00f", "-a", f"-T {TIMEOUT}", "--no-colors", url], capture_output=True)
    output = proc.stdout.decode("utf-8")

    match = re.search(WAF_FOUND, output)
    requests = re.search(REQUESTS, output)
    if match:
        # Opción 1: Linea del wafw00f entera (quitando el [+])
        print(match.group(0)[4:])

        # Opción 2: Cada apartado por separado
        url = match.group(1)
        waf1 = match.group(2)
        waf2 = match.group(3)
        print(f"URL: {url}")
        print(f"WAF 1: {waf1}")
        if waf2 is not None:
            print(f"WAF 2: {waf2}")
        print(requests.group(0)[4:])


    elif re.search(WAF_NOT_FOUND, output):
        print("No WAF detected by the generic detection.")
        print(requests.group(0)[4:])

    else:
        print(f"Site {url} appears to be down (or does not exist).")

wafw00f("hackersploit.org")