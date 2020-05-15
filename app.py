import sys,ast
import fitz
import re
from colour import Color
import os,subprocess


class PdfHighLighter():
    """
    This class is used to highlight the color of pdf of different components.
    """

    def __init__(self):

        self.input_path='/home/techstriker/Downloads/other_pdfs/carlino.pdf'
        self.output_path='/home/techstriker/Downloads/other_pdfs/output/'
        # self.list_values = [{'text':'E03.DC11', 'color':'red', 'type':'background'},{'text':'A23:A27', 'color':'red', 'type':'background'}]
        self.list_values = [{'text': 'Planning', 'color': 'yellow', 'type': 'background'}]
        # self.color = "white"
        self.clear_background_colors = False
        # self.check_inputpath_validations()
        # self.check_outputpath_validations()
        # self.validate_text_list()
        # self.get_color()
        self.clear_all_background_colors()
        self.rotate_angle = 270
        self.text_instances = []
        self.box_instances = []
        self.open_pdf()
        self.search_word_dimensions()
        self.highlight()


    def check_inputpath_validations(self):

        self.input_path = input('Enter input : ')
        if not os.path.exists(self.input_path):
            sys.exit("invalid input path please enter correct path.")
        if ".pdf"  not in self.input_path:
            sys.exit("file should be in pdf format")

    def check_outputpath_validations(self):

        self.output_path = input('Enter output : ')
        if not os.path.exists(self.output_path):
            sys.exit("invalid output path please enter correct path.")

    def validate_text_list(self):
        self.list_values = ast.literal_eval(input('Enter text list  you want to highlight: '))

        if type(self.list_values) != list:
            sys.exit("please enter a valid list. e.g. ['G4:G12', 'E4:E12', 'E6FD5']")

        if len(self.list_values) == 0:
            sys.exit("list should not be  empty")

    def get_color(self):
        self.color = input("Enter the color you want to use for text highlighting,leave blank for default(yellow):")
        self.color_to_rgb(self.color)

    def clear_all_background_colors(self):
        remove_background = input("You want to remove background color or not?(yes/no) :")
        if remove_background == 'yes':
            self.clear_background_colors = True
        elif remove_background == 'no':
            self.clear_background_colors =False
        else:
            sys.exit("Answer should be yes/no")

    def color_to_rgb(self,color):
        try:
            return Color(color).rgb
        except:
            return Color('yellow').rgb

    def filter_list(self,list_text):
        str = list_text
        chr = str[0]
        ranges = list(map(int, re.findall(r'\d+', str)))
        l = [f'{chr}{i}' + " " for i in range(ranges[0], ranges[1] + 1)]
        return l

    def pdf_to_gray_conversion(self):
         file_name = self.input_path.split(".pdf")[0]
        # try:
         path = os.getcwd()
         subprocess.call(path+'/graypdf.sh %s' % (self.input_path), shell=True)
         self.input_path = file_name + "-gray.pdf"
         self.doc = fitz.open(self.input_path)
         self.page = self.doc[0]

        # except:
        #     pass


    def open_pdf(self):
        print(self.clear_background_colors)

        if self.clear_background_colors == True:
            self.pdf_to_gray_conversion()
            self.rotate_angle = 0
        else:
            try:
                self.doc = fitz.open(self.input_path)
                self.page = self.doc[0]
                print(self.page.getText())
            except:
                sys.exit("Can't read pdf file.Something went wrong")

    def choose_text_color(self,color):
        if color == "white" or color == "yellow" or color == "pink":
            return Color("black").rgb
        else:
            return Color("white").rgb

    def search_word_dimensions(self):
        for highlight_details in self.list_values:
            word = highlight_details['text']
            if ":" in word:
                word_list = self.filter_list(word)
                for word in word_list:
                    self.box_instances.append({"text": word,
                                               "dimensions": self.page.searchFor(word),
                                               "color":highlight_details['color'],
                                               "type":highlight_details['type']})
            else:
                self.text_instances.append({"text": word,
                                               "dimensions": self.page.searchFor(word),
                                               "color":highlight_details['color'],
                                               "type":highlight_details['type']})

    def highlight_text(self):
        # print(self.text_instances)
        for inst_list in self.text_instances:
            text = inst_list['text']
            for inst in inst_list['dimensions']:
                rect = fitz.Rect(inst.x0, inst.y0, inst.x1+10.0, inst.y1)
                if inst_list['type'] == 'frame':
                    rgb_color = self.color_to_rgb('white')
                    text_color = self.choose_text_color('white')
                else:
                    rgb_color = self.color_to_rgb(inst_list['color'])
                    text_color = self.choose_text_color(inst_list['color'])
                annot = self.page.addFreetextAnnot(rect, text, fontsize=6.5, fontname="cobo",
                                              text_color=text_color, fill_color=rgb_color, rotate=self.rotate_angle)

    def highlight_box(self):
        # print("box",self.box_instances)
        for inst_list in self.box_instances:
            text = inst_list['text']
            for inst in inst_list['dimensions']:
                inst.x1 = inst.x1 + 73.0
                inst.x0 = inst.x0 - 2.0
                rect = fitz.Rect(inst.x0, inst.y0, inst.x1, inst.y1)
                if inst_list['type'] == 'frame':
                    rgb_color = self.color_to_rgb('white')
                    text_color = self.choose_text_color('white')
                else:
                    rgb_color = self.color_to_rgb(inst_list['color'])
                    text_color = self.choose_text_color(inst_list['color'])
                self.page.addFreetextAnnot(rect, text, fontsize=12, fontname="cobo",
                                              text_color=text_color, fill_color=rgb_color, rotate=self.rotate_angle)

    def save_output_pdf(self):
        try:
            self.doc.save(self.output_path+"/output.pdf", garbage=4, deflate=True,
                     clean=True)
            if self.clear_background_colors:
                os.remove(self.input_path)
            print("*"*20)
            print("All Done")
            print("*"*20)
        except:
            sys.exit("Can't save pdf.Something went wrong")


    def highlight(self):
        self.highlight_box()
        self.highlight_text()
        self.save_output_pdf()


if __name__ == '__main__':
    a_game = PdfHighLighter()

