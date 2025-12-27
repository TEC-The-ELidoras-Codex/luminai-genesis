#!/usr/bin/env python3
"""Grok/X diagnostic: attempt to list models and run a sample completion; write diagnostics to diagnostics/grok-diagnostic.json"""
import json
import logging
import os
import socket
import traceback
from pathlib import Path

logger = logging.getLogger(__name__)

outf = Path("diagnostics") / "grok-diagnostic.json"
Path("diagnostics").mkdir(parents=True, exist_ok=True)
report = {"attempts": [], "dns": {}, "http_fallback": None}
api_key = os.environ.get("GROK_API_KEY") or os.environ.get("XAI_API_KEY")
report["api_key_present"] = bool(api_key)

# DNS resolution check (check both legacy and current endpoints)
for host in ("api.grok.com", "api.x.ai"):
    try:
        ip = socket.gethostbyname(host)
        report["dns"][host] = {"resolved": True, "ip": ip}
    except socket.gaierror as e:
        report["dns"][host] = {
            "resolved": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
        }
    except Exception as _:
        report["dns"][host] = {
            "resolved": False,
            "error": "unknown error",
            "traceback": traceback.format_exc(),
        }

# Try xai client first (if available)
try:
    import xai

    try:
        client = xai.Client(api_key=api_key)
        report["attempts"].append({"client": "xai", "info": "initialized"})
        # try to call a lightweight API
        try:
            resp = client.messages.create(
                model="grok-2",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=20,
            )
            report["attempts"][-1]["response"] = str(
                getattr(resp, "output_text", repr(resp)),
            )
        except Exception as _:
            report["attempts"][-1]["error"] = {
                "message": "call failed",
                "traceback": traceback.format_exc(),
            }
    except Exception as _:
        report["attempts"].append(
            {
                "client": "xai",
                "error": {
                    "message": "init failed",
                    "traceback": traceback.format_exc(),
                },
            },
        )
except Exception as _:
    report["attempts"].append(
        {
            "client": "xai",
            "error": {
                "message": "module import failed",
                "traceback": traceback.format_exc(),
            },
        },
    )

# Then try grok SDK
try:
    import grok

    report["attempts"].append({"client": "grok", "info": "imported"})
    try:
        # Try to call a simple completion
        try:
            if hasattr(grok, "complete"):
                out = grok.complete(prompt="Hello", model="grok-2", max_tokens=20)
                report["attempts"][-1]["response"] = str(out)
            else:
                # Try common client patterns
                for name in ("Client", "Grok", "GrokClient", "GrokAPI"):
                    C = getattr(grok, name, None)
                    if C:
                        try:
                            client = C(api_key=api_key)
                            if hasattr(client, "complete"):
                                out = client.complete(
                                    prompt="Hello", model="grok-2", max_tokens=20,
                                )
                                report["attempts"][-1]["response"] = str(out)
                                break
                        except Exception as e:
                            report["attempts"][-1].setdefault(
                                "client_errors", [],
                            ).append(
                                {
                                    name: {
                                        "message": str(e),
                                        "traceback": traceback.format_exc(),
                                    },
                                },
                            )
        except Exception as e:
            report["attempts"][-1]["error"] = {
                "message": str(e),
                "traceback": traceback.format_exc(),
            }
    except Exception as e:
        report["attempts"].append(
            {
                "client": "grok",
                "error": {"message": str(e), "traceback": traceback.format_exc()},
            },
        )
except Exception as e:
    report["attempts"].append(
        {
            "client": "grok",
            "error": {"message": str(e), "traceback": traceback.format_exc()},
        },
    )

# HTTP fallback test to Grok/XAI REST endpoint(s)
import requests


def _http_probe(url: str, api_key: str | None):
    try:
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        payload = {
            "model": "grok-2",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 20,
        }
        r = requests.post(url, json=payload, headers=headers, timeout=20)
        try:
            txt = r.text
        except Exception:
            txt = None
        return {
            "url": url,
            "status": getattr(r, "status_code", None),
            "text": (txt[:2000] if isinstance(txt, str) else txt),
        }
    except Exception as e:
        return {"url": url, "error": str(e), "traceback": traceback.format_exc()}


# Probe in order: explicit GROK_REST_URL, XAI_API_BASE, api.x.ai default
probe_urls = []
probe_urls.append(os.getenv("GROK_REST_URL"))
probe_urls.append(os.getenv("XAI_API_BASE"))
probe_urls.append("https://api.x.ai/v1/chat/completions")
probe_urls = [u for u in probe_urls if u]

report["http_fallback"] = []
for url in probe_urls:
    report["http_fallback"].append(_http_probe(url, api_key))

# If an API key is present, perform an authenticated XAI probe and save result separately
if api_key:
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        payload = {
            "model": "grok-2",
            "messages": [
                {"role": "user", "content": "Automated probe: are you online?"},
            ],
            "max_tokens": 60,
        }
        try:
            r = requests.post(
                "https://api.x.ai/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=20,
            )
            auth_probe = {
                "status_code": getattr(r, "status_code", None),
                "text": (r.text[:8000] if isinstance(r.text, str) else None),
            }
        except Exception as e:
            auth_probe = {"error": str(e), "traceback": traceback.format_exc()}
    except Exception as e:
        auth_probe = {"error": str(e), "traceback": traceback.format_exc()}
    try:
        p = Path("diagnostics") / "xai-auth-probe.json"
        with p.open("w") as f:
            json.dump(auth_probe, f, indent=2)
    except OSError as _:
        logger.warning("Could not write xai auth probe file")

try:
    with outf.open("w") as f:
        json.dump(report, f, indent=2)
    logger.info("Grok diagnostic written to %s", outf)
except OSError as _:
    logger.exception("Failed to write grok diagnostic file")
logger.info(json.dumps(report, indent=2))
