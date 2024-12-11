# Pac-Man
Pac-Man go brrrr wrumm wum
## Grundfunktionen unseres Pac-Man Spiels:
### Spielfeld:
- Wird aus Datei eingelesen.
- 0: Frei, 1: Wand, 2: Münze, 3: Super-Coin, 4: Röhre, 5: Geisterhaus.

### Pac-Man:
- Animiert und drehbar in alle Himmelsrichtungen.
- Stoppt Animation bei Wandkontakt.#needs to bee added

### Geister:
- 2 Geister bewegen sich pro Tick zur nächsten Position in eine Richtung von Pac-Man (keine Umkehr möglich).
- Nach bestimmter Zeit wechseln Geister in Frightened Mode (zufällige Bewegung, können dann gegessen werden).
- Super-Coins lösen auch Frightened Mode aus.
- Geister können umkehren, falls keine andere Richtung möglich ist.

### Röhre:
- Nur Pac-Man nutzbar, teleportiert ihn zur zufälligen anderen Röhre.
- Geister können hineingehen, aber nur Pac-Man wird teleportiert und gedreht.

### Geisterhaus:
- Nur für Geister betretbar (Pac-Man blockiert durch Wand 1 und Geisterhaus 5). 
- Respawn Poin für die Geister

### Collision:
**Pac-Man trifft Geist:**
 - *Frightened Mode aktiv:*
   - Der kollidierte Geist wird ins Geisterhaus teleportiert.
 - *Frightened Mode nicht aktiv:*
   - Pac-Man verliert ein Leben.
   - Beide Geister werden ins Geisterhaus teleportiert.
   - Todesanimation wird abgespielt.
   - Frightened Mode wird aktiviert.
