from .interpret import execute
import argparse
import sys
def main():
    p=argparse.ArgumentParser(prog="lain")
    p.add_argument("file",nargs=1)
    p.add_argument("memo",nargs='*')
    args=p.parse_args()
    result,*opfoo=(execute(args.file[0],args.memo))
    print(result)
if __name__=="__main__":

    main()
