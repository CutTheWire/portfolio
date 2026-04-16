import json
import os
import aiohttp
import asyncio
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

class GitHubAPI:
    """GitHub REST API 클래스"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.username = "CutTheWire"  # GitHub 사용자명
        self.token = os.getenv("GIT_TOKEN")  # 개인 토큰
        self.treenut_token = os.getenv("GIT_TREENUT_TOKEN")  # TreeNut-KR 조직 토큰
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Portfolio-Backend/1.0"
        }
        self.cache_dir = Path(__file__).resolve().parents[1] / "cache"
        self.cache_file = self.cache_dir / "github_cache.json"
        self.cache_expiration = timedelta(hours=24)
        self._lock = asyncio.Lock()
        self.last_refresh: Optional[datetime] = None
        self.cache = {
            "repositories": None,
            "user_info": None,
            "repository_details": {},
            "repository_languages": {},
            "contributions": {},
            "activity_overview": None
        }
        
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
            print(f"✅ GitHub 개인 토큰 설정됨: {self.token[:8]}...")
        else:
            print("⚠️ GitHub 개인 토큰이 설정되지 않았습니다.")
            
        if self.treenut_token:
            print(f"✅ TreeNut-KR 조직 토큰 설정됨: {self.treenut_token[:8]}...")
        else:
            print("⚠️ TreeNut-KR 조직 토큰이 설정되지 않았습니다.")

    async def initialize_cache(self):
        """서버 시작 시 캐시를 초기화합니다."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cache_loaded = await self._load_cache_from_disk()

        if cache_loaded and not self._is_cache_expired():
            print("✅ GitHub 캐시가 디스크에서 로드되었습니다.")
            return

        print("🔄 GitHub 캐시가 없거나 만료되어 새로 로드합니다.")
        await self.refresh_cache()

    def _is_cache_expired(self) -> bool:
        if not self.last_refresh:
            return True
        return datetime.now(timezone.utc) - self.last_refresh >= self.cache_expiration

    async def _load_cache_from_disk(self) -> bool:
        if not self.cache_file.exists():
            return False

        try:
            data = await asyncio.to_thread(self._read_cache_file)

            if not isinstance(data, dict):
                return False

            self.cache = data.get("cache", self.cache)
            last_refresh = data.get("last_refresh")

            if last_refresh:
                self.last_refresh = datetime.fromisoformat(last_refresh)
            return True
        except Exception as e:
            print(f"❌ 캐시 파일 로드 실패: {str(e)}")
            return False

    def _read_cache_file(self):
        with open(self.cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    async def _save_cache_to_disk(self):
        try:
            await asyncio.to_thread(self._write_cache_file)
        except Exception as e:
            print(f"❌ 캐시 파일 저장 실패: {str(e)}")

    def _write_cache_file(self):
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "last_refresh": self.last_refresh.isoformat() if self.last_refresh else None,
                    "cache": self.cache
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

    async def refresh_cache(self):
        """서버에 저장된 캐시가 만료되었을 때 데이터를 갱신합니다."""
        async with self._lock:
            if not self._is_cache_expired():
                return

            try:
                user_info_task = self.fetch_user_info()
                repos_task = self.fetch_repositories(max_repos=100)
                user_info, repositories = await asyncio.gather(user_info_task, repos_task)

                if user_info:
                    self.cache["user_info"] = user_info
                if repositories is not None:
                    self.cache["repositories"] = repositories

                self.last_refresh = datetime.now(timezone.utc)
                await self._save_cache_to_disk()
                print("✅ GitHub 캐시가 갱신되었습니다.")
            except Exception as e:
                print(f"❌ GitHub 캐시 갱신 실패: {str(e)}")

    async def get_repositories_cached(self, max_repos: int = 100) -> Optional[List[Dict]]:
        if self._is_cache_expired():
            await self.refresh_cache()

        if self.cache["repositories"] is None:
            self.cache["repositories"] = await self.fetch_repositories(max_repos=100)
            if self.cache["repositories"] is not None:
                self.last_refresh = datetime.now(timezone.utc)
                await self._save_cache_to_disk()

        if self.cache["repositories"] is None:
            return None

        return self.cache["repositories"][:max_repos]

    async def get_user_info_cached(self) -> Optional[Dict]:
        if self._is_cache_expired():
            await self.refresh_cache()

        if self.cache["user_info"] is None:
            self.cache["user_info"] = await self.fetch_user_info()
            if self.cache["user_info"] is not None:
                self.last_refresh = datetime.now(timezone.utc)
                await self._save_cache_to_disk()

        return self.cache["user_info"]

    async def get_repository_details_cached(self, repo_name: str) -> Optional[Dict]:
        if self._is_cache_expired():
            await self.refresh_cache()

        cached = self.cache["repository_details"].get(repo_name)
        if cached:
            return cached

        repository = await self.fetch_repository_details(repo_name)
        if repository:
            self.cache["repository_details"][repo_name] = repository
            await self._save_cache_to_disk()

        return repository

    async def get_repository_languages_cached(self, repo_name: str) -> Optional[Dict]:
        if self._is_cache_expired():
            await self.refresh_cache()

        cached = self.cache["repository_languages"].get(repo_name)
        if cached is not None:
            return cached

        languages = await self.fetch_repository_languages(repo_name)
        if languages is not None:
            self.cache["repository_languages"][repo_name] = languages
            await self._save_cache_to_disk()

        return languages

    async def get_user_contributions_cached(self, years: List[int]) -> Optional[Dict]:
        if self._is_cache_expired():
            await self.refresh_cache()

        key = ",".join(str(year) for year in sorted(years))
        cached = self.cache["contributions"].get(key)
        if cached is not None:
            return cached

        contributions = await self.fetch_user_contributions(years=years)
        if contributions is not None:
            self.cache["contributions"][key] = contributions
            await self._save_cache_to_disk()

        return contributions

    async def get_activity_overview_cached(self) -> Optional[Dict]:
        if self._is_cache_expired():
            await self.refresh_cache()

        if self.cache["activity_overview"] is None:
            self.cache["activity_overview"] = await self.fetch_user_activity_overview()
            if self.cache["activity_overview"] is not None:
                self.last_refresh = datetime.now(timezone.utc)
                await self._save_cache_to_disk()

        return self.cache["activity_overview"]

    async def fetch_repositories(self, max_repos: int = 100) -> Optional[List[Dict]]:
        """
        GitHub API에서 리포지토리 목록 가져오기 (전체 리포지토리)
        """
        try:
            all_repos = []
            page = 1
            per_page = 30
            
            while len(all_repos) < max_repos:
                url = f"{self.base_url}/users/{self.username}/repos"
                params = {
                    "sort": "updated",
                    "per_page": per_page,
                    "page": page,
                    "type": "owner"  # 포크된 리포지토리 제외
                }
                
                print(f"🔄 GitHub API 요청: 페이지 {page}")
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=self.headers, params=params) as response:
                        print(f"📡 GitHub API 응답 상태: {response.status}")
                        
                        if response.status == 200:
                            repos = await response.json()
                            
                            if not repos:  # 더 이상 리포지토리가 없으면 종료
                                break
                                
                            # 포크된 리포지토리 필터링
                            filtered_repos = [repo for repo in repos if not repo.get("fork", False)]
                            all_repos.extend(filtered_repos)
                            
                            print(f"📦 페이지 {page}에서 {len(filtered_repos)}개 리포지토리 추가 (총 {len(all_repos)}개)")
                            
                            if len(repos) < per_page:  # 마지막 페이지인 경우
                                break
                                
                            page += 1
                        else:
                            error_text = await response.text()
                            print(f"❌ GitHub API Error: {response.status} - {error_text}")
                            break
            
            # 최대 개수만큼 자르기
            all_repos = all_repos[:max_repos]
            processed_repos = [self._process_repository(repo) for repo in all_repos]
            print(f"📦 최종 처리된 리포지토리 수: {len(processed_repos)}")
            return processed_repos
                        
        except Exception as e:
            print(f"❌ GitHub API 요청 실패: {str(e)}")
            return None
    
    async def fetch_user_info(self) -> Optional[Dict]:
        """
        GitHub 사용자 정보 가져오기
        """
        try:
            url = f"{self.base_url}/users/{self.username}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        user_data = await response.json()
                        return self._process_user_info(user_data)
                    else:
                        print(f"GitHub User API Error: {response.status}")
                        return None
                        
        except Exception as e:
            print(f"GitHub User API 요청 실패: {str(e)}")
            return None
    
    async def fetch_repository_details(self, repo_name: str) -> Optional[Dict]:
        """
        특정 리포지토리의 상세 정보 가져오기
        """
        try:
            url = f"{self.base_url}/repos/{self.username}/{repo_name}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        repo_data = await response.json()
                        return self._process_repository(repo_data)
                    else:
                        print(f"GitHub Repository API Error: {response.status}")
                        return None
                        
        except Exception as e:
            print(f"GitHub Repository API 요청 실패: {str(e)}")
            return None
    
    async def fetch_repository_languages(self, repo_name: str) -> Optional[Dict]:
        """
        리포지토리의 언어 통계 가져오기
        """
        try:
            url = f"{self.base_url}/repos/{self.username}/{repo_name}/languages"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {}
                        
        except Exception as e:
            print(f"GitHub Languages API 요청 실패: {str(e)}")
            return {}
    
    async def fetch_user_contributions(self, years: List[int] = None) -> Optional[Dict]:
        """
        GitHub 사용자의 기여도 정보 가져오기 (개인 + TreeNut-KR 조직 통합)
        """
        if not years:
            years = [2023, 2024, 2025]
            
        try:
            all_contributions = {}  # 전체 기여도를 날짜별로 통합
            total_contributions = 0
            
            for year in years:
                print(f"📊 {year}년 기여도 조회 시작...")
                
                # 개인 기여도 조회
                personal_contributions = await self._fetch_personal_contributions(year)
                
                # TreeNut-KR 조직 기여도 조회
                org_contributions = await self._fetch_treenut_contributions(year)
                
                # 연도별 기여도 통합
                if personal_contributions:
                    for week in personal_contributions["contributionCalendar"]["weeks"]:
                        for day in week["contributionDays"]:
                            date = day["date"]
                            count = day["contributionCount"]
                            
                            # 조직 기여도 추가
                            if date in org_contributions:
                                count += org_contributions[date]
                            
                            all_contributions[date] = count
                            total_contributions += count
                
                    # 조직에만 있는 기여도 추가
                    for date, count in org_contributions.items():
                        if date not in all_contributions:
                            all_contributions[date] = count
                            total_contributions += count
                            
                    print(f"✅ {year}년 통합 기여도 처리 완료")
            
            # 통합된 기여도 데이터 반환
            return self._process_unified_contributions(all_contributions, total_contributions)
            
        except Exception as e:
            print(f"❌ GitHub Contributions API 요청 실패: {str(e)}")
            return None

    async def _fetch_personal_contributions(self, year: int) -> Optional[Dict]:
        """
        개인 기여도 조회 (GraphQL)
        """
        try:
            query = f"""
            query {{
              user(login: "{self.username}") {{
                contributionsCollection(
                  from: "{year}-01-01T00:00:00Z", 
                  to: "{year}-12-31T23:59:59Z"
                ) {{
                  contributionCalendar {{
                    totalContributions
                    weeks {{
                      contributionDays {{
                        date
                        contributionCount
                        color
                      }}
                    }}
                  }}
                }}
              }}
            }}
            """
            
            graphql_headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.github.com/graphql",
                    headers=graphql_headers,
                    json={"query": query}
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if "data" in result and result["data"]["user"]:
                            return result["data"]["user"]["contributionsCollection"]
                        else:
                            print(f"GraphQL 개인 기여도 오류: {result.get('errors', 'Unknown error')}")
                            return None
                    else:
                        error_text = await response.text()
                        print(f"❌ 개인 기여도 API 오류: {response.status} - {error_text}")
                        return None
        except Exception as e:
            print(f"❌ 개인 기여도 조회 오류: {str(e)}")
            return None

    async def _fetch_treenut_contributions(self, year: int) -> Dict[str, int]:
        """
        TreeNut-KR 조직에서의 사용자 기여도 조회
        """
        try:
            # TreeNut-KR 토큰을 사용한 헤더
            treenut_headers = {
                "Authorization": f"token {self.treenut_token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Portfolio-Backend/1.0"
            }
            
            org_contributions = {}
            
            # TreeNut-KR 조직의 리포지토리 목록 가져오기
            async with aiohttp.ClientSession() as session:
                # 조직 리포지토리 목록 조회
                repos_url = f"{self.base_url}/orgs/TreeNut-KR/repos"
                async with session.get(repos_url, headers=treenut_headers, params={"per_page": 100}) as response:
                    if response.status == 200:
                        repos = await response.json()
                        print(f"🌳 TreeNut-KR 조직 리포지토리 {len(repos)}개 발견")
                        
                        # 각 리포지토리에서 사용자의 커밋 조회
                        for repo in repos:
                            repo_name = repo["name"]
                            repo_contributions = await self._fetch_repo_user_commits(
                                session, "TreeNut-KR", repo_name, year, treenut_headers
                            )
                            
                            # 날짜별 기여도 합산
                            for date, count in repo_contributions.items():
                                org_contributions[date] = org_contributions.get(date, 0) + count
                    else:
                        error_text = await response.text()
                        print(f"❌ TreeNut-KR 리포지토리 목록 조회 오류: {response.status} - {error_text}")
            
            total_org_contributions = sum(org_contributions.values())
            print(f"🌳 TreeNut-KR 조직에서 {year}년 기여도: {total_org_contributions}개")
            
            return org_contributions
            
        except Exception as e:
            print(f"❌ TreeNut-KR 조직 기여도 조회 오류: {str(e)}")
            return {}

    async def _fetch_repo_user_commits(self, session: aiohttp.ClientSession, owner: str, repo: str, year: int, headers: Dict) -> Dict[str, int]:
        """
        특정 리포지토리에서 사용자의 연간 커밋 수 조회
        """
        try:
            commits_by_date = {}
            page = 1
            
            while True:
                url = f"{self.base_url}/repos/{owner}/{repo}/commits"
                params = {
                    "author": self.username,
                    "since": f"{year}-01-01T00:00:00Z",
                    "until": f"{year}-12-31T23:59:59Z",
                    "per_page": 100,
                    "page": page
                }
                
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        commits = await response.json()
                        
                        if not commits:
                            break
                            
                        for commit in commits:
                            try:
                                commit_date = commit["commit"]["author"]["date"][:10]  # YYYY-MM-DD 형식
                                commits_by_date[commit_date] = commits_by_date.get(commit_date, 0) + 1
                            except (KeyError, TypeError):
                                continue
                        
                        if len(commits) < 100:
                            break
                            
                        page += 1
                    elif response.status == 409:  # Empty repository
                        break
                    else:
                        print(f"⚠️ {owner}/{repo} 커밋 조회 오류: {response.status}")
                        break
            
            return commits_by_date
            
        except Exception as e:
            print(f"❌ {owner}/{repo} 커밋 조회 예외: {str(e)}")
            return {}

    def _merge_contributions(self, personal_data: Dict, org_contributions: Dict[str, int], year: int) -> Optional[Dict]:
        """
        개인 기여도와 조직 기여도 병합
        """
        if not personal_data:
            return None
            
        try:
            # 개인 기여도를 날짜별로 변환
            date_contributions = {}
            
            for week in personal_data["contributionCalendar"]["weeks"]:
                for day in week["contributionDays"]:
                    date_contributions[day["date"]] = {
                        "date": day["date"],
                        "contributionCount": day["contributionCount"],
                        "color": day.get("color", "#ebedf0")
                    }
            
            # 조직 기여도 추가
            org_total = 0
            for date, count in org_contributions.items():
                if date in date_contributions:
                    date_contributions[date]["contributionCount"] += count
                else:
                    # 새로운 날짜 추가
                    date_contributions[date] = {
                        "date": date,
                        "contributionCount": count,
                        "color": self._get_contribution_color(count)
                    }
                org_total += count
            
            # 모든 날짜의 색상과 레벨 재계산
            for date in date_contributions:
                count = date_contributions[date]["contributionCount"]
                date_contributions[date]["color"] = self._get_contribution_color(count)
                date_contributions[date]["level"] = self._get_contribution_level(count)
            
            # 날짜 순서대로 정렬하여 주별로 재구성
            sorted_dates = sorted(date_contributions.keys())
            weeks = []
            current_week = []
            
            for date in sorted_dates:
                date_obj = datetime.fromisoformat(date)
                day_of_week = date_obj.weekday()
                
                # 월요일을 0으로 하는 시스템을 일요일을 0으로 변환
                sunday_based_day = (day_of_week + 1) % 7
                
                # 첫 주의 경우 일요일부터 시작하도록 빈 칸 추가
                if len(weeks) == 0 and sunday_based_day > 0:
                    current_week = [None] * sunday_based_day
                
                current_week.append(date_contributions[date])
                
                # 토요일이거나 7개가 찬 경우 주 완성
                if len(current_week) == 7:
                    weeks.append({"contributionDays": current_week})
                    current_week = []
            
            # 마지막 주가 완성되지 않은 경우 빈 칸으로 채우기
            if current_week:
                while len(current_week) < 7:
                    current_week.append(None)
                weeks.append({"contributionDays": current_week})
            
            # 결과 반환
            merged_data = {
                "contributionCalendar": {
                    "totalContributions": personal_data["contributionCalendar"]["totalContributions"] + org_total,
                    "weeks": weeks
                }
            }
            
            if org_total > 0:
                print(f"🌳 {year}년 TreeNut-KR 조직 기여도 {org_total}개 추가됨")
                
            return merged_data
            
        except Exception as e:
            print(f"❌ 기여도 병합 오류: {str(e)}")
            return personal_data

    def _get_contribution_color(self, count: int) -> str:
        """
        기여도 수에 따른 색상 반환 (어두운색 → 밝은색)
        """
        if count == 0:
            return "#000000"      # 가장 어두운색 (Less)
        elif count <= 3:
            return "#004c1a"      # 어두운 초록
        elif count <= 6:
            return "#39d353"      # 중간 초록
        elif count <= 9:
            return "#7fff00"      # 밝은 초록
        else:
            return "#00ff44"      # 가장 밝은 초록 (More)

    def _get_contribution_level(self, count: int) -> int:
        """
        기여도 수치를 레벨(0-4)로 변환
        """
        if count == 0:
            return 0
        elif count <= 3:
            return 1
        elif count <= 6:
            return 2
        elif count <= 9:
            return 3
        else:
            return 4

    async def fetch_user_activity_overview(self) -> Optional[Dict]:
        """
        GitHub 사용자 활동 개요 조회 (통합 정보 - 간소화)
        """
        try:
            print("📈 활동 개요 수집 시작...")
            
            # 개인 정보 수집
            user_info = await self.fetch_user_info()
            personal_repos = await self.fetch_repositories(max_repos=100)
            
            # TreeNut-KR 조직 정보 수집 (간소화)
            org_repos = await self._fetch_treenut_repositories()
            
            if not user_info or not personal_repos:
                return None
            
            # 개인 통계 계산
            personal_stars = sum(repo.get("stargazers_count", 0) for repo in personal_repos)
            personal_forks = sum(repo.get("forks_count", 0) for repo in personal_repos)
            
            # 조직 통계 계산
            org_stars = 0
            org_forks = 0
            if org_repos:
                org_stars = sum(repo.get("stargazers_count", 0) for repo in org_repos)
                org_forks = sum(repo.get("forks_count", 0) for repo in org_repos)
            
            # 언어 통계 통합
            languages = {}
            
            # 개인 리포지토리 언어
            for repo in personal_repos:
                lang = repo.get("language")
                if lang:
                    languages[lang] = languages.get(lang, 0) + 1
            
            # 조직 리포지토리 언어
            if org_repos:
                for repo in org_repos:
                    lang = repo.get("language")
                    if lang:
                        languages[lang] = languages.get(lang, 0) + 1
            
            # 올해 생성된 리포지토리 수
            current_year = datetime.now().year
            this_year_repos = 0
            
            for repos in [personal_repos, org_repos or []]:
                for repo in repos:
                    try:
                        created_date = datetime.fromisoformat(repo.get("created_at", "").replace('Z', '+00:00'))
                        if created_date.year == current_year:
                            this_year_repos += 1
                    except:
                        continue
            
            activity_overview = {
                "total_repositories": user_info.get("public_repos", 0) + len(org_repos or []),
                "total_stars": personal_stars + org_stars,
                "total_forks": personal_forks + org_forks,
                "followers": user_info.get("followers", 0),
                "following": user_info.get("following", 0),
                "this_year_repos": this_year_repos,
                "languages": languages,
                "account_age_years": self._calculate_account_age(user_info.get("created_at")),
                "last_activity": user_info.get("updated_at"),
                "organization_contribution": f"TreeNut-KR ({len(org_repos or [])} repos)"
            }
            
            print(f"✅ 통합 활동 개요 수집 완료: {personal_stars + org_stars}⭐, {personal_forks + org_forks}🍴")
            return activity_overview
            
        except Exception as e:
            print(f"❌ 통합 활동 개요 수집 실패: {str(e)}")
            return None

    async def _fetch_treenut_repositories(self) -> Optional[List[Dict]]:
        """
        TreeNut-KR 조직의 리포지토리 목록 조회 (사용자가 기여한 것만)
        """
        try:
            treenut_headers = {
                "Authorization": f"token {self.treenut_token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Portfolio-Backend/1.0"
            }
            
            contributed_repos = []
            
            async with aiohttp.ClientSession() as session:
                # 조직 리포지토리 목록 조회
                repos_url = f"{self.base_url}/orgs/TreeNut-KR/repos"
                async with session.get(repos_url, headers=treenut_headers, params={"per_page": 100}) as response:
                    if response.status == 200:
                        repos = await response.json()
                        
                        # 각 리포지토리에서 사용자의 기여 여부 확인
                        for repo in repos:
                            has_contributions = await self._check_user_contributions_in_repo(
                                session, "TreeNut-KR", repo["name"], treenut_headers
                            )
                            
                            if has_contributions:
                                contributed_repos.append(self._process_repository(repo))
                        
                        print(f"🌳 TreeNut-KR에서 기여한 리포지토리: {len(contributed_repos)}개")
                        return contributed_repos
                    else:
                        print(f"❌ TreeNut-KR 리포지토리 조회 오류: {response.status}")
                        return []
        
        except Exception as e:
            print(f"❌ TreeNut-KR 리포지토리 조회 실패: {str(e)}")
            return []

    async def _check_user_contributions_in_repo(self, session: aiohttp.ClientSession, owner: str, repo: str, headers: Dict) -> bool:
        """
        특정 리포지토리에서 사용자의 기여 여부 확인
        """
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/commits"
            params = {
                "author": self.username,
                "per_page": 1  # 하나만 확인
            }
            
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    commits = await response.json()
                    return len(commits) > 0
                else:
                    return False
                    
        except Exception:
            return False

    def _process_unified_contributions(self, all_contributions: Dict[str, int], total_contributions: int) -> Dict:
        """
        통합된 기여도 데이터를 연속된 잔디밭 형태로 처리
        """
        try:
            # 날짜별로 정렬
            sorted_dates = sorted(all_contributions.keys())
            
            if not sorted_dates:
                return {
                    "total_contributions": 0,
                    "daily_data": [],
                    "max_contributions_per_day": 0,
                    "start_date": None,
                    "end_date": None
                }
            
            # 시작일과 종료일
            start_date = sorted_dates[0]
            end_date = sorted_dates[-1]
            
            # 연속된 날짜 생성 (빈 날짜도 포함)
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
            
            daily_data = []
            current_date = start_dt
            max_contributions = 0
            
            while current_date <= end_dt:
                date_str = current_date.strftime("%Y-%m-%d")
                count = all_contributions.get(date_str, 0)
                
                if count > max_contributions:
                    max_contributions = count
                
                daily_data.append({
                    "date": date_str,
                    "count": count,
                    "level": self._get_contribution_level(count),
                    "color": self._get_contribution_color(count)
                })
                
                current_date += timedelta(days=1)
            
            return {
                "total_contributions": total_contributions,
                "daily_data": daily_data,
                "max_contributions_per_day": max_contributions,
                "start_date": start_date,
                "end_date": end_date
            }
            
        except Exception as e:
            print(f"❌ 통합 기여도 처리 오류: {str(e)}")
            return {
                "total_contributions": 0,
                "daily_data": [],
                "max_contributions_per_day": 0,
                "start_date": None,
                "end_date": None
            }

    def _process_contributions_data(self, contributions_data: Dict) -> Dict:
        """
        기여도 데이터 전처리 (연도 순서: 2023 -> 2024 -> 2025)
        """
        if not contributions_data:
            return {
                "years_ordered": [],
                "years": {},
                "total_contributions": 0,
                "max_contributions_per_day": 0,
                "streak_info": {}
            }
        
        processed_data = {
            "years_ordered": [],  # 순서가 있는 연도 리스트
            "years": {},
            "total_contributions": 0,
            "max_contributions_per_day": 0,
            "streak_info": {}
        }
        
        # 연도를 오름차순으로 정렬 (2023, 2024, 2025)
        sorted_years = sorted(contributions_data.keys())
        processed_data["years_ordered"] = sorted_years
        
        for year in sorted_years:
            data = contributions_data[year]
            
            # None 체크 추가
            if not data or "contributionCalendar" not in data:
                print(f"⚠️ {year}년 기여도 데이터가 유효하지 않습니다.")
                continue
                
            calendar = data["contributionCalendar"]
            total_contributions = calendar.get("totalContributions", 0)
            
            # 일별 기여도 데이터 추출
            daily_contributions = []
            weeks = calendar.get("weeks", [])
            
            for week in weeks:
                contribution_days = week.get("contributionDays", [])
                for day in contribution_days:
                    if day:  # None 체크
                        daily_contributions.append({
                            "date": day.get("date", ""),
                            "count": day.get("contributionCount", 0),
                            "level": self._get_contribution_level(day.get("contributionCount", 0)),
                            "color": day.get("color", "#ebedf0")
                        })
            
            processed_data["years"][year] = {
                "total_contributions": total_contributions,
                "daily_data": daily_contributions
            }
            
            processed_data["total_contributions"] += total_contributions
            
            # 최대 일일 기여도 업데이트
            year_max = max([day["count"] for day in daily_contributions] or [0])
            if year_max > processed_data["max_contributions_per_day"]:
                processed_data["max_contributions_per_day"] = year_max
        
        return processed_data

    def _process_repository(self, repo: Dict) -> Dict:
        """
        리포지토리 데이터 전처리
        """
        return {
            "id": repo.get("id"),
            "name": repo.get("name"),
            "full_name": repo.get("full_name"),
            "description": repo.get("description") or "설명이 없습니다.",
            "html_url": repo.get("html_url"),
            "clone_url": repo.get("clone_url"),
            "language": repo.get("language"),
            "stargazers_count": repo.get("stargazers_count", 0),
            "forks_count": repo.get("forks_count", 0),
            "watchers_count": repo.get("watchers_count", 0),
            "size": repo.get("size", 0),
            "default_branch": repo.get("default_branch", "main"),
            "private": repo.get("private", False),
            "created_at": repo.get("created_at"),
            "updated_at": repo.get("updated_at"),
            "pushed_at": repo.get("pushed_at"),
            "topics": repo.get("topics", []),
            "language_color": self._get_language_color(repo.get("language")),
            "updated_relative": self._format_relative_time(repo.get("updated_at"))
        }
    
    def _process_user_info(self, user: Dict) -> Dict:
        """
        사용자 데이터 전처리
        """
        return {
            "login": user.get("login"),
            "name": user.get("name"),
            "bio": user.get("bio"),
            "company": user.get("company"),
            "location": user.get("location"),
            "email": user.get("email"),
            "blog": user.get("blog"),
            "avatar_url": user.get("avatar_url"),
            "html_url": user.get("html_url"),
            "public_repos": user.get("public_repos", 0),
            "followers": user.get("followers", 0),
            "following": user.get("following", 0),
            "created_at": user.get("created_at"),
            "updated_at": user.get("updated_at")
        }
    
    def _get_language_color(self, language: str) -> str:
        """
        프로그래밍 언어별 색상 반환
        """
        colors = {
            'Python': '#3572A5',
            'JavaScript': '#f1e05a',
            'TypeScript': '#2b7489',
            'HTML': '#e34c26',
            'CSS': '#563d7c',
            'Java': '#b07219',
            'C++': '#f34b7d',
            'C': '#555555',
            'Shell': '#89e051',
            'Dockerfile': '#384d54',
            'Go': '#00ADD8',
            'Rust': '#dea584',
            'Vue': '#4FC08D',
            'React': '#61DAFB'
        }
        return colors.get(language, '#586069')
    
    def _format_relative_time(self, date_string: str) -> str:
        """
        상대 시간 포맷팅
        """
        if not date_string:
            return "알 수 없음"
        
        try:
            date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            diff = now - date
            days = diff.days
            
            if days == 0:
                return '오늘'
            elif days == 1:
                return '1일 전'
            elif days < 7:
                return f'{days}일 전'
            elif days < 30:
                return f'{days // 7}주 전'
            elif days < 365:
                return f'{days // 30}개월 전'
            else:
                return f'{days // 365}년 전'
        except Exception:
            return "알 수 없음"

    def _calculate_account_age(self, created_at: str) -> int:
        """
        계정 나이 계산 (년 단위)
        """
        try:
            if not created_at:
                return 0
            
            created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            return (now - created_date).days // 365
        except:
            return 0


# GitHub API 인스턴스 생성
github_api = GitHubAPI()