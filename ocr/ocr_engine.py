import pytesseract, cv2

def run_tesseract(img_bgr) -> List[Word]:
    data = pytesseract.image_to_data(img_bgr, output_type=pytesseract.Output.DICT, config="--psm 6")
    words = []
    for i, txt in enumerate(data["text"]):
        if not txt.strip():
            continue
        conf = float(data["conf"][i])
        x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
        words.append(Word(text=txt, conf=conf, bbox=(x, y, x+w, y+h)))
    return words

def ocr_conf_stats(words: List[Word]) -> tuple[float, float]:
    confs = [w.conf for w in words]
    mean = sum(confs)/max(1,len(confs))
    low = sum(1 for c in confs if c < 50) / max(1,len(confs))
    return mean, low