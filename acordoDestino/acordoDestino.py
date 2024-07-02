import random
import tkinter as tk
from tkinter import ttk
from collections import Counter, defaultdict

# Definindo clientes e servidores
clients = ['C1', 'C2', 'C3']
servers = ['S1', 'S2', 'S3', 'S4']  # Adicionando S4
messages = ['M1', 'M2', 'M3']

class Server:
    def __init__(self, name):
        self.name = name
        self.received_messages = {}
        self.votes = []

    def receive_messages(self, messages):
        random.shuffle(messages)
        self.received_messages[self.name] = messages.copy()

    def communicate(self, servers):
        for server in servers:
            if server != self:
                self.received_messages[server.name] = server.received_messages[self.name][:]  # Make a copy of received messages

    def vote(self):
        if self.received_messages:
            # Count messages by column index
            column_counts = [{}, {}, {}]
            column_messages = defaultdict(list)

            # Gather votes for each column
            for server_name, messages in self.received_messages.items():
                for col_index, message in enumerate(messages):
                    column_messages[col_index].append((server_name, message))

            # Determine most frequent messages in each column
            for col_index, votes in column_messages.items():
                col_counter = Counter(message for _, message in votes)
                most_common_messages = col_counter.most_common()

                # Keep the original order for ties
                ordered_messages = []
                for server_name, message in votes:
                    if (message, col_counter[message]) in most_common_messages:
                        ordered_messages.append(message)

                column_counts[col_index] = ordered_messages

            final_order = []
            for col_votes in column_counts:
                if col_votes:
                    most_common_message = col_votes[0]  # Take the most frequent message
                    # Check if all servers have the same message in this column
                    if all(msg == most_common_message for msg in col_votes):
                        final_order.append(most_common_message)
                    else:
                        final_order.append("")  # Placeholder for mixed column
                else:
                    final_order.append("")  # Placeholder for empty column

            return final_order

        return []

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Acordo no Destino")
        self.client = None
        self.servers = [Server(name) for name in servers]
        self.init_ui()

    def init_ui(self):
        self.moment = 0
        self.button = tk.Button(self.root, text="Avançar", command=self.advance)
        self.button.pack(pady=10)
        
        self.reset_button = tk.Button(self.root, text="Reiniciar", command=self.reset_simulation, state=tk.DISABLED)
        self.reset_button.pack(pady=10)
        
        self.table = ttk.Treeview(self.root, columns=("C1", "C2", "C3"), show='headings')
        self.table.heading("C1", text="Cliente/Servidor", anchor="center")
        self.table.heading("C2", text="Mensagens Recebidas", anchor="center")
        self.table.heading("C3", text="Votação", anchor="center")
        self.table.pack(pady=10)

    def advance(self):
        self.moment += 1
        if self.moment == 1:
            self.client = random.choice(clients)
            self.update_table_initial()
            self.update_communication()
        elif self.moment == 2:
            self.update_table_voting()
        elif self.moment == 3:
            self.show_final_order()
        elif self.moment == 4:
            self.reset_button.config(state=tk.NORMAL)
        else:
            self.button.config(state=tk.DISABLED)

    def update_table_initial(self):
        self.table.delete(*self.table.get_children())
        self.table.insert("", "end", values=(self.client, "", ""))
        for server in self.servers:
            server.receive_messages(messages)
            self.table.insert("", "end", values=(server.name, ", ".join(server.received_messages[server.name]), ""))

    def update_communication(self):
        for server in self.servers:
            other_servers = [s for s in self.servers if s != server]
            server.communicate(other_servers)

    def update_table_voting(self):
        for server in self.servers:
            order = server.vote()
            self.table.insert("", "end", values=(server.name, "", ", ".join(order)))

    def show_final_order(self):
        final_orders = []
        for server in self.servers:
            order = server.vote()
            final_orders.append(order)

        final_count = Counter(map(tuple, final_orders))
        final_order = list(final_count.most_common(1)[0][0])

        self.table.insert("", "end", values=("Ordem Final", "", ", ".join(final_order)))

    def reset_simulation(self):
        self.moment = 0
        self.client = None
        self.servers = [Server(name) for name in servers]
        self.table.delete(*self.table.get_children())
        self.reset_button.config(state=tk.DISABLED)
        self.button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
