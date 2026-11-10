import os
import sys
import re

def semantic_split(input_file, output_dir, max_chars=2000, overlap_chars=200):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # 使用正则表达式匹配说话人标识，作为切分锚点
    # 兼容 "说话人 1", "说话人 2", "Q:", "A:", "问:", "答:" 等常见前缀
    pattern = re.compile(r'(?=\n说话人\s*\d+|\nQ[:：]|\nA[:：]|\n问[:：]|\n答[:：])')

    # 按照发言段落进行初步分割
    segments = [s.strip() for s in pattern.split('\n' + text) if s.strip()]

    # 进一步切分超大段落
    fine_segments = []
    for segment in segments:
        if len(segment) > max_chars:
            subs = re.split(r'(?<=[。！？\n])', segment)
            temp = ""
            for sub in subs:
                if len(temp) + len(sub) > max_chars:
                    if temp: fine_segments.append(temp)
                    temp = sub
                else:
                    temp += sub
            if temp: fine_segments.append(temp)
        else:
            fine_segments.append(segment)

    chunks = []
    current_chunk = ""

    for seg in fine_segments:
        if not current_chunk:
            current_chunk = seg
        elif len(current_chunk) + len(seg) <= max_chars:
            current_chunk += "\n\n" + seg
        else:
            chunks.append(current_chunk)

            # 生成 overlap 文本
            overlap_text = current_chunk[-overlap_chars:] if len(current_chunk) > overlap_chars else current_chunk
            # 尽量在标点符号后截断，保持句子完整性
            first_punct = re.search(r'[。！？\n]', overlap_text)
            if first_punct and len(overlap_text) - first_punct.end() > 50:
                overlap_text = overlap_text[first_punct.end():].strip()
            else:
                overlap_text = overlap_text.strip()

            current_chunk = f"<OVERLAP_CONTEXT>\n这是一个前置的重叠上下文（上一个切片的结尾片段），仅帮助你理解当前语境，绝对禁止在当前输出中提取、重写或包含这部分重叠内容中的任何数据与对话：\n{overlap_text}\n</OVERLAP_CONTEXT>\n\n" + seg

    if current_chunk:
        chunks.append(current_chunk)

    for i, chunk in enumerate(chunks):
        out_path = os.path.join(output_dir, f"chunk_{i+1:03d}.txt")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(chunk.strip())

    print(f"Success: File semantically split into {len(chunks)} chunks in '{output_dir}'.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python chunker.py <input_file> <output_dir> [max_chars=2000] [overlap_chars=200]")
        print("  max_chars: 目标切片字符数。并行 subagent 模式建议 3000-4000，使每片对应一个 subagent，")
        print("             避免切出十几个碎片导致 subagent 过多。")
        sys.exit(1)
    max_chars = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
    overlap_chars = int(sys.argv[4]) if len(sys.argv) > 4 else 200
    semantic_split(sys.argv[1], sys.argv[2], max_chars, overlap_chars)
