#!/usr/bin/env python3
"""
obs-workshop load generator.

Sends a burst of POST /orders requests to the workshop
API.
"""
import argparse
import json
import random
import sys
import time
import urllib.request
import urllib.error

ITEMS = ["brake-pad", "oil-filter", "spark-plug", "wiper-blade", "air-filter",
         "battery", "headlight", "alternator", "radiator", "fuel-pump"]


def post(url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")
    except urllib.error.URLError as e:
        return None, str(e)


def main():
    parser = argparse.ArgumentParser(description="Obs workshop load generator")
    parser.add_argument("api_base_url", help="e.g. https://xxxx.execute-api.eu-central-1.amazonaws.com/prod")
    parser.add_argument("--count", type=int, default=60, help="number of requests")
    parser.add_argument("--delay", type=float, default=1.0, help="seconds between requests")
    args = parser.parse_args()

    base = args.api_base_url.rstrip("/")
    ok = errors = 0

    for i in range(1, args.count + 1):
        payload = {"item": random.choice(ITEMS), "quantity": random.randint(1, 5)}
        status, _ = post(f"{base}/orders", payload)
        if status and 200 <= status < 300:
            ok += 1
        else:
            errors += 1
        print(f"[{i}/{args.count}] POST /orders -> {status}")

        time.sleep(args.delay)

    print(f"\nDone. Success: {ok}, Non-2xx/errors: {errors}")


if __name__ == "__main__":
    main()
