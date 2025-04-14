import random
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Variables globales para la eficiencia de tiro (se mantienen iguales en ambos experimentos)
TWO_SHOT_SUCCESS = 0.50  # Probabilidad para tiro de 2 (baseline)
THREE_SHOT_SUCCESS = 0.35  # Probabilidad para tiro de 3 (baseline)

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

    # Utiliza las variables globales para definir la eficiencia de tiro (baseline)
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
            # Falló sin foul, se intentará obtener un rebote ofensivo
            return 0, False

# Función que simula una posesión completa (incluye turnover, tiro, y posibilidad de rebote ofensivo)
def simulate_possession(offensive, defensive, free_throw_prob=0.80,
                        foul_probability=0.15, turnover_prob=0.15,
                        offensive_rebound_prob=0.30):
    possession_time = random.uniform(8, 24)  # Duración base de la posesión en segundos
    points = 0

    # Verificar si ocurre un turnover antes de intentar el tiro
    if random.random() < turnover_prob:
        offensive.turnovers += 1
        if random.random() < 0.66:  # 66% de los turnovers se registran como robo para el adversario
            defensive.steals += 1
        return 0, possession_time

    # Inicia la posesión
    while True:
        shot_points, possession_ends = attempt_shot(offensive, free_throw_prob, foul_probability)
        points += shot_points

        if possession_ends:
            return points, possession_time
        else:
            # Si falla sin foul, se evalúa si se consigue un rebote ofensivo
            if random.random() < offensive_rebound_prob:
                offensive.offensive_rebounds += 1
                possession_time += 5  # Se añade tiempo extra por el proceso del rebote
                # Se vuelve a intentar el tiro en la misma posesión
                continue
            else:
                defensive.defensive_rebounds += 1
                return points, possession_time

# Función que simula un cuarto de 12 minutos (720 segundos) con un parámetro custom para rebotes ofensivos
def simulate_quarter_custom(teamA, teamB, quarter_duration=720, offensive_rebound_prob=0.30):
    current_time = 0
    possession_team = teamA if random.random() < 0.5 else teamB

    while current_time < quarter_duration:
        if possession_team == teamA:
            pts, pos_time = simulate_possession(teamA, teamB, free_throw_prob=0.80,
                                                 foul_probability=0.15, turnover_prob=0.15,
                                                 offensive_rebound_prob=offensive_rebound_prob)
            teamA.score += pts
        else:
            pts, pos_time = simulate_possession(teamB, teamA, free_throw_prob=0.80,
                                                 foul_probability=0.15, turnover_prob=0.15,
                                                 offensive_rebound_prob=offensive_rebound_prob)
            teamB.score += pts

        current_time += pos_time
        possession_team = teamA if possession_team == teamB else teamB

        if current_time >= quarter_duration:
            break

# Función que simula un partido completo (4 cuartos) con custom offensive rebound probability
def simulate_game_custom(offensive_rebound_prob=0.30):
    teamA = Team("Equipo A")
    teamB = Team("Equipo B")
    for _ in range(4):
        simulate_quarter_custom(teamA, teamB, quarter_duration=720,
                                offensive_rebound_prob=offensive_rebound_prob)
    return teamA, teamB

# Función para simular múltiples partidos y retornar la distribución del marcador total, usando el valor custom de rebote ofensivo
def simulate_experiments_custom(num_games, offensive_rebound_prob):
    total_scores = []
    for _ in range(num_games):
        teamA, teamB = simulate_game_custom(offensive_rebound_prob=offensive_rebound_prob)
        combined_score = teamA.score + teamB.score
        total_scores.append(combined_score)
    return total_scores

if __name__ == "__main__":
    num_games = 1000

    # Experimento A: Baseline, probabilidad de rebote ofensivo = 0.30
    baseline_rebound = 0.30
    scores_baseline = simulate_experiments_custom(num_games, offensive_rebound_prob=baseline_rebound)

    # Experimento B: Mejorado, probabilidad de rebote ofensivo = 0.50
    improved_rebound = 0.50
    scores_improved = simulate_experiments_custom(num_games, offensive_rebound_prob=improved_rebound)

    # Calcular promedios
    avg_baseline = sum(scores_baseline) / len(scores_baseline)
    avg_improved = sum(scores_improved) / len(scores_improved)

    print(f"Experimento Baseline (Rebote Ofensivo = {baseline_rebound}): Promedio Marcador = {avg_baseline:.2f}")
    print(f"Experimento Mejorado (Rebote Ofensivo = {improved_rebound}): Promedio Marcador = {avg_improved:.2f}")

    # Prueba t para comparar las medias
    from scipy.stats import ttest_ind
    t_stat, p_val = ttest_ind(scores_improved, scores_baseline)
    print(f"t-statistic = {t_stat:.3f}, p-value = {p_val:.3f}")

    # Graficar las distribuciones del marcador total para ambos experimentos
    plt.figure(figsize=(10,6))
    plt.hist(scores_baseline, bins=30, alpha=0.5, label=f'Baseline (Rebote = {baseline_rebound})')
    plt.hist(scores_improved, bins=30, alpha=0.5, label=f'Mejorado (Rebote = {improved_rebound})')
    plt.xlabel('Marcador Total (suma de puntos de ambos equipos)')
    plt.ylabel('Frecuencia')
    plt.title('Distribución del Marcador Total - Variación en Probabilidad de Rebote Ofensivo')
    plt.legend()
    plt.show()
