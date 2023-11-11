from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import gpt4

app = FastAPI()

# CORSミドルウェアを追加
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def handler(request: Request, exc: RequestValidationError):
    error_message = {"detail": "Validation Error", "errors": exc.errors()}
    return JSONResponse(content=error_message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@app.post("/submit")
async def submit_answers(request: Request):
    data = await request.json()

    formatted_answers = {
        f"質問{i + 1}": f"{question}　質問{i + 1}への回答：{answer}"
        for i, (question, answer) in enumerate(data.items())
    }

    answer_of_question = ""
    # 結果を出力
    for key, value in formatted_answers.items():
        answer_of_question += f"{key}:{value}" + "\n"
    answer1, answer2 = gpt4.question_about_nabe(answer_of_question)
    # ここでは単純に回答を返す
    return answer1, answer2
