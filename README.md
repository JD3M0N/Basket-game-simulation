# Basket-game-simulation

A continuación se presenta una revisión extensa y detallada de todo lo analizado, estructurada según los apartados solicitados. Esta revisión integra la definición del problema, la implementación del modelo, los experimentos y los resultados, y concluye con las principales lecciones extraídas del proyecto de simulación del partido de baloncesto.

---

# S1. Introducción

## Breve Descripción del Proyecto
El proyecto consiste en el desarrollo de un simulador de eventos discretos aplicado a un partido de baloncesto. La simulación se implementa en Python y modela el comportamiento de un encuentro deportivo dividiendo el juego en posesiones, donde se simulan eventos tales como intentos de tiro, conversiones, tiros libres, faltas, turnovers, robos y rebotes. Se utiliza el marco temporal de cuatro cuartos de 12 minutos cada uno, permitiendo investigar el impacto de diversas variables en el marcador final.

## Objetivos y Metas
El objetivo principal es analizar y entender cómo influyen ciertos factores—principalmente la eficiencia ofensiva, la defensa y la dinámica de posesiones—en el resultado final del partido. De manera específica, se plantean las siguientes metas:
- **Determinar la influencia de la eficiencia en los tiros** (por ejemplo, incrementando la probabilidad de convertir tiros de 2 puntos de 50% a 60% y tiros de 3 puntos de 35% a 40%) sobre el marcador total.
- **Estudiar el impacto de la mejora defensiva** mediante la reducción de la probabilidad de turnovers (de 15% a 10%) y sus consecuencias en el ritmo del juego.
- **Investigar la relación entre el número total de posesiones y el marcador final,** de manera que se pueda establecer si el marcador es proporcional al número de posesiones y, en ese contexto, estimar el promedio de puntos por posesión (PPP).
- **Realizar un análisis estadístico extenso** mediante la simulación de 1000 partidos, para cuantificar promedios y correlaciones que permitan validar la robustez del modelo.

## El Sistema Específico a Simular y las Variables de Interés
El sistema a simular es un partido de baloncesto, considerado como una serie de posesiones discretas, con cada posesión modelada como una unidad que abarca un intento de tiro (incluyendo la posibilidad de foul, tiro libre, rebote ofensivo o defensivo, y turnover). Las variables de interés incluyen:
- **Tiempo de juego:** 4 cuartos de 12 minutos cada uno (720 segundos por cuarto).
- **Número de posesiones:** Aproximadamente entre 90 y 120 por equipo por partido, con el total ajustado en la simulación según la duración de cada posesión.
- **Eficiencia de tiro:** Porcentajes de acierto para tiros de 2 puntos y 3 puntos (inicialmente 50% y 35%, modificados en experimentos a 60% y 40% respectivamente), además del porcentaje de acierto en tiros libres (80% en promedio).
- **Eventos defensivos:** Probabilidades de turnovers, robos, y la distribución de rebotes (ofensivos y defensivos).
- **Otros eventos:** La ocurrencia de foul y la derivación de tiros libres (con “and one” en caso de acierto y foul, o tiros libres equivalentes en caso de fallo).

## Variables que Describen el Problema
Entre las variables que describen el problema se incluyen:
- **Número total de posesiones por partido.**
- **Puntos por posesión (PPP):** Relaciona la eficiencia ofensiva con el marcador final.
- **Tasas de conversión:** Porcentaje de tiros convertidos, tanto de 2 como de 3 puntos, y tiros libres.
- **Errores y oportunidades:** Turnovers y robos, que afectan la transición y el ritmo del juego.
- **Rebotes:** Distribución entre ofensivos y defensivos, que influyen en el número de posesiones efectivas.

---

# S2. Detalles de Implementación

A continuación se exponen los pasos seguidos para la implementación del modelo, junto con una descripción detallada de cada etapa.

