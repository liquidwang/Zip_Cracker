import threading
import zipfile


class ZipCracker(threading.Thread):
    thread_list = []

    @staticmethod
    def CrackZip(dic_list, target_file):
        thread_index = 0
        ret = []
        for dic_lib in dic_list:
            thread_index += 1
            temp_thread = ZipCracker(target_file, dic_lib, thread_index)
            temp_thread.start()
            ZipCracker.thread_list.append(temp_thread)
            print('Thread', thread_index, 'has started.')

    def __init__(self, target_file, pwd_dic, index):
        threading.Thread.__init__(self)

        self.z_file = zipfile.ZipFile(target_file, 'r')
        self.pwd_num = 0
        self.pwd_dic = pwd_dic
        self.index = index
        self.stop = False

    def __stop(self):
        for thread in ZipCracker.thread_list:
            thread.Stop()
        print('All thread has been terminated.')

    def Stop(self):
        print('Thread:', self.index, 'has been terminated')
        self.stop = True

    def __test_pwd(self, pwd):
        self.pwd_num += 1
        if self.pwd_num % 10000 == 0:
            print('Thread:', self.index, '---', self.pwd_num, 'pwds has been tested...')
        try:
            self.z_file.extractall(pwd=pwd.encode())
            print('Password has been founded!', 'Target zipfile password is:---', pwd)
            print('Ready to terminate all threads...')
            self.__stop()
            return True
        except:
            return False

    def run(self):
        pwd_index = 0
        pwd_lib = open(self.pwd_dic, 'r')
        dic_lib = pwd_lib.readlines()

        while not self.stop:
            try:
                password = dic_lib[pwd_index].strip('\n')
                pwd_index += 1
                if self.__test_pwd(password):
                    print('Total try pwd num', self.pwd_num)
            except Exception as e:
                self.Stop()


# 'test_dict.txt', 'test_dict_2.txt'
dic = ['test_dict.txt', 'test_dict_2.txt']
target_file = 'test_zip.zip'
ZipCracker.CrackZip(dic, target_file)
