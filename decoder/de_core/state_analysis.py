import logging
#logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.DEBUG)
from  de_core.message_storage  import  *


class data_analysis:
    def __init__(self,input_file):
        self.input_file = input_file
        self.pointer_position = 0
        #self.seq_header = sequence_header(self.input_file,self.pointer_position )
        self.marker_bit = 0
        self.List_ReferencePictureListSet = []
        self.List_WeightQuantMatrix = []
        #log = Logger('all.log',level='debug')
        #log.logger.debug('debug')

    def pop_read_data(self,read_length):
        string = self.input_file[pointer_position,pointer_position+read_length]
        pointer_position = pointer_position + read_length
        return string

    def get_read_data(self,read_length):
        string = self.input_file[pointer_position,pointer_position+read_length]
        return string

    def run_video_analysis(self):
        print('run_video_analysis')
        #VideoSequence = video_sequence(self.input_file)
        #VideoSequence.run()
        
    def read_ue():
        string_size=0
        while(pop_read_data(1)==0):
            string_size = string_size+1
        pop_read_data(1)
        pop_read_data(string_size)


    def deal_video_sequence():
        pass
    def deal_extension_and_user_data():
        pass
