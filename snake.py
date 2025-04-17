import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from collections import deque

snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

class SnakeLadderGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Ular Tangga Multi Pemain")
        self.root.geometry("1000x650")
        self.root.configure(bg="#2c3e50")

        # Player colors and symbols
        self.player_colors = ["#3498db", "#e67e22", "#2ecc71", "#9b59b6"]
        self.player_symbols = ["🔵", "🟠", "🟢", "🟣"]
        self.player_color_names = ["Biru", "Oranye", "Hijau", "Ungu"]

        # Canvas
        self.canvas = tk.Canvas(self.root, width=640, height=640, bg="#f9f9f9", bd=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        # Side Panel
        self.side_panel = tk.Frame(self.root, bg="#34495e", width=320, height=640, bd=0)
        self.side_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.side_panel.grid_propagate(False)
        
        # Judul Game
        self.title_frame = tk.Frame(self.side_panel, bg="#2980b9", height=60)
        self.title_frame.pack(fill="x", pady=(0, 20))
        self.title_label = tk.Label(self.title_frame, text="ULAR TANGGA", font=("Helvetica", 18, "bold"), bg="#2980b9", fg="white")
        self.title_label.pack(pady=15)
        
        # Turn indicator
        self.turn_frame = tk.Frame(self.side_panel, bg="#3498db", height=70, bd=1, relief=tk.RAISED)
        self.turn_frame.pack(fill="x", padx=20, pady=10)
        self.turn_label = tk.Label(self.turn_frame, text="Menunggu pemain...", font=("Helvetica", 16, "bold"), bg="#3498db", fg="white")
        self.turn_label.pack(pady=15)

        # Player status frame
        self.status_frame = tk.Frame(self.side_panel, bg="#34495e")
        self.status_frame.pack(fill="x", padx=20, pady=10)
        
        # Player status
        self.player_frames = []
        self.player_labels = []
        self.player_pos_labels = []
        
        # Dice display
        self.dice_frame = tk.Frame(self.side_panel, bg="#2c3e50", height=120, bd=2, relief=tk.GROOVE)
        self.dice_frame.pack(fill="x", padx=20, pady=20)
        self.dice_frame.pack_propagate(False)
        
        self.dice_title = tk.Label(self.dice_frame, text="DADU", font=("Helvetica", 14, "bold"), 
                                 bg="#2c3e50", fg="#ecf0f1")
        self.dice_title.pack(pady=(10, 0))
        
        self.dice_label = tk.Label(self.dice_frame, text="🎲", font=("Helvetica", 40), 
                                  bg="#2c3e50", fg="#ecf0f1")
        self.dice_label.pack()
        
        self.dice_value = tk.Label(self.dice_frame, text="-", font=("Helvetica", 20, "bold"), 
                                  bg="#2c3e50", fg="#f1c40f")
        self.dice_value.pack()

        # Start Game Button
        self.start_button = tk.Button(self.side_panel, text="MULAI PERMAINAN 🎮", font=("Helvetica", 14, "bold"), 
                                     bg="#8e44ad", fg="white", activebackground="#9b59b6", 
                                     activeforeground="white", bd=0, padx=20, pady=10,
                                     command=self.start_game)
        self.start_button.pack(pady=10)

        # Roll Dice Button
        self.roll_button = tk.Button(self.side_panel, text="LEMPAR DADU 🎲", font=("Helvetica", 14, "bold"), 
                                    bg="#27ae60", fg="white", activebackground="#2ecc71", 
                                    activeforeground="white", bd=0, padx=20, pady=10,
                                    command=self.roll_dice)
        
        # Reset button
        self.reset_button = tk.Button(self.side_panel, text="MAIN LAGI 🔄", font=("Helvetica", 14, "bold"), 
                                     bg="#e74c3c", fg="white", activebackground="#c0392b", 
                                     activeforeground="white", bd=0, padx=20, pady=10,
                                     command=self.reset_game)
        
        # Game info section
        self.info_frame = tk.Frame(self.side_panel, bg="#34495e", bd=1, relief=tk.SUNKEN)
        self.info_frame.pack(fill="x", padx=20, pady=(30, 10))
        
        self.info_label = tk.Label(self.info_frame, text="INFO PERMAINAN", font=("Helvetica", 12, "bold"), 
                                 bg="#34495e", fg="#ecf0f1")
        self.info_label.pack(pady=5)
        
        self.snake_info = tk.Label(self.info_frame, text="🐍 - Turun ke bawah", font=("Helvetica", 10), 
                                 bg="#34495e", fg="#e74c3c")
        self.snake_info.pack(anchor='w', padx=10, pady=2)
        
        self.ladder_info = tk.Label(self.info_frame, text="🪜 - Naik ke atas", font=("Helvetica", 10), 
                                  bg="#34495e", fg="#2ecc71")
        self.ladder_info.pack(anchor='w', padx=10, pady=2)
        
        self.win_info = tk.Label(self.info_frame, text="🏆 - Mencapai 100 untuk menang", font=("Helvetica", 10), 
                               bg="#34495e", fg="#f1c40f")
        self.win_info.pack(anchor='w', padx=10, pady=2)
        
        # Queue untuk giliran pemain
        self.player_queue = deque()
        self.total_players = 0
        self.player_positions = []
        self.current_player = 0
        self.game_over = True
        
        # Pion pemain
        self.player_pieces = []
        
        # Posisi kotak pada canvas
        self.positions = {}
        self.draw_board()

    def draw_board(self):
        size = 64
        number = 100
        colors = ["#f9e79f", "#fadbd8", "#d2b4de", "#a9dfbf", "#aed6f1"]

        for row in range(10):
            for col in range(10):
                actual_col = col if row % 2 == 0 else 9 - col
                x1 = actual_col * size
                y1 = row * size
                x2 = x1 + size
                y2 = y1 + size
                color = colors[row % len(colors)]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#888")
                self.canvas.create_text(x1 + 32, y1 + 32, text=str(number), font=("Arial", 10, "bold"))
                self.positions[number] = (x1 + 32, y1 + 32)
                number -= 1

        # Ular
        for start, end in snakes.items():
            x1, y1 = self.positions[start]
            x2, y2 = self.positions[end]
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=3, arrow=tk.LAST)
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="🐍", font=("Arial", 12))

        # Tangga
        for start, end in ladders.items():
            x1, y1 = self.positions[start]
            x2, y2 = self.positions[end]
            self.canvas.create_line(x1, y1, x2, y2, fill="green", width=3, arrow=tk.LAST)
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="🪜", font=("Arial", 12))

    def start_game(self):
        """Mulai permainan dengan menentukan jumlah pemain"""
        num_players = simpledialog.askinteger("Jumlah Pemain", 
                                           "Masukkan jumlah pemain (2-4):", 
                                           minvalue=2, maxvalue=4)
        
        if num_players is None:
            return
        
        self.total_players = num_players
        
        # Inisialisasi queue giliran pemain
        self.player_queue = deque(range(1, num_players + 1)) 
        self.current_player = self.player_queue[0]  # Pemain pertama
        
        # Reset posisi semua pemain
        self.player_positions = [1] * (num_players + 1)
        
        # Hapus frame pemain lama jika ada
        for frame in self.player_frames:
            frame.destroy()
        
        # Reset frame dan label
        self.player_frames = []
        self.player_labels = []
        self.player_pos_labels = []
        
        # Buat frame status untuk setiap pemain
        for i in range(1, num_players + 1):
            player_frame = tk.Frame(self.status_frame, bg=self.player_colors[i-1], bd=1, relief=tk.RAISED)
            player_frame.pack(fill="x", pady=5)
            
            player_label = tk.Label(player_frame, 
                                  text=f"Pemain {i} {self.player_symbols[i-1]}", 
                                  font=("Helvetica", 12, "bold"), 
                                  bg=self.player_colors[i-1], fg="white")
            player_label.pack(side=tk.LEFT, padx=10, pady=5)
            
            player_pos_label = tk.Label(player_frame, 
                                     text=f"Posisi: 1", 
                                     font=("Helvetica", 12), 
                                     bg=self.player_colors[i-1], fg="white")
            player_pos_label.pack(side=tk.RIGHT, padx=10, pady=5)
            
            self.player_frames.append(player_frame)
            self.player_labels.append(player_label)
            self.player_pos_labels.append(player_pos_label)
        
        # Hapus pion pemain lama jika ada
        for piece in self.player_pieces:
            self.canvas.delete(piece)
        
        # Buat pion untuk semua pemain
        self.player_pieces = []
        offset = 12 
        
        for i in range(1, num_players + 1):
            x, y = self.positions[1]  # Semua pemain mulai di posisi 1
            # Distribusikan pion di posisi awal agar tidak tumpang tindih
            piece_offset = ((i-1) * 8) - ((num_players-1) * 4)  # Distribute pieces
            piece = self.canvas.create_oval(
                x - offset + piece_offset, 
                y - offset + piece_offset, 
                x + offset + piece_offset, 
                y + offset + piece_offset, 
                fill=self.player_colors[i-1], 
                outline="black", 
                width=2
            )
            self.player_pieces.append(piece)
        
        # Update UI
        self.start_button.pack_forget()  # Sembunyikan tombol mulai
        self.roll_button.pack(pady=20)  # Tampilkan tombol dadu
        
        # Update label giliran
        self.turn_label.config(text=f"Giliran: Pemain {self.current_player} {self.player_symbols[self.current_player-1]}")
        self.turn_frame.config(bg=self.player_colors[self.current_player-1])
        self.turn_label.config(bg=self.player_colors[self.current_player-1])
        
        # Reset dice
        self.dice_value.config(text="-")
        
        # Set game in progress
        self.game_over = False
        
        # Tampilkan pesan permainan dimulai
        messagebox.showinfo("🎮 Permainan Dimulai", f"Permainan dimulai dengan {num_players} pemain. Giliran Pemain 1!")

    def move_player(self, player_num, new_pos):
        """Pindahkan pion pemain ke posisi baru"""
        x, y = self.positions[new_pos]
        
        # Distribusikan pion agar tidak tumpang tindih di kotak yang sama
        piece_offset = ((player_num-1) * 8) - ((self.total_players-1) * 4)  # Distribute pieces
        offset = 12  # Offset dasar

        self.canvas.coords(
            self.player_pieces[player_num-1], 
            x - offset + piece_offset, 
            y - offset + piece_offset, 
            x + offset + piece_offset, 
            y + offset + piece_offset
        )
        
        # Update label posisi pemain
        self.player_pos_labels[player_num-1].config(text=f"Posisi: {new_pos}")
        self.player_positions[player_num] = new_pos

    def roll_dice(self):
        """Lempar dadu dan pindahkan pemain saat ini"""
        # Jika permainan sudah selesai, abaikan klik pada tombol lempar dadu
        if self.game_over:
            return
            
        dice = random.randint(1, 6)
        self.dice_value.config(text=str(dice))
        
        # Animasi efek lempar dadu
        self.dice_label.config(text="🎯")
        self.root.after(100, lambda: self.dice_label.config(text="🎲"))
        
        # Get current player index (0-based for array access)
        player_idx = self.current_player - 1
        
        # High-light frame pemain yang sedang bermain
        for i, frame in enumerate(self.player_frames):
            if i == player_idx:
                # Darken current player's color
                darker_color = self.darken_color(self.player_colors[i])
                frame.config(bg=darker_color, relief=tk.SUNKEN)
                self.player_labels[i].config(bg=darker_color)
                self.player_pos_labels[i].config(bg=darker_color)
            else:
                # Reset other player's color
                frame.config(bg=self.player_colors[i], relief=tk.RAISED)
                self.player_labels[i].config(bg=self.player_colors[i])
                self.player_pos_labels[i].config(bg=self.player_colors[i])
        
        # Move player
        current_pos = self.player_positions[self.current_player]
        if current_pos + dice <= 100:
            old_pos = current_pos
            new_pos = current_pos + dice
            self.player_positions[self.current_player] = new_pos
            self.move_player(self.current_player, new_pos)
            
            # Check for snake or ladder
            if new_pos in snakes:
                self.player_positions[self.current_player] = snakes[new_pos]
                self.root.after(500, lambda: self.move_player(self.current_player, snakes[new_pos]))
                self.root.after(500, lambda: self.show_message(
                    "🐍 Ular!", 
                    f"Pemain {self.current_player} {self.player_symbols[player_idx]} turun dari {new_pos} ke {snakes[new_pos]}"
                ))
            elif new_pos in ladders:
                self.player_positions[self.current_player] = ladders[new_pos]
                self.root.after(500, lambda: self.move_player(self.current_player, ladders[new_pos]))
                self.root.after(500, lambda: self.show_message(
                    "🪜 Tangga!", 
                    f"Pemain {self.current_player} {self.player_symbols[player_idx]} naik dari {new_pos} ke {ladders[new_pos]}"
                ))
        
        # Cek kondisi kemenangan
        if self.player_positions[self.current_player] == 100:
            self.game_over = True
            self.handle_win(self.current_player)
        else:
            # Pindah giliran ke pemain berikutnya menggunakan queue
            # Rotate queue: pemain saat ini dipindah ke akhir queue
            self.player_queue.append(self.player_queue.popleft())
            self.current_player = self.player_queue[0]
            
            # Update label giliran
            self.turn_label.config(
                text=f"Giliran: Pemain {self.current_player} {self.player_symbols[self.current_player-1]}"
            )
            self.turn_frame.config(bg=self.player_colors[self.current_player-1])
            self.turn_label.config(bg=self.player_colors[self.current_player-1])
    
    def darken_color(self, hex_color):
        """Membuat warna menjadi lebih gelap untuk efek highlight"""
        # Convert hex to RGB
        h = hex_color.lstrip('#')
        rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        
        darkened = tuple(max(0, int(c * 0.7)) for c in rgb)
        
        # Convert back to hex
        return '#{:02x}{:02x}{:02x}'.format(*darkened)
    
    def handle_win(self, winner):
        """Menangani kondisi ketika salah satu pemain menang"""
        # Ubah tampilan UI untuk menandakan game over
        self.roll_button.pack_forget()  # Sembunyikan tombol lempar dadu
        
        # Tampilkan tombol reset
        self.reset_button.pack(pady=20)
        
        # Ubah label giliran menjadi pemberitahuan pemenang
        winner_idx = winner - 1  # Convert to 0-based index
        winner_text = f"🏆 Pemain {winner} {self.player_symbols[winner_idx]} Menang! 🏆"
        self.turn_frame.config(bg="#f1c40f")  # Ubah warna menjadi emas
        self.turn_label.config(text=winner_text, bg="#f1c40f")
        
        # Tampilkan pesan kemenangan
        messagebox.showinfo(
            "🏆 Permainan Berakhir!", 
            f"Selamat! Pemain {winner} {self.player_symbols[winner_idx]} mencapai 100 dan menang!"
        )
            
    def reset_game(self):
        """Reset permainan ke kondisi awal"""
        # Sembunyikan tombol reset
        self.reset_button.pack_forget()
        
        # Tampilkan tombol start
        self.start_button.pack(pady=20)
        
        # Reset status permainan
        self.game_over = True
        
        # Reset label
        self.turn_label.config(text="Menunggu pemain...", bg="#3498db")
        self.turn_frame.config(bg="#3498db")
        self.dice_value.config(text="-")
        
        # Tampilkan pesan
        messagebox.showinfo("🎮 Permainan Selesai", "Klik 'MULAI PERMAINAN' untuk bermain lagi!")
            
    def show_message(self, title, message):
        """Menampilkan pesan informasi tentang snake atau ladder"""
        messagebox.showinfo(title, message)

# Jalankan program
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeLadderGame(root)
    root.mainloop()