## 2.1. Definición del Problema y los Objetivos
El primer paso fue articular claramente el problema: simular un partido de baloncesto para entender cómo afectan la eficiencia de tiro, la defensa y la dinámica de posesiones el marcador final. Los objetivos se definieron de manera SMART (específicos, medibles, alcanzables, relevantes y con plazos definidos):
- **Específico:** Estudiar la relación entre posesiones y marcador, y cómo varían estos indicadores con ajustes en las probabilidades de acierto y turnovers.
- **Medible:** A través de estadísticas obtenidas en 1000 partidos simulados (por ejemplo, puntos promedio, intentos de tiro, etc.).
- **Alcanzable:** Utilizando datos realistas y parámetros basados en información empírica.
- **Relevante:** Permitir tomar decisiones informadas sobre la influencia de ciertos parámetros en el resultado del juego.
- **Plazo:** Definido en el contexto académico del proyecto.

Además, se delimitaron las fronteras del sistema: se modelaron únicamente las posesiones y eventos clave (tiros, foul, tiros libres, turnover, rebotes) a nivel de equipo, sin incluir dinámicas individuales ni estrategias complejas.

## 2.2. Identificación y Recolección de Datos
Se determinó la información necesaria para alimentar el modelo:
- **Datos de juego:** Duración (4 cuartos de 12 minutos) y número aproximado de posesiones.
- **Estadísticas ofensivas:** Porcentajes de acierto para tiros de 2 y 3 puntos, distribución de intentos (2/3 tiros de 2, 1/3 tiros de 3) y porcentaje de aciertos en tiros libres.
- **Datos defensivos:** Número de turnovers (ajustado en experimentos de 15% a 10%), robos (probabilidad de 66% en turnovers que se convierten en robo, y eventualmente modificados) y rebotes.
- **Fuentes y suposiciones:** Se usaron datos empíricos y supuestos basados en la literatura y observación en competiciones reales, ajustándolos a distribuciones de probabilidad (por ejemplo, modelo Bernoulli para cada tiro).

## 2.3. Construcción del Modelo Conceptual
Se desarrolló un modelo conceptual que permitiera visualizar la secuencia de eventos durante un partido:
- **Diagrama de flujo:** El proceso inicia al comienzo del partido, dividendo el juego en 4 cuartos. Cada cuarto se ejecuta en función de un reloj virtual (720 segundos). En cada posesión se determina aleatoriamente qué equipo tiene el balón; se simula un intento de tiro con sus posibles resultados (acierto, fallo, foul) y se considera la posibilidad de turnovers y rebotes. Cada posesión actualiza el marcador y afecta la transición de la posesión.
- **Documentación de supuestos:** Se asumió la independencia de cada posesión (aunque en la realidad pueden existir efectos de racha) y se modelaron las decisiones (tipo de tiro, ocurrencia de foul, obtención de rebote) mediante probabilidades fijas.

## 2.4. Traducción del Modelo a Código/Software
El modelo conceptual se tradujo en código Python:
- **Definición de Clases y Funciones:** Se creó la clase `Team` para almacenar estadísticas y funciones específicas como `attempt_shot`, `simulate_possession` y `simulate_quarter`.
- **Implementación de la Lógica:** Cada función representa un componente del diagrama de flujo. Por ejemplo, `simulate_possession` integra la lógica de tiro, foul, turnovers y rebotes, mientras que `simulate_quarter` gestiona el flujo de un cuarto completo.
- **Integración Modular:** El código se organizó en módulos para facilitar su lectura, depuración y extensión futura.

## 2.5. Verificación y Validación
- **Verificación:** Se realizaron pruebas unitarias de las funciones individuales para asegurarse de que se comportasen como se esperaba. Por ejemplo, se verificó que la función `simulate_possession` devolviera un número razonable de puntos y tiempo de posesión.
- **Validación:** Se compararon los resultados simulados (como promedio de puntos, intentos de tiro y turnovers) con rangos y estadísticas empíricas conocidas del baloncesto. Además, se analizaron los parámetros de la regresión lineal (por ejemplo, la pendiente que representa los puntos por posesión) para confirmar la coherencia del modelo.

## 2.6. Experimentación y Análisis
- **Simulaciones Extensas:** Se ejecutaron 1000 partidos para obtener promedios robustos y analizar la variabilidad de las estadísticas.
- **Análisis de Sensibilidad:** Se modificaron parámetros clave (por ejemplo, incrementos en la eficiencia de tiro y reducción de turnovers) y se observaron los efectos en el marcador final, distribución de posesiones y otras métricas.
- **Análisis de Regresión:** Se realizó un estudio de regresión lineal para explorar la relación entre el número de posesiones y el marcador final. La línea de regresión obtenida permitió estimar el PPP (puntos por posesión) y el coeficiente de correlación, evidenciando la relación (aunque moderada) entre ambas variables.

