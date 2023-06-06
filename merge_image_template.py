import cv2
import os
import numpy as np

# 매개변수 4개 (자른 이미지들의 접두사, 열 개수, 행 개수, 병합 이미지 이름)
def main(input_filename_prefix, column_num, row_num, output_filename):
    path, target_files = read_image(input_filename_prefix)
    merge_image(path, column_num, row_num, target_files, output_filename)

# 이미지 파일 경로 지정
def read_image(input_filename_prefix):
    path = os.getcwd()
    dirname = "/image/new_image"
    path = path + dirname
    # 디렉토리 내 파일 리스트를 불러옴
    file_list = os.listdir(path)

    # 파일명에 해당하는 파일 리스트 추출
    target_files = [file for file in file_list if input_filename_prefix in file]

    return (path, target_files)

def merge_image(path, column_num, row_num, target_files, output_filename):
    # 템플릿 매칭에 사용할 원본 이미지 로드
    original_image_path = os.getcwd() + "/image"
    original_image_path = os.path.join(original_image_path, "lena.png")
    original_image = cv2.imread(original_image_path)
    original_image_gray =  cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    # 템플릿 매칭에 사용할 이미지 크기 계산
    h, w, _ = original_image.shape

    dir_len = len(target_files)

    canvas = 255 * np.ones((original_image.shape[0], original_image.shape[1], 3), dtype=np.uint8)

    # 디렉토리 내 "input_filename_prefix" 파일 개수가 행렬과 일치
    if dir_len == (column_num * row_num):
        # 추출된 파일들을 읽어와서 처리
        for file in target_files:
            # 자른 이미지
            cut_img = os.path.join(path, file)
            template_image = cv2.imread(cut_img)

            # 템플릿 매칭으로 좌표 찾기
            template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
            result = cv2.matchTemplate(original_image_gray, template_gray, cv2.TM_CCOEFF_NORMED)

            # 매칭 결과 좌표 구하기
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            top_left = max_loc
            bottom_right = (top_left[0] + template_gray.shape[1], top_left[1] + template_gray.shape[0])

            # 매칭 결과 이미지에 표시. 유사도 높은 구역에 오리지널 이미지를 삽입
            canvas[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = original_image[top_left[1]:bottom_right[1],
                                                                               top_left[0]:bottom_right[0]]

        # 합쳐진 이미지 저장
        path = os.path.join(path, output_filename)
        cv2.imwrite(path, original_image)

        # 결과 확인
        cv2.imshow('Canvas', canvas)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("디렉토리 내 'prefix_output_filename' 파일의 개수가 원하는 행렬의 개수와 맞지 않습니다. \n확인 부탁드립니다.")