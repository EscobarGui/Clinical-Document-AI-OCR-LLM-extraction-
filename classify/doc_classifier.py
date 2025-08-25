def classify_doc(full_text: str) -> str:
    anchors_pedido = ["pedido", "exame", "solicitação", "guia sp/sadt"]
    anchors_presc  = ["prescrição", "posologia", "via de administração"]
    score_p = sum(full_text.lower().count(a) for a in anchors_pedido)
    score_r = sum(full_text.lower().count(a) for a in anchors_presc)
    if max(score_p, score_r) == 0: return "Desconhecido"
    return "Pedido" if score_p >= score_r else "Prescricao"