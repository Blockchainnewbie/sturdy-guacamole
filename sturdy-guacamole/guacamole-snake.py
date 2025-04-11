import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        # Fensterkonfiguration
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("400x450")  # Höhe erhöht für Punktestand
        self.master.resizable(False, False)
        
        # Spielkonstanten
        self.width = 400
        self.height = 400
        self.cell_size = 20
        self.base_speed = 150  # Basis-Geschwindigkeit in Millisekunden
        self.game_speed = self.base_speed
        self.speed_increase = 5  # Geschwindigkeitssteigerung pro Futter
        
        # Spielvariablen
        self.direction = "Right"
        self.new_direction = "Right"
        self.game_running = False
        self.score = 0
        
        # Initialisiere die Schlange und das Futter
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.create_food()
        
        # Frame für Punktestand
        self.score_frame = tk.Frame(self.master, height=50)
        self.score_frame.pack(fill=tk.X)
        
        # Punktestand-Label
        self.score_label = tk.Label(
            self.score_frame, 
            text="Punkte: 0", 
            font=("Arial", 14)
        )
        self.score_label.pack(pady=10)
        
        # Canvas erstellen
        self.canvas = tk.Canvas(self.master, bg="black", width=self.width, height=self.height)
        self.canvas.pack()
        
        # Startbildschirm anzeigen
        self.show_start_screen()
        
        # Tastaturereignisse
        self.master.bind("<KeyPress>", self.on_key_press)

    def update_score_display(self):
        """Aktualisiert die Punkteanzeige"""
        self.score_label.config(text=f"Punkte: {self.score}")

    def show_start_screen(self):
        """Zeigt den Startbildschirm an"""
        self.canvas.delete("all")
        self.canvas.create_text(
            self.width // 2, self.height // 2 - 30,
            text="Snake Game", fill="white", font=("Arial", 24)
        )
        self.canvas.create_text(
            self.width // 2, self.height // 2 + 10,
            text="Drücke 'Space' zum Starten", fill="white", font=("Arial", 12)
        )
        # Hilfetext für Steuerung hinzufügen
        self.canvas.create_text(
            self.width // 2, self.height // 2 + 50,
            text="Steuerung: Pfeiltasten", fill="white", font=("Arial", 10)
        )

    def create_food(self):
        """Erstellt ein neues Futterstück an einer zufälligen Position"""
        # Berechne alle möglichen Zellpositionen
        positions_x = list(range(0, self.width, self.cell_size))
        positions_y = list(range(0, self.height, self.cell_size))
        
        # Generiere eine zufällige Position, die nicht mit der Schlange kollidiert
        while True:
            food_pos = (random.choice(positions_x), random.choice(positions_y))
            if food_pos not in self.snake:
                return food_pos

    def on_key_press(self, event):
        """Verarbeitet Tastatureingaben"""
        key = event.keysym
        
        # Spiel starten
        if key == "space" and not self.game_running:
            self.game_running = True
            self.start_game()
            return
        
        # Richtungsänderungen - verhindere 180-Grad-Wendungen
        if key == "Up" and self.direction != "Down":
            self.new_direction = "Up"
        elif key == "Down" and self.direction != "Up":
            self.new_direction = "Down"
        elif key == "Left" and self.direction != "Right":
            self.new_direction = "Left"
        elif key == "Right" and self.direction != "Left":
            self.new_direction = "Right"

    def start_game(self):
        """Startet das Spiel"""
        self.canvas.delete("all")
        self.score = 0
        self.update_score_display()
        self.game_speed = self.base_speed
        self.draw_snake()
        self.draw_food()
        self.game_loop()

    def draw_snake(self):
        """Zeichnet die Schlange auf dem Canvas"""
        self.canvas.delete("snake")
        for i, segment in enumerate(self.snake):
            x, y = segment
            # Kopf in anderer Farbe
            fill_color = "darkgreen" if i == 0 else "green"
            self.canvas.create_rectangle(
                x, y, x + self.cell_size, y + self.cell_size,
                fill=fill_color, outline="black", tags="snake"
            )

    def draw_food(self):
        """Zeichnet das Futter auf dem Canvas"""
        self.canvas.delete("food")
        x, y = self.food
        self.canvas.create_oval(
            x, y, x + self.cell_size, y + self.cell_size,
            fill="red", tags="food"
        )

    def game_loop(self):
        """Die Hauptspielschleife"""
        if not self.game_running:
            return
        
        # Aktualisiere die Richtung
        self.direction = self.new_direction
        
        # Bewege die Schlange
        self.move_snake()
        
        # Überprüfe Kollisionen
        if self.check_collisions():
            self.game_over()
            return
        
        # Zeichne die Schlange und das Futter
        self.draw_snake()
        self.draw_food()
        
        # Rufe die Schleife erneut auf
        self.master.after(self.game_speed, self.game_loop)

    def move_snake(self):
        """Bewegt die Schlange in die aktuelle Richtung"""
        head_x, head_y = self.snake[0]
        
        # Berechne die neue Kopfposition basierend auf der Richtung
        if self.direction == "Up":
            head_y -= self.cell_size
        elif self.direction == "Down":
            head_y += self.cell_size
        elif self.direction == "Left":
            head_x -= self.cell_size
        elif self.direction == "Right":
            head_x += self.cell_size
        
        # Füge den neuen Kopf am Anfang der Schlange hinzu
        self.snake.insert(0, (head_x, head_y))
        
        # Prüfe, ob die Schlange das Futter gefressen hat
        if self.snake[0] == self.food:
            # Erhöhe den Punktestand
            self.score += 10
            self.update_score_display()
            
            # Erhöhe die Geschwindigkeit
            if self.game_speed > 50:  # Limitiere die maximale Geschwindigkeit
                self.game_speed -= self.speed_increase
            
            # Generiere neues Futter
            self.food = self.create_food()
        else:
            # Wenn nicht, entferne das letzte Segment
            self.snake.pop()

    def check_collisions(self):
        """Überprüft, ob die Schlange mit einer Wand oder sich selbst kollidiert ist"""
        head_x, head_y = self.snake[0]
        
        # Prüfe Wandkollisionen
        if (head_x < 0 or head_x >= self.width or
            head_y < 0 or head_y >= self.height):
            return True
        
        # Prüfe Selbstkollisionen (ignoriert den Kopf beim Vergleich)
        if self.snake[0] in self.snake[1:]:
            return True
        
        return False

    def game_over(self):
        """Zeigt den Game-Over-Bildschirm an"""
        self.game_running = False
        self.canvas.delete("all")
        self.canvas.create_text(
            self.width // 2, self.height // 2 - 30,
            text="Game Over!", fill="white", font=("Arial", 24)
        )
        self.canvas.create_text(
            self.width // 2, self.height // 2 + 10,
            text=f"Punkte: {self.score}", fill="white", font=("Arial", 18)
        )
        self.canvas.create_text(
            self.width // 2, self.height // 2 + 50,
            text="Drücke 'Space' für ein neues Spiel", fill="white", font=("Arial", 12)
        )
        
        # Setze die Schlange und das Futter zurück
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.create_food()
        self.direction = "Right"
        self.new_direction = "Right"

# Spiel starten
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()