import tkinter as tk
import random
import os
import platform
from datetime import datetime

# Sound-Import je nach Betriebssystem
if platform.system() == "Windows":
    import winsound
    def play_sound(frequency, duration):
        winsound.Beep(frequency, duration)
else:
    # Linux und Mac Alternative
    def play_sound(frequency, duration):
        # Stille Implementierung für Systeme ohne winsound
        pass

class SnakeGame:
    def __init__(self, master):
        # Fensterkonfiguration
        self.master = master
        self.master.title("Snake Game")
        self.master.geometry("400x500")  # Höhe für Highscore erhöht
        self.master.resizable(False, False)
        
        # Spielkonstanten
        self.width = 400
        self.height = 400
        self.cell_size = 20
        self.base_speed = 150
        self.game_speed = self.base_speed
        self.speed_increase = 5
        
        # Spielvariablen
        self.direction = "Right"
        self.new_direction = "Right"
        self.game_running = False
        self.score = 0
        self.highscore = self.load_highscore()
        
        # Spezielle Nahrung
        self.food_types = {
            "normal": {"color": "red", "points": 10, "probability": 0.7},
            "bonus": {"color": "gold", "points": 30, "probability": 0.2},
            "speed": {"color": "purple", "points": 5, "probability": 0.1}
        }
        
        # Initialisiere die Schlange und das Futter
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.create_food()
        self.current_food_type = "normal"
        
        # Frame für Punktestand
        self.score_frame = tk.Frame(self.master, height=100)
        self.score_frame.pack(fill=tk.X)
        
        # Punktestand-Labels
        self.score_label = tk.Label(
            self.score_frame, 
            text="Punkte: 0", 
            font=("Arial", 14)
        )
        self.score_label.pack(pady=5)
        
        self.highscore_label = tk.Label(
            self.score_frame, 
            text=f"Highscore: {self.highscore}", 
            font=("Arial", 12)
        )
        self.highscore_label.pack(pady=5)
        
        # Canvas erstellen
        self.canvas = tk.Canvas(self.master, bg="black", width=self.width, height=self.height)
        self.canvas.pack()
        
        # Startbildschirm anzeigen
        self.show_start_screen()
        
        # Tastaturereignisse
        self.master.bind("<KeyPress>", self.on_key_press)
        
        # Pause-Funktion
        self.paused = False

    def load_highscore(self):
        """Lädt den Highscore aus einer Datei, falls vorhanden"""
        try:
            with open("snake_highscore.txt", "r") as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def save_highscore(self):
        """Speichert den Highscore in einer Datei"""
        with open("snake_highscore.txt", "w") as file:
            file.write(str(self.highscore))

    def update_score_display(self):
        """Aktualisiert die Punkteanzeige"""
        self.score_label.config(text=f"Punkte: {self.score}")
        self.highscore_label.config(text=f"Highscore: {self.highscore}")

    def show_start_screen(self):
        """Zeigt den Startbildschirm an"""
        self.canvas.delete("all")
        self.canvas.create_text(
            self.width // 2, self.height // 2 - 50,
            text="Snake Game", fill="white", font=("Arial", 24)
        )
        
        # Spielanleitung
        self.canvas.create_text(
            self.width // 2, self.height // 2,
            text="Steuerung:", fill="white", font=("Arial", 12, "bold")
        )
        self.canvas.create_text(
            self.width // 2, self.height // 2 + 25,
            text="Pfeiltasten - Bewegen", fill="white", font=("Arial", 10)
        )
        self.canvas.create_text(
            self.width // 2, self.height // 2 + 45,
            text="P - Pause", fill="white", font=("Arial", 10)
        )
        
        # Nahrungstypen erklären
        y_offset = self.height // 2 + 75
        self.canvas.create_text(
            self.width // 2, y_offset,
            text="Nahrungstypen:", fill="white", font=("Arial", 12, "bold")
        )
        
        # Normal Food
        y_offset += 20
        self.canvas.create_oval(
            self.width // 2 - 50, y_offset, self.width // 2 - 30, y_offset + 20,
            fill="red"
        )
        self.canvas.create_text(
            self.width // 2 + 20, y_offset + 10,
            text="Normal: +10 Punkte", fill="white", font=("Arial", 10), anchor="w"
        )
        
        # Bonus Food
        y_offset += 25
        self.canvas.create_oval(
            self.width // 2 - 50, y_offset, self.width // 2 - 30, y_offset + 20,
            fill="gold"
        )
        self.canvas.create_text(
            self.width // 2 + 20, y_offset + 10,
            text="Bonus: +30 Punkte", fill="white", font=("Arial", 10), anchor="w"
        )
        
        # Speed Food
        y_offset += 25
        self.canvas.create_oval(
            self.width // 2 - 50, y_offset, self.width // 2 - 30, y_offset + 20,
            fill="purple"
        )
        self.canvas.create_text(
            self.width // 2 + 20, y_offset + 10,
            text="Speed: +5 Punkte, schneller", fill="white", font=("Arial", 10), anchor="w"
        )
        
        self.canvas.create_text(
            self.width // 2, self.height - 30,
            text="Drücke 'Space' zum Starten", fill="white", font=("Arial", 12)
        )

    def create_food(self):
        """Erstellt ein neues Futterstück an einer zufälligen Position mit zufälligem Typ"""
        # Berechne alle möglichen Zellpositionen
        positions_x = list(range(0, self.width, self.cell_size))
        positions_y = list(range(0, self.height, self.cell_size))
        
        # Wähle den Nahrungstyp basierend auf Wahrscheinlichkeiten
        food_types_list = list(self.food_types.keys())
        probabilities = [self.food_types[t]["probability"] for t in food_types_list]
        self.current_food_type = random.choices(food_types_list, probabilities)[0]
        
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
        
        # Spiel pausieren
        if key == "p" and self.game_running:
            self.paused = not self.paused
            if not self.paused:
                self.game_loop()
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
        self.paused = False
        self.draw_snake()
        self.draw_food()
        self.game_loop()
        
        # Startsound
        play_sound(440, 100)  # A4

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
        food_color = self.food_types[self.current_food_type]["color"]
        self.canvas.create_oval(
            x, y, x + self.cell_size, y + self.cell_size,
            fill=food_color, tags="food"
        )

    def game_loop(self):
        """Die Hauptspielschleife"""
        if not self.game_running or self.paused:
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
            food_info = self.food_types[self.current_food_type]
            
            # Erhöhe den Punktestand basierend auf dem Futtertyp
            points = food_info["points"]
            self.score += points
            
            # Spiele Ton je nach Futtertyp
            if self.current_food_type == "normal":
                play_sound(440, 100)  # A4
            elif self.current_food_type == "bonus":
                play_sound(660, 150)  # E5
            elif self.current_food_type == "speed":
                play_sound(880, 100)  # A5
            
            # Aktualisiere Highscore falls nötig
            if self.score > self.highscore:
                self.highscore = self.score
                self.save_highscore()
            
            self.update_score_display()
            
            # Spezialeffekte je nach Futtertyp
            if self.current_food_type == "speed":
                # Speed-Futter erhöht die Geschwindigkeit stärker
                if self.game_speed > 50:
                    self.game_speed -= 10
            else:
                # Normal und Bonus erhöhen die Geschwindigkeit nur leicht
                if self.game_speed > 50:
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
            play_sound(220, 300)  # Tiefer Ton bei Kollision
            return True
        
        # Prüfe Selbstkollisionen (ignoriert den Kopf beim Vergleich)
        if self.snake[0] in self.snake[1:]:
            play_sound(220, 300)  # Tiefer Ton bei Kollision
            return True
        
        return False

    def game_over(self):
        """Zeigt den Game-Over-Bildschirm an"""
        self.game_running = False
        self.canvas.delete("all")
        
        # Game Over Text
        self.canvas.create_text(
            self.width // 2, self.height // 2 - 50,
            text="Game Over!", fill="white", font=("Arial", 24)
        )
        
        # Punktestand
        self.canvas.create_text(
            self.width // 2, self.height // 2,
            text=f"Punkte: {self.score}", fill="white", font=("Arial", 18)
        )
        
        # Highscore
        highscore_text = "Neuer Highscore!" if self.score >= self.highscore else f"Highscore: {self.highscore}"
        self.canvas.create_text(
            self.width // 2, self.height // 2 + 30,
            text=highscore_text, fill="gold" if self.score >= self.highscore else "white", 
            font=("Arial", 14)
        )
        
        # Datum und Uhrzeit
        current_time = datetime.now().strftime("%d.%m.%Y, %H:%M")
        self.canvas.create_text(
            self.width // 2, self.height // 2 + 60,
            text=f"Gespielt am: {current_time}", fill="white", font=("Arial", 10)
        )
        
        # Neustart-Anweisung
        self.canvas.create_text(
            self.width // 2, self.height - 30,
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