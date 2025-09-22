from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class S(TypedDict, total=False):
    text: str
    length: int

def step1(s: S) -> S:
    # BUG: allows empty/missing text
    if s.get("text"):
        s["length"] = len(s.get("text"))  # silent failure
    else:
        print("text is cannot be empty")
    return s

def step2(s: S) -> S:
    s["ok"] = s["length"] > 0
    return s

b = StateGraph(S)
b.add_node("step1", step1)
b.add_node("step2", step2)
b.add_edge(START, "step1")
b.add_edge("step1", "step2")
b.add_edge("step2", END)
g = b.compile()

if __name__ == "__main__":
    print(g.invoke({}))  # should not silently pass
