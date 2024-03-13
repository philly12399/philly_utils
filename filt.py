def select_lines_with_text(file_path, target_text):
    selected_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if target_text in line:
                selected_lines.append(line.strip())
    return selected_lines
n=100
file_path = f'/home/philly12399/philly_data/2024_3_iros_mark/4300/refined-output_{n}/log.txt'  # 更改為您的文件路徑
target_text = 'Tracklen:'  # 更改為您想要選擇的特定文字

selected_lines = select_lines_with_text(file_path, target_text)
tl =0
cl = 0
for line in selected_lines:
    arr = line.split(';')
    l = int(arr[0][9:])
    tl += l
    if(l >= n):
        cl += 1
    
print(f"AVG len: {tl/len(selected_lines)}")
print(f"Track len >= {n}: {cl}")