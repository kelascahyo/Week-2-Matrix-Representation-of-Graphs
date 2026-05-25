# app.py
import streamlit as st
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# Set up page configuration
st.set_page_config(
    page_title="Matrix Representation of Graphs",
    page_icon="🕸️",
    layout="wide"
)

st.title("🎓 Week 2: Matrix Representation of Graphs Crash Course")
st.write("Understand how graphs become machine-readable through code and interactive visuals.")

# --- SIDEBAR NAV ---
st.sidebar.header("Navigation")
section = st.sidebar.radio("Go to:", ["Theory & Intuition", "Interactive Conversion Tool"])

# --- SECTION 1: THEORY ---
if section == "Theory & Intuition":
    st.header("🏗️ Learn Intuition")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Why Graphs Defy Normal Neural Networks")
        st.write("""
        Traditional neural networks (like CNNs or RNNs) expect data to be structured in neat, predictable grids or sequences (like pixels or text tokens). 
        
        Graphs break these rules entirely:
        * **No fixed structure:** A node can have one neighbor, fifty neighbors, or zero.
        * **Permutation invariance:** If you shuffle the order of rows/columns in your network data, it represents the exact same graph. Standard neural networks get confused by this lack of inherent order.
        """)
        
    with col2:
        st.subheader("The Math Focus")
        st.write("""
        * **Matrix Multiplication Intuition:** Multiplying a graph's structure matrix by a feature matrix allows nodes to effortlessly aggregate data from their immediate neighbors.
        * **Eigenvectors:** Think of them as the 'vibe check' of a graph. They highlight the underlying backbone structural layout, showing which clusters naturally bind together.
        * **Message Propagation:** This is the act of a node collecting information packets from neighbors, combining them with its own, and updating its state.
        """)

    st.write("---")
    st.header("🧩 Core Concepts Breakdown")
    
    # Core Data Table
    concepts_data = {
        "Concept": ["Adjacency Matrix", "Edge List", "Sparse Matrices", "Feature Matrices", "Laplacian Matrix"],
        "What It Is": [
            "A square matrix where index (i, j) indicates if an edge exists between node i and node j.",
            "A simple list of pairs [source, target] representing connections.",
            "A memory-efficient way to store matrices that consist mostly of zeros.",
            "A matrix of shape (num_nodes, num_features) holding the unique attributes of each node.",
            "Calculated as L = D - A (Degree matrix minus Adjacency matrix), used for structural diffusion."
        ],
        "Best Used For": [
            "Dense graphs; lightning-fast structural lookups.",
            "Storing raw graph datasets efficiently.",
            "Large, real-world graphs where connections are rare.",
            "Giving real-world context to structural layouts.",
            "Graph physics, clustering, and spectral graph theory."
        ]
    }
    st.table(concepts_data)

# --- SECTION 2: INTERACTIVE TOOL ---
elif section == "Interactive Conversion Tool":
    st.header("💻 Practical Graph Matrix Converter")
    st.write("Toggle between graph directions to see how data representation changes seamlessly in real-time.")

    tab1, tab2 = st.tabs(["Graph ➔ Adjacency Matrix", "Adjacency Matrix ➔ Graph"])

    # TAB 1: Graph to Matrix
    with tab1:
        st.subheader("Construct a Graph Visual to Generate Matrices")
        
        # User input for edges
        num_nodes = st.slider("Select number of nodes", min_value=3, max_value=6, value=4, key="g_nodes")
        
        st.write("Select which edges to connect:")
        edges = []
        # Generate possible edge check-boxes dynamically
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if st.checkbox(f"Connect Node {i} to Node {j}", value=(i==0 or j==i+1)):
                    edges.append((i, j))
        
        # Build networkx graph
        G = nx.Graph()
        G.add_nodes_from(range(num_nodes))
        G.add_edges_from(edges)
        
        # Plot
        fig, ax = plt.subplots(figsize=(4, 3))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='#4A90E2', node_size=500, font_color='white', font_weight='bold', ax=ax)
        
        col_img, col_mat = st.columns(2)
        with col_img:
            st.pyplot(fig)
        with col_mat:
            st.markdown("**Generated Adjacency Matrix:**")
            adj_matrix = nx.to_numpy_array(G, dtype=int)
            st.code(str(adj_matrix))
            
            st.markdown("**Generated Edge List:**")
            st.code(str(edges))

    # TAB 2: Matrix to Graph
    with tab2:
        st.subheader("Input an Adjacency Matrix to Generate a Graph")
        st.write("Edit the binary connectivity matrix below (4x4 matrix representation):")
        
        # Interactive Matrix creation via columns
        matrix_input = np.zeros((4, 4), dtype=int)
        
        for r in range(4):
            cols = st.columns(4)
            for c in range(4):
                with cols[c]:
                    # Default values to make a nice initial graph shape
                    default_val = 1 if ((r==0 and c==1) or (r==1 and c==0) or (r==1 and c==2) or (r==2 and c==1) or (r==2 and c==3) or (r==3 and c==2)) else 0
                    matrix_input[r, r] = 0 # Forces no self loops for simplicity
                    if r != c:
                        matrix_input[r, c] = cols[c].number_input(f"Row {r}, Col {c}", min_value=0, max_value=1, value=default_val, key=f"m_{r}_{c}")
        
        st.write("---")
        # Build graph from the custom user matrix input
        G_custom = nx.from_numpy_array(matrix_input)
        
        col_mat_out, col_graph_out = st.columns(2)
        with col_mat_out:
            st.markdown("**Your Custom Matrix Input:**")
            st.code(str(matrix_input))
            st.markdown(f"**Identified Edges:** {list(G_custom.edges)}")
            
        with col_graph_out:
            st.markdown("**Reconstructed Visual Graph Output:**")
            fig2, ax2 = plt.subplots(figsize=(4, 3))
            pos2 = nx.circular_layout(G_custom)
            nx.draw(G_custom, pos2, with_labels=True, node_color='#E24A84', node_size=500, font_color='white', font_weight='bold', ax=ax2)
            st.pyplot(fig2)
