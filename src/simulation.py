import random
import matplotlib.pyplot as plt
from scipy.stats import linregress

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
        self.posesions = 0  # opcional, para contar posesiones asignadas

# Función para simular tiros libres
def simulate_free_throws(num_shots, free_throw_prob):
    points = 0
    made = 0
    for _ in range(num_shots):
        if random.random() < free_throw_prob:
            points += 1
            made += 1
    return points, made

# Función que simula un intento de tiro (incluye posibilidad de foul y tiros libres)
def attempt_shot(offensive, free_throw_prob, foul_probability):
    # Decisión aleatoria del tipo de tiro: 2 puntos (2/3) o 3 puntos (1/3)
    shot_type = 2 if random.random() < (2/3) else 3
    offensive.shot_attempts += 1
    
    foul = random.random() < foul_probability  # Existe foul en 15%
    
    # Probabilidad de acierto: 60% para 2 puntos y 40% para 3 puntos (según parámetro modificado)
    success_prob = 0.60 if shot_type == 2 else 0.40
    shot_made = (random.random() < success_prob)
    
    points = 0
    if foul:
        if shot_made:
            # Tiro anotado + "and one" (tiro libre adicional)
            points += shot_type
            offensive.shots_made += 1
            offensive.free_throw_attempts += 1
            if random.random() < free_throw_prob:
                points += 1
                offensive.free_throws_made += 1
        else:
            # Tiro fallado con foul: se otorgan tiros libres según el valor del tiro (2 o 3)
            num_ft = shot_type
            offensive.free_throw_attempts += num_ft
            ft_points, ft_made = simulate_free_throws(num_ft, free_throw_prob)
            points += ft_points
            offensive.free_throws_made += ft_made
        return points, True   # Posesión termina tras tiros libres
    else:
        if shot_made:
            points += shot_type
            offensive.shots_made += 1
            return points, True  # Posesión termina al anotar
        else:
            # Fallo sin foul, se intenta conseguir un rebote ofensivo
            return 0, False

# Función que simula una posesión completa (incluye turnover, tiros, rebote)
def simulate_possession(offensive, defensive, free_throw_prob=0.80,
                        foul_probability=0.15, turnover_prob=0.10, # cambio de turnover 0.15 a 0.10
                        offensive_rebound_prob=0.30):
    possession_time = random.uniform(8, 24)  # Tiempo base en segundos
    points = 0
    
    # Se verifica si ocurre un turnover antes de iniciar el tiro
    if random.random() < turnover_prob:
        offensive.turnovers += 1
        if random.random() < 0.66:  # 66% de los turnovers se registran como robo para la defensa
            defensive.steals += 1
        return 0, possession_time

    # Comienza la posesión: se intenta un tiro, pudiendo darse foul y posibilidad de rebote ofensivo
    while True:
        shot_points, possession_ends = attempt_shot(offensive, free_throw_prob, foul_probability)
        points += shot_points
        
        if possession_ends:
            return points, possession_time
        else:
            # Tiro fallado sin foul, se evalúa la posibilidad de rebote ofensivo
            if random.random() < offensive_rebound_prob:
                offensive.offensive_rebounds += 1
                possession_time += 5  # Se añade tiempo extra por el proceso del rebote ofensivo
                continue  # Se reintenta el tiro en la misma posesión
            else:
                defensive.defensive_rebounds += 1
                return points, possession_time

# Función que simula un cuarto de 12 minutos (720 segundos)
def simulate_quarter(teamA, teamB, quarter_duration=720):
    current_time = 0
    # Asignar aleatoriamente quién inicia la posesión
    possession_team = teamA if random.random() < 0.5 else teamB
    quarter_possessions = 0  # contador de posesiones en el cuarto
    
    while current_time < quarter_duration:
        quarter_possessions += 1
        if possession_team == teamA:
            pts, pos_time = simulate_possession(teamA, teamB)
            teamA.score += pts
        else:
            pts, pos_time = simulate_possession(teamB, teamA)
            teamB.score += pts

        current_time += pos_time
        
        # Alternar posesión al finalizar la posesión actual
        possession_team = teamA if possession_team == teamB else teamB
        
        if current_time >= quarter_duration:
            break
    return quarter_possessions

# Función que simula un partido completo (4 cuartos) y retorna estadísticas
def simulate_game():
    teamA = Team("Equipo A")
    teamB = Team("Equipo B")
    total_possessions = 0
    # Simular 4 cuartos
    for _ in range(4):
        total_possessions += simulate_quarter(teamA, teamB, quarter_duration=720)
    
    # Para este análisis, usamos el total de posesiones del partido
    return teamA, teamB, total_possessions

# Función para simular múltiples partidos y recolectar datos (posesiones totales y marcador final combinado)
def simulate_multiple_games(n):
    possessions_list = []
    total_scores = []
    
    for _ in range(n):
        teamA, teamB, total_possessions = simulate_game()
        # Sumamos el marcador de ambos equipos para tener el marcador total combinado
        combined_score = teamA.score + teamB.score
        possessions_list.append(total_possessions)
        total_scores.append(combined_score)
    
    return possessions_list, total_scores

# Simular 1000 partidos y obtener datos
num_simulations = 1000
posesiones_list, scores_list = simulate_multiple_games(num_simulations)

# Análisis de la relación: calculamos la regresión lineal
slope, intercept, r_value, p_value, std_err = linregress(posesiones_list, scores_list)
print("Regresión Lineal: Marcador Total = {:.2f} * Posesiones + {:.2f}".format(slope, intercept))
print("Coeficiente de correlación (R): {:.2f}".format(r_value))

# Graficar los datos obtenidos y la línea de regresión
plt.figure(figsize=(8, 6))
plt.scatter(posesiones_list, scores_list, alpha=0.5, label="Datos simulados")
# Ordenamos las posesiones para graficar la línea de regresión
posesiones_sorted = sorted(posesiones_list)
plt.plot(posesiones_sorted, [slope * x + intercept for x in posesiones_sorted],
         color='red', label="Línea de regresión")
plt.xlabel("Número total de Posesiones")
plt.ylabel("Marcador Final (combinado)")
plt.title("Relación entre Número de Posesiones y Marcador Final")
plt.legend()
plt.show()
