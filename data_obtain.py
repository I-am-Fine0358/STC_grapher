import pandas as pd
import glob
from matplotlib import pyplot as plt

def read_mpt_files(path):
    # フォルダ内の全てのmptファイルを取得
    mpt_files = glob.glob(path + "/*.mpt")
    # ただし、ファイル名にCVが含まれるものは除外
    mpt_files = [file for file in mpt_files if not "_CV" in file]
    # ファイル名を昇順にソート
    mpt_files.sort()
    print(len(mpt_files))
    return mpt_files

def read_cv_files(path):
    cv_files = glob.glob(path + "/*.mpt")
    mpt_files = [file for file in mpt_files if "_CV" in file]
    cv_files.sort()
    return cv_files

def determine_header_lines(file_path, keyword='Nb header lines'):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if keyword in line:
                header_lines = int(line.split(':')[1].strip())
                return header_lines
    return 0  # Default if keyword is not found

def extract_time_and_voltage(file_path, header_line):
    df = pd.read_csv(file_path, skiprows=header_line-1, delimiter='\t')
    column_names = df.columns
    # 必要な列が存在するかどうかをチェックし、存在する場合のみ抽出
    required_columns = ["time/s", "Ewe/V"]
    existing_columns = [col for col in required_columns if col in column_names]
    if len(existing_columns) == len(required_columns):
        return df[existing_columns]
    else:
        # 必要な列が存在しない場合は、エラーメッセージを表示または空のDataFrameを返す
        print(f"Error: Required columns {required_columns} not found in {file_path}")
        return pd.DataFrame()

def CP_grapher(folder_path):
    all_mpts = read_mpt_files(folder_path)

    data_extracted = pd.DataFrame()

    for file_path in all_mpts:
        header_extracted = determine_header_lines(file_path)
        data_extracted = pd.concat([data_extracted, extract_time_and_voltage(file_path, header_extracted)], ignore_index=True)
        extract_time_and_voltage(file_path, header_extracted).to_csv(file_path.replace(".mpt",".csv"), index=False, encoding='utf-8')

    return data_extracted

"""def CV_grapher(folder_path):
    all_CVs = 
    pass
"""

if __name__ == "__main__":
    CP_grapher("/Users/genkioyafuso/Documents/Sacci_lab/STC_grapher/data_dir/")
