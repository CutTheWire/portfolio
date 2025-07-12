import subprocess
import os
from datetime import datetime

def get_git_tags_info():
    """Git 태그들의 정보를 가져오는 함수"""
    try:
        # 모든 태그를 버전 순으로 정렬하여 가져오기
        tags = subprocess.check_output(
            ["git", "tag", "--sort=-version:refname"]
        ).decode('utf-8', errors='ignore').strip().split('\n')
        
        # 빈 태그 제거
        tags = [tag for tag in tags if tag.strip()]
        
        if not tags:
            print("태그가 없습니다.")
            return []
        
        tag_info_list = []
        
        print(f"총 {len(tags)}개의 태그를 발견했습니다.")
        
        for tag in tags:
            try:
                # 태그의 전체 커밋 해시 가져오기
                commit_hash = subprocess.check_output(
                    ["git", "rev-list", "-n", "1", tag]
                ).decode('utf-8', errors='ignore').strip()
                
                # 태그의 날짜 정보 가져오기 (태그가 생성된 날짜)
                # 먼저 태그 객체의 날짜를 시도
                try:
                    tag_date = subprocess.check_output(
                        ["git", "log", "-1", "--format=%cd", "--date=format:%Y-%m-%d (%a) %H:%M:%S GMT%z", tag]
                    ).decode('utf-8', errors='ignore').strip()
                except subprocess.CalledProcessError:
                    # 태그 객체가 없으면 커밋 날짜 사용
                    tag_date = subprocess.check_output(
                        ["git", "show", "-s", "--format=%cd", "--date=format:%Y-%m-%d (%a) %H:%M:%S GMT%z", tag]
                    ).decode('utf-8', errors='ignore').strip()
                
                # 한국어 요일로 변환
                korean_days = {
                    'Mon': '월', 'Tue': '화', 'Wed': '수', 'Thu': '목',
                    'Fri': '금', 'Sat': '토', 'Sun': '일'
                }
                
                for eng, kor in korean_days.items():
                    tag_date = tag_date.replace(f'({eng})', f'({kor})')
                
                # GMT+0900를 (한국 표준시)로 변경
                tag_date = tag_date.replace('GMT+0900', '(한국 표준시)')
                
                tag_info = {
                    'tag': tag,
                    'commit_hash': commit_hash,
                    'date': tag_date
                }
                
                tag_info_list.append(tag_info)
                print(f"처리 완료: {tag}")
                
            except subprocess.CalledProcessError as e:
                print(f"태그 {tag} 처리 중 오류 발생: {e}")
                continue
        
        return tag_info_list
        
    except subprocess.CalledProcessError as e:
        print(f"Git 명령어 실행 오류: {e}")
        return []
    except Exception as e:
        print(f"예상치 못한 오류: {e}")
        return []

def save_tags_to_txt(tag_info_list, filename="git_tags_info.txt"):
    """태그 정보를 txt 파일로 저장하는 함수"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Git 태그 정보\n")
            f.write("=" * 80 + "\n")
            f.write(f"생성 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"총 태그 수: {len(tag_info_list)}\n")
            f.write("=" * 80 + "\n\n")
            
            for i, tag_info in enumerate(tag_info_list, 1):
                f.write(f"{i:2d}. 태그: {tag_info['tag']}\n")
                f.write(f"    커밋 해시: {tag_info['commit_hash']}\n")
                f.write(f"    생성 날짜: {tag_info['date']}\n")
                f.write("-" * 60 + "\n")
        
        print(f"\n태그 정보가 '{filename}' 파일에 저장되었습니다.")
        return True
        
    except Exception as e:
        print(f"파일 저장 중 오류 발생: {e}")
        return False

def main():
    """메인 함수"""
    print("Git 태그 정보 추출 중...")
    print("=" * 50)
    
    # 현재 디렉토리가 Git 리포지토리인지 확인
    try:
        subprocess.check_output(["git", "rev-parse", "--git-dir"], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("현재 디렉토리가 Git 리포지토리가 아닙니다.")
        return
    
    # 태그 정보 가져오기
    tag_info_list = get_git_tags_info()
    
    if not tag_info_list:
        print("가져올 태그 정보가 없습니다.")
        return
    
    # 파일명 생성 (현재 날짜/시간 포함)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"git_tags_info_{timestamp}.txt"
    
    # 사용자에게 파일명 확인
    print(f"\n파일명: {filename}")
    user_input = input("파일명을 변경하시겠습니까? (y/N): ").strip().lower()
    
    if user_input in ['y', 'yes']:
        custom_filename = input("새 파일명을 입력하세요 (.txt 확장자 제외): ").strip()
        if custom_filename:
            filename = custom_filename + ".txt"
    
    # 파일로 저장
    if save_tags_to_txt(tag_info_list, filename):
        print(f"✅ 성공적으로 {len(tag_info_list)}개의 태그 정보를 저장했습니다.")
        
        # 간단한 미리보기 출력
        print("\n📋 미리보기 (최근 3개 태그):")
        print("-" * 50)
        for tag_info in tag_info_list[:3]:
            print(f"🏷️  {tag_info['tag']}")
            print(f"📅 {tag_info['date']}")
            print(f"🔗 {tag_info['commit_hash'][:8]}...")
            print()
    else:
        print("❌ 파일 저장에 실패했습니다.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  작업이 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n💥 예상치 못한 오류 발생: {e}")