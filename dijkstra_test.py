import tkinter as tk
from tkinter import ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import csv

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

        # Import Button
        self.import_frame = ttk.Frame(master)
        self.import_frame.pack(pady=10)

        self.import_graph_button = ttk.Button(self.import_frame, text="Import Graph", command=self.import_graph)
        self.import_graph_button.grid(row=0, column=0, padx=5)

        # Result Frame
        self.result_frame = ttk.Frame(master)
        self.result_frame.pack(pady=10)

        self.result_label = ttk.Label(self.result_frame, text="Shortest Path Result:")
        self.result_label.pack()

        self.path_length_label = ttk.Label(self.result_frame, text="")
        self.path_length_label.pack()

        self.final_path_label = ttk.Label(self.result_frame, text="")
        self.final_path_label.pack()

        # Store alternate paths
        self.alternate_paths = []

        # Hyperlink for shortest path
        self.shortest_path_link = None

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

    def import_graph(self):
        """Import graph data from a CSV file."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    if row[0] == "Node":
                        self.add_node_from_import(row[1])
                    elif row[0] == "Edge":
                        self.add_edge_from_import(row[1], row[2], row[3])

            # Update visualization
            self.pos = nx.spring_layout(self.graph, k=1.2, iterations=50)
            self.visualize_graph()

    def add_node_from_import(self, node):
        """Add a node to the graph from imported data."""
        if node:
            self.graph.add_node(node)

    def add_edge_from_import(self, node1, node2, weight):
        """Add an edge to the graph from imported data."""
        if node1 in self.graph and node2 in self.graph:
            try:
                weight = float(weight)
                self.graph.add_edge(node1, node2, weight=weight)
            except ValueError:
                print("Invalid weight entered")

    def visualize_graph(self, path_nodes=None, path_edges=None):
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
            if path_edges is not None:
                for edge in path_edges:
                    edge_colors[list(self.graph.edges()).index(edge)] = 'orange'

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

            # Create a hyperlink for the shortest path
            if self.shortest_path_link is not None:
                self.shortest_path_link.destroy()  # Remove the previous link if it exists

            self.shortest_path_link = ttk.Label(self.result_frame, text=f"Final Path: {' -> '.join(path)}",
                                                 foreground="blue", cursor="hand2", font=("Helvetica", 10, "underline"))
            self.shortest_path_link.pack()
            self.shortest_path_link.bind("<Button-1>", lambda e: self.highlight_shortest_path(path))

            # Find alternate paths and store them
            self.alternate_paths = []
            all_paths = list(nx.all_simple_paths(self.graph, source, target))
            for p in all_paths:
                if p != path:  # Ensure the path is not the shortest path
                    length = sum(self.graph[u][v]['weight'] for u, v in zip(p[:-1], p[1:]))
                    self.alternate_paths.append((p, length))

            # Sort alternate paths by length and keep only the top 3
            self.alternate_paths.sort(key=lambda x: x[1])  # Sort by length
            self.alternate_paths = self.alternate_paths[:3]  # Keep only the top 3

            self.display_alternate_paths()  # Show alternate paths

            # Highlight the shortest path in the graph
            self.highlight_shortest_path(path)

        except nx.NetworkXNoPath:
            self.path_length_label.config(text="No path exists between the selected nodes.")
            self.final_path_label.config(text="")
            self.alternate_paths.clear()

    def display_alternate_paths(self):
        """Display the alternate paths with clickable links."""
        for widget in self.result_frame.winfo_children():
            if widget not in [self.result_label, self.path_length_label, self.final_path_label, self.shortest_path_link]:
                widget.destroy()  # Clear previous alternate path links

        if not self.alternate_paths:
            return  # No alternate paths to display

        alternate_label = ttk.Label(self.result_frame, text="Alternate Paths:")
        alternate_label.pack()

        for alt_path, length in self.alternate_paths:
            path_text = f"Alternate Path: {' -> '.join(alt_path)} (Length: {length})"
            alt_path_link = ttk.Label(self.result_frame, text=path_text, foreground="blue", cursor="hand2", font=("Helvetica", 10, "underline"))
            alt_path_link.pack()
            alt_path_link.bind("<Button-1>", lambda e, path=alt_path: self.highlight_alternate_path(path))

    def highlight_shortest_path(self, path):
        """Highlight the shortest path on the graph."""
        path_edges = list(zip(path[:-1], path[1:]))
        self.visualize_graph(path_nodes=path, path_edges=path_edges)

    def highlight_alternate_path(self, path):
        """Highlight an alternate path on the graph."""
        path_edges = list(zip(path[:-1], path[1:]))
        self.visualize_graph(path_nodes=path, path_edges=path_edges)

    def on_closing(self):
        """Handle the window closing event."""
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphLearningPlatform(root)
    root.mainloop()
