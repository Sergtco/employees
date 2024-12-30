from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn
import predictions
import src.predictions as predictions

templates = Jinja2Templates(directory="templates")


def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


def check_result(
    request: Request,
    last_evaluation: int,
    number_project: int,
    average_montly_hours: float,
    time_spend_company: int,
    dept: str,
    salary: int,
):
    salary_str: str
    if salary > 66:
        salary_str = "high"
    elif salary > 33:
        salary_str = "medium"
    else:
        salary_str = "low"
    data = {
        "last_evaluation": last_evaluation,
        "number_project": number_project,
        "average_montly_hours": average_montly_hours,
        "time_spend_company": time_spend_company,
        "dept": dept,
        "salary": salary_str,
    }
    satisfaction_level = predictions.predict_employee_attrition(data)
    return templates.TemplateResponse(request=request, name="result.html", context={"attr_rate": satisfaction_level})


if __name__ == "__main__":
    app = FastAPI()
    app.add_api_route("/", index, methods=["get"])
    app.add_api_route("/api/check_employee", check_result, methods=["get"])
    uvicorn.run(app, host="0.0.0.0", port=6969)
