import os
import re
import sys
import subprocess
import argparse
import yaml
from datetime import datetime

def generate_license_text(license_name, copyright_template):
    current_year = datetime.now().year
    formatted_copyright = copyright_template.format(license=license_name, year=current_year)
    indented_copyright = '\n'.join(f'{line}' for line in formatted_copyright.splitlines())
    license_text = f"""{indented_copyright}"""
    return license_text

# 从配置文件加载设置
def load_config(config_path='check_copyright_config.yaml'):
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

# 获取当前提交中新添加的文件列表
def get_new_files():
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-status', 'HEAD~1', 'HEAD'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        new_files = [
            line.split('\t')[1]
            for line in result.stdout.splitlines()
            if line.startswith('A')
        ]
        return new_files
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while retrieving newly added files: {e}")
        sys.exit(1)

# 检查文件的版权声明
def check_copyright(file_path, config):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # 获取当前年份
            current_year = datetime.now().year
            # 检查许可证声明
            for license_name in config['DEFAULT']['allowed_licenses']:
                license_pattern = re.escape(license_name) + r' License'
                if re.search(license_pattern, content):
                    break
            else:
                print(f"\033[31mThe license declaration format of {file_path} is incorrect\033[0m")
                return False
            # 检查版权声明
            copyright_pattern = config['DEFAULT']['espressif_copyright'].format(license=config['DEFAULT']['license_for_new_files'], year=current_year)
            copyright_pattern = re.escape(copyright_pattern)
            if not re.search(copyright_pattern, content):
                print(f"\033[31mThe copyright declaration format of {file_path} is incorrect\033[0m")
                return False
    except FileNotFoundError:
        print(f"\033[31m{file_path} file not found\033[0m")
        return False
    except Exception as e:
        print(f"\033[31mError occurred while checking {file_path}: {e}\033[0m")
        return False
    return True

# 主函数
def main():
    parser = argparse.ArgumentParser(description="Check the copyright declaration of newly added files in the current commit.")
    parser.add_argument(
        '--config',
        default='check_copyright_config.yaml',
        type=str,
        help='Configuration file path'
    )
    parser.add_argument(
        '--replace',
        action='store_true',
        help='Enable replacement functionality'
    )

    parser.add_argument('files', nargs='+', help="Input file list")

    args = parser.parse_args()

    # 加载配置
    config = load_config(args.config)

    if args.files:
        new_files = args.files
    else:
        # 获取当前提交中新添加的文件列表
        new_files = get_new_files()

    if not new_files:
        print("There are no new files in the current commit.")
        sys.exit(0)

    success = True
    for file_path in new_files:
        if not check_copyright(file_path, config):
            success = False

    if success == False:
        license_text = generate_license_text(config['DEFAULT']['license_for_new_files'], config['DEFAULT']['espressif_copyright'])
        print("The correct license format is as follows:")
        print(f"{license_text}")

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
