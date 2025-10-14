from fastapi import FastAPI, HTTPException
from models import Curso
from fastapi import Path

app = FastAPI()

cursos = {
    1: {"curso": "python", "aulas": 20, "horas": 120},
    2: {"curso": "Java", "aulas": 30, "horas": 139},
}


@app.get("/cursos")
async def get_cursos():
    return cursos


@app.get("/cursos/{curso_id}")
async def get_curso(
    curso_id: int = Path(
        title="Id do curso",
        description=f"Deve ser entre {min(cursos)} e {max(cursos)}",
        gt=0,
        lt=3,
    )
):
    try:
        curso = cursos[curso_id]
        return curso
    except:
        raise HTTPException(status_code=404, detail="Curso não encontrado.")


@app.post("/cursos")
async def post_curso(curso: Curso):
    next_id: int = len(cursos) + 1
    cursos[next_id] = curso
    curso.id = next_id
    return curso


@app.put("/cursos/{curso_id}")
async def put_cursos(curso_id: int, curso: Curso):
    if curso_id in cursos:
        cursos[curso_id] = curso
        curso.id = curso_id
        return curso
    else:
        raise HTTPException(
            status_code=404, detail=f"Curso com o id {curso_id} não existe!"
        )


@app.delete("/cursos/{curso_id}")
async def del_curso(curso_id: int):
    if curso_id in cursos:
        del cursos[curso_id]
        return cursos
    else:
        raise HTTPException(status_code=404, detail="ID não encontrado!")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=8000)
