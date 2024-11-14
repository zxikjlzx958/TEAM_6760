import os
import json
import argparse

from tqdm import tqdm
import torch
import numpy as np

from FlagEmbedding import FlagReranker

def load_data(source_path):
    """Load and return a dictionary of the corpus from text files."""
    masked_file_ls = os.listdir(source_path)
    corpus_dict = {int(file.replace('.txt', '')): read_txt(os.path.join(source_path, file)) for file in tqdm(masked_file_ls)}
    return corpus_dict


def read_txt(p):
    """Read the content of a text file and return it."""
    text = ''
    with open(p,'r') as f:
        text += f.read(-1)
    return text


if __name__ == "__main__":
    # 使用argparse解析命令列參數
    parser = argparse.ArgumentParser(description='Process some paths and files.')
    parser.add_argument('--question_path', type=str, required=True, help='讀取發布題目路徑')  # 問題文件的路徑
    parser.add_argument('--source_path', type=str, required=True, help='讀取參考資料路徑')  # 參考資料的路徑
    parser.add_argument('--output_path', type=str, required=True, help='輸出符合參賽格式的答案路徑')  # 答案輸出的路徑

    device = 'cpu'
    if torch.cuda.is_available():
        device = 'cuda:0'
    elif torch.backends.mps.is_available():
        device = 'mps'


    args = parser.parse_args()  # 解析參數

    answer_dict = {"answers": []}  # 初始化字典

    reranker = FlagReranker('BAAI/bge-reranker-v2-m3', device=device)

    with open(args.question_path, 'rb') as f:
        qs_ref = json.load(f)  # 讀取問題檔案

    source_path_insurance = os.path.join(args.source_path, 'insurance') # 設定參考資料路徑
    corpus_dict_insurance = load_data(source_path_insurance)

    source_path_finance = os.path.join(args.source_path, 'finance')  # 設定參考資料路徑
    corpus_dict_finance = load_data(source_path_finance)

    with open(os.path.join(args.source_path, 'faq/pid_map_content.json'), 'rb') as f:
        key_to_source_dict = json.load(f)  # 讀取參考資料文件
        key_to_source_dict = {int(key): value for key, value in key_to_source_dict.items()}

    corpus_dict_faq = {key: str(value) for key, value in key_to_source_dict.items()}

    corpus = {'insurance': corpus_dict_insurance, 'finance': corpus_dict_finance, 'faq': corpus_dict_faq}

    with open(args.question_path, 'rb') as f:
        qs_ref = json.load(f)

    for q_dict in tqdm(qs_ref['questions']):

        max_score = -1e99
        passages = list()

        interval = 512

        idx = list()
        for s in q_dict['source']:
            passage = corpus[q_dict['category']][s]
            for start in range(0, len(passage), interval):
                p = passage[start:min(start+interval, len(passage))]
                passages.append(p)
                idx.append(s)

        score = reranker.compute_score([[q_dict['query'], passage] for passage in passages])
        s = np.argmax(score)
        retrieved = idx[s]

        answer_dict['answers'].append({"qid": q_dict['qid'], "retrieve": retrieved})
            
    with open(args.output_path, 'w', encoding='utf8') as f:
        json.dump(answer_dict, f, ensure_ascii=False, indent=4)  # 儲存檔案，確保格式和非ASCII字符
