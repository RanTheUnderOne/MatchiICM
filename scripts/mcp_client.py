#!/usr/bin/env python3
"""Minimal MCP (JSON-RPC 2.0 / streamable-http) client for prod-mcp.nadlanai.org.

Real adapter that replaces the _mock/*.json loads. Same data shape comes out, so
downstream ICM stages (match.py etc.) don't change.

Usage:
  from mcp_client import MCPClient
  c = MCPClient(user_id="nadlanai.solutions@gmail.com")
  leads = c.call("list_leads", {"user_id": c.user_id, "limit": 50})
"""
import ast
import json
import re
import urllib.request

MCP_URL = "https://prod-mcp.nadlanai.org/mcp"
DEFAULT_USER = "nadlanai.solutions@gmail.com"

# strip Python enum reprs like <PropertyType.APARTMENT: 'apartment'> -> 'apartment'
_ENUM_RE = re.compile(r"<[A-Za-z_]+\.[A-Za-z_]+:\s*('[^']*')>")


class MCPClient:
    def __init__(self, user_id=DEFAULT_USER, url=MCP_URL):
        self.user_id = user_id
        self.url = url
        self.session = self._init()
        self._id = 1

    def _post(self, payload, want_headers=False):
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json, text/event-stream")
        req.add_header("User-Agent", "matchi-icm/1.0")
        if getattr(self, "session", None):
            req.add_header("Mcp-Session-Id", self.session)
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            sid = resp.headers.get("mcp-session-id")
        # streamable-http may wrap JSON in SSE ("data: {...}")
        if body.lstrip().startswith("data:"):
            body = body.split("data:", 1)[1].strip()
        parsed = json.loads(body)
        return (parsed, sid) if want_headers else parsed

    def _init(self):
        self.session = None
        payload = {"jsonrpc": "2.0", "id": 0, "method": "initialize",
                   "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                              "clientInfo": {"name": "matchi-icm", "version": "1.0"}}}
        _, sid = self._post(payload, want_headers=True)
        if not sid:
            raise RuntimeError("MCP init returned no mcp-session-id header")
        return sid

    def call(self, tool, arguments):
        self._id += 1
        payload = {"jsonrpc": "2.0", "id": self._id, "method": "tools/call",
                   "params": {"name": tool, "arguments": arguments}}
        resp = self._post(payload)
        if "error" in resp:
            raise RuntimeError(f"MCP error on {tool}: {resp['error']}")
        result = resp["result"]
        if result.get("isError"):
            txt = result["content"][0]["text"] if result.get("content") else "unknown"
            raise RuntimeError(f"tool {tool} failed: {txt}")
        # prefer structuredContent.result; fall back to text content
        sc = result.get("structuredContent", {})
        if "result" in sc:
            return sc["result"]
        return result.get("content", [{}])[0].get("text")


def parse_repr(s):
    """Parse a Python-repr dict string (with enum reprs) into a real dict."""
    cleaned = _ENUM_RE.sub(r"\1", s)
    return ast.literal_eval(cleaned)