## 2.7. Documentación y Elaboración de Informes
Todos los pasos, desde la definición del problema hasta la experimentación, fueron documentados cuidadosamente:
- **Reporte Técnico:** Se preparó un informe que detalla la metodología, la implementación, los experimentos realizados y el análisis estadístico.
- **Código y Comentarios:** El código fuente incluyó comentarios detallados que explican la lógica, las funciones y los parámetros ajustables, facilitando futuras revisiones o mejoras.
- **Presentación de Resultados:** Se generaron gráficos (por ejemplo, la dispersión del número de posesiones vs. el marcador final y la línea de regresión) para apoyar visualmente los hallazgos.

---

# S3. Resultados y Experimentos

## Hallazgos de la Simulación
- **Eficiencia Ofensiva y Marcador:**  
  Cuando se incrementó la eficiencia de tiro (a 60% para tiros de 2 puntos y 40% para tiros de 3 puntos), los promedios de puntos aumentaron significativamente en comparación con parámetros iniciales más conservadores.
- **Impacto de los Turnovers:**  
  La reducción del porcentaje de turnovers de 15% a 10% se tradujo en un menor número de errores (alrededor de 8.6–8.8 turnovers por partido) y, como consecuencia, un ajuste en el ritmo del juego, con un marcador final combinado alrededor de 112 puntos para cada equipo.
- **Relación entre Posesiones y Marcador Final:**  
  El análisis de regresión lineal entre el número total de posesiones y el marcador final combinado produjo la ecuación:
  
  > **Marcador Total = 1.23 × Posesiones + 34.18**
  
  Con un coeficiente de correlación (R) de 0.30. Esto indica que, en promedio, cada posesión adicional se asocia a 1.23 puntos más, si bien la variabilidad es alta, lo que sugiere que otros factores influyen en el resultado.

## Interpretación de los Resultados
- **Influencias Directas:**  
  La eficiencia ofensiva es un determinante clave del marcador. Al mejorar la tasa de conversión, se incrementa el puntaje, lo que es congruente con la hipótesis de que el marcador final es producto del número de posesiones multiplicado por la eficiencia (PPP).
- **Impacto de la Defensa:**  
  La reducción en los turnovers no sólo disminuye la cantidad de errores ofensivos, sino que también afecta la cantidad de oportunidades defensivas (robos y rebotes). Esto se traduce en posesiones más prolongadas y, en consecuencia, en una leve reducción del puntaje global.
- **Relación Posesiones vs. Marcador:**  
  Aunque se observa una tendencia lineal (con una pendiente que se interpreta como PPP), el coeficiente de correlación de 0.30 indica que el número de posesiones por sí solo no explica completamente la variación en el marcador final. La eficiencia en cada posesión, junto con la interacción de otros eventos (fouls, rebotes, etc.), agrega una complejidad importante al sistema.

## Hipótesis Extraídas de los Resultados
- **Hipótesis 1:** La eficiencia ofensiva, medida en puntos por posesión, es directamente proporcional al marcador final, siempre y cuando se mantenga constante el número de posesiones.
- **Hipótesis 2:** La reducción de turnovers genera un control del balón más eficiente, lo cual se traduce en un ritmo de juego menor y en un marcador final levemente inferior, al disminuirse las oportunidades de contraataque.
- **Hipótesis 3:** Aunque existe una relación positiva entre el número de posesiones y el marcador final, la variabilidad en la eficiencia de cada posesión (debida a factores como la posibilidad de foul, rebotes y tiros libres) agrega ruido al modelo, explicando la moderada correlación obtenida.

## Experimentos Realizados para Validar las Hipótesis
- **Variación de la Eficiencia de Tiro:**  
  Se realizaron simulaciones modificando las probabilidades de acierto de tiros de 2 y 3 puntos, observándose incrementos significativos en el puntaje.
- **Modificación de la Probabilidad de Turnovers:**  
  Cambiar la tasa de turnover de 15% a 10% mostró una disminución en los errores, alterando el número de posesiones y repercutiendo en la distribución de rebotes y el marcador final.
