import json

def save_txt(txt_address,sentence_list):
    with open(txt_address,'a',encoding='utf-8') as txt_file:
        for element in sentence_list:
            txt_file.write(json.dumps(element,ensure_ascii=False)+'\n')
