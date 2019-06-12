import os
import re
import time

import func


def args_got():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-td", "--tex_dir", help="贴图集所在目录", default="./Texture2D", type=str, metavar="tex_dir")
    parser.add_argument("-ad", "--atlas_dir", help="切割文件所在目录", default="./TextAsset", type=str, metavar="atlas_dir")
    parser.add_argument("-tf", "--tex_file", help="单独贴图集文件", type=str, metavar="tex_file")
    parser.add_argument("-af", "--atlas-file", help="单独贴图集文件", type=str, metavar="atlas_file")
    parser.add_argument("-s", "--save_path", help="保存目录，默认为运行目录下out文件夹", default="./out", type=str, metavar="save_path")

    args = parser.parse_args()

    return args


def run(args):
    if args.atlas_file is not None and args.tex_file is not None:
        texture = [args.tex_file]
        atlas = [args.atlas_file]

    elif args.tex_dir is not None and args.atlas_dir is not None:

        texture = func.all_file(args.tex_dir)
        atlas = func.all_file(args.atlas_dir)

    else:
        print("没有可用的输入！！")
        return

    texture = list(filter(lambda x: re.match(r'^.+\.png$', x, re.IGNORECASE), texture))
    atlas = list(filter(lambda x: re.match(r'^.+(?:\.atlas|\.atlas\.txt)$', x, re.IGNORECASE), atlas))

    texture_names = list(map(lambda x: os.path.splitext(os.path.splitext(os.path.basename(x))[0])[0], texture))
    atlas_name = list(map(lambda x: os.path.splitext(os.path.splitext(os.path.basename(x))[0])[0], atlas))

    if not (texture_names and atlas_name):
        print("没有可用的输入组合！！")
        return

    count = 1
    for index in range(len(texture_names)):
        try:
            if atlas_name[index] == texture_names[index]:
                name, group = func.pos_spilt(atlas[index])
                func.spilt_tex(texture[index], group, name, args.save_path)
                print(f'完成一个，当前第{count}个，为{name}')
                count += 1
        except IndexError:
            continue

    print("完成，将于15s后关闭")

    time.sleep(15)


if __name__ == '__main__':
    args = args_got()
    run(args)

