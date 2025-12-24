#!/usr/bin/env python3
"""Grok/X diagnostic: attempt to list models and run a sample completion; write diagnostics to diagnostics/grok-diagnostic.json"""
import json
import os
import sys
import socket
import traceback

outf = "diagnostics/grok-diagnostic.json"
os.makedirs("diagnostics", exist_ok=True)
report = {"attempts": [], "dns": {}, "http_fallback": None}
api_key = os.environ.get("GROK_API_KEY") or os.environ.get("XAI_API_KEY")
report["api_key_present"] = bool(api_key)

# DNS resolution check
try:
    ip = socket.gethostbyname("api.grok.com")
    report["dns"]["api.grok.com"] = {"resolved": True, "ip": ip}
except Exception as e:
    report["dns"]["api.grok.com"] = {"resolved": False, "error": str(e), "traceback": traceback.format_exc()}

# Try xai client first
try:
    import xai
    try:
        client = xai.Client(api_key=api_key)
        report["attempts"].append({"client": "xai", "info": "initialized"})
        # try to call a lightweight API
        try:
            resp = client.messages.create(model="grok-2", messages=[{"role": "user", "content": "Hello"}], max_tokens=20)
            report["attempts"][-1]["response"] = str(getattr(resp, "output_text", repr(resp)))
        except Exception as e:
            report["attempts"][-1]["error"] = {"message": str(e), "traceback": traceback.format_exc()}
    except Exception as e:
        report["attempts"].append({"client": "xai", "error": {"message": str(e), "traceback": traceback.format_exc()}})
except Exception as e:
    report["attempts"].append({"client": "xai", "error": {"message": str(e), "traceback": traceback.format_exc()}})

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
                                out = client.complete(prompt="Hello", model="grok-2", max_tokens=20)
                                report["attempts"][-1]["response"] = str(out)
                                break
                        except Exception as e:
                            report["attempts"][-1].setdefault("client_errors", []).append({name: {"message": str(e), "traceback": traceback.format_exc()}})
        except Exception as e:
            report["attempts"][-1]["error"] = {"message": str(e), "traceback": traceback.format_exc()}
    except Exception as e:
        report["attempts"].append({"client": "grok", "error": {"message": str(e), "traceback": traceback.format_exc()}})
except Exception as e:
    report["attempts"].append({"client": "grok", "error": {"message": str(e), "traceback": traceback.format_exc()}})

# HTTP fallback test to Grok REST endpoint (if API key present)
if api_key:
    import requests

    try:
        url = os.getenv("GROK_REST_URL", "https://api.grok.com/v1/chat/completions")
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"model": "grok-2", "messages": [{"role": "user", "content": "Hello"}], "max_tokens": 20}
        r = requests.post(url, json=payload, headers=headers, timeout=20)
        try:
            txt = r.text
        except Exception:
            txt = None
        report["http_fallback"] = {"status": getattr(r, "status_code", None), "text": (txt[:2000] if isinstance(txt, str) else txt)}
    except Exception as e:
        report["http_fallback"] = {"error": str(e), "traceback": traceback.format_exc()}

with open(outf, "w") as f:
    json.dump(report, f, indent=2)
print(json.dumps(report, indent=2))
