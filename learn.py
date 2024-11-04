import tkinter as tk
from tkinter import ttk, filedialog
import os
import random
from datetime import datetime

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("文件浏览器 & 贪吃蛇")
        self.geometry("1000x700")
        
        # 设置主题颜色
        self.configure(bg='#f0f0f0')
        self.style = ttk.Style()
        self.style.configure('TNotebook', background='#f0f0f0')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('Custom.TButton', 
                           padding=5, 
                           background='#4a90e2',
                           foreground='white')
        
        # 创建标签页
        self.notebook = ttk.Notebook(self)
        self.file_browser_frame = FileBrowser(self.notebook)
        self.snake_game_frame = SnakeGame(self.notebook)
        
        self.notebook.add(self.file_browser_frame, text="  📁 文件浏览器  ")
        self.notebook.add(self.snake_game_frame, text="  🐍 贪吃蛇游戏  ")
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

class FileBrowser(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # 创建工具栏
        self.toolbar = ttk.Frame(self)
        self.toolbar.pack(fill='x', padx=10, pady=5)
        
        style = ttk.Style()
        style.configure('Toolbar.TButton', padding=5)
        
        ttk.Button(self.toolbar, 
                  text="📂 打开文件夹", 
                  command=self.open_folder,
                  style='Toolbar.TButton').pack(side='left', padx=5, pady=5)
        ttk.Button(self.toolbar, 
                  text="⬆️ 上级目录", 
                  command=self.go_up,
                  style='Toolbar.TButton').pack(side='left', padx=5, pady=5)
        
        # 当前路径显示
        self.path_var = tk.StringVar()
        ttk.Entry(self.toolbar, 
                 textvariable=self.path_var, 
                 state='readonly',
                 width=80).pack(side='left', padx=5, pady=5, fill='x', expand=True)
        
        # 创建树形视图
        style.configure("Custom.Treeview",
                       background="#ffffff",
                       foreground="#333333",
                       rowheight=25,
                       fieldbackground="#ffffff")
        style.configure("Custom.Treeview.Heading",
                       background="#e1e1e1",
                       foreground="#333333",
                       padding=5)
        
        # 创建带滚动条的框架
        tree_frame = ttk.Frame(self)
        tree_frame.pack(expand=True, fill='both', padx=10, pady=5)
        
        # 滚动条
        scrollbar_y = ttk.Scrollbar(tree_frame)
        scrollbar_y.pack(side='right', fill='y')
        
        scrollbar_x = ttk.Scrollbar(tree_frame, orient='horizontal')
        scrollbar_x.pack(side='bottom', fill='x')
        
        # 树形视图
        self.tree = ttk.Treeview(tree_frame, 
                                columns=('Size', 'Modified', 'Type'),
                                style="Custom.Treeview",
                                yscrollcommand=scrollbar_y.set,
                                xscrollcommand=scrollbar_x.set)
        
        self.tree.heading('#0', text='名称', anchor='w')
        self.tree.heading('Size', text='大小', anchor='w')
        self.tree.heading('Modified', text='修改时间', anchor='w')
        self.tree.heading('Type', text='类型', anchor='w')
        
        self.tree.column('#0', width=300, minwidth=200)
        self.tree.column('Size', width=100, minwidth=80)
        self.tree.column('Modified', width=150, minwidth=100)
        self.tree.column('Type', width=100, minwidth=80)
        
        self.tree.pack(expand=True, fill='both')
        
        # 配置滚动条
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)
        
        # 设置初始目录
        self.current_path = os.getcwd()
        self.update_tree()
        
    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"
        
    def format_time(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
        
    def open_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.current_path = path
            self.update_tree()
            
    def go_up(self):
        self.current_path = os.path.dirname(self.current_path)
        self.update_tree()
        
    def update_tree(self):
        self.path_var.set(self.current_path)
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            # 首先添加文件夹
            folders = []
            files = []
            
            for item in os.listdir(self.current_path):
                full_path = os.path.join(self.current_path, item)
                modified = os.path.getmtime(full_path)
                modified_str = self.format_time(modified)
                
                if os.path.isdir(full_path):
                    folders.append((item, '文件夹', modified_str, '文件夹'))
                else:
                    size = os.path.getsize(full_path)
                    size_str = self.format_size(size)
                    ext = os.path.splitext(item)[1]
                    files.append((item, size_str, modified_str, ext if ext else '文件'))
            
            # 排序并插入
            for item, size, modified, type_ in sorted(folders):
                self.tree.insert('', 'end', text=item, values=(size, modified, type_),
                               image='') # 可以添加文件夹图标
                
            for item, size, modified, type_ in sorted(files):
                self.tree.insert('', 'end', text=item, values=(size, modified, type_),
                               image='') # 可以添加文件图标
                
        except Exception as e:
            print(f"Error: {e}")

class SnakeGame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_game()
        
    def setup_game(self):
        # 游戏控制区域
        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(pady=10)
        
        # 样式设置
        style = ttk.Style()
        style.configure('Game.TButton', 
                       padding=10,
                       font=('Helvetica', 10, 'bold'))
        
        # 分数显示
        self.score_label = ttk.Label(self.control_frame, 
                                   text="分数: 0",
                                   font=('Helvetica', 16, 'bold'))
        self.score_label.pack(side='left', padx=20)
        
        # 控制按钮
        ttk.Button(self.control_frame, 
                  text="🎮 新游戏",
                  command=self.new_game,
                  style='Game.TButton').pack(side='left', padx=10)
        
        # 游戏画布
        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(expand=True, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, 
                              width=600, 
                              height=600, 
                              bg='#1a1a1a',
                              highlightthickness=0)
        self.canvas.pack()
        
        # 游戏说明
        instructions = """
        游戏说明:
        • 使用方向键控制蛇的移动
        • 吃到食物可以增加分数
        • 撞到墙壁或自己会结束游戏
        """
        ttk.Label(self, 
                 text=instructions,
                 font=('Helvetica', 10),
                 justify='left').pack(pady=10)
        
        # 游戏变量
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = 'Right'
        self.food = None
        self.score = 0
        self.game_on = False
        
        # 绑定按键
        self.bind_all('<Key>', self.change_direction)
        
        # 绘制网格
        self.draw_grid()
        
    def draw_grid(self):
        # 绘制淡色网格
        for i in range(0, 600, 20):
            self.canvas.create_line(i, 0, i, 600, fill='#2a2a2a')
            self.canvas.create_line(0, i, 600, i, fill='#2a2a2a')
        
    def new_game(self):
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = 'Right'
        self.score = 0
        self.score_label.config(text=f"分数: {self.score}")
        self.game_on = True
        self.create_food()
        self.update()
        
    def create_food(self):
        x = random.randint(0, 29) * 20
        y = random.randint(0, 29) * 20
        self.food = (x, y)
        
    def move(self):
        head = self.snake[0]
        
        if self.direction == 'Right':
            new_head = (head[0] + 20, head[1])
        elif self.direction == 'Left':
            new_head = (head[0] - 20, head[1])
        elif self.direction == 'Up':
            new_head = (head[0], head[1] - 20)
        else:  # Down
            new_head = (head[0], head[1] + 20)
            
        # 检查是否吃到食物
        if new_head == self.food:
            self.snake.insert(0, new_head)
            self.score += 10
            self.score_label.config(text=f"分数: {self.score}")
            self.create_food()
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()
            
        # 检查碰撞
        if (new_head[0] < 0 or new_head[0] >= 600 or
            new_head[1] < 0 or new_head[1] >= 600 or
            new_head in self.snake[1:]):
            self.game_on = False
            self.canvas.create_text(300, 300,
                                  text=f"游戏结束!\n最终得分: {self.score}\n按新游戏重新开始",
                                  fill='white',
                                  font=('Helvetica', 20, 'bold'),
                                  justify='center')
            return
            
    def change_direction(self, event):
        if event.keysym == 'Up' and self.direction != 'Down':
            self.direction = 'Up'
        elif event.keysym == 'Down' and self.direction != 'Up':
            self.direction = 'Down'
        elif event.keysym == 'Left' and self.direction != 'Right':
            self.direction = 'Left'
        elif event.keysym == 'Right' and self.direction != 'Left':
            self.direction = 'Right'
            
    def update(self):
        self.canvas.delete('all')
        self.draw_grid()
        
        # 绘制食物
        if self.food:
            # 绘制一个圆形的食物
            x, y = self.food
            self.canvas.create_oval(
                x + 2, y + 2,
                x + 18, y + 18,
                fill='#ff4444',
                outline='#ff6666'
            )
        
        # 绘制蛇
        # 头部
        head = self.snake[0]
        self.canvas.create_rectangle(
            head[0], head[1],
            head[0] + 20, head[1] + 20,
            fill='#4CAF50',
            outline='#66BB6A'
        )
        
        # 身体
        for segment in self.snake[1:]:
            self.canvas.create_rectangle(
                segment[0] + 1, segment[1] + 1,
                segment[0] + 19, segment[1] + 19,
                fill='#81C784',
                outline='#A5D6A7'
            )
            
        if self.game_on:
            self.move()
            self.after(100, self.update)

if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()