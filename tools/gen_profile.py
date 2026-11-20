#!/usr/bin/env python3
"""Generate the driver catalogue in profile/README.md from the drivers' own repositories.

Between the markers

    <!-- BEGIN GENERATED: catalogue -->  ...  <!-- END GENERATED: catalogue -->
    <!-- BEGIN GENERATED: summary -->    ...  <!-- END GENERATED: summary -->

the script writes a table per function group. Every cell is read from the driver's repository through the GitHub
API: the description (chip), driver.yml (bus, MCU family, hardware level, safety class), CMakeLists.txt (C++ standard) and the
latest release (tag, release candidate or not). Only the grouping below is curated; a driver with no group makes
the script fail, so a new driver cannot be left off the page.

    python3 tools/gen_profile.py            rewrite the README between the markers
    python3 tools/gen_profile.py --check    exit 1 if the README differs from what would be generated

Standard library only (Python 3.9+). The token comes from GITHUB_TOKEN or GH_TOKEN, else `gh auth token`; a public
read works without one but is rate limited.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ORG = "kokeb-labs-drivers"
README = Path(__file__).resolve().parent.parent / "profile" / "README.md"
API = "https://api.github.com"
# Repositories in the organization that are not drivers.
NOT_DRIVERS = {"driver-requests"}

# Function groups, in page order. The only curated data: which group a driver belongs to.
GROUPS = [
    ("Analog-to-digital converters", ["driver-ads7952", "driver-ads9324"]),
    ("Position and motion sensing", ["driver-as5047u", "driver-bno08x"]),
    ("Motor and servo control", ["driver-tmc5160", "driver-tmc9660", "driver-dynamixel"]),
    ("Fieldbus and communication", ["driver-canopen-client"]),
    ("Security", ["driver-se05x"]),
    ("Solenoid, valve and power", ["driver-max22200", "driver-tle92466ed", "driver-pf1550"]),
    ("GPIO, PWM and LEDs", ["driver-pcal9555", "driver-pca9685", "driver-ws2812-rmt"]),
    ("Memory", ["driver-at25040b"]),
    ("Display and buttons", ["driver-isf15acp4"]),
    ("Temperature, pressure, flow and gas sensors", ["driver-bmp581", "driver-mcp9700", "driver-ntc-thermistor",
                                                      "driver-sfm-flow-meter", "driver-alicat-basis2",
                                                      "driver-fdo2"]),
]
BUS_NAMES = {"canopen": "CANopen", "modbus": "Modbus", "onewire": "1-Wire"}
LEVELS = {"H0": "H0 host model", "H1": "H1 bench", "H2": "H2 verified"}
SAFETY = {"passive": "Passive", "sensing": "Sensing", "actuating": "Actuating", "unclassified": "Not classified"}


def token() -> str:
    for var in ("GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(var):
            return os.environ[var]
    try:
        return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


TOKEN = token()


def get(path: str, raw: bool = False):
    """GET an API path; the decoded JSON, or the raw text; None on 404."""
    req = urllib.request.Request(API + path)
    req.add_header("Accept", "application/vnd.github.raw+json" if raw else "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as err:
        if err.code == 404:
            return None
        raise
    return body if raw else json.loads(body)


def public_drivers() -> list[dict]:
    repos, page = [], 1
    while True:
        chunk = get(f"/orgs/{ORG}/repos?type=public&per_page=100&page={page}")
        repos += chunk
        if len(chunk) < 100:
            break
        page += 1
    return sorted((r for r in repos if r["name"].startswith("driver-") and r["name"] not in NOT_DRIVERS
                   and not r["archived"] and not r.get("fork")), key=lambda r: r["name"])


def yaml_list(text: str, key: str) -> list[str]:
    m = re.search(rf"^{key}:\s*\[([^\]]*)\]", text, re.M)
    return [v.strip() for v in m.group(1).split(",") if v.strip()] if m else []


def facts(repo: dict) -> dict:
    name = repo["name"]
    meta = get(f"/repos/{ORG}/{name}/contents/driver.yml", raw=True) or ""
    cmake = get(f"/repos/{ORG}/{name}/contents/CMakeLists.txt", raw=True) or ""
    releases = get(f"/repos/{ORG}/{name}/releases?per_page=5") or []
    releases = [r for r in releases if not r["draft"]]
    found = re.finditer(r"cxx_std_(\d+)|CMAKE_CXX_STANDARD\s+(\d+)", cmake)
    std = sorted({int(m.group(1) or m.group(2)) for m in found})
    level = re.search(r"^\s+level:\s*(H[012])\b", meta, re.M)
    safety = re.search(r"^safety:[ \t]*(?:#.*)?\n(?:[ \t]+\S.*\n)*?[ \t]+class:\s*(passive|sensing|actuating)\b", meta, re.M)
    mcus = yaml_list(meta, "mcus")
    desc = re.sub(r"^C\+\+\d+ (?:(?:driver|library) for (?:the )?)?", "", repo.get("description") or "").rstrip(".")
    return {
        "name": name,
        "what": desc,
        "bus": ", ".join(BUS_NAMES.get(b, b.upper()) for b in yaml_list(meta, "bus")) or "n/a",
        "mcus": [m for m in mcus if m != "any"],
        "peripheral": (re.search(r"^peripheral:\s*(\w+)", meta, re.M) or [None, None])[1],
        "std": f"C++{max(std)}" if std else "not stated",
        "tag": releases[0]["tag_name"] if releases else "none yet",
        "rc": bool(releases and releases[0]["prerelease"]),
        "level": level.group(1) if level else "H0",
        "safety": safety.group(1) if safety else "unclassified",
    }


def bus_cell(f: dict) -> str:
    if f["mcus"]:
        what = ", ".join(m.upper() for m in f["mcus"])
        return f"{f['bus']} ({what} only)"
    return f["bus"]


def render(all_facts: list[dict]) -> tuple[str, str]:
    by_name = {f["name"]: f for f in all_facts}
    grouped = {n for _, names in GROUPS for n in names}
    missing = sorted(set(by_name) - grouped)
    if missing:
        sys.exit(f"gen_profile: no group for {', '.join(missing)}: add them to GROUPS in tools/gen_profile.py")
    gone = sorted(grouped - set(by_name))
    if gone:
        sys.exit(f"gen_profile: GROUPS lists {', '.join(gone)}, which is not a public driver; remove it")
    out = []
    for title, names in GROUPS:
        out += [f"### {title}", "", "| Driver | Chip or device | Bus | Standard | Latest release | Hardware | Safety class |",
                "| --- | --- | --- | --- | --- | --- | --- |"]
        for n in names:
            f = by_name[n]
            tag = f"`{f['tag']}`" + (" (release candidate)" if f["rc"] else "")
            out.append(f"| [`{n}`](https://github.com/{ORG}/{n}) | {f['what']} | {bus_cell(f)} | {f['std']} | "
                       f"{tag} | {LEVELS[f['level']]} | {SAFETY[f['safety']]} |")
        out.append("")
    n = len(all_facts)
    rcs = sum(f["rc"] for f in all_facts)
    stds = sorted({f["std"] for f in all_facts})
    levels = {lv: sum(f["level"] == lv for f in all_facts) for lv in LEVELS}
    parts = [f"{levels[lv]} at {lv}" for lv in LEVELS if levels[lv]]
    classes = {k: sum(f["safety"] == k for f in all_facts) for k in SAFETY}
    kinds = ", ".join(f"{classes[k]} {SAFETY[k].lower()}" for k in SAFETY if classes[k])
    state = (f"All {n} are at a release candidate." if rcs == n else
             f"{rcs} of {n} are at a release candidate, the rest at a full release.")
    summary = (f"**{n} public drivers.** {state} "
               f"Language standard today: {', '.join(stds)}.\n"
               f"Hardware level: {', '.join(parts)}. Safety class: {kinds}.")
    return "\n".join(out).rstrip() + "\n", summary


def splice(text: str, name: str, body: str) -> str:
    pat = re.compile(rf"(<!-- BEGIN GENERATED: {name} -->\n).*?(<!-- END GENERATED: {name} -->)", re.S)
    if not pat.search(text):
        sys.exit(f"gen_profile: markers for '{name}' not found in {README}")
    return pat.sub(lambda m: m.group(1) + body.rstrip("\n") + "\n" + m.group(2), text)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="exit 1 if the README is out of date, change nothing")
    args = ap.parse_args()
    catalogue, summary = render([facts(r) for r in public_drivers()])
    old = README.read_text(encoding="utf-8")
    new = splice(splice(old, "catalogue", catalogue), "summary", summary)
    if args.check:
        if new != old:
            print("profile/README.md is out of date; run `python3 tools/gen_profile.py` and commit the result.")
            return 1
        print("profile/README.md catalogue is up to date.")
        return 0
    if new != old:
        README.write_text(new, encoding="utf-8")
        print("profile/README.md updated.")
    else:
        print("profile/README.md already up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
