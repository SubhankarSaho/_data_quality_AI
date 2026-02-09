from typing import TypedDict
from langgraph.graph import StateGraph
from llm_chain import generate_explanation

class RootCauseState(TypedDict):
    metric: str
    value: float
    z_score: float
    pipeline_ok: bool
    explanation: str

def decision_node(state: RootCauseState):
    if not state["pipeline_ok"]:
        state["explanation"] = "Metric anomaly likely caused by a data pipeline failure."
    elif abs(state["z_score"]) > 3:
        state["explanation"] = generate_explanation(
            state["metric"],
            state["value"],
            state["z_score"]
        )
    else:
        state["explanation"] = "Metric variation is within expected range."
    return state

graph = StateGraph(RootCauseState)
graph.add_node("decide", decision_node)
graph.set_entry_point("decide")
graph.set_finish_point("decide")

root_cause_graph = graph.compile()
