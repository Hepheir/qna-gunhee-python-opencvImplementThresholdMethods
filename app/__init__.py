import cv2


def my_threshold(src,
                 thresh,
                 maxval,
                 type,
                 dst = None):
    """영상을 흑/백으로 분류하여 처리하는 것-> 이때 기준이 되는 임계값을 어떻게 결정, 임계값보다 크면 백, 작으면 흑
    item()은 특정한 row와 column 화소값 읽어오기 가능
    itemset()은 세팅 가능
    image(): 특정한 화소값 읽어와서 세팅까지가능 -> 대신 느림

    '-'

    """
    height = src.shape[0]
    width = src.shape[1]

    if dst is None:
        dst = src.copy()

    for y in range(height):
        for x in range(width):
            # 각 픽셀별로 처리

            # cv2.THRESH_BINARY
            # 임계값(thresh)보다 크면 백(maxval)으로 지정, 아니면 흑(0)으로 설정
            if type == cv2.THRESH_BINARY:
                if dst.item(y, x) > thresh:
                    dst.itemset(y, x, maxval)
                else:
                    dst.itemset(y, x, 0)

            # cv2.THRESH_BINARY_INV
            # 임계값(thresh)보다 크면 흑(0)으로 지정, 아니면 백(maxval)으로 설정
            elif type == cv2.THRESH_BINARY_INV:
                if dst.item(y, x) < thresh:
                    dst.itemset(y, x, maxval)
                else:
                    dst.itemset(y, x, 0)

            # cv2.THRESH_TRUNC
            # 임계값(thresh)보다 크면 백(maxval)으로 지정, 아니면 원래상태 그대로 (변경없음)
            elif type == cv2.THRESH_TRUNC:
                if dst.item(y, x) > thresh:
                    dst.itemset(y, x, maxval)

            # cv2.THRESH_TOZERO
            # 임계값(thresh)보다 크면 그대로, 아니면 흑
            elif type == cv2.THRESH_TOZERO:
                if dst.item(y, x) < thresh:
                    dst.itemset(y, x, 0)

             # cv2.THRESH_TOZERO_INV
             # 임계값(thresh)보다 크면 흑, 작으면 그대로
            elif type == cv2.THRESH_TOZERO_INV:
                if dst.item(y, x) > thresh:
                    dst.itemset(y, x, 0)

    return thresh, dst


def my_adaptiveThreshold(src, # 원본 이미지
                         maxValue, # 새로 넣을 값
                         adaptiveMethod, # 임계값을 정하는 방법
                         thresholdType, # 임계값으로 이미지를 어떻게 바꿀지
                         blockSize, # 필터 적용할 커널 크기
                         C): # 잘 모르겠음
    height = src.shape[0]
    width = src.shape[1]

    dst = src.copy() # 원본을 수정하지 않게 복사함.

    if adaptiveMethod == cv2.ADAPTIVE_THRESH_GAUSSIAN_C:
        threshold_img = cv2.GaussianBlur(src, (blockSize, blockSize), 0) - C

    elif adaptiveMethod == cv2.ADAPTIVE_THRESH_MEAN_C:
        threshold_img = cv2.medianBlur(src, blockSize) - C

    else:
        raise Exception('올바른 adaptiveMethod가 아닙니다.')

    for y in range(height):
        for x in range(width):
            thresh = threshold_img.item(y, x)

            # 각 픽셀별로 처리

            # cv2.THRESH_BINARY
            # 임계값(thresh)보다 크면 백(maxValue)으로 지정, 아니면 흑(0)으로 설정
            if thresholdType == cv2.THRESH_BINARY:
                if dst.item(y, x) > thresh:
                    dst.itemset(y, x, maxValue)
                else:
                    dst.itemset(y, x, 0)

            # cv2.THRESH_BINARY_INV
            # 임계값(thresh)보다 크면 흑(0)으로 지정, 아니면 백(maxValue)으로 설정
            elif thresholdType == cv2.THRESH_BINARY_INV:
                if dst.item(y, x) < thresh:
                    dst.itemset(y, x, maxValue)
                else:
                    dst.itemset(y, x, 0)

            # cv2.THRESH_TRUNC
            # 임계값(thresh)보다 크면 백(maxValue)으로 지정, 아니면 원래상태 그대로 (변경없음)
            elif thresholdType == cv2.THRESH_TRUNC:
                if dst.item(y, x) > thresh:
                    dst.itemset(y, x, maxValue)

            # cv2.THRESH_TOZERO
            # 임계값(thresh)보다 크면 그대로, 아니면 흑
            elif thresholdType == cv2.THRESH_TOZERO:
                if dst.item(y, x) < thresh:
                    dst.itemset(y, x, 0)

             # cv2.THRESH_TOZERO_INV
             # 임계값(thresh)보다 크면 흑, 작으면 그대로
            elif thresholdType == cv2.THRESH_TOZERO_INV:
                if dst.item(y, x) > thresh:
                    dst.itemset(y, x, 0)

    return dst



def prob_1(image):
    """① cv2.threshold와 cv2.adaptiveThreshold를 이용하여 <그림 1>과 같은 결과가 나타나도록 하시오."""
    picture_a = image
    picture_b = cv2.threshold(image, 125, 255, cv2.THRESH_BINARY)[1]
    picture_c = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 2)

    cv2.imshow("Sample Image", picture_a)
    cv2.imshow("Binary image (cv2.threshold)", picture_b)
    cv2.imshow("Binary image (cv2.adaptiveThreshold)", picture_c)
    return


def prob_2(image):
    """② cv2.threshold 기능을 수행하는 함수를 직접 작성하여 <그림 1>(b)와 같은 결과가 나타나도록 하시오."""
    thresh_bin = my_threshold(image, 125, 255, cv2.THRESH_BINARY)[1]
    thresh_bin_inv = my_threshold(image, 125, 255, cv2.THRESH_BINARY_INV)[1]
    thresh_tozero = my_threshold(image, 125, 255, cv2.THRESH_TOZERO)[1]

    cv2.imshow("Binary image(my_threshold, cv2.THRESH_BINARY)", thresh_bin)
    cv2.imshow("Binary image(my_threshold, cv2.THRESH_BINARY_INV)", thresh_bin_inv)
    cv2.imshow("Binary image(my_threshold, cv2.THRESH_TOZERO)", thresh_tozero)
    return


def prob_3(image):
    """③ cv2.adaptiveThreshold 기능을 수행하는 함수를 직접 작성하여 <그림 1>(c)와 같은 결과가 나타나도록 하시오."""
    adaptive_mean_thresh = my_adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 2)
    adaptive_gaussian_thresh = my_adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 2)

    cv2.imshow("Binary image(my_adaptiveThreshold, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY)", adaptive_mean_thresh)
    cv2.imshow("Binary image(my_adaptiveThreshold, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY)", adaptive_gaussian_thresh)
    return


image = cv2.imread("asset/sonnet-for-lena.jpeg", cv2.IMREAD_GRAYSCALE)
prob_3(image)
cv2.waitKey(0)
