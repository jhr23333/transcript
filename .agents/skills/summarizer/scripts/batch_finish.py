import os
import sys
import re
import subprocess

def batch_finish(folder_path):
    """
    扫描文件夹中的 temp_chunk_*.md 文件，合并它们，
    自动清除其中的录音标注注释，并转换为 QA_Summary.docx。
    """
    # 1. 收集切片文件并按数值顺序排序
    chunk_pattern = re.compile(r'temp_chunk_(\d+)\.md')
    chunks = []

    for filename in os.listdir(folder_path):
        match = chunk_pattern.search(filename)
        if match:
            chunks.append((int(match.group(1)), filename))

    # 按照切片编号进行升序排序
    chunks.sort()

    if not chunks:
        print(f"未在 {folder_path} 中找到 temp_chunk_*.md 文件")
        return

    output_md = os.path.join(folder_path, "QA_Summary.md")

    # 2. 合并切片内容并进行正则清洗
    print(f"正在合并 {len(chunks)} 个切片...")
    merged_content = ""
    for index, filename in chunks:
        chunk_path = os.path.join(folder_path, filename)
        with open(chunk_path, 'r', encoding='utf-8') as f_in:
            merged_content += f_in.read() + "\n\n"
        print(f"  已添加 {filename}")

    # 直接在合并内容中清除带有“录音”字样的中英文括号标注，例如“（录音称 XXX）”或“（录音原话口误）”
    print("正在自动清洗录音标注注释...")
    merged_content = re.sub(r'（录音.*?）', '', merged_content)
    merged_content = re.sub(r'\(录音.*?\)', '', merged_content)
    merged_content = re.sub(r'（录音原话口误.*?）', '', merged_content)
    merged_content = re.sub(r'\(录音原话口误.*?\)', '', merged_content)
    # 清理可能残留的多余空格
    merged_content = re.sub(r' +', ' ', merged_content)

    # 将清洗并合并后的完整 Markdown 写入最终的目标文件
    print(f"正在写入合并后的文件: {output_md}")
    with open(output_md, 'w', encoding='utf-8') as f_out:
        f_out.write(merged_content)

    # 3. 调用 md2word.py 进行 Word 转换
    # 获取当前脚本所在目录以定位同目录下的 md2word.py 转换脚本
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    md2word_path = os.path.join(scripts_dir, "md2word.py")
    output_docx = os.path.join(folder_path, "QA_Summary.docx")

    print(f"正在将 {output_md} 转换为 {output_docx}...")
    try:
        # 执行转换脚本进行排版与格式化输出
        subprocess.run([sys.executable, md2word_path, output_md, output_docx], check=True)
        print("成功完成合并、清洗与 Word 转换一键化处理！")
    except subprocess.CalledProcessError as e:
        print(f"Word 转换过程中发生错误: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python batch_finish.py <专属目录路径>")
        sys.exit(1)

    target_folder = sys.argv[1]
    batch_finish(target_folder)
