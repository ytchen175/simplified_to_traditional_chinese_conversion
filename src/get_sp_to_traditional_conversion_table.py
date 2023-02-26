import re
import json
import pdfplumber

file_path = "../material/標準字對照簡化字.pdf"
pdf = pdfplumber.open(file_path) 

simplified_to_traditional_conversion_table = dict()

START_PAGE = 7
END_PAGE = 91

for page in range(START_PAGE, END_PAGE+1):
    p0 = pdf.pages[page]
    text = p0.extract_text()

    founded = re.findall(r"([\u4E00-\u9FFF])\(([\u4E00-\u9FFF])\)(\*?)", text)

    for t in founded:
        traditional = t[0] # 正體字
        simplified = t[1] # 簡化字
        ambiguity_symbol = t[2] # 非對稱簡繁字

        if simplified not in simplified_to_traditional_conversion_table:
            simplified_to_traditional_conversion_table.update(
                {
                    simplified: {
                        '正體字': [], 
                        '非對稱簡繁字': False
                    }
                }
            )

        if ambiguity_symbol:
            simplified_to_traditional_conversion_table[simplified]['非對稱簡繁字'] = True

        simplified_to_traditional_conversion_table[simplified]['正體字'].append(traditional)


with open("簡化字對照標準字總表.json", "w", encoding='utf-8') as outfile:
    json.dump(simplified_to_traditional_conversion_table, outfile, indent = 4, ensure_ascii = False)