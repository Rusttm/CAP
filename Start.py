import sys

if __name__ == '__main__':
    rc = 1
    try:
        print("main()")
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
    sys.exit(rc)