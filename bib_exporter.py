import re
import os

class BibWasher:
    def __init__(self, originalFilePath, washList):
        # self.cwd = r'/Users/blc/Library/CloudStorage/OneDrive-UniversityofIdaho/Lit Review_0222/bibliomatrics resource/web of science/bib0308'
        # os.chdir(self.cwd)
        self.wash_list = washList
        self.original_file_path = originalFilePath
        self.original_file_name = self.original_file_path.split('/')[-1]
        self.new_file_name = 'washed_' + self.original_file_name
        self.read_file_lines()
        self.write_file_lines()

    def read_file_lines(self):
        with open(self.original_file_path, 'r') as original_file:
            self.original_lines = original_file.readlines()

    def write_file_lines(self):
        with open(self.new_file_name, 'w') as new_file:
            wash_flag = False
            for line in self.original_lines:
                # the line beginning was vailidated with the re = r'\@article'
                # for all the items begin with that string we may apply this as a flag of beginning fo items
                item_beginning = '@article'
                if self.check_item_in_line(item_beginning, line):
                    # confirm if the readline position in the beginning of an item
                    item_name = self.extract_item_in_line(line)
                    if item_name in self.wash_list:
                        # self.wash_list.pop(item_name)
                        wash_flag = True
                        continue
                    else:
                        wash_flag = False
                        new_file.write(line)
                elif wash_flag is True:
                    continue
                elif wash_flag is False:
                    new_file.write(line)


    def check_item_in_line(self, item, line):
        item_checker = re.findall(item, line)
        if len(item_checker) != 0:
            return True
        else:
            return False

    def extract_item_in_line(self, exline):
        item = re.findall(r"(?<=\@article\{.).*(?=,)", exline)[0]
        return(item)


def check_test(item, line):
    item_checker = re.findall(item, line)
    if len(item_checker) != 0:
        return True
    else:
        return False


if __name__ == '__main__':
    # wash_str = 'WOS:000758201500001'
    # line = '@article{ WOS:000758201500001,'
    # if check_test(wash_str, line):
    #     print('true')
    #     extract_item(line)
    # else:
    #     print('false')
    bw = BibWasher()