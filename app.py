import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import heapq
import time

st.set_page_config(page_title="FreshBasket UAE Dashboard", layout="wide")

st.title("🛒 FreshBasket UAE Operations Dashboard")
st.markdown("Optimization of Grocery Quick-Commerce Operations Across Dubai Using Data Structures & Algorithms")

# Sidebar Navigation
pages = ["Problem 1: Network & Exploration", 
         "Problem 2: Shortest Delivery Routes", 
         "Problem 3: Order Management Pipeline", 
         "Problem 4: Sorting, Searching & MST",
         "Case Study: The Ramadan Surge",
         "Critical Thinking"]

selection = st.sidebar.radio("Navigate", pages)

# Data Initialization
nodes = ['S1', 'S2', 'S3', 'S4', 'S5', 'Z1', 'Z2', 'Z3', 'Z4', 'Z5']
edges = [
    ('S1', 'Z1', 4, 8, 2.5),
    ('S1', 'Z2', 3, 6, 2.0),
    ('S1', 'S2', 5, 10, 3.5),
    ('S2', 'Z2', 2, 4, 1.5),
    ('S2', 'Z1', 6, 12, 4.0),
    ('S2', 'S3', 7, 14, 5.0),
    ('S3', 'Z3', 3, 7, 2.0),
    ('S3', 'S4', 8, 16, 5.5),
    ('S3', 'Z4', 6, 12, 4.0),
    ('S4', 'Z4', 3, 6, 2.0),
    ('S4', 'S5', 10, 20, 7.0),
    ('S5', 'Z5', 4, 8, 2.5),
    ('Z1', 'Z3', 6, 13, 4.0),
    ('Z2', 'Z3', 5, 11, 3.5),
    ('Z3', 'Z4', 7, 15, 5.0),
    ('Z4', 'Z5', 9, 18, 6.0),
    ('S1', 'S3', 9, 18, 6.5)
]

def create_graph(subset_edges=None):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    if subset_edges:
        for u, v, d, t, c in subset_edges:
            G.add_edge(u, v, weight=d, cost=c)
    else:
        for u, v, d, t, c in edges:
            G.add_edge(u, v, weight=d, cost=c)
    return G

G = create_graph()

def plot_graph(graph, title="FreshBasket Network", highlight_edges=None):
    fig, ax = plt.subplots(figsize=(10, 6))
    pos = nx.spring_layout(graph, seed=42)
    
    node_colors = ['lightblue' if n.startswith('S') else 'lightgreen' for n in graph.nodes()]
    nx.draw(graph, pos, with_labels=True, node_color=node_colors, 
            node_size=800, font_weight='bold', ax=ax)
    
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)
    
    if highlight_edges:
        nx.draw_networkx_edges(graph, pos, edgelist=highlight_edges, width=3, edge_color='red', ax=ax)
        
    ax.set_title(title)
    return fig

if selection == "Problem 1: Network & Exploration":
    st.header("Problem 1: Network & Exploration")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Network Graph")
        st.pyplot(plot_graph(G))
        st.caption("Blue: Dark Stores, Green: Delivery Zones. Edge labels: Distance (km)")
        
    with col2:
        st.subheader("Adjacency List")
        adj_data = [{"Node": n, "Neighbors": ", ".join([f"{nbr} ({G[n][nbr]['weight']} km)" for nbr in G.neighbors(n)])} for n in G.nodes()]
        st.dataframe(pd.DataFrame(adj_data))
        
    st.divider()
    
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("BFS Traversal (starting from S3)")
        st.text("Order: S3 → S1 → S2 → S4 → Z3 → Z4 → Z1 → Z2 → S5 → Z5")
        st.markdown("**Explanation**: S3's neighbours in sorted order are S1, S2, S4, Z3, Z4. S1 is dequeued and adds Z1, Z2, etc. (FIFO Queue)")
        
    with col4:
        st.subheader("DFS Traversal (starting from S3)")
        st.text("Order: S3 → S1 → S2 → Z1 → Z3 → Z2 → Z4 → S4 → S5 → Z5")
        st.markdown("**Explanation**: Follows first unvisited sorted neighbor down to depth. (LIFO Stack)")
        
    st.subheader("Business Application: Urgent Order at Z5")
    st.success("Recommendation: Dispatch from **S5 (Silicon Oasis Dark Store)**. It is only 1 hop away from Z5 with 4 km distance (8 mins). Minimum hops and shortest path.")

