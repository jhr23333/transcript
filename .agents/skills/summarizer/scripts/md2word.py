import sys
import re

try:
    from docx import Document
    from docx.shared import Pt
    from docx.oxml.ns import qn
except ImportError:
    print("未检测到 python-docx 库，请先执行：pip install python-docx")
    sys.exit(1)

def convert_md_to_docx(md_path, docx_path):
    """
    读取 Markdown 文件并将其转换为 Word 文档 (docx)。
    这个函数会将纯文本中的 Q&A 提取并设置对应格式。

    参数:
    md_path: 输入的 markdown 文件路径
    docx_path: 输出的 word 文件路径
    """
    doc = Document()

    # 设置正常段落的基础字体样式
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Microsoft YaHei'  # 使用中文字体如微软雅黑更美观
    font.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    font.size = Pt(11)

    # 以 UTF-8 格式读取合并后的 QA 总文件
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 简单的按双换行分割段落，处理大模型生成的 MD
    paragraphs = content.split('\n\n')
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue

        # 去除 markdown 中可能出现的一些简单星号加粗符
        p = re.sub(r'\*\*(.*?)\*\*', r'\1', p)

        paragraph = doc.add_paragraph()
        # 针对提出的问题部分，对其进行字体加粗高亮显示
        if p.startswith('Q：') or p.startswith('Q:'):
            run = paragraph.add_run(p)
            run.bold = True
        # 处理可能出现的标题
        elif p.startswith('#'):
            header_level = len(p) - len(p.lstrip('#'))
            clean_text = p.lstrip('#').strip()
            doc.add_heading(clean_text, level=min(header_level, 9))
        # 其他正常的答案内容段落
        else:
            paragraph.add_run(p)

    # 保存最后的 word 文档
    doc.save(docx_path)
    print(f"成功将 {md_path} 转换为 {docx_path}")

if __name__ == "__main__":
    # 解析命令行传入的输入输出参数
    if len(sys.argv) < 3:
        print("用法: python md2word.py <输入.md> <输出.docx>")
        sys.exit(1)

    input_md = sys.argv[1]
    output_docx = sys.argv[2]
    convert_md_to_docx(input_md, output_docx)
