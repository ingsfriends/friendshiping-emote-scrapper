from PIL import Image
from io import BytesIO
import os
import requests
from time import sleep


def download_image(url, verbose=True):
    """주어진 URL에서 이미지를 다운로드하고 반환합니다.
    
    Args:
        url (str): 이미지를 다운로드할 URL
        verbose (bool): 시스템 로그 출력 여부 (기본값: True)
    
    Returns:
        Image: 다운로드한 이미지 객체
    """
    if verbose: print(f"이미지 URL: {url}")

    # URL에서 이미지 다운로드
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    if verbose: print(f"이미지 크기: {img.size}")  # img.size == (너비, 높이)
    if verbose: print()

    return img


def center_and_save_image(img, output_path):
    """주어진 이미지를 768*768 크기의 흰색 캔버스에 중앙 정렬하여 저장합니다.

    ※ 참고: 768*768은 PixAI LoRA 훈련 시 권장하는 최소 사이즈 입니다.
    
    Args:
        img (Image): 중앙에 배치할 이미지
        output_path (str): 결과 이미지를 저장할 경로
    """
    # 768*768 크기의 흰색 캔버스를 생성
    canvas = Image.new('RGB', (768, 768), (255, 255, 255))
    
    # 다운로드한 이미지의 크기 가져오기
    w, h = img.size
    
    # 이미지를 캔버스 중앙에 배치할 위치 계산
    x_offset = (768 - w) // 2
    y_offset = (768 - h) // 2
    
    # 이미지를 캔버스에 붙여넣기
    canvas.paste(img, (x_offset, y_offset))
    
    # 결과 이미지를 지정한 경로에 저장
    canvas.save(output_path)


if __name__ == "__main__":
    """우정잉 OGQ 마켓 무단 스크랩 코드

    주어진 OGQ 이모티콘 아이디를 바탕으로 전체 이모티콘 세트 이미지를 다운로드하고, 중앙에 정렬한 후 저장합니다.
    무단 스크랩하는 시점에서 이미 양심 터진 흑화 잉모노지만, 그나마 조금이라도 양심을 더 챙기기 위해 각 이미지마다 3초씩 대기하며 반복 처리합니다.
    """
    __URL_FORMAT = "https://storep-phinf.pstatic.net/{OGQ_ID}/original_{EMOTE_ID}.png?type=m480_480"

    # 처리할 이모티콘 세트 아이디 목록
    OGQ_IDS = (
        # 민킈티콘
        # https://cafe.naver.com/ingsfriends/88600
        # https://ogqmarket.naver.com/artworks/sticker/detail?artworkId=627c80ea90e91
        "ogq_627c80ea90e91",
        
        # 민킈티콘2
        # https://cafe.naver.com/ingsfriends/150845
        # https://ogqmarket.naver.com/artworks/sticker/detail?artworkId=638712a37abec
        "ogq_638712a37abec",

        # 세모의 둥근 일상
        # https://cafe.naver.com/ingsfriends/117386
        # https://ogqmarket.naver.com/artworks/sticker/detail?artworkId=62ddacd1b2878
        "ogq_62ddacd1b2878",
    )

    # 사용자 홈 디렉토리 설정
    HOME_DIR = "/Users/evil_ingmono/Downloads/temp" # TODO: 다운로드 받을 폴더 위치 바꿔주세요.

    # 각 폴더에 대해 이미지 다운로드 및 처리
    for ogq_id in OGQ_IDS:
        # 폴더 (없으면) 생성
        this_dir = os.path.join(HOME_DIR, ogq_id)
        os.makedirs(this_dir, exist_ok=True)        # exist_ok=True : 이미 해당 폴더가 있어도 에러나지 않음.
        
        # 각 폴더에 대해 이미지 1부터 24번까지 다운로드 및 처리 (OGQ 마켓 이모티콘은 한 세트 당 24장 존재)
        for emote_id in range(1, 25):
            # 이미지 다운로드
            img = download_image(__URL_FORMAT.format(OGQ_ID=ogq_id, EMOTE_ID=str(emote_id)))
            
            # 저장 경로 설정
            output_path = os.path.join(this_dir, f"processed_{emote_id}.png")
            
            # 이미지 중앙 정렬 후 저장
            center_and_save_image(img, output_path)
            
            # 과도한 서버 요청량 민폐를 방지하기 위한 3초 대기
            sleep(3)