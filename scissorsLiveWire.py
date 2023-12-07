import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import graphConstructor
import dijkstra


class InteractiveScissorsApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill="both", expand=True)
        self.image_path = filedialog.askopenfilename()
        self.image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        self.anchor_points = []
        self.canvas.bind("<Button-1>", self.on_click)
        self.done_button = tk.Button(root, text="Done", command=self.on_done)
        self.done_button.pack()
        self.initialize_graph()

    def initialize_graph(self):
        # Convert image to grayscale and calculate the graph
        gray_image = self.image.convert('L')
        image_array = np.array(gray_image)
        Gx, Gy, G = graphConstructor.sobel_filters(image_array)
        self.graph = graphConstructor.construct_graph_with_gradients(
            image_array, G)

    def on_click(self, event):
        # Disable further clicks
        self.canvas.unbind("<Button-1>")
        self.canvas.config(cursor="watch")
        self.root.config(cursor="watch")

        # Get the x, y position of the click
        x, y = event.x, event.y
        # Add the point to the list of anchor points
        self.anchor_points.append((y, x))
        # If there are at least two points, draw the path between the last two points
        if len(self.anchor_points) > 1:
            self.draw_path_between_points(
                self.anchor_points[-2], self.anchor_points[-1])
        # Rebind the click event and reset the cursor after processing is done
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.config(cursor="cross")
        self.root.config(cursor="arrow")

    def on_done(self):
        # Close the lasso by connecting the last point to the first
        if len(self.anchor_points) > 2:
            self.draw_path_between_points(
                self.anchor_points[-1], self.anchor_points[0])
            self.canvas.unbind("<Button-1>")  # Disable adding new points
            self.save_image()

    def draw_path_between_points(self, start, end):
        # Calculate the path using the Intelligent Scissors algorithm on the precomputed graph
        path = run_intelligent_scissors(self.graph, start, end)
        draw = ImageDraw.Draw(self.image)
        # Draw the path directly on the image
        for i in range(len(path) - 1):
            draw.line((path[i][1], path[i][0], path[i+1][1],
                      path[i+1][0]), fill="red", width=1)

        # Update the canvas with the new image
        self.photo = ImageTk.PhotoImage(self.image)  # Update the photo object
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

    def save_image(self):
        # Save the final image with the drawn path
        output_image_path = self.image_path.replace(".", "_with_path.")
        self.image.save(output_image_path)
        messagebox.showinfo(
            "Image saved", f"Image saved as {output_image_path}")


def run_intelligent_scissors(graph, start, end):
    distances, predecessors = dijkstra.dijkstra_with_predecessors(graph, start)

    path = dijkstra.backtrack_path(predecessors, start, end)

    return path


# game loop
root = tk.Tk()
app = InteractiveScissorsApp(root)
root.mainloop()
