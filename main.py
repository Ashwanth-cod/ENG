from fpdf import FPDF
import os

# Define PDF class
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "ENG Programming Language - Extended Documentation", ln=True, align="C")
        self.ln(5)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 8, title, ln=True, fill=True)
        self.ln(2)

    def chapter_body(self, text):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, text)
        self.ln()

    def code_block(self, code):
        self.set_font("Courier", "", 10)
        self.set_fill_color(245, 245, 245)
        self.multi_cell(0, 6, code, border=1, fill=True)
        self.ln(1)

# Create PDF instance
pdf = PDF()
pdf.add_page()

# Sections
pdf.chapter_title("Introduction")
pdf.chapter_body("""ENG is a lightweight interpreted programming language designed for educational and scripting purposes. It has Python-like syntax and allows users to define variables, write control flow structures, and call custom functions in a simplified format.""")

pdf.chapter_title("Syntax Guide")

# Variables
pdf.chapter_body("➤ Variables")
pdf.code_block('let name = "value"')

# Input
pdf.chapter_body("➤ Input")
pdf.code_block('let name = input "Enter your name" str\nlet age = input "Enter your age" int')

# Output
pdf.chapter_body("➤ Output")
pdf.code_block('say "Hello, " + name')

# Conditionals
pdf.chapter_body("➤ Conditionals")
pdf.code_block('if age > 20:\n  say "You are over 20"\nend')

# Loops
pdf.chapter_body("➤ Loops")
pdf.code_block('repeat 3 times:\n  say "looping..."\nend')

# Functions
pdf.chapter_body("➤ Functions")
pdf.code_block('define greet(person):\n  say "Hi " + person\nend\n\ncall greet("Alice")')

# Lists and methods
pdf.chapter_title("Working with Lists")
pdf.chapter_body("""Lists are used to store multiple values. ENG provides common list methods for manipulation:""")
pdf.code_block("""let items = list()\ncall items.append("Apple")\ncall items.pop()\ncall items.remove("Apple")\ncall items.clear()\ncall items.sort()\ncall items.reverse()""")

pdf.chapter_body("Equivalent Python:")
pdf.code_block("""items = []\nitems.append("Apple")\nitems.pop()\nitems.remove("Apple")\nitems.clear()\nitems.sort()\nitems.reverse()""")

# Dictionaries and methods
pdf.chapter_title("Working with Dictionaries")
pdf.chapter_body("""Dictionaries allow key-value pairs. ENG supports common dictionary operations:""")
pdf.code_block("""let user = dict()\ncall user.update({"name": "Ash", "age": 25})\ncall user.get("age")\ncall user.keys()\ncall user.values()\ncall user.items()""")

pdf.chapter_body("Equivalent Python:")
pdf.code_block("""user = {}\nuser.update({"name": "Ash", "age": 25})\nuser.get("age")\nuser.keys()\nuser.values()\nuser.items()""")

# License
pdf.chapter_title("License")
pdf.chapter_body("""Copyright (c) 2025 Ashwanth

This software and language specification (collectively referred to as "ENG") is the intellectual property of Ashwanth.

Permission is hereby granted to use, modify, and distribute ENG for educational and personal projects under the following terms:

1. You may not claim ownership of ENG or represent it as your own original work.
2. You may not use ENG, or any modified version of it, for commercial purposes without explicit written permission from the original author.
3. You must give credit to the original author, Ashwanth, in any public usage, fork, or distribution.
4. Modified versions must include this license and be used as a base with acknowledgment.
5. Any attempt to plagiarize or relicense ENG is strictly prohibited.

ENG is provided "as is", without warranty of any kind. The author is not liable for any damages or misuse.""")

# Contact
pdf.chapter_title("Contact")
pdf.chapter_body("GitHub: https://github.com/Ashwanth-cod/ENG\nEmail: fi.programming.tamil@gmail.com")

# Save the PDF
output_path = "/mnt/data/ENG_Language_Documentation_Complete.pdf"
pdf.output(output_path)

output_path
