import os
import re
import csv
import subprocess


def csv_to_md(caption,csv_name):
	if caption:
		caption = '\n:'+caption
	with open(csv_name,encoding='utf-8') as csv_file:
		list_table = list(csv.reader(csv_file))
	list_table.insert(1,['-']*len(list_table[0]))
	md_table = ['|'.join(i)+'\n' for i in list_table]
	return str().join(md_table)+caption

def src_to_table(md):
	list_csv = re.findall(r'!\[.*?\]\(.+?\.csv\)',md)
	for i in list_csv:
		table_info = re.split(r'[\(\)\[\]]',i)
		table = csv_to_md(table_info[1],table_info[3])
		md = md.replace(i,table)
	return md

def mmd_to_svg(md):
	if '```mermaid' in md:
		subprocess.run(['mmdc.cmd','-i','init.md','-o','_temp_.md'])
		with open('_temp_.md',encoding='utf-8') as md_file:
			md = md_file.read()
	return md

def md_to_docx(md):
	cmd = ['pandoc','-f','markdown','-C','-o','init.docx','--quiet']
	if os.path.exists('reference.docx'):
		cmd.append('--reference-doc=reference.docx')
	subprocess.run(cmd,input=md.encode())

def main():
	with open('init.md',encoding='utf-8') as md_file:
		md = md_file.read()
	md_to_docx(src_to_table(mmd_to_svg(md)))
	subprocess.run(['cmd','/c','del','_temp_*'])

main()
