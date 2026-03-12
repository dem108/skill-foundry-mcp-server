#!/usr/bin/env python3

from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
from typing import Any

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

MCP_RESOURCE = "https://mcp.ai.azure.com"
DEFAULT_MCP_SERVER_URL = "https://mcp.ai.azure.com"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Minimal bearer-token MCP client for the Foundry MCP Server. "
            "If --bearer-token is not provided, the script acquires one via Azure CLI."
        )
    )
    parser.add_argument(
        "--server-url",
        default=os.environ.get("FOUNDRY_MCP_SERVER_URL", DEFAULT_MCP_SERVER_URL),
        help=(
            "Foundry MCP Server Streamable HTTP endpoint. Defaults to "
            "FOUNDRY_MCP_SERVER_URL or https://mcp.ai.azure.com."
        ),
    )
    parser.add_argument(
        "--bearer-token",
        default=os.environ.get("FOUNDRY_MCP_BEARER_TOKEN"),
        help=(
            "Bearer token for the MCP server. Defaults to FOUNDRY_MCP_BEARER_TOKEN. "
            "If omitted, the script runs `az account get-access-token`."
        ),
    )
    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="List available MCP tools after session initialization.",
    )
    parser.add_argument(
        "--tool",
        help="Optional MCP tool name to call after connecting.",
    )
    parser.add_argument(
        "--arguments",
        default="{}",
        help="JSON object passed to --tool. Defaults to {}.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=30.0,
        help="HTTP request timeout in seconds. Default: 30.",
    )
    parser.add_argument(
        "--read-timeout-seconds",
        type=float,
        default=300.0,
        help="HTTP read timeout in seconds. Default: 300.",
    )

    args = parser.parse_args()

    if not args.list_tools and not args.tool:
        parser.error("Specify at least one of --list-tools or --tool.")

    return args


def parse_tool_arguments(raw_arguments: str) -> dict[str, Any]:
    try:
        parsed = json.loads(raw_arguments)
    except json.JSONDecodeError as exc:
        raise ValueError(f"--arguments must be valid JSON: {exc}") from exc

    if not isinstance(parsed, dict):
        raise ValueError("--arguments must decode to a JSON object.")

    return parsed


def acquire_bearer_token(explicit_token: str | None) -> str:
    if explicit_token:
        return explicit_token

    command = [
        "az",
        "account",
        "get-access-token",
        "--resource",
        MCP_RESOURCE,
        "--query",
        "accessToken",
        "-o",
        "tsv",
    ]

    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "Azure CLI was not found. Install `az` or provide --bearer-token explicitly."
        ) from exc

    if completed.returncode != 0:
        stderr = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(
            "Failed to acquire Entra bearer token with Azure CLI. "
            f"Command: {' '.join(command)}. Output: {stderr}"
        )

    token = completed.stdout.strip()
    if not token:
        raise RuntimeError(
            "Azure CLI returned an empty access token for https://mcp.ai.azure.com."
        )

    return token


def dump_model(value: Any) -> str:
    if hasattr(value, "model_dump_json"):
        return value.model_dump_json(indent=2, exclude_none=True)
    if hasattr(value, "model_dump"):
        return json.dumps(value.model_dump(exclude_none=True), indent=2)
    return json.dumps(value, indent=2, default=str)


async def run_client(
    *,
    server_url: str,
    bearer_token: str,
    list_tools: bool,
    tool_name: str | None,
    tool_arguments: dict[str, Any],
    timeout_seconds: float,
    read_timeout_seconds: float,
) -> None:
    http_client = httpx.AsyncClient(
        headers={"Authorization": f"Bearer {bearer_token}"},
        timeout=httpx.Timeout(timeout_seconds, read=read_timeout_seconds),
    )

    async with http_client:
        async with streamable_http_client(
            url=server_url,
            http_client=http_client,
        ) as streams:
            read_stream = streams[0]
            write_stream = streams[1]

            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                if list_tools:
                    tools = await session.list_tools()
                    print(dump_model(tools))

                if tool_name:
                    result = await session.call_tool(tool_name, tool_arguments)
                    print(dump_model(result))


def main() -> int:
    args = parse_args()

    try:
        tool_arguments = parse_tool_arguments(args.arguments)
        bearer_token = acquire_bearer_token(args.bearer_token)
        asyncio.run(
            run_client(
                server_url=args.server_url,
                bearer_token=bearer_token,
                list_tools=args.list_tools,
                tool_name=args.tool,
                tool_arguments=tool_arguments,
                timeout_seconds=args.timeout_seconds,
                read_timeout_seconds=args.read_timeout_seconds,
            )
        )
    except Exception as exc:  # surfaced to stderr with non-zero exit for shell use
        print(f"manual_mcp_client.py: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
