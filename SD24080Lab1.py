
"""
BFS and DFS Search Algorithm Explorer
Run: python -m streamlit run bfs_simple.py
"""

import json
import os
from collections import deque

import streamlit as st
from graphviz import Digraph, escape


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="BFS and DFS Explorer",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
<style>
h1 {
    color: #0891b2;
}
.stButton button {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("Python Search Algorithms")
st.caption(
    "Interactive Breadth-First Search (BFS) "
    "and Depth-First Search (DFS)"
)


# --------------------------------------------------
# 2. DISPLAY ORIGINAL ASSIGNMENT GRAPH
# --------------------------------------------------

st.subheader("Original Graph from Assignment")

image_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "graph.png"
)

if os.path.exists(image_path):
    st.image(
        image_path,
        caption="Directed graph provided in the assignment",
        width="stretch"
    )
else:
    st.warning(
        "Graph image not found. Save the assignment image "
        "as graph.png in the same folder as bfs_simple.py."
    )


# --------------------------------------------------
# 3. DEFAULT DIRECTED GRAPH
# --------------------------------------------------

default_graph = {
    "A": ["B", "D"],
    "B": ["C", "E", "G"],
    "C": ["A"],
    "D": ["C"],
    "E": ["H"],
    "F": [],
    "G": ["F"],
    "H": ["F", "G"]
}


# --------------------------------------------------
# 4. BREADTH-FIRST SEARCH (BFS)
# --------------------------------------------------

def bfs(graph, start):
    visited = {start}
    queue = deque([(start, 0)])

    order = []
    levels = {}
    steps = []

    while queue:
        node, level = queue.popleft()
        order.append(node)

        levels.setdefault(level, []).append(node)

        steps.append({
            "node": node,
            "level": level,
            "queue": [item[0] for item in queue],
            "visited": order.copy()
        })

        for neighbour in sorted(graph[node]):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append((neighbour, level + 1))

    return order, levels, steps


# --------------------------------------------------
# 5. DEPTH-FIRST SEARCH (DFS)
# --------------------------------------------------

def dfs(graph, start):
    visited = set()
    order = []
    steps = []

    def visit(node):
        visited.add(node)
        order.append(node)

        steps.append({
            "node": node,
            "visited": order.copy()
        })

        for neighbour in sorted(graph[node]):
            if neighbour not in visited:
                visit(neighbour)

    visit(start)

    return order, steps


# --------------------------------------------------
# 6. SIDEBAR SETTINGS
# --------------------------------------------------

st.sidebar.header("Search Settings")

st.sidebar.caption(
    "Choose the algorithm and starting node. "
    "Alphabetical tie-breaking is applied automatically."
)

algorithm = st.sidebar.radio(
    "Select algorithm",
    ["BFS", "DFS", "Compare BFS and DFS"]
)

start_node = st.sidebar.selectbox(
    "Starting node",
    sorted(default_graph.keys()),
    index=0
)

if st.sidebar.button("Run Search", type="primary"):
    st.session_state["search_run"] = True

if "search_run" not in st.session_state:
    st.session_state["search_run"] = False


# --------------------------------------------------
# 7. RUN SEARCH
# --------------------------------------------------

