import logging
#logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.DEBUG)
from  de_core.file_rw  import  *
from  de_core.decoder_process  import  *


class run_decoder:
    def __init__(self,input_file):
        self.video_seq = video_sequence(input_file)

    def run_video_analysis(self):
        print('run_video_analysis')
        #VideoSequence = video_sequence(self.input_file)
        #VideoSequence.run()
        