- **Análisis de Regresión:**  
  La relación entre el número de posesiones y el marcador final se evaluó mediante regresión lineal, permitiendo extraer un PPP promedio, aunque con una correlación moderada (R=0.30). Esto respalda la idea de que el marcador es el producto del número de posesiones por la eficiencia en cada una, pero que existen múltiples fuentes de variabilidad.

## Necesidad de Análisis Estadístico
El análisis estadístico es fundamental para:
- **Cuantificar la Relación:** Medir el PPP mediante la regresión lineal y evaluar la fuerza de la relación (coeficiente de correlación).
- **Validar el Modelo:** Comparar los resultados simulados con datos empíricos reales o con expectativas teóricas.
- **Realizar un Análisis de Sensibilidad:** Observar cómo cambios en parámetros (eficiencia de tiro, turnover, duración de posesión) afectan el marcador final, contribuyendo a entender la robustez del modelo.

## Análisis de Parada de la Simulación
Se estableció un límite temporal en cada cuarto (720 segundos) y se simuló el partido completo en función del tiempo transcurrido en cada posesión. Este enfoque permite:
- Asegurar que la simulación se detenga de forma realista.
- Contabilizar el número total de posesiones que, a su vez, sirven para evaluar la relación con el marcador.
- Garantizar que la simulación cumpla con las restricciones temporales propias de un partido real.

---

# S4. Conclusiones

El proyecto de simulación del partido de baloncesto ha permitido desarrollar y analizar un modelo de eventos discretos capaz de reflejar aspectos clave de un encuentro deportivo. Entre las principales conclusiones se destacan:

1. **Importancia de la Eficiencia Ofensiva:**  
   Incrementar la probabilidad de acierto en tiros (60% para tiros de 2 y 40% para tiros de 3) conduce a un aumento considerable en la puntuación final. Esto confirma la hipótesis de que la eficiencia en cada posesión es determinante en el marcador.

2. **Impacto de la Defensa (Turnovers y Rebotes):**  
   Reducir la tasa de turnovers de 15% a 10% mejora el manejo del balón y disminuye los robos, lo que afecta la cantidad de posesiones y el ritmo del partido. A pesar de ello, la disminución en los errores reduce situaciones de contraataque, produciendo un ligero ajuste en el puntaje.

3. **Relación entre Posesiones y Marcador Final:**  
   La regresión lineal realizada entre el número total de posesiones y el marcador final combinada sugiere que, en promedio, cada posesión adicional aporta alrededor de 1.23 puntos. Sin embargo, el coeficiente de correlación moderado (R=0.30) indica que existen otros factores (eficiencia individual en la conversión, eventos aleatorios como faltas y rebotes) que influyen en el marcador, de modo que el número de posesiones explica solo parcialmente la variabilidad.

4. **Validación y Robustez del Modelo:**  
   El modelo implementado en Python, basado en datos y supuestos razonables, ha demostrado ser una herramienta útil para explorar preguntas de investigación relacionadas con la dinámica de un partido de baloncesto. La experimentación con diferentes parámetros ha permitido identificar la sensibilidad del sistema a cambios en la eficiencia de tiro y la gestión de errores.

5. **Perspectivas Futuras:**  
   Para profundizar en el análisis, se podrían introducir asimetrías entre equipos (por ejemplo, un equipo con mejor eficiencia defensiva o mayor capacidad ofensiva), incorporar efectos de racha (momentum) y mejorar la validación comparando con datos reales de competiciones. Además, el análisis multivariable que incluya otros indicadores (como la duración promedio de posesión) enriquecería la comprensión del juego.

En conclusión, la simulación ofrece una ventana para comprender cómo la interacción de diversas variables—posesiones, eficiencia en tiros, turnovers y rebotes—se combinan para determinar el resultado final de un partido de baloncesto. La estructura meticulosa del proyecto (desde la definición del problema hasta el análisis estadístico) garantiza que los hallazgos sean sólidos y permitan abordar las interrogantes iniciales de forma cuantitativa. Este enfoque servirá como base para futuros estudios y mejoras en modelos de simulación deportiva, contribuyendo al análisis y la toma de decisiones en contextos competitivos.

