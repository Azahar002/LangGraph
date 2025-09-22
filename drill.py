from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class S(TypedDict, total = False):
    text: str
    clean: str
    token: int
    chars: int
    summary: str

def validate(state: S) -> S:
    assert "text" in state, "required Key 'text ' missing"
    assert isinstance(state["text"], str), "text must be a string"
    clean = state["text"].strip()
    assert clean, "text cannot be empty or white space"
    state["text"] = clean
    return state


def normalize(state: S) -> S:
    state["clean"] = " ".join(state["text"].split())
    return state

def stats(state: S) -> S:
    state["token"]= len(state["clean"].split())
    state['chars']=len(state["clean"])
    return state

def summarize(s: S) -> S:
    s["summary"] = f"{s['token']} tokens, {s['chars']} chars | head: {s['clean'][:20]}"
    return s

b = StateGraph(S)
#add nodes

b.add_node("validate", validate)
b.add_node("normalize", normalize)
b.add_node("stats", stats)
b.add_node("summarize", summarize)


#add edges
b.add_edge(START, "validate")
b.add_edge("validate", "normalize")
b.add_edge("normalize", "stats")
b.add_edge( "stats", "summarize")
b.add_edge( "summarize", END)

workflow = b.compile()

if __name__ == "__main__":
    out = workflow.invoke({"text": "   Langgraph makes control explicit.        "})
    print(out)

    assert out["clean"] == "Langgraph makes control explicit."
    assert out["token"] == 4
    assert out["summary"].startswith("4 tokens")
