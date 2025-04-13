import random

# Clase para representar a un equipo y almacenar estadísticas
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
    # Decisión aleatoria del tipo de tiro: 2 puntos (2/3) o 3 puntos (1/3)
    shot_type = 2 if random.random() < (2/3) else 3
    offensive.shot_attempts += 1

    # Determinar si ocurre foul (15% de probabilidad)
    foul = random.random() < foul_probability

    # Probabilidad de acierto: 50% para tiro de 2, 35% para tiro de 3
    success_prob = 0.50 if shot_type == 2 else 0.35
    shot_made = (random.random() < success_prob)

    points = 0
    if foul:
        if shot_made:
            # Tiro exitoso + "and one": se otorga tiro libre
            points += shot_type
            offensive.shots_made += 1
            offensive.free_throw_attempts += 1
            if random.random() < free_throw_prob:
                points += 1
                offensive.free_throws_made += 1
        else:
            # Tiro fallado con foul: se otorgan tiros libres según el valor del tiro
            num_ft = shot_type
            offensive.free_throw_attempts += num_ft
            ft_points, ft_made, _ = simulate_free_throws(num_ft, free_throw_prob)
            points += ft_points
            offensive.free_throws_made += ft_made
        # Después de tiros libres, la posesión termina
        return points, True
    else:
        if shot_made:
            points += shot_type
            offensive.shots_made += 1
            return points, True
        else:
            # Falló sin foul, se puede intentar obtener un rebote ofensivo
            return 0, False

# Función que simula una posesión completa (incluye turnover, tiros, rebote)
def simulate_possession(offensive, defensive, free_throw_prob=0.80,
                        foul_probability=0.15, turnover_prob=0.15,
                        offensive_rebound_prob=0.30):
    possession_time = random.uniform(8, 24)  # Duración base en segundos de la posesión
    points = 0

    # Verificar si ocurre un turnover antes de intentar el tiro
    if random.random() < turnover_prob:
        offensive.turnovers += 1
        # 66% de los turnovers son robos para el adversario
        if random.random() < 0.66:
            defensive.steals += 1
        return 0, possession_time

    # Se inicia la posesión: intento de tiro (puede incluir foul)
    while True:
        shot_points, possession_ends = attempt_shot(offensive, free_throw_prob, foul_probability)
        points += shot_points

        if possession_ends:
            return points, possession_time
        else:
            # Fallo sin foul: se evalúa la posibilidad de rebote ofensivo
            if random.random() < offensive_rebound_prob:
                offensive.offensive_rebounds += 1
                possession_time += 5  # Se añade tiempo extra por el rebote
                # Se vuelve a intentar el tiro en la misma posesión
                continue
            else:
                defensive.defensive_rebounds += 1
                return points, possession_time

# Función que simula un cuarto de 12 minutos (720 segundos)
def simulate_quarter(teamA, teamB, quarter_duration=720):
    current_time = 0
    # Asignar aleatoriamente qué equipo inicia la posesión
    possession_team = teamA if random.random() < 0.5 else teamB
    
    while current_time < quarter_duration:
        if possession_team == teamA:
            pts, pos_time = simulate_possession(teamA, teamB)
            teamA.score += pts
        else:
            pts, pos_time = simulate_possession(teamB, teamA)
            teamB.score += pts

        current_time += pos_time
        # Alternar la posesión al finalizar cada posesión
        possession_team = teamA if possession_team == teamB else teamB

        if current_time >= quarter_duration:
            break

# Función que simula un partido completo (4 cuartos) y retorna los equipos con sus estadísticas
def simulate_game():
    teamA = Team("Equipo A")
    teamB = Team("Equipo B")
    for _ in range(4):
        simulate_quarter(teamA, teamB, quarter_duration=720)
    return teamA, teamB

