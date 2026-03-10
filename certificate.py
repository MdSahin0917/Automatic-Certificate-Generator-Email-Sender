# from PIL import Image, ImageDraw, ImageFont
# import os
# import textwrap
# import re

# def draw_wrapped_text(draw, text, font, y, img_width, margin_ratio=0.1, fill="black", line_spacing=10):
#     """
#     Draw text inside margins (auto-wrap).
#     - margin_ratio = fraction of image width to keep as margin
#     - y = starting y position
#     """
#     # Calculate margins
#     margin = int(img_width * margin_ratio)
#     max_width = img_width - 2 * margin

#     # Wrap text
#     lines = []
#     words = text.split()
#     line = []
#     for word in words:
#         test_line = " ".join(line + [word])
#         if draw.textlength(test_line, font=font) <= max_width:
#             line.append(word)
#         else:
#             lines.append(" ".join(line))
#             line = [word]
#     if line:
#         lines.append(" ".join(line))

#     # Draw each line
#     for l in lines:
#         text_width = draw.textlength(l, font=font)
#         x = (img_width - text_width) / 2  # center
#         draw.text((x, y), l, font=font, fill=fill)
#         y += font.size + line_spacing

#     return y

# def draw_text_with_bold_words(draw, text, bold_words, regular_font, bold_font, y, img_width, margin_ratio=0.1, fill="black", line_spacing=10):
#     """
#     Draw text with specific words in bold font
#     """
#     margin = int(img_width * margin_ratio)
#     max_width = img_width - 2 * margin
    
#     print(f"\n--- Drawing text with bold words ---")
#     print(f"Full text: '{text}'")
#     print(f"Bold words to highlight: {bold_words}")
    
#     # Clean bold words - remove any punctuation for matching
#     clean_bold_words = []
#     for word in bold_words:
#         if word and word.strip():
#             # Remove punctuation for matching
#             clean_word = re.sub(r'[^\w\s]', '', word)
#             clean_bold_words.append(clean_word.lower())
    
#     print(f"Cleaned bold words for matching: {clean_bold_words}")
    
#     # Split text into words
#     words = text.split()
#     print(f"Text split into words: {words}")
    
#     lines = []
#     current_line = []
#     current_line_width = 0
    
#     # First, wrap the text into lines
#     for word in words:
#         # Clean the word for matching (remove punctuation)
#         clean_word = re.sub(r'[^\w\s]', '', word)
        
#         # Check if this word should be bold (case-insensitive comparison)
#         is_bold = False
#         for bold_word in clean_bold_words:
#             if bold_word and clean_word.lower() == bold_word.lower():
#                 is_bold = True
#                 print(f"✓ BOLD MATCH: Word '{word}' (cleaned: '{clean_word}') matches bold word '{bold_word}'")
#                 break
        
#         if not is_bold:
#             print(f"  Regular word: '{word}' (cleaned: '{clean_word}')")
        
#         font_to_use = bold_font if is_bold else regular_font
#         word_width = draw.textlength(word + " ", font=font_to_use)
        
#         if current_line_width + word_width <= max_width:
#             current_line.append((word, is_bold))
#             current_line_width += word_width
#         else:
#             if current_line:
#                 lines.append(current_line)
#             current_line = [(word, is_bold)]
#             current_line_width = word_width
    
#     if current_line:
#         lines.append(current_line)
    
#     print(f"Created {len(lines)} lines of text")
    
#     # Draw each line with mixed fonts
#     current_y = y
#     for line_idx, line in enumerate(lines):
#         x = margin
#         line_text = ""
        
#         for word, is_bold in line:
#             line_text += word + " "
#             font_to_use = bold_font if is_bold else regular_font
#             draw.text((x, current_y), word + " ", font=font_to_use, fill=fill)
#             word_width = draw.textlength(word + " ", font=font_to_use)
#             x += word_width
        
#         print(f"Line {line_idx+1}: '{line_text.strip()}'")
#         current_y += regular_font.size + line_spacing
    
#     print(f"--- Finished drawing text ---\n")
#     return current_y

# def generate_certificate(name, partiType, title, TEMPLATE_FILE, OUTPUT_FOLDER, FONT_BODY, FONT_HIGHLIGHT, paText, prText1, prText2):
#     img = Image.open(TEMPLATE_FILE).convert("RGB")
#     draw = ImageDraw.Draw(img)

#     # Image width
#     img_width = img.width

#     # Clean the name for display (remove any extra spaces)
#     clean_name = name.strip()
#     print(f"\n=== Generating certificate for {clean_name} ===")
    
#     if partiType == "Participant":
#         # Replace {name} with actual name in paText
#         paText_filled = paText.replace("{name}", clean_name)
#         print(f"Participant text: '{paText_filled}'")
#         print(f"Name to highlight: '{clean_name}'")
#         # Draw with name in bold
#         draw_text_with_bold_words(draw, paText_filled, [clean_name], FONT_BODY, FONT_HIGHLIGHT, 500, img.width)
     
#     elif partiType == "Presenter":
#         # First replace {ptype} if it exists (it should already be replaced in main)
#         # Then replace {name} in prText1
#         prText1_filled = prText1.replace("{name}", clean_name)
#         print(f"Presenter text part 1: '{prText1_filled}'")
#         print(f"Title: '{title}'")
        
#         # Extract presentation type from prText1_filled
#         words = prText1_filled.split()
#         ptype = ""
#         for i, word in enumerate(words):
#             if word.lower() == "an" and i+1 < len(words):
#                 ptype = words[i+1]
#                 # Remove any punctuation
#                 ptype = ptype.strip('.,!?;:')
#                 break
        
#         # Make sure name is in the bold_words list
#         bold_words = [clean_name]
#         if ptype:
#             bold_words.append(ptype)
        
#         print(f"Bold words for presenter: {bold_words}")
        
#         # Draw the first line with bold words
#         current_y = draw_text_with_bold_words(draw, prText1_filled, bold_words, FONT_BODY, FONT_HIGHLIGHT, 400, img.width)

#         # Add some spacing before the title
#         current_y += 20

#         # Draw title in bold and centered
#         text_width = draw.textlength(title, font=FONT_HIGHLIGHT)
#         x = (img_width - text_width) / 2  
#         draw.text((x, current_y), title, font=FONT_HIGHLIGHT, fill="navy")
#         print(f"Drew title at position ({x}, {current_y})")
        
#         # Update Y position after title
#         current_y += FONT_HIGHLIGHT.size + 20

#         # Draw prText2 (no bold words needed here)
#         draw_wrapped_text(draw, prText2, FONT_BODY, current_y, img.width)
#         print(f"Drew part 2 text")

#     else:
#         print(f"Invalid participation type '{partiType}'. User must be either 'Participant' or 'Presenter'.")

#     # Save as PDF
#     cert_path = os.path.join(OUTPUT_FOLDER, f"{clean_name}.pdf")
#     img.save(cert_path, "PDF")
#     print(f"Certificate generated for {clean_name}")
#     print(f"=== Done ===\n")
#     return cert_path




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