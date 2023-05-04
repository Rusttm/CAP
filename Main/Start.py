import sys
import logging as log
import Main.ContMain.ContCAPMS as ContCAPMS



if __name__ == '__main__':
    msapi1 = ContCAPMS.ContCAPMS()
    msapi1.get_cont_id()
    msapi2 = ContCAPMS.ContCAPMS()
    msapi3 = ContCAPMS.ContCAPMS()
    rc = 1
    try:
        # print("main()")
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
    sys.exit(rc)