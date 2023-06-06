import cv2
import os
import numpy as np
import glob

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
    dir_len = len(target_files)

    # 전체 이미지에서 가장 큰 크기 기준으로 캔버스 생성
    cut_img_zero_path = os.path.join(path, target_files[0])
    cut_img_zero = cv2.imread(cut_img_zero_path)

    # 이미지 전체 불러와서
    piece_list = glob.glob("./image/new_image/lena_*.png")
    pieces = []
    for file in piece_list:
        pieces.append(cv2.imread(file))

    widths = [piece.shape[1] for piece in pieces] # 너비 저장
    heights = [piece.shape[0] for piece in pieces] # 높이 저장

    new_width = max(widths) # 가장 큰 너비
    new_height = max(heights) # 가장 큰 높이


    # 빈 이미지 생성
    img_merged = np.zeros((new_height * row_num, new_width * column_num, 3), dtype=np.uint8)

    # 디렉토리 내 "input_filename_prefix" 파일 개수가 행렬과 일치
    if dir_len == (column_num * row_num):
        # 추출된 파일들을 읽어와서 처리
        
        y, x = 0, 0 # cut 삽입 좌표
        cnt = 0
        for file in target_files:
            # 자른 이미지
            cut_img_path = os.path.join(path, file)
            print(cut_img_path)
            cut_img = cv2.imread(cut_img_path)
            cut_img_height, cut_img_width = cut_img.shape[:2]

            img_merged[y:y + cut_img_height, x:x + cut_img_width] = cut_img

            # y, x 좌표 조정
            y += cut_img_height
            cnt += 1
            if cnt >= row_num:
                cnt = 0
                y = 0
                x += cut_img_width

        # 합쳐진 이미지 저장
        cv2.imwrite('merged_image.jpg', img_merged)
    else:
        print("디렉토리 내 'prefix_output_filename' 파일의 개수가 원하는 행렬의 개수와 맞지 않습니다. \n확인 부탁드립니다.")