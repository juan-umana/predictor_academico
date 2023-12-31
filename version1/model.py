#%% Librerias
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
from pgmpy.estimators import BayesianEstimator
from pgmpy.sampling import BayesianModelSampling
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from sklearn.metrics import accuracy_score, confusion_matrix
import pandas as pd
from sklearn.model_selection import train_test_split
import os
import numpy as np

#%% Red bayesiana para predecir el éxito académico

# Estructura de la red
model_success = BayesianNetwork([('grade_1','grade_2'),('grade_2','success'),
                              ('age','success'),
                              ('inflation','success'),
                              ('scholarship','success'),
                              ('course','success'),
                              ('tuition','success'),
                              ('application','success')])

# Subir csv
data_model = pd.read_csv('data_model.csv')

#%% Dividir datos en train y test
X_train, X_test = train_test_split(data_model, test_size=0.2, stratify= data_model['success'], random_state=42)

#%% Emplear el módulo de ajuste de pgmpy para ajustar la CPDs del nuevo modelo
emv_success = MaximumLikelihoodEstimator(model = model_success, data = X_train)

# Obtener las CPDs ajustadas
cpds = emv_success.get_parameters()

#%%
print("Calculando cpds...")
cpdem_grade_1 = emv_success.estimate_cpd (node = 'grade_1')
#print(cpdem_grade_1)
cpdem_grade_2 = emv_success.estimate_cpd(node = 'grade_2')
#print(cpdem_grade_2)
cpdem_age =emv_success.estimate_cpd(node = 'age')
#print(cpdem_age)
cpdem_inflation = emv_success.estimate_cpd (node = 'inflation')
#print(cpdem_inflation)
cpdem_scholarship = emv_success.estimate_cpd(node = 'scholarship')
#print(cpdem_scholarship)
cpdem_course = emv_success.estimate_cpd(node = 'course')
#print(cpdem_course)
cpdem_tuition = emv_success.estimate_cpd(node = 'tuition')
#print(cpdem_tuition)
cpdem_application = emv_success.estimate_cpd(node = 'application')
#print(cpdem_application)
cpdem_success = emv_success.estimate_cpd(node = 'success')
#print(cpdem_success)

#%% Predecir para la variable de éxito académico

#Asociar las CPDs al modelo
model_success.add_cpds(cpdem_grade_1,
                       cpdem_grade_2,
                       cpdem_age,
                       cpdem_inflation,
                       cpdem_scholarship,
                       cpdem_course,
                       cpdem_tuition,
                       cpdem_application,
                       cpdem_success)

#Revisar que el modelo esté completo
print("Modelo completo:",model_success.check_model())

# Crear un objeto de inferencia
inference = VariableElimination(model_success)

def make_predictions(inference):

    # Crear una lista para guardar las predicciones
    predictions = []

    for _, row in X_test.iterrows():

        # Crear un diccionario de evidencias con los datos de cada fila en datos de prueba
        evidence = {variable: row[variable] for variable in row.index if variable!='success'}

        # Realizar la inferencia para obtener la CPD de "success" dado la evidencia
        result = inference.query(variables=['success'], evidence=evidence)
        try:
        # Agregar la predicción a la lista de predicciones
            list_result = list(result.values)
            max_val = list_result.index(max(result.values))
            if max_val == 0:
                predictions.append('Dropout')
            elif max_val == 1:
                predictions.append('Enrolled')
            else:
                predictions.append('Graduate')
        except:
            predictions.append('NaN')

    # Obtener el ground truth para comparar las predicciones
    y_true = X_test['success'].tolist()

    # Calcular la exactitud del modelo
    accuracy = accuracy_score(y_true, predictions)
    print(f'Exactitud (Accuracy): {accuracy}')

    # Calcular la matriz de confusión
    confusion = confusion_matrix(y_true, predictions)

    # Extraer los valores de Verdaderos positivos, falsos positivos, falsos negativos y verdaderos negativos.
    # Se entiende como positivo haberse graduado, y negativo seguir matrículado o desertar
    t_drop, drop_as_enr, drop_as_grad, enr_as_drop, t_enr, enr_as_grad, grad_as_drop, grad_as_enr, t_grad = confusion.ravel()
    true_positives = sum({t_grad})
    false_positives = sum({drop_as_grad, enr_as_grad})
    true_negatives = sum({t_drop, drop_as_enr, enr_as_drop, t_enr})
    false_negatives = sum({grad_as_drop, grad_as_enr})

    return true_positives, false_positives, true_negatives, false_negatives

if __name__ == "__main__":
    tp, fp, tn, fn = make_predictions(inference)
    print(f'Verdaderos Positivos: {tp}')
    print(f'Falsos Positivos: {fp}')
    print(f'Verdaderos Negativos: {tn}')
    print(f'Falsos Negativos: {fn}')