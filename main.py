import cut_image
import merge_image
import merge_image_template

row, col = 3,4
if __name__ == '__main__':

    cut_image.main("lena.png", row, col, "lena_cut")
    merge_image_template.main("lena_cut", row, col, "lena_merge.png")
