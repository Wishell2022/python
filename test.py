import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import json
import matplotlib.pyplot as plt

# 全局变量来存储文件路径
file_path = None

# 浏览文件的函数
def browse_file():
    global file_path
    file_path = filedialog.askopenfilename(
        title="选择一个文件",
        filetypes=[("所有文件", "*.*"), ("文本文件", "*.txt"), ("Python文件", "*.py")]
    )
    if file_path:
        messagebox.showinfo("文件路径", f"你选择的文件路径为:\n{file_path}")

# 打印文件路径的函数
def print_file_path():
    if file_path:
        print("文件路径为:", file_path)
    else:
        print("未选择文件")

# 提取 CHA 和 CHB 的值并绘图的函数
def extract_cha_chb(row):
    try:
        # 转换为字典
        record = json.loads(row)
        # 获取 "CHA" 和 "CHB" 的值
        cha_value = record.get("CHA", None)
        chb_value = record.get("CHB", None)
        return cha_value, chb_value
    except json.JSONDecodeError:
        return None, None

def extract_and_plot():
    if not file_path:
        messagebox.showwarning("警告", "请先选择一个文件")
        return
    
    data = pd.read_excel(file_path, sheet_name='Sheet1')
    data[['CHA_value', 'CHB_value']] = data.iloc[:, 0].apply(extract_cha_chb).apply(pd.Series)
    cha_chb_values = data[['CHA_value', 'CHB_value']].dropna()
    cha_chb_values.plot(kind='line', title='CHA 和 CHB 值的折线图')
    plt.show()

# 创建主窗口
root = tk.Tk()
root.title("文件浏览器")
root.geometry("400x200")

# 创建并放置按钮
file_button = tk.Button(root, text="选择文件", command=browse_file)
file_button.pack(pady=20)

print_button = tk.Button(root, text="打印文件路径", command=print_file_path)
print_button.pack(pady=20)

plot_button = tk.Button(root, text="提取CHA和CHB", command=extract_and_plot)
plot_button.pack(pady=20)

# 启动主窗口循环
root.mainloop()
