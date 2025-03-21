"""
README自动翻译工具 - 增强版
支持参数配置、进度显示、代码块跳过和错误重试
"""

import argparse
import re
from pathlib import Path
from retrying import retry
from tqdm import tqdm
from googletrans import Translator
import chardet


def detect_file_encoding(file_path):
    """自动检测文件编码"""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding'] if result['confidence'] > 0.7 else 'utf-8'


def split_blocks(content):
    """将内容分割为可翻译段落（跳过代码块）"""
    in_code_block = False
    buffer = []
    blocks = []

    for line in content.split('\n'):
        code_start = re.match(r'^```|^~~~', line.strip())
        if code_start:
            if in_code_block:
                # 结束代码块时保存缓冲区内容
                if buffer:
                    blocks.append(('text', '\n'.join(buffer)))
                    buffer = []
                blocks.append(('code', line))
                in_code_block = False
            else:
                # 开始代码块时保存之前内容
                if buffer:
                    blocks.append(('text', '\n'.join(buffer)))
                    buffer = []
                blocks.append(('code', line))
                in_code_block = True
        else:
            if in_code_block:
                blocks.append(('code', line))
            else:
                buffer.append(line)

    # 添加最后剩余内容
    if buffer:
        blocks.append(('text', '\n'.join(buffer)))

    return blocks


@retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000)
def translate_text(text, translator):
    """带重试机制的翻译函数"""
    if not text.strip():
        return text
    return translator.translate(text, dest='zh-cn').text


def translate_file(input_path, output_path):
    """执行文件翻译"""
    # 初始化翻译器
    translator = Translator()

    try:
        # 检测文件编码
        encoding = detect_file_encoding(input_path)

        # 读取文件内容
        with open(input_path, 'r', encoding=encoding) as f:
            content = f.read()

        # 分割处理块
        blocks = split_blocks(content)

        # 初始化进度条
        total_blocks = sum(1 for b in blocks if b[0] == 'text')
        progress = tqdm(total=total_blocks, desc='翻译进度', unit='block')

        translated_blocks = []
        for block_type, text in blocks:
            if block_type == 'code':
                translated_blocks.append(text)
            else:
                # 翻译文本段落
                translated = translate_text(text, translator)
                translated_blocks.append(translated)
                progress.update(1)

        progress.close()

        # 写入翻译结果
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(translated_blocks))

        print(f"\n翻译完成！文件已保存至 {output_path}")

    except Exception as e:
        print(f"\n翻译失败: {str(e)}")
        raise


if __name__ == "__main__":
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='README翻译工具')
    parser.add_argument('-i', '--input', default='README.md',help='输入文件路径（默认：README.md）')
    parser.add_argument('-o', '--output', default='README_ch.md',help='输出文件路径（默认：readme_ch.md）')

    args = parser.parse_args()

    # 检查输入文件是否存在
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误：输入文件 {args.input} 不存在")
        exit(1)

    # 执行翻译
    translate_file(str(input_path), args.output)