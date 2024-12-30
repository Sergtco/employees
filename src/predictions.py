import pandas as pd
from catboost import Pool
import pickle


def prepare_data(data):

    df = pd.DataFrame([data])

    cat_features = ["salary", "dept"]
    predict_pool = Pool(data=df, cat_features=cat_features)
    return predict_pool


def predict_employee_attrition(
    employee_data,
    model_filename="employee_attrition.cb",
):
    loaded_model = pickle.load(open(model_filename, "rb"))
    predict_pool = prepare_data(employee_data)
    predicted_price = loaded_model.predict(predict_pool)
    return predicted_price[0]
