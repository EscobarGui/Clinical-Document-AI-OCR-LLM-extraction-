import uuid
from .schemas import ExtractionResult, FieldSpan
from ingest.pdf_loader import pdf_to_images
from ingest.preproc import clean
from ocr.ocr_engine import run_tesseract, ocr_conf_stats
from ocr.htr_engine import run_htr_on_line
from classify.doc_classifier import classify_doc
from extract.rules import extract_solicitante
from extract.clinical_ner import extract_solicitacao_entities
from normalize.tuss_mapper import TussMapper

TUSS = TussMapper("data/tuss.csv")

def process_document(pdf_path: str) -> ExtractionResult:
    doc_id = str(uuid.uuid4())
    images = pdf_to_images(pdf_path)           # [np.array(BGR), ...]
    words_all, text_all = [], []

    for img in images:
        img2 = clean(img)                      # deskew, denoise, binarize
        words = run_tesseract(img2)
        mean_conf, low_ratio = ocr_conf_stats(words)

        # fallback HTR por linhas ruins (stub)
        if mean_conf < 70 or low_ratio > 0.30:
            # TODO: cortar por linhas e chamar run_htr_on_line em cada linha ruim
            pass

        words_all.extend(words)
        text_all.append(" ".join(w.text for w in words))

    full_text = "\n".join(text_all)
    doc_type = classify_doc(full_text)

    # --------- Extração de campos ----------
    solicitante = extract_solicitante(full_text)

    termos = extract_solicitacao_entities(full_text)  # ["hemograma completo", "tireoide tsh", ...]
    mapped = []
    min_score = 0.86
    for t in termos:
        code, name, s = TUSS.map_term(t)
        mapped.append({"term": t, "tuss_code": code, "tuss_name": name, "score": s})

    # --------- Roteamento (auto vs review) ----------
    auto_ok = all(x["score"] >= min_score for x in mapped) and solicitante.score >= 0.8
    route = "auto" if auto_ok else "review"

    return ExtractionResult(
        doc_id=doc_id,
        doc_type=doc_type,
        ocr_conf_mean=sum(w.conf for w in words_all)/max(1,len(words_all)),
        fields={
            "Solicitante": solicitante,
            "Solicitacao": FieldSpan(text=str(mapped), bbox=None, score=min(y["score"] for y in mapped) if mapped else 0.0)
        },
        model_versions={"ocr":"tesseract-5.3","htr":"trocr-base","ner":"biobertpt-v1"},
        route=route,
        errors=[]
    )
