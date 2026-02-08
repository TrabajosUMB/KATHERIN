import tkinter as tk
from tkinter import ttk, messagebox
import time

class KnightTourGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Recorrido del Caballo - Knight's Tour")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Configuración del tablero
        self.board_size = 8
        self.cell_size = 60
        self.board = [[-1 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.move_count = 0
        self.animation_running = False
        self.animation_speed = 500  # milisegundos entre movimientos
        
        # Movimientos posibles del caballo (en forma de L)
        self.knight_moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        
        # Colores
        self.color_light = "#F0D9B5"
        self.color_dark = "#B58863"
        self.color_visited = "#7FC97F"
        self.color_current = "#FF6B6B"
        
        self.setup_gui()
    
    def setup_gui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Panel de control
        control_frame = ttk.LabelFrame(main_frame, text="Control", padding="10")
        control_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Entrada de posición inicial
        ttk.Label(control_frame, text="Posición Inicial:", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Fila (1-8):").grid(row=0, column=1, padx=5)
        self.row_entry = ttk.Entry(control_frame, width=8)
        self.row_entry.grid(row=0, column=2, padx=5)
        self.row_entry.insert(0, "1")
        
        ttk.Label(control_frame, text="Columna (A-H):").grid(row=0, column=3, padx=5)
        self.col_entry = ttk.Entry(control_frame, width=8)
        self.col_entry.grid(row=0, column=4, padx=5)
        self.col_entry.insert(0, "A")
        
        # Botones
        self.start_button = ttk.Button(control_frame, text="▶ Iniciar Recorrido", command=self.start_tour)
        self.start_button.grid(row=0, column=5, padx=10)
        
        self.clear_button = ttk.Button(control_frame, text="🗑 Limpiar", command=self.clear_board)
        self.clear_button.grid(row=0, column=6, padx=5)
        
        # Control de velocidad
        ttk.Label(control_frame, text="Velocidad:").grid(row=1, column=0, padx=5, pady=5)
        self.speed_scale = ttk.Scale(control_frame, from_=100, to=1000, orient=tk.HORIZONTAL, length=200)
        self.speed_scale.set(500)
        self.speed_scale.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
        ttk.Label(control_frame, text="Rápido ← → Lento").grid(row=1, column=4, padx=5)
        
        # Contador de movimientos
        self.move_label = ttk.Label(control_frame, text="Movimientos: 0/64", font=("Arial", 11))
        self.move_label.grid(row=1, column=5, columnspan=2, padx=10)
        
        # Canvas para el tablero
        board_frame = ttk.Frame(main_frame)
        board_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.canvas = tk.Canvas(
            board_frame,
            width=self.cell_size * self.board_size + 50,
            height=self.cell_size * self.board_size + 50,
            bg="white"
        )
        self.canvas.pack()
        
        # Panel de información
        info_frame = ttk.LabelFrame(main_frame, text="Información", padding="10")
        info_frame.grid(row=1, column=1, padx=(10, 0), sticky=(tk.N, tk.S, tk.E, tk.W))
        
        info_text = """
🎯 Instrucciones:
        
1. Ingresa la posición inicial:
   • Fila: 1-8
   • Columna: A-H
   
2. Ajusta la velocidad de 
   animación con el control
   deslizante
   
3. Presiona "Iniciar Recorrido"
   para comenzar
   
4. Presiona "Limpiar" para
   reiniciar el tablero

📋 Leyenda:
   • ♞ = Posición actual
   • 🟢 = Casillas visitadas
   • Números = Orden de visita
        """
        
        info_label = tk.Label(info_frame, text=info_text, justify=tk.LEFT, font=("Arial", 10))
        info_label.pack()
        
        self.draw_board()
    
    def draw_board(self):
        """Dibuja el tablero de ajedrez"""
        self.canvas.delete("all")
        
        # Margen para las etiquetas
        margin = 25
        
        # Dibujar etiquetas de columnas (A-H)
        columns = "ABCDEFGH"
        for i in range(self.board_size):
            x = margin + i * self.cell_size + self.cell_size // 2
            self.canvas.create_text(x, 15, text=columns[i], font=("Arial", 12, "bold"))
            self.canvas.create_text(x, margin + self.board_size * self.cell_size + 15, 
                                  text=columns[i], font=("Arial", 12, "bold"))
        
        # Dibujar etiquetas de filas (8-1)
        for i in range(self.board_size):
            y = margin + i * self.cell_size + self.cell_size // 2
            self.canvas.create_text(10, y, text=str(8-i), font=("Arial", 12, "bold"))
            self.canvas.create_text(margin + self.board_size * self.cell_size + 15, y, 
                                  text=str(8-i), font=("Arial", 12, "bold"))
        
        # Dibujar casillas del tablero
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = margin + col * self.cell_size
                y1 = margin + row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Color de la casilla
                color = self.color_light if (row + col) % 2 == 0 else self.color_dark
                
                # Si la casilla ha sido visitada, cambiar color
                if self.board[row][col] != -1:
                    color = self.color_visited
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=1)
                
                # Mostrar número de movimiento si la casilla ha sido visitada
                if self.board[row][col] != -1:
                    self.canvas.create_text(
                        x1 + self.cell_size // 2,
                        y1 + self.cell_size // 2,
                        text=str(self.board[row][col] + 1),
                        font=("Arial", 16, "bold"),
                        fill="white"
                    )
    
    def draw_knight(self, row, col):
        """Dibuja el caballo en la posición especificada"""
        margin = 25
        x = margin + col * self.cell_size
        y = margin + row * self.cell_size
        
        # Resaltar casilla actual
        self.canvas.create_rectangle(
            x, y, x + self.cell_size, y + self.cell_size,
            fill=self.color_current, outline="black", width=2
        )
        
        # Dibujar icono del caballo
        self.canvas.create_text(
            x + self.cell_size // 2,
            y + self.cell_size // 2,
            text="♞",
            font=("Arial", 40),
            fill="white"
        )
    
    def parse_position(self):
        """Convierte la entrada del usuario en coordenadas del tablero"""
        try:
            row_input = self.row_entry.get().strip()
            col_input = self.col_entry.get().strip().upper()
            
            # Validar fila (1-8)
            row = int(row_input)
            if row < 1 or row > 8:
                raise ValueError("La fila debe estar entre 1 y 8")
            
            # Validar columna (A-H)
            if col_input not in "ABCDEFGH" or len(col_input) != 1:
                raise ValueError("La columna debe ser una letra entre A y H")
            
            # Convertir a índices del array (0-7)
            row_idx = 8 - row  # Invertir porque el tablero se dibuja de arriba a abajo
            col_idx = ord(col_input) - ord('A')
            
            return row_idx, col_idx
        
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
            return None, None
    
    def is_safe(self, row, col):
        """Verifica si una posición es válida y no ha sido visitada"""
        return (0 <= row < self.board_size and 
                0 <= col < self.board_size and 
                self.board[row][col] == -1)
    
    def count_unvisited_neighbors(self, row, col):
        """Cuenta cuántos movimientos válidos hay desde una posición (heurística de Warnsdorff)"""
        count = 0
        for move_row, move_col in self.knight_moves:
            next_row = row + move_row
            next_col = col + move_col
            if self.is_safe(next_row, next_col):
                count += 1
        return count
    
    def solve_knight_tour(self, row, col):
        """Resuelve el recorrido del caballo usando backtracking con heurística de Warnsdorff"""
        self.board[row][col] = self.move_count
        self.move_count += 1
        
        # Si hemos visitado todas las casillas, éxito
        if self.move_count == self.board_size * self.board_size:
            return True
        
        # Obtener movimientos posibles y ordenarlos por la heurística de Warnsdorff
        possible_moves = []
        for move_row, move_col in self.knight_moves:
            next_row = row + move_row
            next_col = col + move_col
            if self.is_safe(next_row, next_col):
                count = self.count_unvisited_neighbors(next_row, next_col)
                possible_moves.append((count, next_row, next_col))
        
        # Ordenar por número de movimientos disponibles (menor primero)
        possible_moves.sort()
        
        # Intentar cada movimiento
        for _, next_row, next_col in possible_moves:
            if self.solve_knight_tour(next_row, next_col):
                return True
        
        # Backtrack
        self.move_count -= 1
        self.board[row][col] = -1
        return False
    
    def animate_tour(self, path):
        """Anima el recorrido del caballo"""
        if not self.animation_running:
            return
        
        if not path:
            self.animation_running = False
            self.start_button.config(state=tk.NORMAL)
            self.clear_button.config(state=tk.NORMAL)
            messagebox.showinfo("¡Completado!", "El caballo ha completado el recorrido de las 64 casillas.")
            return
        
        row, col = path.pop(0)
        self.board[row][col] = self.move_count
        self.move_count += 1
        
        self.draw_board()
        self.draw_knight(row, col)
        self.move_label.config(text=f"Movimientos: {self.move_count}/64")
        
        # Programar siguiente movimiento
        self.animation_speed = int(self.speed_scale.get())
        self.root.after(self.animation_speed, lambda: self.animate_tour(path))
    
    def start_tour(self):
        """Inicia el recorrido del caballo"""
        if self.animation_running:
            return
        
        # Obtener posición inicial
        start_row, start_col = self.parse_position()
        if start_row is None or start_col is None:
            return
        
        # Limpiar tablero
        self.clear_board()
        
        # Deshabilitar botones durante la animación
        self.start_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.DISABLED)
        
        # Resolver el problema
        self.move_count = 0
        if not self.solve_knight_tour(start_row, start_col):
            messagebox.showerror("No hay solución", 
                               "No se encontró una solución desde esta posición inicial.\n" +
                               "Intenta con otra posición.")
            self.clear_board()
            self.start_button.config(state=tk.NORMAL)
            self.clear_button.config(state=tk.NORMAL)
            return
        
        # Crear path para la animación
        path = []
        positions = [(0, 0)] * (self.board_size * self.board_size)
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] != -1:
                    positions[self.board[row][col]] = (row, col)
        
        # Limpiar tablero para la animación
        self.board = [[-1 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.move_count = 0
        
        # Iniciar animación
        self.animation_running = True
        self.animate_tour(positions)
    
    def clear_board(self):
        """Limpia el tablero"""
        self.animation_running = False
        self.board = [[-1 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.move_count = 0
        self.move_label.config(text="Movimientos: 0/64")
        self.draw_board()
        self.start_button.config(state=tk.NORMAL)
        self.clear_button.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    app = KnightTourGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
