import random

# Definición de la clase para representar a un equipo
class Team:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turnovers = 0
        self.steals = 0
        self.offensive_rebounds = 0
        self.defensive_rebounds = 0
        self.shot_attempts = 0
        self.shots_made = 0
        self.free_throw_attempts = 0
        self.free_throws_made = 0

# Función para simular tiros libres
def simulate_free_throws(num_shots, free_throw_prob):
    points = 0
    made = 0
    for _ in range(num_shots):
        if random.random() < free_throw_prob:
            points += 1
            made += 1
    return points, made, num_shots

# Función que simula un intento de tiro (incluye posibilidad de foul y tiros libres)
def attempt_shot(offensive, free_throw_prob, foul_probability):
    # Determinar el tipo de tiro: 2 puntos (2/3 de prob) o 3 puntos (1/3 de prob)
    shot_type = 2 if random.random() < (2/3) else 3
    offensive.shot_attempts += 1

    # Probabilidad de foul
    foul = random.random() < foul_probability

    # Probabilidad de acierto (usar valores medios: 50% para 2, 35% para 3)
    success_prob = 0.50 if shot_type == 2 else 0.35
    shot_made = (random.random() < success_prob)

    points = 0
    # En caso de foul:
    if foul:
        if shot_made:
            # Tiro anotado + "and one" (1 tiro libre)
            points += shot_type
            offensive.shots_made += 1
            offensive.free_throw_attempts += 1
            if random.random() < free_throw_prob:
                points += 1
                offensive.free_throws_made += 1
        else:
            # Tiro fallado: se otorgan tiros libres equivalentes (2 o 3)
            num_ft = shot_type
            offensive.free_throw_attempts += num_ft
            ft_points, ft_made, _ = simulate_free_throws(num_ft, free_throw_prob)
            points += ft_points
            offensive.free_throws_made += ft_made
        # Tras tiros libres, la posesión termina
        return points, True  # True indica que la posesión termina
    else:
        # Sin foul
        if shot_made:
            points += shot_type
            offensive.shots_made += 1
            return points, True  # Posesión termina si anota
        else:
            # Tiro fallado sin foul: posibilidad de rebote ofensivo
            return 0, False  # False indica que la posesión podría continuar por ofensivo

# Función que simula una posesión completa, considerando turnovers, tiros, y rebotes ofensivos
def simulate_possession(offensive, defensive, free_throw_prob=0.80, foul_probability=0.15,
                        turnover_prob=0.15, offensive_rebound_prob=0.30):
    possession_time = random.uniform(8, 24)  # Duración base de la posesión (en segundos)
    points = 0

    # Verificar si ocurre un turnover antes de intentar tiro
    if random.random() < turnover_prob:
        offensive.turnovers += 1
        # Determinar si es robo (steal) para el otro equipo (66% de los turnovers)
        if random.random() < 0.66:
            defensive.steals += 1
        return 0, possession_time

    # Se inicia la secuencia de tiro dentro de la posesión
    while True:
        shot_points, possession_ends = attempt_shot(offensive, free_throw_prob, foul_probability)
        points += shot_points

        if possession_ends:
            # La posesión finaliza por tiro anotado o tras tiros libres
            return points, possession_time
        else:
            # Tiro fallado sin foul: se verifica si se obtiene rebote ofensivo
            if random.random() < offensive_rebound_prob:
                offensive.offensive_rebounds += 1
                # Se añade tiempo por el proceso del rebote ofensivo (por ejemplo, 5 segundos)
                possession_time += 5
                # Se vuelve a intentar un tiro en la misma posesión
                continue
            else:
                # Sin rebote ofensivo, se registra un rebote defensivo para el otro equipo
                defensive.defensive_rebounds += 1
                return points, possession_time

# Función para simular un cuarto de 12 minutos (720 segundos)
def simulate_quarter(teamA, teamB, quarter_num, quarter_duration=720):
    current_time = 0
    # Se asigna aleatoriamente qué equipo inicia la posesión
    possession_team = teamA if random.random() < 0.5 else teamB
    
    while current_time < quarter_duration:
        if possession_team == teamA:
            pts, pos_time = simulate_possession(teamA, teamB)
            teamA.score += pts
        else:
            pts, pos_time = simulate_possession(teamB, teamA)
            teamB.score += pts

        current_time += pos_time

        # Alternar la posesión al final de cada posesión
        possession_team = teamA if possession_team == teamB else teamB

        # Si se excede el tiempo del cuarto, se termina la simulación del cuarto
        if current_time >= quarter_duration:
            break

# Función principal para simular el partido completo
def simulate_game():
    teamA = Team("Equipo A")
    teamB = Team("Equipo B")

    print("Simulación del partido de baloncesto\n")
    for quarter in range(1, 5):
        simulate_quarter(teamA, teamB, quarter, quarter_duration=720)
        print(f"Después del Q{quarter}: {teamA.name} {teamA.score} - {teamB.score} {teamB.name}\n")

    print("Resultado Final:")
    print(f"{teamA.name}: {teamA.score} puntos")
    print(f"{teamB.name}: {teamB.score} puntos\n")
    
    # Estadísticas adicionales
    print("Estadísticas:")
    for team in [teamA, teamB]:
        print(f"--- {team.name} ---")
        print(f"Tiros intentados: {team.shot_attempts}, Tiros convertidos: {team.shots_made}")
        print(f"Tiros libres: {team.free_throw_attempts} intentados, {team.free_throws_made} convertidos")
        print(f"Turnovers: {team.turnovers}")
        print(f"Robos: {team.steals}")
        print(f"Rebotes Ofensivos: {team.offensive_rebounds}")
        print(f"Rebotes Defensivos: {team.defensive_rebounds}")
        print()

if __name__ == "__main__":
    simulate_game()