elif selection == "Problem 2: Shortest Delivery Routes":
    st.header("Problem 2: Shortest Delivery Routes")
    
    st.subheader("Part A: Dijkstra's Algorithm (S2 to Z4)")
    st.markdown("**Shortest Path:** S2 → S3 → Z4")
    st.markdown("**Total Distance:** 13 km | **Total Cost:** 9.00 AED")
    
    # Highlight path
    path_edges = [('S2', 'S3'), ('S3', 'Z4')]
    col1, col2 = st.columns([2, 1])
    with col1:
        st.pyplot(plot_graph(G, "Shortest Path S2 to Z4", highlight_edges=path_edges))
        
    st.divider()
    
    st.subheader("Part B: Floyd-Warshall (Dark Stores All-Pairs Shortest Path)")
    # Matrix creation
    ds_nodes = ['S1', 'S2', 'S3', 'S4', 'S5']
    ds_dist = [[0, 5, 9, 17, 27],
               [5, 0, 7, 15, 25],
               [9, 7, 0,  8, 18],
               [17,15, 8,  0, 10],
               [27,25, 18, 10, 0]]
    df_fw = pd.DataFrame(ds_dist, index=ds_nodes, columns=ds_nodes)
    st.dataframe(df_fw.style.background_gradient(cmap='YlOrRd'))
    
    col3, col4 = st.columns(2)
    with col3:
        st.info("**Farthest pair**: S1 and S5 (27 km)")
        st.info("**Best-connected (lowest avg distance)**: S3 (10.5 km avg)")
    with col4:
        st.success("**New Road Recommendation**: S1 to S4 direct link. It would reduce the worst-case distance (S1 to S5) by 6 km and improve corridor resilience.")

elif selection == "Problem 3: Order Management Pipeline":
    st.header("Problem 3: Order Management Pipeline")
    
    st.subheader("Part A: BST for Order Lookup")
    st.markdown("Orders: 5042, 5018, 5067, 5009, 5031, 5055, 5081, 5025")
    st.code('''
                    5042  (root)  
                   /    \\  
                5018    5067   (Before deleting 5067)
               /    \\    /    \\  
            5009  5031 5055  5081  
                  /  
                5025  
    ''')
    st.markdown("**Traversals**:")
    st.markdown("- **In-order**: 5009, 5018, 5025, 5031, 5042, 5055, 5067, 5081")
    st.markdown("- **Pre-order**: 5042, 5018, 5009, 5031, 5025, 5067, 5055, 5081")
    st.markdown("- **Post-order**: 5009, 5025, 5031, 5018, 5055, 5081, 5067, 5042")
    st.markdown("**Search 5055**: 3 comparisons (5042 -> 5067 -> 5055)")
    st.markdown("**Delete 5067**: Two children case. Replace with In-order successor (5081).")
    
    st.divider()
    
    st.subheader("Part B: Delivery Route as Doubly Linked List")
    st.markdown("**Original**: NULL ⇄ [Z1] ⇄ [Z3] ⇄ [Z2] ⇄ [Z4] ⇄ [Z5] ⇄ NULL")
    st.markdown("**Insert Z3 VIP (Remove Dupe)**: NULL ⇄ [Z3] ⇄ [Z1] ⇄ [Z2] ⇄ [Z4] ⇄ [Z5] ⇄ NULL")
    st.markdown("**Remove Z4 (Cancelled)**: NULL ⇄ [Z3] ⇄ [Z1] ⇄ [Z2] ⇄ [Z5] ⇄ NULL")
    st.markdown("**Why Doubly Linked List?**: Allows O(1) insertions/deletions at any node compared to O(n) for arrays. Also supports backward traversal.")
    
    st.divider()
    
    st.subheader("Part C: Priority Queue & Stack")
    st.markdown("**Min-Heap Orders**: A(3), B(1), C(4), D(1), E(2), F(5)")
    st.markdown("**Dequeue Order**: B, D, E, A, C, F")
    st.warning("**FIFO Guarantee?** Standard Min-heap does NOT guarantee FIFO for equal priorities. Needs secondary key (timestamp) to enforce FIFO.")
    
    st.markdown("**Stack Undo**: `[Received | Confirmed | Preparing | Dispatched]`")
    st.markdown("After pop (undo): `[Received | Confirmed | Preparing]` -> Status is **Preparing**")

