__author__ = 'alex'
import Key_Util
import Encrypt


def main():
    keys = Key_Util.key_distribute(10)
    Encrypt.AES_with_given_keys(keys)


if __name__ == '__main__':
    main()