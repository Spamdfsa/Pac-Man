- Spielfeldgröße kann durch die die Variable "SCALING" in Zeile 401 Skalliert werden
- Es kann ein neues Spielfeld durch verändern der Matrix in der datei "map.json" Initialisiert werden (0 = Weg ohne Münze, 1= Wand, 2 = Weg mit Münze, 3 = große Münze, 4 = Tunnel, 5 = Geisterhaus). Dazu muss eine neue Spielfeld.png bereit gestellt werden, welche gleich zur neuen Matrix ist. 

# Pac-Man
	Pac-Man go brrrr wrumm wum background_video Bilder müssen noch entpackt werden

## Grundfunktionen unseres Pac-Man Spiels:

### Steuerung:
-Pac-Man wird durch WASD oder Pfeiltasten gesteuert
-Im Highscore Menü kommt man durch ESC zurück ins Menü
-ESC schließt das Spiel, wenn man im Menü oder im Spiel ist

### Spielfeld:
- Wird aus Datei eingelesen.
- 0: Frei, 1: Wand, 2: Münze, 3: Super-Coin, 4: Röhre, 5: Geisterhaus.

### Pac-Man:
- Animiert und drehbar in alle Himmelsrichtungen.
- Stoppt bei Wandkontakt

### Geister:
- 2 Geister bewegen sich pro Tick zur nächsten Position in eine Richtung von Pac-Man (keine Umkehr möglich).
- Nach bestimmter Zeit wechseln Geister in Frightened Mode (zufällige Bewegung, können dann gegessen werden).
- Super-Coins lösen auch Frightened Mode aus.
- Geister können umkehren, falls keine andere Richtung möglich ist.

### Röhre:
- Nur für Pac-Man nutzbar, teleportiert ihn zur zufälligen anderen Röhre.
- Geister können hineingehen, aber nur Pac-Man wird teleportiert und gedreht.

### Geisterhaus:
- Nur für Geister betretbar (Pac-Man blockiert durch Wand 1 und Geisterhaus 5). 
- Respawn Point für die Geister

### Collision:
**Pac-Man trifft Geist:**
 - *Frightened Mode aktiv:*
   - Der kollidierte Geist wird ins Geisterhaus teleportiert.
 - *Frightened Mode nicht aktiv:*
   - Pac-Man verliert ein Leben.
   - Beide Geister werden ins Geisterhaus teleportiert.
   - Frightened Mode wird aktiviert.

### Level:
-Nach sammeln aller Münzen wird das Spielfeld zurück gesetz und der Gamespeed erhöht, der Score wirdforgeführt. 

###Highscores:
-Highscores sind in Highscore/highscores.json gespeichert. Highscores können nur durch löschen dieser datei gelöscht werden.
-Stürzt das Spiel beim laden des Highscoremenüs ab, ist highscores.json zu löschen.

###Cheats:
-Pos1 versetz einen in das nächste Level
