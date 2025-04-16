import tkinter as tk
from tkinter import messagebox
import random

snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

class SnakeLadderGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Ular Tangga 2 Pemain")
        self.root.geometry("1000x650")
        self.root.configure(bg="#2c3e50")

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
        self.turn_label = tk.Label(self.turn_frame, text="Giliran: Pemain 1 🔵", font=("Helvetica", 16, "bold"), bg="#3498db", fg="white")
        self.turn_label.pack(pady=15)

        # Player status
        self.status_frame = tk.Frame(self.side_panel, bg="#34495e")
        self.status_frame.pack(fill="x", padx=20, pady=10)
        
        # Player 1 status
        self.p1_frame = tk.Frame(self.status_frame, bg="#2980b9", bd=1, relief=tk.RAISED)
        self.p1_frame.pack(fill="x", pady=5)
        self.p1_label = tk.Label(self.p1_frame, text="Pemain 1 🔵", font=("Helvetica", 12, "bold"), bg="#2980b9", fg="white")
        self.p1_label.pack(side=tk.LEFT, padx=10, pady=5)
        self.p1_pos_label = tk.Label(self.p1_frame, text="Posisi: 1", font=("Helvetica", 12), bg="#2980b9", fg="white")
        self.p1_pos_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Player 2 status
        self.p2_frame = tk.Frame(self.status_frame, bg="#e67e22", bd=1, relief=tk.RAISED)
        self.p2_frame.pack(fill="x", pady=5)
        self.p2_label = tk.Label(self.p2_frame, text="Pemain 2 🟠", font=("Helvetica", 12, "bold"), bg="#e67e22", fg="white")
        self.p2_label.pack(side=tk.LEFT, padx=10, pady=5)
        self.p2_pos_label = tk.Label(self.p2_frame, text="Posisi: 1", font=("Helvetica", 12), bg="#e67e22", fg="white")
        self.p2_pos_label.pack(side=tk.RIGHT, padx=10, pady=5)

        # Dice display
        self.dice_frame = tk.Frame(self.side_panel, bg="#2c3e50", height=120, bd=2, relief=tk.GROOVE)
        self.dice_frame.pack(fill="x", padx=20, pady=20)
        self.dice_frame.pack_propagate(False)
        
        self.dice_title = tk.Label(self.dice_frame, text="DADU", font=("Helvetica", 14, "bold"), bg="#2c3e50", fg="#ecf0f1")
        self.dice_title.pack(pady=(10, 0))
        
        self.dice_label = tk.Label(self.dice_frame, text="🎲", font=("Helvetica", 40), bg="#2c3e50", fg="#ecf0f1")
        self.dice_label.pack()
        
        self.dice_value = tk.Label(self.dice_frame, text="-", font=("Helvetica", 20, "bold"), bg="#2c3e50", fg="#f1c40f")
        self.dice_value.pack()

        # Button Dadu
        self.roll_button = tk.Button(self.side_panel, text="LEMPAR DADU 🎲", font=("Helvetica", 14, "bold"), bg="#27ae60", fg="white", activebackground="#2ecc71", activeforeground="white", bd=0, padx=20, pady=10, command=self.roll_dice)
        self.roll_button.pack(pady=20)
        
        # Reset button
        self.reset_button = tk.Button(self.side_panel, text="MAIN LAGI 🔄", font=("Helvetica", 14, "bold"), bg="#e74c3c", fg="white", activebackground="#c0392b", activeforeground="white", bd=0, padx=20, pady=10,command=self.reset_game)
        
        # Game info section
        self.info_frame = tk.Frame(self.side_panel, bg="#34495e", bd=1, relief=tk.SUNKEN)
        self.info_frame.pack(fill="x", padx=20, pady=(30, 10))
        
        self.info_label = tk.Label(self.info_frame, text="INFO PERMAINAN", font=("Helvetica", 12, "bold"), bg="#34495e", fg="#ecf0f1")
        self.info_label.pack(pady=5)
        
        self.snake_info = tk.Label(self.info_frame, text="🐍 - Turun ke bawah", font=("Helvetica", 10), bg="#34495e", fg="#e74c3c")
        self.snake_info.pack(anchor='w', padx=10, pady=2)
        
        self.ladder_info = tk.Label(self.info_frame, text="🪜 - Naik ke atas", font=("Helvetica", 10), bg="#34495e", fg="#2ecc71")
        self.ladder_info.pack(anchor='w', padx=10, pady=2)
        
        self.win_info = tk.Label(self.info_frame, text="🏆 - Mencapai 100 untuk menang", font=("Helvetica", 10), bg="#34495e", fg="#f1c40f")
        self.win_info.pack(anchor='w', padx=10, pady=2)

        self.positions = {}
        self.draw_board()

        # Pemain
        self.p1_pos = 1
        self.p2_pos = 1
        self.current_player = 1
        self.game_over = False

        self.player1_piece = None
        self.player2_piece = None
        self.create_players()

    # Board
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

    def create_players(self):
        x1, y1 = self.positions[self.p1_pos]
        x2, y2 = self.positions[self.p2_pos]
        self.player1_piece = self.canvas.create_oval(x1 - 12, y1 - 12, x1 + 12, y1 + 12, fill="#3498db", outline="black", width=2)
        self.player2_piece = self.canvas.create_oval(x2 - 12, y2 + 5, x2 + 12, y2 + 29, fill="#e67e22", outline="black", width=2)

    def move_player(self, player_num, new_pos):
        x, y = self.positions[new_pos]
        if player_num == 1:
            self.canvas.coords(self.player1_piece, x - 12, y - 12, x + 12, y + 12)
            self.p1_pos_label.config(text=f"Posisi: {new_pos}")
        else:
            self.canvas.coords(self.player2_piece, x - 12, y + 5, x + 12, y + 29)
            self.p2_pos_label.config(text=f"Posisi: {new_pos}")

    def roll_dice(self):
        if self.game_over:
            return
            
        dice = random.randint(1, 6)
        self.dice_value.config(text=str(dice))
        
        # Animasi lempar dadu
        self.dice_label.config(text="🎯")
        self.root.after(100, lambda: self.dice_label.config(text="🎲"))

        # Hilight player
        if self.current_player == 1:
            self.p1_frame.config(bg="#1a5276", relief=tk.SUNKEN)
            self.p1_label.config(bg="#1a5276")
            self.p1_pos_label.config(bg="#1a5276")
            self.p2_frame.config(bg="#e67e22", relief=tk.RAISED)
            self.p2_label.config(bg="#e67e22")
            self.p2_pos_label.config(bg="#e67e22")
            
            # Move player
            if self.p1_pos + dice <= 100:
                old_pos = self.p1_pos
                self.p1_pos += dice
                self.move_player(1, self.p1_pos)
                
                # Check for snake or ladder
                if self.p1_pos in snakes:
                    self.p1_pos = snakes[self.p1_pos]
                    self.root.after(500, lambda: self.move_player(1, self.p1_pos))
                    self.root.after(500, lambda: self.show_message("🐍 Ular!", f"Pemain 1 turun dari {old_pos + dice} ke {self.p1_pos}"))
                elif self.p1_pos in ladders:
                    self.p1_pos = ladders[self.p1_pos]
                    self.root.after(500, lambda: self.move_player(1, self.p1_pos))
                    self.root.after(500, lambda: self.show_message("🪜 Tangga!", f"Pemain 1 naik dari {old_pos + dice} ke {self.p1_pos}"))
        else:
            self.p2_frame.config(bg="#9c4600", relief=tk.SUNKEN)
            self.p2_label.config(bg="#9c4600")
            self.p2_pos_label.config(bg="#9c4600")
            self.p1_frame.config(bg="#2980b9", relief=tk.RAISED)
            self.p1_label.config(bg="#2980b9")
            self.p1_pos_label.config(bg="#2980b9")
            
            # Move player
            if self.p2_pos + dice <= 100:
                old_pos = self.p2_pos
                self.p2_pos += dice
                self.move_player(2, self.p2_pos)
                
                # Check for snake or ladder
                if self.p2_pos in snakes:
                    self.p2_pos = snakes[self.p2_pos]
                    self.root.after(500, lambda: self.move_player(2, self.p2_pos))
                    self.root.after(500, lambda: self.show_message("🐍 Ular!", f"Pemain 2 turun dari {old_pos + dice} ke {self.p2_pos}"))
                elif self.p2_pos in ladders:
                    self.p2_pos = ladders[self.p2_pos]
                    self.root.after(500, lambda: self.move_player(2, self.p2_pos))
                    self.root.after(500, lambda: self.show_message("🪜 Tangga!", f"Pemain 2 naik dari {old_pos + dice} ke {self.p2_pos}"))

        # Cek kondisi kemenangan
        if self.p1_pos == 100:
            self.game_over = True
            self.handle_win(1)
        elif self.p2_pos == 100:
            self.game_over = True
            self.handle_win(2)
        else:
            # Ganti giliran
            self.current_player = 2 if self.current_player == 1 else 1
            giliran = "Pemain 1 🔵" if self.current_player == 1 else "Pemain 2 🟠"
            self.turn_label.config(text=f"Giliran: {giliran}")
    
    def handle_win(self, winner):
        """Menangani kondisi ketika salah satu pemain menang"""
        # game over
        self.roll_button.pack_forget()
        
        # Tampilkan tombol reset
        self.reset_button.pack(pady=20)
        
        # Pemberitahuan pemenang
        winner_text = f"🏆 Pemain {winner} Menang! 🏆"
        self.turn_frame.config(bg="#f1c40f")
        self.turn_label.config(text=winner_text, bg="#f1c40f")
        player_color = "🔵" if winner == 1 else "🟠"
        messagebox.showinfo("🏆 Permainan Berakhir!", f"Selamat! Pemain {winner} {player_color} mencapai 100 dan menang!")
            
    def reset_game(self):
        """Reset permainan ke kondisi awal"""
        # Reset posisi pemain
        self.p1_pos = 1
        self.p2_pos = 1
        self.move_player(1, self.p1_pos)
        self.move_player(2, self.p2_pos)
        
        # Reset UI elements
        self.turn_frame.config(bg="#3498db")
        self.turn_label.config(text="Giliran: Pemain 1 🔵", bg="#3498db")
        
        self.p1_frame.config(bg="#2980b9", relief=tk.RAISED)
        self.p1_label.config(bg="#2980b9")
        self.p1_pos_label.config(bg="#2980b9")
        
        self.p2_frame.config(bg="#e67e22", relief=tk.RAISED)
        self.p2_label.config(bg="#e67e22")
        self.p2_pos_label.config(bg="#e67e22")
        
        self.dice_value.config(text="-")
        
        self.reset_button.pack_forget()
        self.roll_button.pack(pady=20)
        
        # Reset status permainan
        self.current_player = 1
        self.game_over = False
        
        messagebox.showinfo("🎮 Permainan Baru", "Permainan baru telah dimulai!")
            
    def show_message(self, title, message):
        """Menampilkan pesan informasi tentang snake atau ladder"""
        messagebox.showinfo(title, message)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeLadderGame(root)
    root.mainloop()