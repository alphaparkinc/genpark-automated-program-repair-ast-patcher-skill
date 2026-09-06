"""
MCP Server for Automated Program Repair AST Patcher Skill.
"""

import json
import sys
from client import AutomatedProgramRepair

APR = AutomatedProgramRepair()


def handle_request(req: dict) -> dict:
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "generate_candidate_patches",
                    "description": "Generate mutated AST candidate patches for faulty code lines",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "source_code": {"type": "string"},
                            "faulty_line": {"type": "integer"}
                        },
                        "required": ["source_code", "faulty_line"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "generate_candidate_patches":
            res = APR.generate_candidate_patches(
                args["source_code"],
                args["faulty_line"]
            )
            return {"content": [{"type": "text", "text": json.dumps(res)}]}

        return {"error": f"Unknown tool: {tool_name}"}

    return {"error": f"Unknown method: {method}"}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            resp["id"] = req.get("id")
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
