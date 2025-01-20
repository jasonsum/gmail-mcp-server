from mcp import ListToolsResult
import streamlit as st
import asyncio
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM

app = MCPApp(name="mcp_basic_agent")

def format_list_tools_result(list_tools_result: ListToolsResult):
    res = ""
    for tool in list_tools_result.tools:
        res += f"- **{tool.name}**: {tool.description}\n\n"
    return res


async def main():
    await app.initialize()

    finder_agent = Agent(
        name="finder",
        instruction="""You are an agent with access to the filesystem,
        as well as the ability to fetch URLs. Your job is to identify
        the closest match to a user's request, make the appropriate tool calls,
        and return the URI and CONTENTS of the closest match.""",
        server_names=["fetch", "filesystem"],
    )
    await finder_agent.initialize()
    llm = await finder_agent.attach_llm(OpenAIAugmentedLLM)

    tools = await finder_agent.list_tools()
    tools_str = format_list_tools_result(tools)

    with st.expander("View Tools"):
        st.markdown(tools_str)

if __name__ == "__main__":
    asyncio.run(main())