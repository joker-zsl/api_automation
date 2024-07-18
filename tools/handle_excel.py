
from pathlib import Path
from openpyxl import load_workbook

def read_data(exc_path,sheetname):
    """
    这是读取excel表格函数
    :param exc_path: 用例文件的路径
    :param sheetname: 用例表单的名字
    :return:
    """
    wb = load_workbook(exc_path)
    sh = wb[sheetname]
    cases = list(sh.values)  # 所有的用例的列表  [(第一行-title),(第二行用例),(),()]
    title = cases[0] # 得到标题行
    list_case = []
    for case in cases[1:]:
        data = dict(zip(title,case))  # 第一条用例的字典
        list_case.append(data)  # 每一条用例追加到列表里。
    return list_case

if __name__ == '__main__':
    exc_path = Path(__file__).absolute().parent.parent /"datas" / "testcase_mall.xlsx"
    print(read_data(exc_path, "登录"))

