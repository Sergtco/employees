from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn
import predictions

templates = Jinja2Templates(directory="templates")


def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


def check_result(
    request: Request,
    last_evaluation: float,
    number_project: int,
    average_montly_hours: float,
    time_spend_company: int,
    dept: str,
    salary: int,
    work_accident: str = "",
    promotion_last_5years: str = "",
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
        "Work_accident": 1 if work_accident == "on" else 0,
        "promotion_last_5years": 1 if promotion_last_5years == "on" else 0,
        "dept": dept,
        "salary": salary_str,
    }
    satisfaction_level = predictions.predict_employee_attrition(data)
    msg: str
    if satisfaction_level < 33:
        msg = "Вам нужно поговорить с сотрудником!"
    elif satisfaction_level < 66:
        msg = "Сотрудник явно чем-то не доволен!"
    else:
        msg = "Сотрудник всем доволен!"

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={"attr_rate": satisfaction_level, "msg": msg},
    )


if __name__ == "__main__":
    app = FastAPI()
    app.add_api_route("/", index, methods=["get"])
    app.add_api_route("/api/check_employee", check_result, methods=["get"])
    uvicorn.run(app, host="0.0.0.0", port=6969)
