import subprocess

# Run data_preprocess.py
subprocess.run(['python', 'Preprocess/data_preprocess.py', '--source_path', 'reference', '--output_path', 'data'], check=True)

# Run retrieval.py
subprocess.run(['python', 'Model/retrieval.py', '--question_path', 'Test/questions_preliminary.json', '--source_path', 'data', '--output_path', 'pred_retrieve.json'], check=True)
