'''
a = '0010'
print(hex(int(a,2)))
'''
from  de_core.file_rw  import  *
from  de_core.state_analysis  import  *
read_file = 'Mobile_176x144_30_44_golden_f10_used.txt'
read_data = input_decoder_file(read_file)
DA =  data_analysis(read_data)
DA.run_video_analysis()
