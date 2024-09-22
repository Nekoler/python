import re
import os
import subprocess

def csv_to_md(csv_name):
	with open(csv_name,encoding='utf-8') as csv:
		res = subprocess.run(['pandoc','-f','csv','-t','markdown'],stdin=csv,stdout=subprocess.PIPE,text=True)
	return res.stdout

def src_to_table(md):
	in_csv = re.findall(r'!\[.*?\]\(.+?\.csv\)',md)
	if in_csv:
		for i in in_csv:
			csv_name = re.split(r'[\(\)\[\]]',i)[-2]
			table = csv_to_md(csv_name)
			md = md.replace(i,table)
		global md_name
		md_name = '_temp_table.md'
		with open(md_name,'w',encoding='utf-8') as new_md:
			new_md.write(md)

def mmd_to_svg(md):
	if '```mermaid' in md:
		global md_name
		subprocess.run(['mmdc.cmd','-p','D:/Portable/Bin/Node.js/node_modules/puppeteerConfigFile.json','-i',md_name,'-o','_temp_.md'])
		md_name = '_temp_.md'

def md_to_docx():
	global md_name
	if os.path.exists('reference.docx'):
		subprocess.run(['pandoc',md_name,'-C','--reference-doc=reference.docx','-o','init.docx','--quiet'])
	else:
		subprocess.run(['pandoc',md_name,'-C','-o','init.docx','--quiet'])

def main():
	global md_name
	md_name = 'init.md'
	md = open(md_name,encoding='utf-8').read()
	src_to_table(md)
	mmd_to_svg(md)
	md_to_docx()
	subprocess.run(['cmd','/c','del','_temp_*'])

main()