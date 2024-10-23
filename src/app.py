import tkinter as tk
from tkinter import messagebox
import sys
from io import StringIO
# some_file.py
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
from ManaOptimizer.ManaSimulation import ManaSimulation  # Assuming ManaSimulation is in the same directory or PYTHONPATH

class RedirectedOutput:
    """ Class to redirect stdout and stderr to the Tkinter Text widget in real-time """
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = StringIO()
        self.update_interval = 100  # Update interval in milliseconds

        # Schedule periodic updates
        self.text_widget.after(self.update_interval, self.update_terminal)

    def write(self, string):
        self.buffer.write(string)

    def flush(self):
        pass  # No-op, but needed for file-like objects

    def update_terminal(self):
        """ Method to update the Text widget from the buffer """
        content = self.buffer.getvalue()
        if content:
            self.text_widget.insert(tk.END, content)
            self.text_widget.see(tk.END)  # Auto-scroll to the end
            self.buffer.truncate(0)
            self.buffer.seek(0)

        # Schedule the next update
        self.text_widget.after(self.update_interval, self.update_terminal)

class DeckOptimizerApp:
    MAX_ELEMENTS = 12  # Maximum number of allowed elements

    def __init__(self, root):
        self.root = root
        self.root.title("Stormbound Deck Optimizer")
        
        # Input Label
        self.input_label = tk.Label(root, text="Enter a List of Cards (comma-separated):")
        self.input_label.pack(pady=10)
        
        # Input Textbox
        self.input_entry = tk.Entry(root, width=50)
        self.input_entry.pack(pady=5)
        self.input_entry.bind("<KeyRelease>", self.update_count)  # Bind key release event to update the counter

        # Element Count Label
        self.count_label = tk.Label(root, text=f"Number of elements: 0 (Max: {self.MAX_ELEMENTS})")
        self.count_label.pack(pady=5)

        # Run Button
        self.run_button = tk.Button(root, text="Run Simulation", command=self.run_simulation)
        self.run_button.pack(pady=15)
        
        # Result Label
        self.result_label = tk.Label(root, text="Simulation Result:")
        self.result_label.pack(pady=10)
        
        # Result Text
        self.result_text = tk.Text(root, height=10, width=60, wrap=tk.WORD)
        self.result_text.pack(pady=5)

        # Terminal Output Label
        self.terminal_label = tk.Label(root, text="Terminal Output:")
        self.terminal_label.pack(pady=10)

        # Terminal Text (to show terminal outputs)
        self.terminal_text = tk.Text(root, height=10, width=60, wrap=tk.WORD, bg="black", fg="white")
        self.terminal_text.pack(pady=5)

        # Redirect stdout and stderr to terminal_text widget
        sys.stdout = RedirectedOutput(self.terminal_text)
        sys.stderr = RedirectedOutput(self.terminal_text)

    def update_count(self, event):
        # Split input into a list of trimmed elements
        elements = [item.strip() for item in self.input_entry.get().split(",") if item.strip()]
        
        # Enforce maximum number of elements
        if len(elements) > self.MAX_ELEMENTS:
            # Revert entry to the first 12 elements and display warning
            elements = elements[:self.MAX_ELEMENTS]
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, ", ".join(elements))
            messagebox.showwarning("Limit Reached", f"Maximum of {self.MAX_ELEMENTS} elements allowed.")
        
        # Update count label
        self.count_label.config(text=f"Number of elements: {len(elements)} (Max: {self.MAX_ELEMENTS})")

    def run_simulation(self):
        try:
            # Fetch input and convert to list
            card_list = self.input_entry.get().split(",")
            
            # Attempt to convert each item to a numeric type (int, float, etc.)
            card_list = [int(card.strip()) for card in card_list if card.strip().isdigit()]

            if not card_list:
                messagebox.showerror("Error", "Please enter valid numeric card values.")
                return

            # Create an instance of ManaSimulation
            simulation = ManaSimulation(card_list, 12, debug=True)
            
            # Run the simulation (assuming the class has a method called `calculate_avg_wasted_mana` returning results)
            result = simulation.calculate_avg_wasted_mana()
            
            # Display the result
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, str(result))
            
            # Print to terminal (for demonstration purposes)
            print("Simulation completed successfully!")
        except ValueError:
            print("Error: All card inputs must be valid numbers.")
            messagebox.showerror("Error", "All card inputs must be valid numbers.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Main Function
if __name__ == "__main__":
    root = tk.Tk()
    app = DeckOptimizerApp(root)
    root.mainloop()
