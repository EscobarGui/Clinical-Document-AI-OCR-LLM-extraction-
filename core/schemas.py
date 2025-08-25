from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

BBox = Tuple[int, int, int, int]  # x0, y0, x1, y1

@dataclass
class Word:
    text: str
    conf: float
    bbox: BBox

@dataclass
class FieldSpan:
    text: str
    bbox: Optional[BBox]
    score: float         # confiança do campo (OCR/NER/Regra)

@dataclass
class ExtractionResult:
    doc_id: str
    doc_type: str                 # "Pedido" | "Prescricao" | "Desconhecido"
    ocr_conf_mean: float
    fields: Dict[str, FieldSpan]  # {"Solicitante":..., "Destinatario":..., "Solicitacao":...}
    model_versions: Dict[str, str]# {"ocr":"tesseract-5.3", "htr":"trocr-base", "ner":"biobertpt-v1"}
    route: str                    # "auto" | "review"
    errors: List[str]