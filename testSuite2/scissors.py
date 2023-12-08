import dijkstra
from graphConstructor4way import construct_graph_with_gradients, energy_filter
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFile
# Increase the limit to a larger value
import PIL
PIL.Image.MAX_IMAGE_PIXELS = 933120000
# from graphConstructor import construct_graph_with_gradients, energy_filter


class InteractiveScissorsApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, cursor="cross")
        # Open an image file
        self.image_path = filedialog.askopenfilename()
        if not self.image_path:
            raise Exception("No image selected")
        self.image = Image.open(self.image_path)
        width, height = self.image.size
        self.canvas.config(width=width, height=height+50)
        self.canvas.pack(fill="both", expand=True)
        # Set window size to match image size
        self.root.geometry(f"{width}x{height}")
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        self.anchor_points = []
        self.canvas.bind("<Button-1>", self.on_click)
        self.done_button = tk.Button(root, text="Done", command=self.on_done)
        self.done_button.pack()
        self.actions = []  # List to track actions (anchor points and lines)
        self.undo_button = tk.Button(
            root, text="Undo", command=self.undo_last_action)
        self.undo_button.pack()
        self.initialize_graph()

    def initialize_graph(self):
        # Convert image to grayscale and calculate the graph
        gray_image = self.image.convert('L')
        image_array = np.array(gray_image)
        Gx, Gy, G, Ex, Ey = energy_filter(image_array)
        self.graph = construct_graph_with_gradients(
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
            # i
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

    def undo_last_action(self):
        if self.actions:
            # Remove the last action
            self.actions.pop()

            # Redraw the image without the last line
            self.redraw_image()

    def redraw_image(self):
        # Clear the canvas
        self.canvas.delete("all")
        # Redraw the image
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        # Redraw all lines except the last one
        for start, end in self.actions:
            self.draw_path_between_points(start, end)


def run_intelligent_scissors(graph, start, end):
    distances, predecessors = dijkstra.dijkstra_with_predecessors(graph, start)

    path = dijkstra.backtrack_path(predecessors, start, end)

    return path


# game loop
root = tk.Tk()
app = InteractiveScissorsApp(root)
root.mainloop()
