import random
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Variables globales para la eficiencia de tiro
TWO_SHOT_SUCCESS = 0.50  # Probabilidad inicial para tiro de 2
THREE_SHOT_SUCCESS = 0.35  # Probabilidad inicial para tiro de 3

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

    # Utilizar variables globales para definir la eficiencia de tiro
    success_prob = TWO_SHOT_SUCCESS if shot_type == 2 else THREE_SHOT_SUCCESS
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
        return points, True
    else:
        if shot_made:
            points += shot_type
            offensive.shots_made += 1
            return points, True
        else:
            # Falló sin foul, se intenta obtener un rebote ofensivo
            return 0, False

# Función que simula una posesión completa (incluye turnover, tiros, rebote)
def simulate_possession(offensive, defensive, free_throw_prob=0.80,
                        foul_probability=0.15, turnover_prob=0.15,
                        offensive_rebound_prob=0.30):
    possession_time = random.uniform(8, 24)  # Duración en segundos de la posesión
    points = 0

    # Verificar si ocurre un turnover antes de intentar el tiro
    if random.random() < turnover_prob:
        offensive.turnovers += 1
        if random.random() < 0.66:
            defensive.steals += 1
        return 0, possession_time

    while True:
        shot_points, possession_ends = attempt_shot(offensive, free_throw_prob, foul_probability)
        points += shot_points

        if possession_ends:
            return points, possession_time
        else:
            # Si el tiro falla sin foul, evaluar rebote ofensivo
            if random.random() < offensive_rebound_prob:
                offensive.offensive_rebounds += 1
                possession_time += 5  # Tiempo extra por el rebote
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
        # Alternar la posesión
        possession_team = teamA if possession_team == teamB else teamB

        if current_time >= quarter_duration:
            break

# Función que simula un partido completo (4 cuartos) y retorna los equipos
def simulate_game():
    teamA = Team("Equipo A")
    teamB = Team("Equipo B")
    for _ in range(4):
        simulate_quarter(teamA, teamB, quarter_duration=720)
    return teamA, teamB

# Función para simular múltiples partidos y retornar la distribución del marcador total
def simulate_experiments(num_games):
    total_scores = []
    for _ in range(num_games):
        teamA, teamB = simulate_game()
        combined_score = teamA.score + teamB.score
        total_scores.append(combined_score)
    return total_scores

if __name__ == "__main__":
    num_games = 1000

    # Experimento 1: Baseline (eficiencia de tiro 50% y 35%)
    TWO_SHOT_SUCCESS = 0.50
    THREE_SHOT_SUCCESS = 0.35
    baseline_scores = simulate_experiments(num_games)

    # Experimento 2: Mejora en eficiencia ofensiva (eficiencia de tiro 60% y 40%)
    TWO_SHOT_SUCCESS = 0.60
    THREE_SHOT_SUCCESS = 0.40
    improved_scores = simulate_experiments(num_games)

    # Realizar prueba de hipótesis con test t para comparar medias
    from scipy.stats import ttest_ind
    t_stat, p_val = ttest_ind(improved_scores, baseline_scores)

    print(f"Experimento Baseline: Promedio Marcador = {sum(baseline_scores)/len(baseline_scores):.2f}")
    print(f"Experimento Mejorado: Promedio Marcador = {sum(improved_scores)/len(improved_scores):.2f}")
    print(f"t-statistic = {t_stat:.3f}, p-value = {p_val:.3f}")

    # Graficar las distribuciones del marcador total para ambos experimentos
    plt.figure(figsize=(10,6))
    plt.hist(baseline_scores, bins=30, alpha=0.5, label='Baseline (50/35% Eficiencia)')
    plt.hist(improved_scores, bins=30, alpha=0.5, label='Mejorado (60/40% Eficiencia)')
    plt.xlabel('Marcador Total (suma de puntos de ambos equipos)')
    plt.ylabel('Frecuencia')
    plt.title('Distribución del Marcador Total en 1000 Simulaciones')
    plt.legend()
    plt.show()
