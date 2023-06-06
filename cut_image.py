import os
import cv2
import string, secrets
import random
import numpy as np

# 매개변수 4개 (원본 이미지 파일 이름, 열 개수, 행 개수, 자른 이미지들의 접두사)
def main(image_file_name, column_num, row_num, prefix_output_filename):
    path, img = read_image(image_file_name)
    cut_image(path, img, column_num, row_num, prefix_output_filename)

# 이미지 파일 경로 지정
def read_image(image_file_name):
    path = os.getcwd()
    dirname = "image"
    path = os.path.join(path, dirname)
    img_file = os.path.join(path, image_file_name)

    img = cv2.imread(img_file)

    return(path, img)

# 현재 작업 중인 디렉토리에 자른 이미지를 모아두기 위한 폴더 생성
def make_dir(path):
    folder_name = "new_image"

    folder_path = os.path.join(path, folder_name)

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"폴더 '{folder_name}'가 생성되었습니다.")
    else:
        print(f"폴더 '{folder_name}'가 이미 존재합니다.")

    return folder_path

# 이미지 자르기
def cut_image(path, img, column_num, row_num, prefix_output_filename):
    h, w, _ = img.shape

    sub_height = h // row_num
    sub_width = w // column_num

    height_remainder = h % row_num
    width_remainder = w % column_num

    # 생성된 이미지를 담을 폴더 생성
    folder_name = make_dir(path)
    path = os.path.join(path, folder_name)

    # 높이와 너비 분할이 균등하면
    if (height_remainder == 0) and (width_remainder == 0):
        for row in range(row_num):
            for col in range(column_num):
                # 랜덤 문자열 생성 // 알파벳 + 숫자(10 ~ 50)
                rand = secrets.choice(string.ascii_letters) + str(random.randint(10, 50))
                rand_file_name = prefix_output_filename + rand + ".png"
                img_file = os.path.join(path, rand_file_name)

                # 자를 이미지 영역
                x1 = col * sub_width
                y1 = row * sub_height
                x2 = x1 + sub_width
                y2 = y1 + sub_height
                sub_img = img[y1:y2, x1:x2]

                # 이미지 자른 후 임의 변환
                sub_img = random_conversion_image(sub_img)

                # 이미지 저장
                cv2.imwrite(img_file, sub_img)

    # 높이와 너비 분할이 균등하지 않으면
    else:
        # 가장자리 픽셀을 복제하여 추가된 테두리 영역 채우기
        img = cv2.copyMakeBorder(img, 0, row_num - height_remainder, 0, column_num - width_remainder,
                                 cv2.BORDER_REPLICATE)

        for row in range(row_num):
            for col in range(column_num):
                # 랜덤 문자열 생성 // 알파벳 + 숫자(10 ~ 50)
                rand = secrets.choice(string.ascii_letters) + str(random.randint(10, 50))
                rand_file_name = prefix_output_filename + rand + ".png"
                img_file = os.path.join(path, rand_file_name)
                print(img_file)

                # 자를 이미지 영역
                x1 = col * sub_width
                y1 = row * sub_height
                x2 = x1 + sub_width
                y2 = y1 + sub_height
                sub_img = img[y1:y2, x1:x2]

                # 이미지 자른 후 임의 변환
                sub_img = random_conversion_image(sub_img)

                # 이미지 저장
                cv2.imwrite(img_file, sub_img)

# 이미지 임의 변환
def random_conversion_image(img):
    # 50% 확률로 좌우 반전
    if np.random.rand() < 0.5:
        img = cv2.flip(img, 1)

    # 50% 확률로 상하 반전
    if np.random.rand() < 0.5:
        img = cv2.flip(img, 0)  # 상하 반전

    # 50% 확률로 90도 회전
    if np.random.rand() < 0.5:
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    return(img)