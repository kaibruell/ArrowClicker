import keyboard
import pyautogui
import time
import threading

# Deaktivieren des FailSafe (nur wenn du dir sicher bist!)
# Achtung: Dies ist nicht empfohlen, aber hilft bei deinem Problem
pyautogui.FAILSAFE = False

# Konfiguration
STEP_SIZE = 10  # Pixel pro Tastendruck
ACCEL_FACTOR = 1.05  # Beschleunigung
MAX_SPEED = 30  # Maximale Geschwindigkeit
MIN_SPEED = 1  # Minimale Geschwindigkeit für Präzisionsarbeit
DEFAULT_DELAY = 0.005  # Aktualisierungsrate (Sekunden)

# Maus-Tasten
MOVE_UP = 'w'     # Anstelle von up
MOVE_DOWN = 's'   # Anstelle von down
MOVE_LEFT = 'a'   # Anstelle von left
MOVE_RIGHT = 'd'  # Anstelle von right
PRECISION = 'shift'
LEFT_CLICK = ','   # Komma für Linksklick
RIGHT_CLICK = '.'  # Punkt für Rechtsklick
TOGGLE_MODE = 'pause'  # Pause-Taste als Modus-Umschalter
EXIT_KEY = 'esc'   # ESC-Taste zum Beenden

# Status für Mausklicks
left_pressed = False
right_pressed = False

# Geschwindigkeiten speichern
speeds = {
    'up': 0,
    'down': 0,
    'left': 0,
    'right': 0
}

# Modus (True = Mausmodus, False = Eingabemodus)
mouse_mode = True

# Flag für laufendes Programm
running = True

def mouse_mover():
    """Thread-Funktion für flüssige Mausbewegung"""
    global running, speeds, mouse_mode
    
    while running:
        # Nur im Mausmodus bewegen
        if mouse_mode:
            # Bewegungsrichtung berechnen
            dx = speeds['right'] - speeds['left']
            dy = speeds['down'] - speeds['up']
            
            # Maus bewegen, wenn nötig
            if dx != 0 or dy != 0:
                try:
                    pyautogui.move(dx, dy)
                except Exception as e:
                    print(f"Fehler bei Mausbewegung: {e}")
        
        # Kurze Pause
        time.sleep(DEFAULT_DELAY)

def toggle_mode():
    """Wechselt zwischen Maus- und Eingabemodus"""
    global mouse_mode, speeds
    mouse_mode = not mouse_mode
    
    # Geschwindigkeiten zurücksetzen beim Moduswechsel
    for direction in speeds:
        speeds[direction] = 0
    
    # Maustasten loslassen
    pyautogui.mouseUp(button='left')
    pyautogui.mouseUp(button='right')
    
    print(f"\nModus gewechselt: {'MAUS-Modus' if mouse_mode else 'EINGABE-Modus'}")

def exit_program(e):
    """Beendet das Programm sauber"""
    global running
    running = False
    print("\nProgramm wird beendet...")

# Modus-Wechsel-Handler registrieren
keyboard.on_press_key(TOGGLE_MODE, lambda _: toggle_mode())
# ESC-Taste zum Beenden registrieren
keyboard.on_press_key(EXIT_KEY, exit_program)

print(f"Dual-Modus Tastatursteuerung aktiviert:")
print(f"- {TOGGLE_MODE}: Zwischen MAUS-Modus und EINGABE-Modus wechseln")
print(f"- {EXIT_KEY}: Programm beenden")
print(f"- Im MAUS-Modus:")
print(f"  - {MOVE_UP}/{MOVE_DOWN}/{MOVE_LEFT}/{MOVE_RIGHT}: Maus bewegen (WASD)")
print(f"  - {PRECISION}: Präzisionssteuerung (langsamer)")
print(f"  - {LEFT_CLICK}: Linksklick (Komma ,)")
print(f"  - {RIGHT_CLICK}: Rechtsklick (Punkt .)")
print("- Im EINGABE-Modus: Alle Tasten funktionieren normal")
print("\nAktueller Modus: MAUS-Modus")

# Maus-Thread starten
mouse_thread = threading.Thread(target=mouse_mover)
mouse_thread.daemon = True
mouse_thread.start()

try:
    # Hauptschleife
    while running:
        # Nur im Mausmodus Steuerung aktivieren
        if mouse_mode:
            # Shift für Präzision
            slow_mode = keyboard.is_pressed(PRECISION)
            
            # Aufwärtsbewegung (W)
            if keyboard.is_pressed(MOVE_UP):
                if speeds['up'] == 0:  # Anfangsgeschwindigkeit setzen
                    speeds['up'] = MIN_SPEED if slow_mode else STEP_SIZE
                else:  # Beschleunigen
                    if not slow_mode:
                        speeds['up'] = min(speeds['up'] * ACCEL_FACTOR, MAX_SPEED)
                speeds['down'] = 0  # Gegenrichtung stoppen
            else:
                speeds['up'] = 0  # Stoppen wenn Taste losgelassen
                
            # Abwärtsbewegung (S)
            if keyboard.is_pressed(MOVE_DOWN):
                if speeds['down'] == 0:
                    speeds['down'] = MIN_SPEED if slow_mode else STEP_SIZE
                else:
                    if not slow_mode:
                        speeds['down'] = min(speeds['down'] * ACCEL_FACTOR, MAX_SPEED)
                speeds['up'] = 0
            else:
                speeds['down'] = 0
                
            # Linksbewegung (A)
            if keyboard.is_pressed(MOVE_LEFT):
                if speeds['left'] == 0:
                    speeds['left'] = MIN_SPEED if slow_mode else STEP_SIZE
                else:
                    if not slow_mode:
                        speeds['left'] = min(speeds['left'] * ACCEL_FACTOR, MAX_SPEED)
                speeds['right'] = 0
            else:
                speeds['left'] = 0
                
            # Rechtsbewegung (D)
            if keyboard.is_pressed(MOVE_RIGHT):
                if speeds['right'] == 0:
                    speeds['right'] = MIN_SPEED if slow_mode else STEP_SIZE
                else:
                    if not slow_mode:
                        speeds['right'] = min(speeds['right'] * ACCEL_FACTOR, MAX_SPEED)
                speeds['left'] = 0
            else:
                speeds['right'] = 0
                
            # Linksklick
            if keyboard.is_pressed(LEFT_CLICK) and not left_pressed:
                pyautogui.mouseDown(button='left')
                left_pressed = True
            elif not keyboard.is_pressed(LEFT_CLICK) and left_pressed:
                pyautogui.mouseUp(button='left')
                left_pressed = False
                
            # Rechtsklick
            if keyboard.is_pressed(RIGHT_CLICK) and not right_pressed:
                pyautogui.mouseDown(button='right')
                right_pressed = True
            elif not keyboard.is_pressed(RIGHT_CLICK) and right_pressed:
                pyautogui.mouseUp(button='right')
                right_pressed = False
            
        # Kurze Pause für CPU-Entlastung
        time.sleep(0.01)
        
except KeyboardInterrupt:
    running = False
finally:
    # Sauberes Beenden
    running = False
    print("\nProgramm beendet.")
