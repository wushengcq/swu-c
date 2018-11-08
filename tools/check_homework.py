#! /usr/bin/env python2
# -*- encoding=utf-8 -*-
import os
import sys

# 从每个学生目录中提取出指定的作业文件
# 参数 file_name 是作业文件的名字，也可以是一个 ~/assignment/ 目录下的相对路径
def collect(file_name):
	files = []
	for f in os.listdir('/home/'):
		if os.path.isdir(os.path.join('/home/', f)) and (f.startswith('s') or f.startswith('z')):
			files.append(os.path.join('/home/', f + '/assignment/' + file_name))
	return files

# 对作业文件进行批改
# 参数 source_file 是作业代码文件;
# 参数 result_out 是记录作业情况的输出流对象
def correct(source_file, result_out):
	print(source_file)
	uid = source_file[source_file.find("/",1)+1 : source_file.find("/assignment")]
	print(uid)
	# 先打印出学生学号
	result_out.write("<br><br><br><table style='border-collapse:collapse;border:1px solid gray;background-color:#fff' width='95%' cellpadding='10'>\n")
	result_out.write("<tr><td class='usr'>学号后四位</td><td class='usr'>" + uid + "</td></tr>")
	result_out.write("<tr><td style='width:200px'>源代码路径</td><td>" + source_file + "</td></tr>\n")
	if os.path.exists(source_file):
		# 输出代码内容
		printSource(source_file, result_out)
		# 编译代码
		binary_file = gcpp(source_file, result_out)
		# 执行代码
		# execute(binary_file, result_out)
	else:
		result_out.write("<tr><td></td><td class='err'>没有找到源代码文件！</td></tr>\n")
	result_out.write("</table>")

# 将代码原样进行输出
def printSource(source_file, result_out):
	result_out.write("<tr><td>源代码</td><td><pre>\n")
	with open(source_file, 'r') as f:
		for line in f:
			line = line.replace("<", "&lt;")
			line = line.replace(">", "&gt;")
			result_out.write(line)
	result_out.write("</pre></td></tr>\n")

# 对C源代码进行编译
def gcc(source_file, result_out):
	result_out.write("<tr><td>代码编译</td>")
	binary_file = "./" + source_file[source_file.rfind("/") + 1:source_file.rfind(".")] + ".out"
	if os.path.exists(binary_file):
		os.remove(binary_file)

	cmd = "gcc -std=c99 -Wall -o " + binary_file + " " + source_file + " -lm"
	print(cmd)
	result_out.write("<td><pre>\n" + cmd + "\n\n")
	fi,fo,fe = os.popen3(cmd)
	for i in fe.readlines():
		result_out.write(i)

	result_out.write("</pre></td></tr>\n")
	return binary_file

# 对C++源代码进行编译
def gcpp(source_file, result_out):
	result_out.write("<tr><td>代码编译</td>")
	binary_file = "./" + source_file[source_file.rfind("/") + 1:source_file.rfind(".")] + ".out"
	if os.path.exists(binary_file):
		os.remove(binary_file)

	cmd = "g++ -Wall -o " + binary_file + " " + source_file + " -lm"
	print(cmd)
	result_out.write("<td><pre>\n" + cmd + "\n\n")
	fi,fo,fe = os.popen3(cmd)
	for i in fe.readlines():
		result_out.write(i)

	result_out.write("</pre></td></tr>\n")
	return binary_file

# 执行代码，输出执行结果
def execute(execute_file, result_out):
	result_out.write("<tr><td>执行结果</td>")
	if not os.path.exists(execute_file):
		result_out.write("<td class='fail'>源代码编译失败</td></tr>")
		return		

	result_out.write("<td><pre>\n")
	fi,fo,fe = os.popen3(execute_file)
	for i in fo.readlines():
		result_out.write(i)
	for i in fe.readlines():
		result_out.write(i)
	result_out.write("</pre></td></tr>")
	

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Usage：\n\tcheck_homework.py <file_path_under_assignment_dir>\n")
		exit()

	file_path = sys.argv[1]
	# 指定nginx下的网站目录，以便可以直接通过浏览器访问结果
	prefix = "/usr/share/nginx/c/assignment/"
	out = open(prefix + "./" + file_path.replace("/", "_") + ".html", 'w')
	out.write("<html><head><meta charset='utf-8'><style>.err{background-color:#f8bbd0}\n" 
		+ ".fail{background-color:#e1bee7}\n"
		+ ".usr{background-color:#bbdefb}\n"
		+ "td{border:1px solid gray}\n"\
		+ "pre{white-space:pre-wrap;}</style></head><body style='background-color:#333'>")

	fs = collect(file_path)
	count = 0
	for f in fs:
		correct(f, out)
		count += 1
		if count > 60:
			break
	
	out.write("<br><br><br></body></html>")
	out.close(); 