if st.session_state["search_run"]:

    bfs_order, bfs_levels, bfs_steps = bfs(
        default_graph, start_node
    )

    dfs_order, dfs_steps = dfs(
        default_graph, start_node
    )

    if algorithm == "BFS":
        selected_order = bfs_order
    elif algorithm == "DFS":
        selected_order = dfs_order
    else:
        selected_order = bfs_order

    visited_nodes = set(selected_order)

    st.divider()

    # --------------------------------------------------
    # 8. INTERACTIVE GRAPH VISUALIZATION
    # --------------------------------------------------

    graph_column, result_column = st.columns([3, 2])

    with graph_column:
        st.subheader("Directed Graph Visualization")

        st.caption(
            "Yellow = starting node | "
            "Cyan = visited | Grey = unvisited"
        )

        dot = Digraph()

        dot.attr(
            bgcolor="transparent",
            rankdir="LR",
            size="12,7!",
            dpi="100"
        )

        dot.attr(
            "node",
            shape="circle",
            style="filled",
            fontname="Arial",
            fontcolor="#111827",
            fontsize="14",
            width="0.65",
            height="0.65"
        )

        dot.attr(
            "edge",
            color="#64748b",
            arrowsize="0.8"
        )

        node_ids = {
            node: f"node_{i}"
            for i, node in enumerate(default_graph)
        }

        for node in default_graph:

            if node == start_node:
                color = "#fde68a"
            elif node in visited_nodes:
                color = "#67e8f9"
            else:
                color = "#e2e8f0"

            if node in selected_order:
                position = selected_order.index(node) + 1
                label = f"{node}\n#{position}"
            else:
                label = node

            dot.node(
                node_ids[node],
                escape(label),
                fillcolor=color,
                color="#0891b2"
            )

        for node, neighbours in default_graph.items():
            for neighbour in neighbours:
                dot.edge(
                    node_ids[node],
                    node_ids[neighbour]
                )

        st.graphviz_chart(dot, width="stretch")

    # --------------------------------------------------
    # 9. TRAVERSAL RESULTS
    # --------------------------------------------------

    with result_column:

        st.subheader("Traversal Results")

        if algorithm == "BFS":

            st.markdown("### Breadth-First Search")

            st.code(
                " -> ".join(bfs_order),
                language="text"
            )

            st.metric(
                "Visited Nodes",
                f"{len(bfs_order)} / {len(default_graph)}"
            )

            st.markdown("### BFS Levels")

            for level, nodes in bfs_levels.items():
                st.write(
                    f"**Level {level}:** "
                    + ", ".join(nodes)
                )

            st.markdown("### Search Process")

            for i, step in enumerate(bfs_steps, start=1):
                st.write(
                    f"**Step {i}:** Visit {step['node']} "
                    f"(Level {step['level']})"
                )

                st.caption(
                    "Queue remaining: "
                    + (
                        ", ".join(step["queue"])
                        if step["queue"]
                        else "Empty"
                    )
                )

        elif algorithm == "DFS":

            st.markdown("### Depth-First Search")

            st.code(
                " -> ".join(dfs_order),
                language="text"
            )

            st.metric(
                "Visited Nodes",
                f"{len(dfs_order)} / {len(default_graph)}"
            )

            st.markdown("### Search Process")

            for i, step in enumerate(dfs_steps, start=1):
                st.write(
                    f"**Step {i}:** Visit {step['node']}"
                )

                st.caption(
                    "Visited so far: "
                    + " -> ".join(step["visited"])
                )

            st.info(
                "DFS explores the alphabetically first "
                "unvisited neighbour as deeply as possible "
                "before backtracking."
            )

        else:

            st.markdown("### BFS vs DFS")

            st.write("**BFS traversal**")

            st.code(
                " -> ".join(bfs_order),
                language="text"
            )

            st.write("**DFS traversal**")

            st.code(
                " -> ".join(dfs_order),
                language="text"
            )

            st.markdown("### BFS Levels")

            for level, nodes in bfs_levels.items():
                st.write(
                    f"**Level {level}:** "
                    + ", ".join(nodes)
                )

            st.markdown("### Key Difference")

            st.write(
                "BFS explores the graph level by level "
                "using a queue (FIFO)."
            )

            st.write(
                "DFS explores one branch as deeply as possible "
                "before backtracking."
            )


# --------------------------------------------------
# 10. FOOTER
# --------------------------------------------------

else:
    st.info(
        "Select an algorithm and starting node in the sidebar, "
        "then click Run Search to display the results."
    )

st.divider()

st.caption(
    "Search Algorithm Explorer | "
    "Directed Graph | Alphabetical Tie-Breaking"
)