elif selection == "Problem 4: Sorting, Searching & MST":
    st.header("Problem 4: Sorting, Searching & Infrastructure")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Part A: Merge Sort")
        st.markdown("**Unsorted**: [12, 3, 7, 9, 2, 15, 6, 4]")
        st.markdown("**Sorted**: [2, 3, 4, 6, 7, 9, 12, 15]")
        st.markdown("**Total comparisons in merge phase**: 17")
        st.markdown("**Time Complexity**: $O(N \\log N)$")
    
    with col2:
        st.subheader("Part B: Binary Search (Target 9)")
        st.markdown("**Binary Search**: 2 comparisons (Mid index 3 (6) -> Right -> Mid index 5 (9))")
        st.markdown("**Linear Search**: 6 comparisons (Index 0 to 5)")
        st.markdown("**Scale Analysis (500 lookups, 1000 orders)**:")
        st.markdown("- Binary Search: ~5,000 comparisons")
        st.markdown("- Linear Search: ~250,000 avg comparisons (50x improvement)")
        
    st.divider()
    
    st.subheader("Part C: Kruskal's MST (Cost)")
    st.markdown("**Total MST Cost:** 26.00 AED")
    mst_edges = [('S2','Z2'), ('S1','Z2'), ('S3','Z3'), ('S4','Z4'), ('S1','Z1'), ('S5','Z5'), ('Z2','Z3'), ('S3','Z4'), ('Z4','Z5')]
    st.pyplot(plot_graph(G, "Minimum Spanning Tree", highlight_edges=mst_edges))
    
    st.subheader("Part D: Divide and Conquer for Peak Delivery Hour")
    st.markdown("**Approach**: Split 24h half, base case 1. Compare left peak vs right peak up the tree.")
    st.error("**Honest Assessment**: Divide and Conquer $O(N)$ is NOT better than simple linear scan $O(N)$ here. Linear scan has less overhead, $O(1)$ space, and better cache locality.")

elif selection == "Case Study: The Ramadan Surge":
    st.header("Layer 2 Case Study: The Ramadan Surge")
    st.markdown("Volume tripling from 800 to 2,400 orders/day. AED 50k budget, 5 days to build.")
    
    st.subheader("CS-1: Priorities & Justification")
    ptable = pd.DataFrame([
        {"Priority": "1st", "Problem": "Problem Y: Order Pile-up", "Cost (AED)": 15000, "Time": "2 days", "Monthly Impact": "AED 80k/mo (VIP retention)"},
        {"Priority": "2nd", "Problem": "Problem X: Route Chaos", "Cost (AED)": 25000, "Time": "4 days", "Monthly Impact": "AED 35k/mo (Fuel savings)"},
        {"Priority": "Dropped", "Problem": "Problem Z: Dark Store Connectivity", "Cost (AED)": 30000, "Time": "5 days", "Monthly Impact": "AED 20k/mo (Stock-out red.)"}
    ])
    st.table(ptable)
    st.markdown("**Justification**: Problem Y has the highest ROI and shortest build time (preventing VIP churn). Problem X reduces 30% fuel costs. Problem Z takes too long (5 days) compared to the limited bandwidth and can be handled via WhatsApp temporarily.")
    
    st.subheader("CS-2: Algorithm Selection (Priority 1)")
    st.success("**Algorithm: Min-Heap Priority Queue (timestamp composite key)**. O(log N) insert/extract. Beats Zone-based FIFO (ignores VIPs) and BST (more overhead/memory).")
    
    st.subheader("CS-3: Trade-Off Analysis & Fallback")
    st.markdown("- **Largest Risk**: Route system fails during execution. \n- **Fallback**: Pre-compute top 3 fixed routes offline and give printouts to riders, while switching back to dual-FIFO for orders.")

elif selection == "Critical Thinking":
    st.header("Layer 3: Critical Thinking")
    
    st.subheader("CT-1: The Google Maps API Challenge")
    st.markdown("""
    **Justification for In-House Dijkstra/Floyd-Warshall:**
    1. **Cost at Scale**: Tens of thousands of API calls during Ramadan peak will rack up huge ongoing expenses vs free pre-computation.
    2. **Customization**: API lacks custom multi-stop zone-based queue ordering.
    3. **Privacy**: Protect delivery density/pattern data from Google and competitors.
    **Recommendation**: Hybrid approach. In-house Floyd-Warshall for planned dispatch, Google Maps API ONLY for real-time traffic jam rerouting.
    """)
    
    st.subheader("CT-2: Data Structures Team Decision")
    st.warning("**NO to AVL Tree.** Complex code, rotations will slow down juniors, massive bug risk during Ramadan volume.")
    st.success("**Use Python Dict + SortedList (Skip-list).** O(1) direct access and O(log N) sorted queries. Very ship-able and maintainable for existing team.")
    
    st.subheader("CT-3: When the Algorithm is Right but Business is Wrong")
    st.markdown("""
    **S5 (Silicon Oasis) Closure Override:**
    - Algorithm ignores that Z5 is a 40% MoM growing expat segment.
    - Closing S5 turns 8-min delivery into 38-min delivery (breaching 30-min promise).
    - Noon Minutes is opening a dark store there soon.
    **Conclusion**: Retain S5 to defend turf. Algorithm optimized for cost, but missed growth trajectories, competitive dynamics, and brand promise constraints.
    """)
