__author__ = 'alex'
import key_util
import encryption
import decryption


def main():
    # n = int(input("请输入用户总数:\n"))
    # keys = key_util.key_distribute(n)
    # encryption.AES_with_given_keys(keys)
    decryption.decrypt()


if __name__ == '__main__':
    main()