#去除matlab生成fir滤波器空格等

# 1. 读取文件并去除换行符
def remove_newlines(file_path, output_file=None):
    # 打开并读取文件内容
    with open(file_path, 'r',encoding='utf-8') as file:
        content = file.read()
    
    # 2. 去除换行符
    cleaned_content = content.replace('\n', ' ').strip()
    
    # 如果需要将结果保存到新的文件
    if output_file:
        with open(output_file, 'w',encoding='utf-8') as output:
            output.write(cleaned_content)
        print(f"Cleaned content has been saved to {output_file}")
    else:
        # 如果不保存文件，则打印处理后的结果
        print(cleaned_content)

# 运行示例
input_file = r'C:\Users\203\Desktop\fir.txt'  # 使用原始字符串
output_file = r'C:\Users\203\Desktop\out.txt'  # 可选的输出文件路径
remove_newlines(input_file, output_file)