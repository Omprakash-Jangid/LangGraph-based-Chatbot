from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3, requests, os
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
load_dotenv()

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite')

# tools 
Search_tool = DuckDuckGoSearchRun(region='us', language='en') #pre build tool for search

@tool
def calculator(first_number: float, second_number: float, operation: str) -> str:
    """Perform a simple calculation.
    Args:
        first_number (float): The first number.
        second_number (float): The second number.
        operation (str): The operation to perform ('add', 'subtract', 'multiply', 'divide').
    Returns:
        str: The result of the calculation or an error message.
    """
    if operation == 'add':
        return str(first_number + second_number)
    elif operation == 'subtract':
        return str(first_number - second_number)
    elif operation == 'multiply':
        return str(first_number * second_number)
    elif operation == 'divide':
        if second_number != 0:
            return str(first_number / second_number)
        else:
            return "Error: Division by zero is not allowed."
    else:
        return "Error: Unsupported operation."

@tool
def get_stock_price(stock_symbol: str) -> str:
    """Get the current stock price for a given stock symbol.
    Args:
        stock_symbol (str): The stock symbol to look up.
    Returns:
        str: The current stock price or an error message.
    """ 
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_symbol}&apikey={os.getenv('ALPHA_VANTAGE_API_KEY')}"
    r = requests.get(url)
    return r.json()

# make tool list
tools = [Search_tool, calculator,  get_stock_price]
llm_with_tools = llm.bind_tools(tools)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    #response = llm.invoke(messages)
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
# Checkpointer
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)
graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for check in checkpointer.list(None):
        all_threads.add(check.config['configurable']['thread_id'])
    return list(all_threads)

#test
CONFIG = {'configurable': {'thread_id': 'thread_id-1'}}
response = chatbot.invoke(
                {"messages": [HumanMessage(content="what is my name buddy?")]},
                config=CONFIG
            )

print("Response:",response)