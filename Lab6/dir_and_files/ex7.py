import sys

def copy(src, dst):
    with open(src, 'r') as src_file:
        content = src_file.read()

        with open(dst, 'w') as dst_file:
            dst_file.write(content)

def main():
    if len(sys.argv) < 3:
        print("Provide src and dst files in args")
    else:
        src, dst = sys.argv[1:3]
        copy(src, dst)

main()
