import subprocess
import os
from datetime import datetime

def get_available_tags():
    """사용 가능한 태그 목록 반환"""
    try:
        tags = subprocess.check_output(
            ["git", "tag", "--sort=-version:refname"]
        ).decode('utf-8', errors='ignore').strip().split('\n')
        return [tag for tag in tags if tag]  # 빈 문자열 제거
    except subprocess.CalledProcessError:
        return []

def get_changes_between_tags(tag1, tag2):
    """두 태그 사이의 변경사항 분석 (tag1과 tag2 모두 포함)"""
    try:
        # 첫 번째 태그가 첫 번째 커밋인지 확인
        try:
            subprocess.check_output(
                ["git", "rev-parse", f"{tag1}^"], 
                stderr=subprocess.DEVNULL
            )
            # tag1^가 존재하면 tag1^..tag2 범위 사용
            range_spec = f"{tag1}^..{tag2}"
        except subprocess.CalledProcessError:
            # tag1^가 존재하지 않으면 (첫 번째 커밋) tag2까지의 모든 변경사항
            range_spec = f"{tag2}"
        
        # 파일별 변경 상태 조회
        diff_output = subprocess.check_output(
            ["git", "diff", "--name-status", range_spec]
        ).decode('utf-8', errors='ignore').strip().split('\n')
        
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

def get_file_author_info(filepath, tag1, tag2):
    """특정 파일의 최신 작성자 정보 조회"""
    try:
        # 첫 번째 태그가 첫 번째 커밋인지 확인
        try:
            subprocess.check_output(
                ["git", "rev-parse", f"{tag1}^"], 
                stderr=subprocess.DEVNULL
            )
            range_spec = f"{tag1}^..{tag2}"
        except subprocess.CalledProcessError:
            range_spec = f"{tag2}"
        
        # 해당 파일을 수정한 커밋들 조회
        log_output = subprocess.check_output([
            "git", "log", "--pretty=format:%an <%ae>|%ad", 
            "--date=short", range_spec, "--", filepath
        ]).decode('utf-8', errors='ignore').strip()
        
        if log_output:
            # 첫 번째 라인이 가장 최신 커밋 정보
            author_info = log_output.split('\n')[0].split('|')
            return {
                'author': author_info[0],
                'date': author_info[1] if len(author_info) > 1 else 'Unknown'
            }
        return None
    except subprocess.CalledProcessError:
        return None

def get_commits_between_tags(tag1, tag2):
    """두 태그 사이의 모든 커밋 정보 조회 (tag1과 tag2 모두 포함)"""
    try:
        # 첫 번째 태그가 첫 번째 커밋인지 확인
        try:
            subprocess.check_output(
                ["git", "rev-parse", f"{tag1}^"], 
                stderr=subprocess.DEVNULL
            )
            range_spec = f"{tag1}^..{tag2}"
        except subprocess.CalledProcessError:
            range_spec = f"{tag2}"
        
        commits = subprocess.check_output([
            "git", "log", "--pretty=format:%H|%an|%ae|%ad|%s", 
            "--date=short", range_spec
        ]).decode('utf-8', errors='ignore').strip().split('\n')
        
        commit_list = []
        for commit in commits:
            if commit:
                parts = commit.split('|')
                if len(parts) >= 5:
                    commit_list.append({
                        'hash': parts[0][:8],  # 짧은 해시
                        'author': parts[1],
                        'email': parts[2],
                        'date': parts[3],
                        'message': parts[4]
                    })
        return commit_list
    except subprocess.CalledProcessError:
        return []

def is_binary_file(filepath):
    """파일이 바이너리인지 확인"""
    binary_extensions = {
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg',
        '.pdf', '.zip', '.tar', '.gz', '.rar', '.7z',
        '.exe', '.dll', '.so', '.dylib',
        '.jar', '.war', '.ear',
        '.mp3', '.mp4', '.avi', '.mov', '.wmv',
        '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'
    }
    
    ext = os.path.splitext(filepath)[1].lower()
    return ext in binary_extensions

def get_file_diff(filepath, tag1, tag2):
    """특정 파일의 변경 내용 조회 (tag1과 tag2 모두 포함)"""
    try:
        # 첫 번째 태그가 첫 번째 커밋인지 확인
        try:
            subprocess.check_output(
                ["git", "rev-parse", f"{tag1}^"], 
                stderr=subprocess.DEVNULL
            )
            range_spec = f"{tag1}^..{tag2}"
        except subprocess.CalledProcessError:
            range_spec = f"{tag2}"
        
        diff = subprocess.check_output(
            ["git", "diff", range_spec, "--", filepath],
            stderr=subprocess.DEVNULL
        ).decode('utf-8', errors='ignore')
        return diff
    except subprocess.CalledProcessError:
        return None

