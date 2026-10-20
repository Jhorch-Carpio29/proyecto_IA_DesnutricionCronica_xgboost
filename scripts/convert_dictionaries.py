#!/usr/bin/env python3
"""
Convert ENDES PDF Dictionaries to Markdown format with high precision.
Preserves exact table structure, variable definitions, and value options.
"""

import os
import glob
import re
import pdfplumber

TARGET_MODULES = [
    'data/1031-mef',
    'data/1036-inmunizacion',
    'data/1041-programasocial',
]

def convert_single_pdf(pdf_path, modulo_name):
    pdf_filename = os.path.basename(pdf_path)
    print(f"Processing: {pdf_filename} in {modulo_name}...")
    
    with pdfplumber.open(pdf_path) as pdf:
        num_pages = len(pdf.pages)
        p1_text = pdf.pages[0].extract_text() or ''
        title = ''
        for line in p1_text.splitlines():
            line_s = line.strip()
            if 'DICCIONARIO DE VARIABLES' in line_s:
                title = line_s
                break
        if not title:
            base = pdf_filename.replace('Diccionario - ', '').replace('.pdf', '')
            title = f'DICCIONARIO DE VARIABLES ({base})'

        # Extract all raw rows across pages
        raw_rows = []
        for p_idx, page in enumerate(pdf.pages):
            page_num = p_idx + 1
            table = page.extract_table()
            if not table:
                continue
            for r_idx, row in enumerate(table):
                raw_rows.append((page_num, r_idx, [str(c) if c is not None else '' for c in row]))

    processed_rows = []
    for page_num, r_idx, row in raw_rows:
        # Check if entire row is empty
        if not any(c.strip() for c in row):
            continue

        c0 = row[0].strip()
        c1 = row[1].strip()

        # Handle header collision in REC43 (page 7): "Nº\n127", "VARIABLE\nH35"
        if 'Nº\n' in c0 and 'VARIABLE\n' in c1:
            row_data = []
            for cell in row:
                parts = cell.split('\n', 1)
                row_data.append(parts[1].strip() if len(parts) > 1 else '')
            processed_rows.append(row_data)
            continue

        # Handle header collision in REC0111 (page 6 row 0): "Nº 69", "VVA13R9IABLE"
        if 'VVA13R9IABLE' in c1 or ('RegDiEón' in row[2] and 'REC0111' in pdf_filename):
            row_data = [
                '69', 'V139', 'Región, residencia habitual De-jure', 'N', '2', '0:25, 97',
                row[6].strip(), row[7].strip(), row[8].strip()
            ]
            processed_rows.append(row_data)
            continue

        # Skip standard headers
        if c0 == 'Nº' or 'VARIABLE' in c1:
            continue

        # Fix PS_CUNAMAS_VISITA numbering anomalies in INEI PDF
        if 'PS_CUNAMAS_VISITA' in pdf_filename:
            if c1 == 'PS100C1_A':
                c0 = '7'
            elif c1 == 'PS100C1_M':
                c0 = '8'
            elif c1 == 'PS100C_1S':
                c0 = '9'
            elif c0 == '9' and not c1:
                c0 = ''
            row[0] = c0

        processed_rows.append(row)

    # Fix REC91 S119NA cell omission on page 1
    if 'REC91' in pdf_filename:
        for i in range(len(processed_rows) - 1):
            if processed_rows[i][6].strip() == '12' and 'extranjera' in processed_rows[i][7]:
                if processed_rows[i+1][6].strip() == '1' and 'Quechua' in processed_rows[i+1][7] and not processed_rows[i+1][1].strip():
                    processed_rows[i+1][0] = '14'
                    processed_rows[i+1][1] = 'S119NA'
                    processed_rows[i+1][2] = 'Lengua materna de la madre'
                    processed_rows[i+1][3] = 'N'
                    processed_rows[i+1][4] = '2'
                    processed_rows[i+1][5] = '1:12'
                    break

    # Fix REC0111 V139 where options 1 to 15 appeared before the overlapping page 6 header
    if 'REC0111' in pdf_filename:
        v139_row_idx = None
        for i, r in enumerate(processed_rows):
            if r[1].strip() == 'V139':
                v139_row_idx = i
                break
        if v139_row_idx is not None:
            opt1_idx = None
            for j in range(v139_row_idx - 1, -1, -1):
                if processed_rows[j][6].strip() == '1' and processed_rows[j][7].strip() == 'Amazonas':
                    opt1_idx = j
                    break
            if opt1_idx is not None:
                v139_meta = processed_rows[v139_row_idx][:6]
                processed_rows[opt1_idx][0] = v139_meta[0]
                processed_rows[opt1_idx][1] = v139_meta[1]
                processed_rows[opt1_idx][2] = v139_meta[2]
                processed_rows[opt1_idx][3] = v139_meta[3]
                processed_rows[opt1_idx][4] = v139_meta[4]
                processed_rows[opt1_idx][5] = v139_meta[5]
                del processed_rows[v139_row_idx]

    # Build Markdown
    md_lines = []
    md_lines.append(f"# {title}\n")
    md_lines.append("**ENCUESTA DEMOGRÁFICA Y DE SALUD FAMILIAR ENDES**  ")
    md_lines.append(f"*Módulo:* `{modulo_name}` | *Archivo fuente:* `{pdf_filename}` | *Páginas originales:* {num_pages}\n")
    md_lines.append("| Nº | VARIABLE | DESCRIPCIÓN DE LAS VARIABLES | TIPO DE CARÁCTER | LONGITUD | RANGO DE VARIACIÓN | VALORES | DESCRIPCIÓN DE LAS ALTERNATIVAS | OBS |")
    md_lines.append("|:---|:---|:---|:---|:---|:---|:---|:---|:---|")

    for row in processed_rows:
        clean_cells = []
        for c in row:
            # Replace internal linebreaks with <br>
            c_clean = c.replace('\r\n', '<br>').replace('\n', '<br>').replace('|', '&#124;').strip()
            clean_cells.append(c_clean)
        while len(clean_cells) < 9:
            clean_cells.append('')
        clean_cells = clean_cells[:9]
        line = '| ' + ' | '.join(clean_cells) + ' |'
        md_lines.append(line)

    return '\n'.join(md_lines) + '\n'

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    count = 0
    for mod_rel in TARGET_MODULES:
        mod_dir = os.path.join(base_dir, mod_rel)
        mod_name = os.path.basename(mod_dir)
        pdf_pattern = os.path.join(mod_dir, "Diccionario*.pdf")
        pdf_files = sorted(glob.glob(pdf_pattern))
        
        for pdf_path in pdf_files:
            md_content = convert_single_pdf(pdf_path, mod_name)
            md_filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".md"
            out_path = os.path.join(mod_dir, md_filename)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            print(f"  -> Generated: {out_path} ({len(md_content.splitlines())} lines)")
            count += 1
            
    print(f"\nSuccessfully converted {count} dictionaries to .md!")

if __name__ == '__main__':
    main()
