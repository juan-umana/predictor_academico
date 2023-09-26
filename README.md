# Predictor académico
## Código fuente del predictor de éxito académico en estudiantes universitarios

Producto de analítica de datos para universidades que quieran estudiar los factores por los cuales los estudiantes no culminan sus estudios en el tiempo predestinado. Esto, con el fin de tomar decisiones informadas respecto al acompañamiento brindado a los estudiantes y las políticas educativas que se implementan.  

### Pregunta de negocio

¿Cuáles variables pueden considerarse factores de riesgo para que un estudiante no tenga éxito académico en la universidad y cómo predecir la necesidad de un estudiante de atender a programas de apoyo y consejería?

#### Autores
[Daniela Ruiz](https://github.com/danielaruizl1)  
[Juan D. Umaña](https://github.com/juan-umana)

### Metodología

El predictor académico ha sido desarrollado con datos recolectados por el estudio [Early prediction of student's performance in higher education: a case study](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success)

En su primera versión el predictor utilizó las variables continuas y categoricas con mayor correlación sobre la variable objetivo: haberse graduado como estado de éxito académico.

Posteriormente estos predictores son utilizados en una red bayesiana para parametrizar un modelo predictivo en el cual se recolecte la información de futuros estudiantes y se ofrezca información temprana sobre el posible desempeño que tendrá en su carrera.

Por último, el producto se ofrece como un tablero interactivo alojado en un servidor AWS para que usuarios puedan acceder al modelo de forma remota y evaluar las predicciones para sus estudiantes.

### Resultados

#### Selección de variables

El estudio contempla 36 variables con potencial predictor y una variable target categórica que denota si el estudiante se gradúo (éxito) o si se retiro o aún se encuentra matriculado (fracaso). Las variables se pueden agrupar de la siguiente forma:

Variables contínuas:

- application_order_dic = Application order (between 0 - first choice; and 9 last choice)
- prev_qual_grade_dic = Grade of previous qualification (between 0 and 200)
- admission_grade = Admission grade (between 0 and 200)
- age = Age of studend at enrollment
- units_i_semester_credited/enrolled/evaluations/approved/wo_evaluation = number of units redited/enrolled/evaluations/approved/wo_evaluation in semester i
- units_i_semester_grade = Grade average in the ith semester (between 0 and 20)
- unemployment_rate
- inflation_rate
- GDP

Variables categóricas:

- 'marital_status'
- 'application_mode'
- 'application_order'
- 'course'
- 'daytime/evening_attendance'
- 'previous_qualification'
- 'nacionality'
- 'mothers_qualification'
- 'fathers_qualification'
- 'mothers_occupation'
- 'fathers_occupation'
- 'displaced'
- 'educational_special_needs'
- 'debtor'
- 'tuition_fees_up_to_date'
- 'gender'
- 'scholarship_holder'
- 'age_at_enrollment'
- 'international'

De acuerdo con las correlaciones en las variables contínuas se decidió tomar las siguientes variables para las siguientes etapas del modelo:

- units_i_semester_approved (positive correlation)
- units_i_semester_grade (positive correlation)
- course (positive correlation)
- tuition_fees_up_to_date (positive correlation)
- scholarship_holder (positive correlation)
- application_mode (positive correlation)
- age_at_enrollment (negative correlation)
- units_i_semester_wo_evaluation (negative correlation)
- inflation_rate (negative correlation)

#### Descripción de predictores

A continuación mostramos estadisticas y gráficos descriptivos de los predictores seleccionados:

##### Unidades curriculares aprovadas en el primer y segundo semestre
##### Calificaciones de las unidades aprovadas en el primer y segundo semestre
##### Cursos
##### Matrícula
##### Beca
##### Tipo de aplicación
##### Edad al momento de inscripción
##### Unidades sin evaluación en el primer y segundo semestre
##### Tasa de inflación

