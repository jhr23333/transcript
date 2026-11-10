# 专家交流纪要工作流

在 Codex 中把专家访谈、业绩说明会和机构交流的转写稿整理成 Q&A 纪要，保留量化数据、技术术语和追问语境。输出 UTF-8 Markdown 和 Word。

## 使用方式

1. 将本仓库作为 Codex 工作区打开，或把 .agents/skills/summarizer/ 复制到目标项目的同名目录。
2. 安装 Python 3 和 Word 导出依赖，运行下方命令。
3. 提供 UTF-8 转写稿，并请 Codex「把这份转写稿整理成标准 Q&A 纪要」。音频输入需要先用自行配置的工具转写。
4. 在任务目录查看 QA_Summary.md 和 QA_Summary.docx。

```sh
python -m pip install -r requirements.txt
```

[SKILL.md](.agents/skills/summarizer/SKILL.md) 记录保真规则、术语核验、分片处理和交付步骤。模型负责纪要整理和复核，脚本负责切片、合并和导出。

## 手动运行脚本

```sh
python .agents/skills/summarizer/scripts/chunker.py task/transcript_raw.txt task/temp_chunks 3500 200
python .agents/skills/summarizer/scripts/batch_finish.py task
```

运行第二条命令前，先按工作流整理每个切片，并将结果以 temp_chunk_001.md 等顺序编号保存到 task 目录。
