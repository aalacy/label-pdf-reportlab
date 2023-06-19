import os
from barcode.writer import ImageWriter
import barcode
from barcode.base import Barcode

Barcode.default_writer_options["write_text"] = False

from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

pdfmetrics.registerFont(
    TTFont("Arial", os.path.join(os.getcwd(), "fonts", "arial.ttf"))
)
pdfmetrics.registerFont(
    TTFont("Arial-Bold", os.path.join(os.getcwd(), "fonts", "arialbd.ttf"))
)
pdfmetrics.registerFont(
    TTFont("Arial-Narrow", os.path.join(os.getcwd(), "fonts", "arialn.ttf"))
)
pdfmetrics.registerFont(
    TTFont("Arial-Narrow-Bold", os.path.join(os.getcwd(), "fonts", "arialnbd.ttf"))
)

registerFontFamily(
    "Arial",
    normal="Arial",
    bold="Arial-Bold",
    italic="Arial-Bold",
    boldItalic="Arial-Bold",
)

color_map = {
    "orange": colors.orange,
    "blue": colors.blue,
    "lightblue": colors.lightblue,
    "green": colors.green,
    "yellow": colors.yellow,
    "red": colors.red,
    "none": colors.white,
}

# Define image dimensions
scale = 0.8
im_width, im_height = 298 // 3 - 30, 106 - 30
im_width = im_width * scale
im_height = im_height * scale
barcode_height = 106 // 3
label_width, label_height = 298, 106  # Label dimensions in pixels
pdf_width, pdf_height = (
    label_width / 72 * inch,
    label_height / 72 * inch,
)  # Convert pixels to points
margin = 10
title_font_size = 22
rect_font_size = 24
label_font_size = 7
paragraph_font_size = 7
path = "./"

def generate_barcode(uid, filename):
    # Generate barcode
    EAN = barcode.get_barcode_class("code128")
    ean = EAN(str(uid), writer=ImageWriter())

    # Save barcode image
    return ean.save(filename)


def draw_barcode(c, uid, coord):
    generate_barcode(uid, os.path.join(path, "barcode2"))

    # Add barcode
    barcode = Image(
        os.path.join(path, "barcode2.png"),
        width=1.74 * (298 // 3),
        height=1.2 * barcode_height,
    )
    barcode.drawOn(c, coord, label_height - 10 - barcode_height)


# Reset fill color and stroke color to black for text
def reset_fillcolor(c):
    c.setFillColor(colors.black)
    c.setStrokeColor(colors.black)  # Reset stroke color to black


def rect_string(c, coord, total_thc):
    box_width = (
        95  # Define the width of the box. Change this value as per your requirements.
    )
    box_height = (
        32  # Define the height of the box. Change this value as per your requirements.
    )

    reset_fillcolor(c)

    title_margin = 19
    box_start_y = -im_width - box_height - margin - title_margin
    # move the origin up and to the left
    # draw a rectangle
    rect_start_x = 7
    c.rect(
        rect_start_x,
        box_start_y,
        box_width,
        box_height,
        stroke=True,
    )
    # (note after rotate the y coord needs to be negative!)
    text_start_y = box_start_y + box_height - 8
    text_start_x = rect_start_x + 2
    c.setFont("Arial-Bold", label_font_size)
    c.drawString(text_start_x, text_start_y, "TOTAL THC:")
    c.setFont("Arial-Bold", rect_font_size)
    c.drawString(text_start_x, text_start_y - 21, total_thc)


def make_label(
    icon,
    distro,
    text0,
    total_cann,
    total_thc,
    total_cbd,
    pkg_date,
    batch,
    uid,
    strain_type,
    sample_id,
    cultivator,
    color1,
):
    # Create a new PDF with custom page size
    coord = label_height - im_height

    c = canvas.Canvas("test.pdf", pagesize=(pdf_width, pdf_height))

    c.rotate(90)

    # scale the canvas due to the big image size
    c.scale(scale, scale)

    # Add image to the PDF
    im = Image(os.path.join(path, f"{icon}.jpg"), width=im_width, height=im_height)
    im.drawOn(c, coord + 20, -im_width - margin)

    # restore scale to normal
    c.scale(1.25, 1.25)

    # drawing title text
    c.setFont("Arial-Narrow-Bold", title_font_size)
    c.drawString(12, -im_width - margin * 2, text0)

    # Add text for total cannabinoids in larger font with a box around it.
    rect_string(c, coord, total_thc)

    # restore coordinate to the normal
    c.rotate(-90)

    paragraph_start_x = coord + 75
    draw_barcode(c, uid, paragraph_start_x)

    # Set size and position of highlight box
    highlight_width = im_width * scale  # Adjust width as per your requirements
    highlight_height = 10  # Adjust height as per your requirements
    highlight_x_position = 0  # Adjust x_position as per your requirements
    highlight_y_position = coord - 10  # Adjust y_position as per your requirements

    # Get the color from color_map, or default to orange if not found
    highlight_color = color_map.get(color1)

    # Define highlight color
    # highlight_color = colors.orange
    c.setFillColor(highlight_color)
    c.setStrokeColor(highlight_color)  # Set stroke color to match fill color

    line_width = 2  # Set line width as per your requirements.
    c.setLineWidth(line_width)

    # Draw the highlight
    c.rect(
        highlight_x_position,
        highlight_y_position,
        highlight_width,
        highlight_height,
        fill=True,
        stroke=True,
    )

    # Reset fill color and stroke color to black for text
    reset_fillcolor(c)

    # Add NAME with orange highlight
    c.setFont("Arial-Narrow", 13)
    c.drawString(7, highlight_y_position - highlight_height - 5, strain_type.upper())

    # Add 5 lines of text
    c.setFont("Arial", 6)
    thc_text = f"THC: {total_thc}"
    total_cann_text = f"TOTAL CANNABINOIDS: {total_cann} {thc_text} CBD:"
    batch_text = f"BATCH#: {batch}"
    sample_id_text = f"SAMPLE ID: {sample_id} {batch_text}"
    distro_text = f"DISTRO: {distro}"
    cultivator_text = f"CULTIVATOR: {cultivator}"
    pkg_text = f"{text0} -  PACKAGED: " + pkg_date

    diff_height = 9
    paragraph_start_y = label_height - barcode_height - 15
    c.drawString(paragraph_start_x, paragraph_start_y, total_cann_text)
    paragraph_start_y -= diff_height
    c.drawString(paragraph_start_x, paragraph_start_y, total_cbd)
    paragraph_start_y -= diff_height
    c.drawString(paragraph_start_x, paragraph_start_y, sample_id_text)
    paragraph_start_y -= diff_height
    c.drawString(paragraph_start_x, paragraph_start_y, distro_text)
    paragraph_start_y -= diff_height
    c.drawString(paragraph_start_x, paragraph_start_y, cultivator_text)
    paragraph_start_y -= diff_height
    c.drawString(paragraph_start_x, paragraph_start_y, pkg_text)

    # Save the PDF
    c.save()

    return  # anvil.media.from_file(path+fn+'.pdf', 'PDF', fn+'.pdf')


if __name__ == "__main__":
    make_label(
        icon="symmatree",
        distro="XYZ MANAGEMENT CENTER - C11-1234566-LIC",
        text0="OG KUSH",
        total_cann="31.83 mg/pkg%",
        total_cbd="0.00%",
        total_thc="30.77%",
        pkg_date="06/07/2023",
        batch="OGK-1055",
        uid="5901234123457",
        strain_type="indica",
        sample_id="VAL-220622-015",
        cultivator="SALINAS SPENCE RD - CCL21-0001247",
        color1="lightblue",
    )
