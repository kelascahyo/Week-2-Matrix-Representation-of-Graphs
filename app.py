# app.py
import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import json

# Page Setup
st.set_page_config(page_title="Week 2: Graph Representations", layout="wide")

st.title("🎓 Week 2 Crash Course: Matrix Representations & D3.js")
st.write("Explore how visual graphs translate into machine-readable mathematical models, rendered in real-time using D3.js.")

# --- SIDEBAR NAV ---
st.sidebar.header("Course Navigation")
section = st.sidebar.radio("Go to:", ["1. Learn Intuition & Theory", "2. Interactive Python-to-D3 Tool"])

# ==========================================
# SECTION 1: THEORY & INTUITION
# ==========================================
if section == "1. Learn Intuition & Theory":
    st.header("🏗️ Core Intuition")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Why Standard NNs Struggle with Graphs")
        st.write("""
        Traditional architectures (like CNNs or RNNs) expect grids or sequences—data with a fixed grid structure or sequential order. 
        
        Graphs break these paradigms:
        - **Varying Topology:** A node can have zero neighbors or millions.
        - **Permutation Invariance:** Shuffling the structural list index changes the matrix layout entirely, but the underlying physical graph remains identical.
        """)
        
    with col2:
        st.subheader("Mathematical Focus")
        st.write("""
        - **Matrix Multiplication:** Allows nodes to cleanly pull, weight, and aggregate context matrices from their connected neighbors.
        - **Eigenvectors:** Define structural backbones, showing where data naturally clusters or flows.
        - **Message Propagation:** The structural dance where nodes gather neighbor embeddings, mix them with local attributes, and update state steps.
        """)

    st.write("---")
    st.subheader("🧩 Key Graph Matrices")
    
    st.table({
        "Representation": ["Adjacency Matrix", "Edge List", "Sparse Matrix", "Feature Matrix", "Laplacian Matrix"],
        "Mathematical Purpose": [
            "A square matrix where index A[i][j] = 1 indicates a connection.",
            "A streamlined list of pairs mapping [source, target] connections directly.",
            "Memory-saving compressed arrays that ignore zeros in mostly-disconnected systems.",
            "An N x F array storing the real-world properties/attributes of every individual node.",
            "Calculated as L = D - A (Degree minus Adjacency). Used to analyze graph diffusion and layout physics."
        ]
    })

# ==========================================
# SECTION 2: INTERACTIVE PIPELINE TOOL
# ==========================================
elif section == "2. Interactive Python-to-D3 Tool":
    st.header("💻 Interactive Force-Directed Graph Pipeline")
    st.write("Modify the graph structure in Python using the checkboxes. NetworkX processes the math, and passes the network to **D3.js** for browser physics rendering.")

    # Python State Configuration
    st.subheader("Step 1: Configure Graph Structure (Python)")
    num_nodes = st.slider("Total Nodes:", min_value=3, max_value=7, value=5)
    
    # Generate dynamic interaction checkboxes for potential edges
    st.write("Toggle Connections:")
    edges = []
    cols = st.columns(3)
    idx = 0
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            with cols[idx % 3]:
                # Pre-check a few boxes for an attractive starting shape
                is_default = (i == 0 or j == i + 1)
                if st.checkbox(f"Connect {i} ↔ {j}", value=is_default, key=f"e_{i}_{j}"):
                    edges.append((i, j))
            idx += 1

    # --- COMPUTATION WITH NETWORKX ---
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    G.add_edges_from(edges)
    
    # Extract matrices using NetworkX
    adj_matrix = nx.to_numpy_array(G, dtype=int).tolist()
    edge_list = list(G.edges())
    
    # Format the data cleanly into the explicit JSON format D3 force graphs require
    d3_data = {
        "nodes": [{"id": str(n), "label": f"Node {n}"} for n in G.nodes()],
        "links": [{"source": str(u), "target": str(v)} for u, v in G.edges()]
    }

    st.write("---")
    
    # Screen Layout Split
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("Step 2: Machine-Readable Output")
        st.markdown("**Adjacency Matrix ($A$):**")
        st.code(str(nx.to_numpy_array(G, dtype=int)))
        
        st.markdown("**Edge List Data:**")
        st.code(str(edge_list))

    with col_right:
        st.subheader("Step 3: D3.js Force-Directed Rendering")
        
        # --- EMBEDDED D3.JS RUNTIME INJECTION ---
        d3_html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://d3js.org/d3.v7.min.js"></script>
            <style>
                body {{
                    margin: 0;
                    background-color: transparent;
                    font-family: sans-serif;
                }}
                .node {{
                    fill: #FF4B4B;
                    stroke: #fff;
                    stroke-width: 2px;
                    cursor: pointer;
                }}
                .link {{
                    stroke: #999;
                    stroke-opacity: 0.6;
                    stroke-width: 2px;
                }}
                text {{
                    fill: #31333F;
                    font-size: 12px;
                    font-weight: bold;
                    pointer-events: none;
                }}
            </style>
        </head>
        <body>
            <svg width="500" height="300"></svg>
            <script>
                // Data injected straight from NetworkX processing pipeline
                const graphData = {json.dumps(d3_data)};

                const svg = d3.select("svg");
                const width = +svg.attr("width");
                const height = +svg.attr("height");

                // Initialize Force Simulator
                const simulation = d3.forceSimulation(graphData.nodes)
                    .force("link", d3.forceLink(graphData.links).id(d => d.id).distance(80))
                    .force("charge", d3.forceManyBody().strength(-150))
                    .force("center", d3.forceCenter(width / 2, height / 2));

                // Draw Link elements
                const link = svg.append("g")
                    .attr("class", "links")
                    .selectAll("line")
                    .data(graphData.links)
                    .enter().append("line")
                    .attr("class", "link");

                // Draw Node elements
                const node = svg.append("g")
                    .attr("class", "nodes")
                    .selectAll("circle")
                    .data(graphData.nodes)
                    .enter().append("circle")
                    .attr("class", "node")
                    .attr("r", 14)
                    .call(d3.drag()
                        .on("start", dragstarted)
                        .on("drag", dragged)
                        .on("end", dragended));

                // Add Text Node Labels
                const labels = svg.append("g")
                    .selectAll("text")
                    .data(graphData.nodes)
                    .enter().append("text")
                    .attr("dx", 18)
                    .attr("dy", 4)
                    .text(d => d.label);

                // Update physical coordinate positions loop on tick
                simulation.on("tick", () => {{
                    link
                        .attr("x1", d => d.source.x)
                        .attr("y1", d => d.source.y)
                        .attr("x2", d => d.target.x)
                        .attr("y2", d => d.target.y);

                    node
                        .attr("cx", d => d.x)
                        .attr("cy", d => d.y);

                    labels
                        .attr("x", d => d.x)
                        .attr("y", d => d.y);
                }});

                // Dragging Interactivity Handlers
                function dragstarted(event, d) {{
                    if (!event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                }}
                function dragged(event, d) {{
                    d.fx = event.x;
                    d.fy = event.y;
                }}
                function dragended(event, d) {{
                    if (!event.active) simulation.alphaTarget(0);
                    d.fx = null;
                    d.fy = null;
                }}
            </script>
        </body>
        </html>
        """
        
        # Render the raw generated D3 platform output block inside the Streamlit view
        components.html(d3_html_template, height=320, scrolling=False)