# Función para simular múltiples partidos y acumular estadísticas
def simulate_multiple_games(n):
    # Diccionarios para acumular estadísticas de cada equipo
    totalsA = {
        'score': 0,
        'shot_attempts': 0,
        'shots_made': 0,
        'free_throw_attempts': 0,
        'free_throws_made': 0,
        'turnovers': 0,
        'steals': 0,
        'offensive_rebounds': 0,
        'defensive_rebounds': 0
    }
    totalsB = {
        'score': 0,
        'shot_attempts': 0,
        'shots_made': 0,
        'free_throw_attempts': 0,
        'free_throws_made': 0,
        'turnovers': 0,
        'steals': 0,
        'offensive_rebounds': 0,
        'defensive_rebounds': 0
    }
    winsA = 0
    winsB = 0

    for _ in range(n):
        teamA, teamB = simulate_game()

        totalsA['score'] += teamA.score
        totalsA['shot_attempts'] += teamA.shot_attempts
        totalsA['shots_made'] += teamA.shots_made
        totalsA['free_throw_attempts'] += teamA.free_throw_attempts
        totalsA['free_throws_made'] += teamA.free_throws_made
        totalsA['turnovers'] += teamA.turnovers
        totalsA['steals'] += teamA.steals
        totalsA['offensive_rebounds'] += teamA.offensive_rebounds
        totalsA['defensive_rebounds'] += teamA.defensive_rebounds

        totalsB['score'] += teamB.score
        totalsB['shot_attempts'] += teamB.shot_attempts
        totalsB['shots_made'] += teamB.shots_made
        totalsB['free_throw_attempts'] += teamB.free_throw_attempts
        totalsB['free_throws_made'] += teamB.free_throws_made
        totalsB['turnovers'] += teamB.turnovers
        totalsB['steals'] += teamB.steals
        totalsB['offensive_rebounds'] += teamB.offensive_rebounds
        totalsB['defensive_rebounds'] += teamB.defensive_rebounds

        if teamA.score > teamB.score:
            winsA += 1
        elif teamB.score > teamA.score:
            winsB += 1

    # Calcular los promedios de cada estadística
    averagesA = {k: v/n for k, v in totalsA.items()}
    averagesB = {k: v/n for k, v in totalsB.items()}
    win_rateA = winsA / n * 100
    win_rateB = winsB / n * 100

    return averagesA, averagesB, win_rateA, win_rateB

# Simulación de 1000 partidos y presentación de promedios
if __name__ == "__main__":
    num_games = 1000
    averagesA, averagesB, win_rateA, win_rateB = simulate_multiple_games(num_games)

    print(f"Simulación de {num_games} partidos\n")

    print("Equipo A - Promedios:")
    print(f"Puntos: {averagesA['score']:.2f}")
    print(f"Intentos de tiro: {averagesA['shot_attempts']:.2f}")
    print(f"Tiros convertidos: {averagesA['shots_made']:.2f}")
    print(f"Intentos de tiros libres: {averagesA['free_throw_attempts']:.2f}")
    print(f"Tiros libres convertidos: {averagesA['free_throws_made']:.2f}")
    print(f"Turnovers: {averagesA['turnovers']:.2f}")
    print(f"Robos: {averagesA['steals']:.2f}")
    print(f"Rebotes ofensivos: {averagesA['offensive_rebounds']:.2f}")
    print(f"Rebotes defensivos: {averagesA['defensive_rebounds']:.2f}")
    print(f"Tasa de victorias: {win_rateA:.2f}%\n")

    print("Equipo B - Promedios:")
    print(f"Puntos: {averagesB['score']:.2f}")
    print(f"Intentos de tiro: {averagesB['shot_attempts']:.2f}")
    print(f"Tiros convertidos: {averagesB['shots_made']:.2f}")
    print(f"Intentos de tiros libres: {averagesB['free_throw_attempts']:.2f}")
    print(f"Tiros libres convertidos: {averagesB['free_throws_made']:.2f}")
    print(f"Turnovers: {averagesB['turnovers']:.2f}")
    print(f"Robos: {averagesB['steals']:.2f}")
    print(f"Rebotes ofensivos: {averagesB['offensive_rebounds']:.2f}")
    print(f"Rebotes defensivos: {averagesB['defensive_rebounds']:.2f}")
    print(f"Tasa de victorias: {win_rateB:.2f}%")
