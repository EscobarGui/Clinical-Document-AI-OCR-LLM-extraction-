from fastapi import FastAPI
from pydantic import BaseModel
from core.pipeline import process_document
from app.repo_sqlite import Repo

app = FastAPI()
repo = Repo("data/mvp.db")

class ApprovePayload(BaseModel):
    doc_id: str
    fields: dict   # campos editados pelo revisor
    reason: str | None = None

@app.post("/process")
def process_endpoint(pdf_path: str):
    res = process_document(pdf_path)
    repo.save_inference(res)      # salva log + versão de modelo + tempos
    if res.route == "review":
        repo.enqueue_review(res.doc_id, res.fields)
    return res

@app.post("/review/approve")
def approve(payload: ApprovePayload):
    repo.save_review(payload.doc_id, payload.fields, decision="approve", reason=payload.reason)
    # TODO: enviar para fila/API do sistema alvo
    return {"ok": True}

@app.post("/review/reject")
def reject(doc_id: str, reason: str):
    repo.save_review(doc_id, {}, decision="reject", reason=reason)
    return {"ok": True}