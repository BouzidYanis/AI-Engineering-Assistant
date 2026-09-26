"""Run with python -m agent.agent [question]."""

import argparse
import asyncio
import os
from pathlib import Path
import sys

from agent.prompts import DEFAULT_QUESTION, SYSTEM_PROMPT

PROJECT_ROOT = Path(__file__).resolve().parents[1]


async def run(question: str) -> str:
    """Investigate a question with a scoped MCP session and hosted model."""
    from dotenv import load_dotenv
    from langchain.agents import create_agent
    from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
    from langchain_mcp_adapters.tools import load_mcp_tools
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    load_dotenv(PROJECT_ROOT / ".env")
    token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not token:
        raise ValueError("Définissez HUGGINGFACEHUB_API_TOKEN dans .env ou l'environnement.")
    model = ChatHuggingFace(llm=HuggingFaceEndpoint(
        repo_id=os.getenv("HF_MODEL_ID", "openai/gpt-oss-20b"),
        huggingfacehub_api_token=token,
        max_new_tokens=2048,
        temperature=0.1,
    ))
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server.server"],
        cwd=str(PROJECT_ROOT),
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            assistant = create_agent(
                model=model,
                tools=await load_mcp_tools(session),
                system_prompt=SYSTEM_PROMPT,
            )
            result = await assistant.ainvoke(
                {"messages": [("user", question)]},
                config={"recursion_limit": 30},
            )
            return result["messages"][-1].text


def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnostic applicatif et migration via MCP.")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()
    try:
        print(asyncio.run(run(args.question)))
    except KeyboardInterrupt:
        raise SystemExit(130)
    except Exception as exc:
        print(f"Échec de l'analyse : {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
