import sys

class Graph:
    def __init__(self):
        self.n = 0
        self.adj_list = []

    def set_number_vertices(self, n):
        """Sets the number of vertices of the graph to n."""
        self.n = n
        # Initialize adjacency list with n empty sublists
        self.adj_list = [[] for _ in range(n)]

    def add_edge(self, u, v):
        """Adds edge {u, v}."""
        # Check if vertices are within bounds
        if u < 0 or u >= self.n or v < 0 or v >= self.n:
            print(f"Error: Vertices {u} and {v} must be between 0 and {self.n - 1}")
            return
        
        # Add u to v's list and v to u's list (undirected graph)
        if u not in self.adj_list[v]:
            self.adj_list[v].append(u)
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
            
        # Optional: Sort lists for consistent printing
        self.adj_list[v].sort()
        self.adj_list[u].sort()

    def read_from_file(self, filename):
        """Reads the graph from a file."""
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
                
                # First line is the number of vertices
                if not lines:
                    return
                self.set_number_vertices(int(lines[0].strip()))
                
                # Subsequent lines are edges
                for line in lines[1:]:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        u = int(parts[0])
                        v = int(parts[1])
                        self.add_edge(u, v)
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
        except ValueError:
            print("Error: Invalid file format.")

    def print(self):
        """Prints the graph."""
        print(f"Graph with {self.n} vertices.")
        print("Adjacency List:")
        for i in range(self.n):
            print(f"Vertex {i}: {self.adj_list[i]}")

# 测试代码 (作业里没要求，但为了确保你的环境没问题，我们先跑一下)
if __name__ == "__main__":
    # 创建一个测试图
    g = Graph()
    g.set_number_vertices(4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.print()
    print("\n[System Check]: If you see the graph structure above, Phase 1 is complete.")