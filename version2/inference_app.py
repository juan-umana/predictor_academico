import pickle

# Read model from PKL file 
filename='C:/Users/jd.umana10/Documents/GitHub/predictor_academico_2/aprendizaje_estructura/model.pkl'
file = open(filename, 'rb')
model_success = pickle.load(file)
file.close()


# Print model 
print(model_success)

# Check_model check for the model structure and the associated CPD and returns True if everything is correct otherwise throws an exception
print(model_success.check_model())

# Infering the posterior probability
from pgmpy.inference import VariableElimination

infer = VariableElimination(model_success)

<<<<<<< HEAD
evidence = {'marital_status': 1, 'application_mode': 44, 'application_order': 1,
            'course': 9003, 'attendance': 1, 'prev_qualification': 39, 'nationality': 1,
            'displaced': 1, 'debtor': 0, 'tuition': 1, 'gender': 1, 'scholarship': 0,
            'international': 0, 'units_1_credited': 0, 'units_1_enrolled': 6,
            'units_1_approved': 6, 'units_1_grade': 14, 'units_2_credited': 0,
            'units_2_enrolled': 6, 'units_2_approved': 6, 'units_2_grade': 15,
            'unemployment_rate': 12, 'inflation_rate': 1, 'gdp': 2}
=======
evidence = {'gdp': 2}
>>>>>>> 66b8b51ea0395ded85186a2f4d2e865e47914440

posterior_p = infer.query(["target"], evidence=evidence)
print(posterior_p)
