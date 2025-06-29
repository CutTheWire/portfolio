import subprocess
import os
from datetime import datetime

def get_available_tags():
    """사용 가능한 태그 목록 반환"""
    try:
        tags = subprocess.check_output(
            ["git", "tag", "--sort=-version:refname"]
        ).decode().strip().split('\n')
        return [tag for tag in tags if tag]  # 빈 문자열 제거
    except subprocess.CalledProcessError:
        return []

def get_changes_between_tags(tag1, tag2):
    """두 태그 사이의 변경사항 분석"""
    try:
        # 파일별 변경 상태 조회
        diff_output = subprocess.check_output(
            ["git", "diff", "--name-status", f"{tag1}..{tag2}"]
        ).decode().strip().split('\n')
        
        changes = {
            'added': [],
            'modified': [],
            'deleted': [],
            'renamed': []
        }
        
        for line in diff_output:
            if not line:
                continue
                
            parts = line.split('\t')
            status = parts[0]
            
            if status == 'A':
                changes['added'].append(parts[1])
            elif status == 'M':
                changes['modified'].append(parts[1])
            elif status == 'D':
                changes['deleted'].append(parts[1])
            elif status.startswith('R'):
                changes['renamed'].append(f"{parts[1]} → {parts[2]}")
        
        return changes
    except subprocess.CalledProcessError as e:
        print(f"Error getting changes: {e}")
        return None

def get_file_diff(filepath, tag1, tag2):
    """특정 파일의 변경 내용 조회"""
    try:
        diff = subprocess.check_output(
            ["git", "diff", f"{tag1}..{tag2}", "--", filepath]
        ).decode()
        return diff
    except subprocess.CalledProcessError:
        return None

def generate_markdown_report(tag1, tag2, output_file="changes_report.md"):
    """마크다운 보고서 생성"""
    changes = get_changes_between_tags(tag1, tag2)
    if not changes:
        print("변경사항을 가져올 수 없습니다.")
        return
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Changes between {tag1} and {tag2}\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # 요약 섹션
        f.write("## Summary\n\n")
        f.write(f"- **Added files**: {len(changes['added'])}\n")
        f.write(f"- **Modified files**: {len(changes['modified'])}\n")
        f.write(f"- **Deleted files**: {len(changes['deleted'])}\n")
        f.write(f"- **Renamed files**: {len(changes['renamed'])}\n\n")
        
        # 추가된 파일
        if changes['added']:
            f.write("## 🆕 Added Files\n\n")
            for file in changes['added']:
                f.write(f"- `{file}`\n")
            f.write("\n")
        
        # 수정된 파일
        if changes['modified']:
            f.write("## ✏️ Modified Files\n\n")
            for file in changes['modified']:
                f.write(f"- `{file}`\n")
            f.write("\n")
        
        # 삭제된 파일
        if changes['deleted']:
            f.write("## 🗑️ Deleted Files\n\n")
            for file in changes['deleted']:
                f.write(f"- `{file}`\n")
            f.write("\n")
        
        # 이름 변경된 파일
        if changes['renamed']:
            f.write("## 📝 Renamed Files\n\n")
            for file in changes['renamed']:
                f.write(f"- `{file}`\n")
            f.write("\n")
        
        # 상세 변경사항
        f.write("## 📋 Detailed Changes\n\n")
        
        # 수정된 파일들의 diff 표시
        for file in changes['modified']:
            diff = get_file_diff(file, tag1, tag2)
            if diff:
                f.write(f"### {file}\n\n")
                f.write("```diff\n")
                f.write(diff)
                f.write("```\n\n")
        
        # 새로 추가된 파일 내용
        for file in changes['added']:
            try:
                content = subprocess.check_output(
                    ["git", "show", f"{tag2}:{file}"]
                ).decode()
                f.write(f"### {file} (New File)\n\n")
                file_ext = os.path.splitext(file)[1]
                lang = {'.py': 'python', '.js': 'javascript', '.md': 'markdown', 
                       '.html': 'html', '.css': 'css', '.json': 'json'}.get(file_ext, '')
                f.write(f"```{lang}\n")
                f.write(content)
                f.write("```\n\n")
            except subprocess.CalledProcessError:
                f.write(f"### {file} (New File)\n\n")
                f.write("Could not retrieve file content.\n\n")

def document_changes_for_tag(tag):
    try:
        commit_hash = subprocess.check_output(
            ["git", "rev-list", "-n", "1", tag]
        ).decode().strip()
    except subprocess.CalledProcessError:
        print(f"Tag '{tag}' does not exist.")
        return

    # 해당 커밋의 변경사항 조회
    diff_output = subprocess.check_output(
        ["git", "diff-tree", "--no-commit-id", "--name-status", "-r", commit_hash]
    ).decode().splitlines()

    changed_files = []
    new_files = []

    for line in diff_output:
        status, filename = line.split("\t", 1)
        changed_files.append(filename)
        if status == "A":
            new_files.append(filename)

    # 문서 형태로 출력
    print(f"# Changes for tag {tag}")
    print("## Changed Files")
    for f in changed_files:
        print(f"- {f}")
    print("## New Files")
    for f in new_files:
        print(f"- {f}")

tag = "v1.2.0"
document_changes_for_tag(tag)

def main():
    """메인 함수"""
    tags = get_available_tags()
    
    if not tags:
        print("사용 가능한 태그가 없습니다.")
        return
    
    print("사용 가능한 태그:")
    for i, tag in enumerate(tags, 1):
        print(f"{i}. {tag}")
    
    try:
        choice1 = int(input("\n첫 번째 태그 번호를 선택하세요: ")) - 1
        choice2 = int(input("두 번째 태그 번호를 선택하세요: ")) - 1
        
        if 0 <= choice1 < len(tags) and 0 <= choice2 < len(tags):
            tag1 = tags[choice1]
            tag2 = tags[choice2]
            
            print(f"\n{tag1}과 {tag2} 사이의 변경사항을 분석 중...")
            
            output_file = f"changes_{tag1}_to_{tag2}.md"
            generate_markdown_report(tag1, tag2, output_file)
            
            print(f"보고서가 '{output_file}'에 생성되었습니다.")
        else:
            print("잘못된 선택입니다.")
    
    except ValueError:
        print("숫자를 입력해주세요.")
    except KeyboardInterrupt:
        print("\n작업이 취소되었습니다.")

if __name__ == "__main__":
    main()