def get_new_file_content(filepath, tag):
    """새로 추가된 파일의 내용을 안전하게 가져오기"""
    try:
        content = subprocess.check_output(
            ["git", "show", f"{tag}:{filepath}"],
            stderr=subprocess.DEVNULL
        ).decode('utf-8', errors='ignore')
        return content
    except subprocess.CalledProcessError:
        # 파일이 해당 태그에 존재하지 않으면 None 반환
        return None

def generate_markdown_report(tag1, tag2, output_file="changes_report.md"):
    """마크다운 보고서 생성 (tag1과 tag2 모두 포함)"""
    changes = get_changes_between_tags(tag1, tag2)
    if not changes:
        print("변경사항을 가져올 수 없습니다.")
        return
    
    # 커밋 정보 조회
    commits = get_commits_between_tags(tag1, tag2)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Changes from {tag1} to {tag2}\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Note**: This report includes changes from {tag1} to {tag2} (both inclusive)\n\n")
        
        # 요약 섹션
        f.write("## Summary\n\n")
        f.write(f"- **Added files**: {len(changes['added'])}\n")
        f.write(f"- **Modified files**: {len(changes['modified'])}\n")
        f.write(f"- **Deleted files**: {len(changes['deleted'])}\n")
        f.write(f"- **Renamed files**: {len(changes['renamed'])}\n")
        f.write(f"- **Total commits**: {len(commits)}\n\n")
        
        # 커밋 히스토리 섹션
        if commits:
            f.write("## 📝 Commit History\n\n")
            for commit in commits:
                f.write(f"- **{commit['hash']}** by {commit['author']} ({commit['date']})\n")
                f.write(f"  {commit['message']}\n\n")
        
        # 추가된 파일
        if changes['added']:
            f.write("## 🆕 Added Files\n\n")
            for file in changes['added']:
                author_info = get_file_author_info(file, tag1, tag2)
                if author_info:
                    f.write(f"- `{file}` - Added by **{author_info['author']}** ({author_info['date']})\n")
                else:
                    f.write(f"- `{file}`\n")
            f.write("\n")
        
        # 수정된 파일
        if changes['modified']:
            f.write("## ✏️ Modified Files\n\n")
            for file in changes['modified']:
                author_info = get_file_author_info(file, tag1, tag2)
                if author_info:
                    f.write(f"- `{file}` - Last modified by **{author_info['author']}** ({author_info['date']})\n")
                else:
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
            if is_binary_file(file):
                author_info = get_file_author_info(file, tag1, tag2)
                f.write(f"### {file} (Binary File)\n")
                if author_info:
                    f.write(f"*Last modified by: **{author_info['author']}** on {author_info['date']}*\n\n")
                f.write("*Binary file - diff not shown*\n\n")
            else:
                diff = get_file_diff(file, tag1, tag2)
                if diff:
                    author_info = get_file_author_info(file, tag1, tag2)
                    f.write(f"### {file}\n")
                    if author_info:
                        f.write(f"*Last modified by: **{author_info['author']}** on {author_info['date']}*\n\n")
                    f.write("```diff\n")
                    f.write(diff)
                    f.write("```\n\n")
        
        # 새로 추가된 파일 내용
        for file in changes['added']:
            if is_binary_file(file):
                author_info = get_file_author_info(file, tag1, tag2)
                f.write(f"### {file} (New Binary File)\n")
                if author_info:
                    f.write(f"*Added by: **{author_info['author']}** on {author_info['date']}*\n\n")
                f.write("*Binary file - content not shown*\n\n")
            else:
                content = get_new_file_content(file, tag2)
                author_info = get_file_author_info(file, tag1, tag2)
                f.write(f"### {file} (New File)\n")
                if author_info:
                    f.write(f"*Added by: **{author_info['author']}** on {author_info['date']}*\n\n")
                
                if content is not None:
                    file_ext = os.path.splitext(file)[1]
                    lang = {'.py': 'python', '.js': 'javascript', '.md': 'markdown', 
                           '.html': 'html', '.css': 'css', '.json': 'json'}.get(file_ext, '')
                    f.write(f"```{lang}\n")
                    f.write(content)
                    f.write("```\n\n")
                else:
                    f.write("*File content not available*\n\n")

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
            
            print(f"\n{tag1}부터 {tag2}까지의 변경사항을 분석 중...")
            
            output_file = f"changes_{tag1}_to_{tag2}.md"
            generate_markdown_report(tag1, tag2, output_file)
            
            print(f"보고서가 '{output_file}'에 생성되었습니다.")
        else:
            print("잘못된 선택입니다.")
    
    except ValueError as e:
        print(f"숫자를 입력해주세요., 오류: {e}")
    except KeyboardInterrupt as e:
        print(f"\n작업이 취소되었습니다., 오류: {e}")

if __name__ == "__main__":
    main()