import os
import argparse

from tqdm import tqdm
import pdfplumber
import fitz

import pytesseract

from PIL import Image
import io


def preprocess(source_path, type, output_path):
    """Extract text from PDF files and save the results as text files."""
    masked_file_ls = os.listdir(source_path)
    folder = os.path.join(output_path, type)

    if not os.path.isdir(folder):
        os.makedirs(folder)

    for file in tqdm(masked_file_ls):
        text = read_pdf(os.path.join(source_path, file))
        txt = file.replace('.pdf', '')
        with open(os.path.join(folder, txt+'.txt'), 'w') as f:
            f.write(text)


def read_pdf(pdf_path):
    """Extract text and images from a PDF file, concatenate, and return the result."""
    text = extract_text(pdf_path)
    img = extract_images(pdf_path)

    res = ''
    if text:
        res += text
    if img:
        res += img
    
    return res.strip().replace(" ", "").replace("\n", "")


def extract_text(pdf_loc):
    """Extract text from a PDF file and return the concatenated text."""
    pdf = pdfplumber.open(pdf_loc)
    pages = pdf.pages
    pdf_text = ''
    for _, page in enumerate(pages):
        text = page.extract_text()
        if text:
            pdf_text += text
    pdf.close()
    return pdf_text


def extract_images(pdf_loc):
    """Extract text from images in a PDF file and return the concatenated text.."""
    pdf = fitz.open(pdf_loc)
    
    pdf_text = ''
    for i in range(len(pdf)):
        page = pdf[i]
        images = page.get_images(full=True)

        for _, img in enumerate(images):
            xref = img[0]
            image = pdf.extract_image(xref)["image"]

            try:
                img = Image.open(io.BytesIO(image))
                text = pytesseract.image_to_string(img, lang="chi_tra+eng").strip().replace(" ", "").replace("\n", "")

                if len(text) > 10:
                    pdf_text += text
            except:
                print()
    pdf.close()

    return pdf_text

if __name__ == "__main__":
    # 使用argparse解析命令列參數
    parser = argparse.ArgumentParser(description='Process some paths and files.')
    parser.add_argument('--source_path', type=str, required=True, help='讀取參考資料路徑')  # 參考資料的路徑
    parser.add_argument('--output_path', type=str, required=True, help='經處理後的參考資料輸出路徑')  # 經處理後的參考資料輸出路徑

    args = parser.parse_args()  # 解析參數

    answer_dict = {"answers": []}  # 初始化字典

    if not os.path.isdir(args.output_path):
        os.makedirs(args.output_path)

    source_path_finance = os.path.join(args.source_path, 'finance')  # 設定參考資料路徑
    preprocess(source_path_finance, 'finance', args.output_path)

    source_path_insurance = os.path.join(args.source_path, 'insurance')  # 設定參考資料路徑
    preprocess(source_path_insurance, 'insurance', args.output_path)
    
    source_path_faq = os.path.join(args.source_path, 'faq')

    masked_file_ls = os.listdir(source_path_faq)
    folder = os.path.join(args.output_path, 'faq')

    if not os.path.isdir(folder):
        os.makedirs(folder)

    import shutil
    for file in tqdm(masked_file_ls):
        shutil.copy(os.path.join(source_path_faq, file), os.path.join(folder, file))