
from PIL import Image, ImageDraw, ImageFont
import os
import re


# ==============================
# WRAPPED CENTER TEXT
# ==============================
def draw_wrapped_text(draw, text, font, y, img_width, margin_ratio=0.1, fill="black", line_spacing=10):

    margin = int(img_width * margin_ratio)
    max_width = img_width - 2 * margin

    words = text.split()
    lines = []
    line = ""

    for word in words:
        test = line + word + " "
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            lines.append(line.strip())
            line = word + " "

    if line:
        lines.append(line.strip())

    for l in lines:
        text_width = draw.textlength(l, font=font)
        x = (img_width - text_width) / 2
        draw.text((x, y), l, font=font, fill=fill)
        y += font.size + line_spacing

    return y


# ==============================
# WRAPPED TEXT WITH BOLD WORDS
# ==============================
def draw_text_with_bold_words(draw, text, bold_words, regular_font, bold_font, y, img_width,
                              margin_ratio=0.1, fill="black", line_spacing=10):

    margin = int(img_width * margin_ratio)
    max_width = img_width - 2 * margin

    bold_words = [re.sub(r'[^\w\s]', '', w).lower() for w in bold_words]

    words = text.split()
    lines = []
    current_line = []
    current_width = 0

    for word in words:

        clean_word = re.sub(r'[^\w\s]', '', word).lower()
        is_bold = clean_word in bold_words
        font = bold_font if is_bold else regular_font

        word_width = draw.textlength(word + " ", font=font)

        if current_width + word_width <= max_width:
            current_line.append((word, is_bold))
            current_width += word_width
        else:
            lines.append(current_line)
            current_line = [(word, is_bold)]
            current_width = word_width

    if current_line:
        lines.append(current_line)

    current_y = y

    for line in lines:

        # calculate full width
        total_width = 0
        for word, is_bold in line:
            font = bold_font if is_bold else regular_font
            total_width += draw.textlength(word + " ", font=font)

        # center align
        x = (img_width - total_width) / 2

        for word, is_bold in line:
            font = bold_font if is_bold else regular_font
            draw.text((x, current_y), word + " ", font=font, fill=fill)
            x += draw.textlength(word + " ", font=font)

        current_y += regular_font.size + line_spacing

    return current_y


# ==============================
# CERTIFICATE GENERATOR
# ==============================
def generate_certificate(name, partiType, title,
                         TEMPLATE_FILE, OUTPUT_FOLDER,
                         FONT_BODY, FONT_HIGHLIGHT,
                         paText, prText1, prText2):

    img = Image.open(TEMPLATE_FILE).convert("RGB")
    draw = ImageDraw.Draw(img)

    img_width = img.width
    clean_name = name.strip()

    if partiType == "Participant":

        text = paText.replace("{name}", clean_name)

        draw_text_with_bold_words(
            draw,
            text,
            [clean_name],
            FONT_BODY,
            FONT_HIGHLIGHT,
            500,
            img_width
        )

    elif partiType == "Presenter":

        text1 = prText1.replace("{name}", clean_name)

        # detect presentation type
        words = text1.split()
        ptype = ""

        for i, w in enumerate(words):
            if w.lower() == "an" and i + 1 < len(words):
                ptype = words[i + 1].strip(".,!?;:")
                break

        bold_words = [clean_name]
        if ptype:
            bold_words.append(ptype)

        current_y = draw_text_with_bold_words(
            draw,
            text1,
            bold_words,
            FONT_BODY,
            FONT_HIGHLIGHT,
            400,
            img_width
        )

        current_y += 20

        # draw title
        title_width = draw.textlength(title, font=FONT_HIGHLIGHT)
        x = (img_width - title_width) / 2

        draw.text((x, current_y), title, font=FONT_HIGHLIGHT, fill="navy")

        current_y += FONT_HIGHLIGHT.size + 20

        draw_wrapped_text(
            draw,
            prText2,
            FONT_BODY,
            current_y,
            img_width
        )

    else:
        print("Invalid participation type")

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    cert_path = os.path.join(OUTPUT_FOLDER, f"{clean_name}.pdf")
    img.save(cert_path, "PDF")

    return cert_path
