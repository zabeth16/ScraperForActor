def calculate_next_pages(last_page):
    # 每一页增加的数字，比如每页有30张图片
    page_increment = 30
    
    # 计算接下来的三个页码
    next_pages = [last_page + i * page_increment for i in range(1, 4)]
    
    return next_pages

if __name__ == "__main__":
    # 动态输入上次抓完的页码
    last_page = int(input("请输入上次抓完的页码: "))
    
    # 计算接下来的三个页码
    next_pages = calculate_next_pages(last_page)
    
    # 输出接下来的三个页码
    print("接下来的三个页码是: ", next_pages)