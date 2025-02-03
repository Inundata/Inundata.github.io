from dotenv import load_dotenv
import os
from datetime import datetime
import requests

load_dotenv()

# 🔹 GitHub 정보 설정
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub Personal Access Token
REPO_OWNER = "Inundata"  # GitHub 사용자명
REPO_NAME = "Inundata.github.io"  # 리포지토리 이름
TAG_NAME = "v1.0"  # 릴리즈 태그 (최초 릴리즈 시 사용)
RELEASE_NAME = "Data Release"
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"

# 🔹 업로드할 파일 설정
# f_name = f"temperature_{datetime.today().strftime('%y%m%d')}.xlsx"
# f_path = f"{file_path}/{f_name}"  # 파일 절대경로

# 🔹 요청 헤더 설정
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_release(GITHUB_API_URL, TAG_NAME, headers):
    """기존 릴리즈 정보를 가져옴. 존재하면 ID 반환, 없으면 None 반환"""
    release_url = f"{GITHUB_API_URL}/releases/tags/{TAG_NAME}"
    response = requests.get(release_url, headers=headers)
    
    if response.status_code == 200:
        release_info = response.json()
        return release_info["id"], release_info["upload_url"].split("{")[0]
    
    return None, None

def create_release(GITHUB_API_URL, TAG_NAME, RELEASE_NAME, headers):
    """새로운 릴리즈 생성"""
    release_url = f"{GITHUB_API_URL}/releases"
    release_data = {
        "tag_name": TAG_NAME,
        "name": RELEASE_NAME,
        "body": "자동 생성된 기온 데이터 파일 릴리즈입니다.",
        "draft": False,
        "prerelease": False
    }
    response = requests.post(release_url, headers=headers, json=release_data)

    if response.status_code == 201:
        release_info = response.json()
        return release_info["id"], release_info["upload_url"].split("{")[0]
    
    print(f"❌ 릴리즈 생성 실패: {response.json()}")

def get_existing_assets(release_id, headers):
    """기존 릴리즈의 업로드된 파일 목록을 가져옴"""
    assets_url = f"{GITHUB_API_URL}/releases/{release_id}/assets"
    response = requests.get(assets_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"⚠️ 기존 업로드된 파일 목록을 가져오는 데 실패: {response.json()}")
        return []
    
def delete_existing_asset(release_id, f_name, headers):
    """같은 이름의 파일이 존재하면 삭제"""
    assets = get_existing_assets(release_id, headers)
    for asset in assets:
        if asset["name"] == f_name:
            asset_id = asset["id"]
            delete_url = f"{GITHUB_API_URL}/releases/assets/{asset_id}"
            response = requests.delete(delete_url, headers=headers)
            
            if response.status_code == 204:
                print(f"🗑️ 기존 파일 삭제 완료: {f_name}")
            else:
                print(f"❌ 기존 파일 삭제 실패: {response.json()}")

def upload_file(release_id, upload_url, f_name, f_path, headers):
    """파일을 GitHub Releases에 업로드"""
    upload_url = f"{upload_url}?name={f_name}"

    # 기존 파일이 있으면 삭제
    delete_existing_asset(release_id, f_name, headers)

    complete_path = f"{f_path}/{f_name}"
    with open(complete_path, "rb") as f:
        upload_headers = headers.copy()
        upload_headers["Content-Type"] = "application/octet-stream"
        response = requests.post(upload_url, headers=upload_headers, data=f)

    if response.status_code == 201:
        download_url = response.json()["browser_download_url"]
        print(f"✅ 파일 업로드 성공! 다운로드 링크: {download_url}")
        return download_url
    
    print(f"❌ 파일 업로드 실패: {response.json()}")

def main(f_name, f_path):
    """메인 실행 함수"""
    # 1️⃣ 기존 릴리즈 확인 (없으면 새로 생성)
    release_id, upload_url = get_release(GITHUB_API_URL, TAG_NAME, headers)
    if not release_id:
        print("🔹 기존 릴리즈 없음 → 새 릴리즈 생성 중...")
        release_id, upload_url = create_release(GITHUB_API_URL, TAG_NAME, RELEASE_NAME, headers)
    else:
        print(f"✅ 기존 릴리즈 확인 완료 (ID: {release_id})")

    # 2️⃣ 파일 업로드
    download_url = upload_file(release_id, upload_url, f_name, f_path, headers)

    # 3️⃣ 다운로드 링크 출력
    print(f"\n📥 데이터 다운로드  경로: {download_url}")

    return download_url