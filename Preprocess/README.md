# Preprocess資料夾
包含用於資料前處理之程式碼 data_preprocess.py  

## data_preprocess.py  
用於進行資料前處理  
會讀取source_path裡的finance和insurance資料夾內所有pdf檔案  
提取每個pdf檔案的文字以及圖片內的文字後  
將文字儲存至output_path對應的資料夾內的txt檔案  
最後將source_path內的faq資料夾複製到output_path  
source_path應為資料集中reference的路徑  

### Usage
```
python Preprocess/data_preprocess.py  --source_path <path_to_reference_folder> --output_path <path_to_output_folder>
```

### Example
```
python Preprocess/data_preprocess.py  --source_path reference --output_path data
```