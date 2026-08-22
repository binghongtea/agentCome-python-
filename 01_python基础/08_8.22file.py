# f = open('test.txt','w')
#
# f.write('hello world\n')
# f.write('nihao python\n')
#
# f.close()
# def lins():
#     print('-' * 50)
#
# f = open('test.txt','rt')
# print(f.read())
# f.close()
#
# lins()
#
# f = open('test.txt','rt')
# print(f.read(5))
# print(f.read(7))
# f.close()
#
# lins()
#
# f = open('test.txt','rt')
# print(f.readline())
# print(f.readline(3))
# f.close()
#
# lins()
# f = open('test.txt','r', encoding="utf-8")
# print(f.readlines(5))
# f.close()

# import os
#
# for root,dirs,files in os.walk(os.getcwd()):
#       print("当前路径：", root)
#       print("目录：", dirs)
#       print("文件：", files)
#       print()

def copyFile(sorce_file_path,dest_file_path):
    sorce_file = open(sorce_file_path,'r')
    dest_file = open(dest_file_path,'w')

    content = sorce_file.read(1024)
    while content:
        dest_file.write(content)
        content = sorce_file.read(1024)

    sorce_file.close()
    dest_file.close()

copyFile('test.txt','D:/ttt.txt')