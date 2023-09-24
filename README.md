# Predictor académico
## Código fuente del predictor de éxito académico en estudiantes universitarios

Producto de analítica de datos para universidades que quieran incorporar un apoyo en el proceso de acompañamiento a los estudiantes y la toma de decisiones asociada como apoyos o consejería  

### Pregunta de negocio

¿Cuáles variables pueden considerarse factores de riesgo para que un estudiante no tenga éxito académico en la universidad y cómo predecir la necesidad de un estudiante de atender a programas de apoyo y consejería?

#### Autores
[Daniela Ruiz](https://github.com/danielaruizl1)  
[Juan D. Umaña](https://github.com/juan-umana)

### Metodología

El predictor académico ha sido desarrollado con datos recolectados por el estudio [Early prediction of student's performance in higher education: a case study](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success)

En su primera versión el predictor utilizó las variables continuas y categoricas con mayor correlación (positiva y negativa) sobre la variable objetivo: haberse graduado como estado de éxito académico.

Posteriormente estos predictores son utilizados en una red bayesiana para parametrizar un podelo predictivo en el cual se recolecte la información de futuros estudiantes y se ofrezca información temprana sobre el posible desempeño que tendrá en su carrera.

Por último, el producto se ofrece como un tablero interactivo alojado en un servidor AWS para que usuarios puedan acceder al modelo de forma remota y evaluar las predicciones para sus estudiantes.
