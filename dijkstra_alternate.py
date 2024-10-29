import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

class GraphLearningPlatform:
    def __init__(self, master):
        self.master = master
        self.master.title("Dijkstra Algorithm Visualizer")
        self.master.geometry("1000x700")  # Increased size for better visualization

        # Graph structure
        self.graph = nx.Graph()
        self.pos = {}  # To store the node positions

        # Title Label
        self.title_label = ttk.Label(master, text="Dijkstra Algorithm Visualizer", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        # Input frame
        self.input_frame = ttk.Frame(master)
        self.input_frame.pack(pady=10)

        self.node_label = ttk.Label(self.input_frame, text="Node:")
        self.node_label.grid(row=0, column=0)

        self.node_entry = ttk.Entry(self.input_frame, width=15)
        self.node_entry.grid(row=0, column=1)

        self.add_node_button = ttk.Button(self.input_frame, text="Add Node", command=self.add_node)
        self.add_node_button.grid(row=0, column=2, padx=5)

        self.edge_label = ttk.Label(self.input_frame, text="Edge (node1,node2,weight):")
        self.edge_label.grid(row=1, column=0)

        self.edge_entry = ttk.Entry(self.input_frame, width=20)
        self.edge_entry.grid(row=1, column=1)

        self.add_edge_button = ttk.Button(self.input_frame, text="Add Edge", command=self.add_edge)
        self.add_edge_button.grid(row=1, column=2, padx=5)

        # Control Buttons for Algorithm
        self.control_frame = ttk.Frame(master)
        self.control_frame.pack(pady=10)

        self.source_label = ttk.Label(self.control_frame, text="Source Node:")
        self.source_label.grid(row=0, column=0)

        self.source_entry = ttk.Entry(self.control_frame, width=10)
        self.source_entry.grid(row=0, column=1)

        self.target_label = ttk.Label(self.control_frame, text="Target Node:")
        self.target_label.grid(row=0, column=2)

        self.target_entry = ttk.Entry(self.control_frame, width=10)
        self.target_entry.grid(row=0, column=3)

        self.run_algorithm_button = ttk.Button(self.control_frame, text="Run Dijkstra's Algorithm", command=self.run_algorithm)
        self.run_algorithm_button.grid(row=0, column=4, padx=5)

        # Result Frame
        self.result_frame = ttk.Frame(master)
        self.result_frame.pack(pady=10)

        self.result_label = ttk.Label(self.result_frame, text="Shortest Path Result:")
        self.result_label.pack()

        self.path_length_label = ttk.Label(self.result_frame, text="")
        self.path_length_label.pack()

        self.final_path_label = ttk.Label(self.result_frame, text="")
        self.final_path_label.pack()

        # Hyperlink for shortest path
        self.shortest_path_link = None

        # Alternate path section
        self.alternate_path_links = []  # To store alternate path labels (hyperlinks)

        # Matplotlib Figure
        self.figure, self.ax = plt.subplots(figsize=(9, 7))  # Larger figure size for better visualization
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack(pady=10)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_node(self):
        """Add a node to the graph."""
        node = self.node_entry.get()
        if node:
            self.graph.add_node(node)
            self.node_entry.delete(0, tk.END)
            # Update node positions only when adding nodes
            self.pos = nx.spring_layout(self.graph, k=1.2, iterations=50)
            self.visualize_graph()

    def add_edge(self):
        """Add an edge to the graph with a weight."""
        edge_input = self.edge_entry.get().split(',')
        if len(edge_input) == 3:
            node1, node2, weight = edge_input
            try:
                weight = float(weight)
                if node1 in self.graph and node2 in self.graph:
                    self.graph.add_edge(node1, node2, weight=weight)
                    self.edge_entry.delete(0, tk.END)
                    self.visualize_graph()  # Update the graph visualization with same node positions
            except ValueError:
                print("Invalid weight entered")

    def visualize_graph(self, path_nodes=None, path_edges=None, alternate_path_nodes=None, alternate_path_edges=None):
        """Visualize the current graph."""
        self.ax.clear()  # Clear previous plot
        if self.graph.number_of_nodes() == 0:
            self.ax.set_title("Graph Visualization")
            self.canvas.draw()
            return

        # Set default node and edge colors
        node_colors = ['lightblue' for node in self.graph.nodes()]
        edge_colors = ['black' for edge in self.graph.edges()]

        # Highlight the shortest path nodes and edges if provided
        if path_nodes is not None:
            for node in path_nodes:
                node_colors[list(self.graph.nodes()).index(node)] = 'orange'
            for edge in path_edges:
                edge_colors[list(self.graph.edges()).index(edge)] = 'orange'

        # Highlight the alternate path nodes and edges if provided
        if alternate_path_nodes is not None:
            for node in alternate_path_nodes:
                node_colors[list(self.graph.nodes()).index(node)] = 'blue'
        if alternate_path_edges is not None:
            for edge in alternate_path_edges:
                edge_colors[list(self.graph.edges()).index(edge)] = 'blue'

        # Draw the graph with the updated node and edge colors
        nx.draw(self.graph, self.pos, with_labels=True, node_color=node_colors, edge_color=edge_colors,
                node_size=700, font_size=12, font_color='black', font_weight='bold')

        # Draw edge labels (weights)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, self.pos, edge_labels=edge_labels, font_color='red', font_size=10)

        self.ax.set_title("Graph Visualization")
        self.canvas.draw()  # Update the canvas

    def run_algorithm(self):
        """Run Dijkstra's algorithm and display the shortest path and alternate paths."""
        source = self.source_entry.get()
        target = self.target_entry.get()

        if source not in self.graph or target not in self.graph:
            self.path_length_label.config(text="Source or target node not found in graph.")
            return

        try:
            # Get the shortest path
            path_length, path = nx.single_source_dijkstra(self.graph, source, target=target)
            self.path_length_label.config(text=f"Shortest Path Length: {path_length}")
            self.final_path_label.config(text=f"Final Path: {' -> '.join(path)}")

            # Create a hyperlink for the shortest path
            if self.shortest_path_link is not None:
                self.shortest_path_link.destroy()  # Remove the previous link if it exists

            self.shortest_path_link = ttk.Label(self.result_frame, text=f"Shortest Path: {' -> '.join(path)}",
                                                 foreground="blue", cursor="hand2", font=("Helvetica", 10, "underline"))
            self.shortest_path_link.pack()
            self.shortest_path_link.bind("<Button-1>", lambda e: self.highlight_shortest_path(path))

            # Highlight the shortest path nodes and edges
            path_nodes = path
            path_edges = list(zip(path[:-1], path[1:]))

            # Visualize the graph with highlighted shortest path nodes and edges
            self.visualize_graph(path_nodes=path_nodes, path_edges=path_edges)

            # Find and display alternate routes by removing the shortest path edges
            self.find_alternate_paths(source, target, path_edges)

        except nx.NetworkXNoPath:
            self.path_length_label.config(text="No path exists between the source and target.")
            return

    def highlight_shortest_path(self, path):
        """Highlight the selected shortest path in the visualization."""
        path_edges = list(zip(path[:-1], path[1:]))
        path_nodes = path
        self.visualize_graph(path_nodes=path_nodes, path_edges=path_edges)

    def find_alternate_paths(self, source, target, path_edges):
        """Find alternate paths by removing the edges of the found shortest path."""
        alternate_paths = []
        G_temp = self.graph.copy()

        # Remove the edges of the shortest path one by one and find alternate paths
        for edge in path_edges:
            G_temp.remove_edge(*edge)
            try:
                path_length, path = nx.single_source_dijkstra(G_temp, source, target=target)
                alternate_paths.append((path_length, path))
            except nx.NetworkXNoPath:
                continue

        # Clear previous alternate path labels
        for link in self.alternate_path_links:
            link.destroy()
        self.alternate_path_links.clear()

        if alternate_paths:
            # Sort alternate paths by their length
            alternate_paths = sorted(alternate_paths, key=lambda x: x[0])

            # Display and visualize alternate paths as clickable hyperlinks
            for idx, (path_length, path) in enumerate(alternate_paths):
                alt_path_label = ttk.Label(self.result_frame, text=f"Alternate Path {idx + 1}: {' -> '.join(path)}",
                                           foreground="blue", cursor="hand2", font=("Helvetica", 10, "underline"))
                alt_path_label.pack()
                alt_path_label.bind("<Button-1>", lambda e, p=path: self.highlight_alternate_path(p))
                self.alternate_path_links.append(alt_path_label)

    def highlight_alternate_path(self, path):
        """Highlight the selected alternate path in the visualization."""
        path_edges = list(zip(path[:-1], path[1:]))
        path_nodes = path
        self.visualize_graph(path_nodes=path_nodes, path_edges=path_edges)

    def on_closing(self):
        """Handle window close event."""
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphLearningPlatform(root)
    root.mainloop()
