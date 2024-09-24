# from fpdf import FPDF

# # Function to convert a TXT file to PDF


# def txt_to_pdf(txt_filename, pdf_filename):
#     # Create instance of FPDF class
#     pdf = FPDF()

#     # Add a page
#     pdf.add_page()

#     # Set font
#     pdf.set_font("Arial", size=12)

#     # Open the text file in read mode
#     with open(txt_filename, 'r', encoding='utf-8') as file:
#         # Insert the texts in pdf
#         for line in file:
#             # Encode to ISO-8859-1, replace characters that cannot be encoded
#             line = line.encode('latin-1', 'replace').decode('latin-1')
#             pdf.cell(200, 10, txt=line, ln=True, align='L')

#     # Save the pdf with name .pdf
#     pdf.output(pdf_filename)


# # Example usage
# txt_filename = "output.txt"
# pdf_filename = "articles.pdf"
# txt_to_pdf(txt_filename, pdf_filename)

# print(f"Converted '{txt_filename}' into '{pdf_filename}' successfully!")

from fpdf import FPDF

# Function to convert a TXT file to PDF


def txt_to_pdf(txt_filename, pdf_filename):
    # Create instance of FPDF class
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set font
    pdf.set_font("Arial", size=12)

    # Define the character limit for each line (change according to your page size and font)
    line_width_limit = 190

    # Open the text file in read mode
    with open(txt_filename, 'r', encoding='utf-8') as file:
        for line in file:
            # Encode to ISO-8859-1, replace characters that cannot be encoded
            line = line.encode('latin-1', 'replace').decode('latin-1').strip()
            if line:
                # Split line into words
                words = line.split()
                line_to_add = ''
                for word in words:
                    # Check if adding the next word exceeds the line width
                    if pdf.get_string_width(line_to_add + word + ' ') < line_width_limit:
                        line_to_add += word + ' '
                    else:
                        # Add the line and start a new one
                        pdf.cell(200, 10, txt=line_to_add, ln=True, align='L')
                        line_to_add = word + ' '
                # Add the last portion of the line
                if line_to_add:
                    pdf.cell(200, 10, txt=line_to_add, ln=True, align='L')

    # Save the pdf with name .pdf
    pdf.output(pdf_filename)
    print(f"Converted '{txt_filename}' into '{pdf_filename}' successfully!")


# Example usage
txt_filename = "output.txt"
pdf_filename = "articles.pdf"
txt_to_pdf(txt_filename, pdf_filename)
