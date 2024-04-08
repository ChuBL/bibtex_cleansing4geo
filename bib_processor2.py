import os
import re
import bib_exporter
from pybtex.database import parse_file
import random

class BibProcessor:

    def __init__(self, FILENAME):
        self.target_words = ['geo']
        self.annoying_words = ['geoaesthetics', 'geobacillus', 'geobacter', 'geobia', 'geocomposite', 'geocultural', 'geodiver', 'geoduck', 'geoffrey', 'geogebra', 'geogle', 'geogram', 'geograms', 'geoje', 'geolexica', 'geolinguistic', 'geometers', 'geometr', 'geometric', 'geometrical', 'geometrically', 'geometricians', 'geometrico', 'geometrid', 'geometridae', 'geometries', 'geometriesmelt', 'geometrization', 'geometry', 'geometrybuilding', 'geophilic', 'geopolitical', 'geopolitically', 'geopolitics', 'geopolitik', 'georacle', 'georg', 'george', 'georges', 'georgetown', 'georgi', 'georgia', 'georgian', 'georgina', 'georgiy', 'georgopoulos', 'georgy', 'geosmin', 'geospelling', 'geostationary', 'geostory', 'geosynchronous', 'geosynthetics', 'geotaxis', 'geotextile', 'geotrichum']
        # self.revive_words = ['knowledge graph', 'semantic web', 'geoscience']

        self.bib_data = parse_file(FILENAME)
        self.original_item_list = self.get_item_list()
        self.item_list = self.original_item_list
        self.wash_annoying_items()

        self.titles_list = self.get_field_list('Title')
        self.abstracts_list = self.get_field_list('Abstract')
        self.keywords_list = self.get_field_list('Keywords')

        self.target_words_dict = self.load_target_words_of_bib()


    def get_field_string(self, itemName, fieldName):
        """
        itemName be like 'WOS:000410135700006';
        fieldName be like 'Title', 'Abstract', 'Keywords';
        """
        try:
            field_value = self.bib_data.entries[itemName].fields[fieldName]
        except KeyError:
            field_value = ''
        
        return field_value
    
    def get_item_list(self):
        item_list = []
        for item in self.bib_data.entries:
            item_list.append(item)
        
        return item_list

    def get_field_list(self, fieldName):
        field_list = []
        for item_name in self.bib_data.entries:
            field_list.append(self.get_field_string(item_name, fieldName))

        return field_list
        
    def get_unique_words(self, dirtyString):
        unique_words = re.sub(r'\{|\}', r'', dirtyString)
        unique_words = ' '.join(set(unique_words.lower().split(' ')))
        return unique_words

    def get_target_words_in_string(self, string, targetWords):
        washed_string = self.get_unique_words(string)
        check_results = []
        for target_word in targetWords:
            re_filter = r'\b{}[A-Za-z]*\b'.format(target_word)
            checkers = list(set(re.findall(re_filter, washed_string)))
            for check in checkers:
                check_results.append(check)
        # rule out the duplicated factors in the list
        check_results = list(set(check_results))
        return check_results

    def get_target_words_in_field(self, fieldName):
        '''maybe not a good function, suspended'''
        fields_list = self.get_field_list(fieldName)
        # try to rule out the words started with '{' or end with '}'
        for field in fields_list:
            field = self.get_unique_words(field)
            check_results = []
            for target_word in self.target_words:
                re_filter = r'\b{}[A-Za-z]*\b'.format(target_word)
                checkers = re.findall(re_filter, field)
                check_results.append(checkers)
            
        return check_results

    def wash_annoying_items(self):
        wash_item_list = []
        for item in self.item_list:
            intergrated_string = self.get_intergrated_string(item)
        
            annoy_checker = self.get_target_words_in_string(intergrated_string, self.annoying_words)
            if len(annoy_checker) != 0:
                # revive_chance = self.get_target_words_in_string(intergrated_string, self.revive_words)
                # if len(revive_chance) == 0:
                #     wash_item_list.append(item)
                target_checker = self.get_target_words_in_string(intergrated_string, self.target_words)
                wash_flag = True
                for word in target_checker:
                    if word not in self.annoying_words:
                        wash_flag = False
                        break

                if wash_flag is True:
                    wash_item_list.append(item)

        self.washed_item_list = wash_item_list
        '''
        for item in wash_item_list:
            self.bib_data.entries.pop(item)
        '''

    def load_target_words_of_bib(self):
        '''
        read the fields of title abstract keywords of bib,
        get the target words from them,
        save each result as a list and put three lists together to the dict
        dict structure would be like:
        {'wos:112233': [['title', 'words'], ['abstract', 'words'], ['keywords', 'words']]}
        '''
        target_words_dict = {}
        for item_name in self.bib_data.entries:
            title_string = self.get_item_field(item_name, 'Title')
            target_in_title = self.get_target_words_in_string(title_string, self.target_words)

            abstract_string = self.get_item_field(item_name, 'Abstract')
            target_in_abstract = self.get_target_words_in_string(abstract_string, self.target_words)

            keywords_string = self.get_item_field(item_name, 'Keywords')
            target_in_keywords = self.get_target_words_in_string(keywords_string, self.target_words)

            target_list = []
            target_list.append(target_in_title)
            target_list.append(target_in_abstract)
            target_list.append(target_in_keywords)
            target_words_dict[item_name] = target_list

        return target_words_dict

    def show_target_words(self):
        frequency_dict = {}
        for item in self.target_words_dict:
            intergrate_keywords = list(set([y for x in self.target_words_dict[item] for y in x]))
            # for keywords in self.target_words_dict[item]:
            #     intergrate_string.append(keywords)

            for keyword in intergrate_keywords:
                if keyword in frequency_dict:
                    frequency_dict[keyword] += 1
                else:
                    frequency_dict[keyword] = 1

        sorted_frequency_dict = dict(sorted(frequency_dict.items(), key=lambda item: item[1]))
        for item in sorted_frequency_dict:
            print(item, sorted_frequency_dict[item])

    def get_title_list(self):
        return self.titles_list

    def get_keywords_list(self):
        return self.keywords_list

    def get_abstract_list(self):
        return self.abstracts_list

    def get_intergrated_string(self, itemName):
        item_title = self.get_item_field(itemName, 'Title')
        item_abstract = self.get_item_field(itemName, 'Abstract')
        item_keywords = self.get_item_field(itemName, 'Keywords')
        intergrated_string = item_title + item_abstract + item_keywords
        return intergrated_string

    def print_item_detail(self, itemName):
        print(itemName)
        item_title = self.get_item_field(itemName, 'Title')
        item_abstract = self.get_item_field(itemName, 'Abstract')
        item_keywords = self.get_item_field(itemName, 'Keywords')
        print(item_title)
        print(item_abstract)
        print(item_keywords)

    def get_random_item(self):
        rand_item = random.choice(self.item_list)
        return rand_item

    def get_item_field(self, itemName, fieldName):
        try:
            field_string = self.bib_data.entries[itemName].fields[fieldName]
        except KeyError:
            field_string = ''
        return field_string

    def export_to(self, FILENAME):
        self.bib_data.to_file(FILENAME, 'plain text')



if __name__ == '__main__':
    # os.chdir('/Users/blc/Library/CloudStorage/OneDrive-UniversityofIdaho/Lit Review_0222/bibliomatrics resource/web of science/bib0308')
    working_dir = "."

    file_name = '2024Apr.bib'
    file_path = os.path.join(working_dir, file_name)
    bib = BibProcessor(file_path)
    #bib.show_target_words()
    
    washbib = bib_exporter.BibWasher(file_path, bib.washed_item_list)
