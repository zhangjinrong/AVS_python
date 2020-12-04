import logging
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',level=logging.DEBUG)



class data_analysis:
    def __init__(self,input_file):
        self.input_file = input_file
        self.pointer_position = 0
        self.seq_header = sequence_header()
        self.marker_bit
        self.List_ReferencePictureListSet = []
        log = Logger('all.log',level='debug')
        log.logger.debug('debug')

    def pop_read_data(read_length):
        string = self.input_file[pointer_position,pointer_position+read_length]
        pointer_position = pointer_position + read_length
        return string

    def func_sequence_header():
        if(self.pop_read_data(32)==dict('video_sequence_start_code')):
            self.seq_header.video_sequence_start_code = dict('video_sequence_start_code')
            log.logger.info('video_sequence_start_code')
            self.seq_header.profile_id = self.pop_read_data(8)
            self.seq_header.level_id = self.pop_read_data(8)
            self.seq_header.progressive_sequence = self.pop_read_data(1)
            self.seq_header.field_coded_sequence = self.pop_read_data(1)
            self.seq_header.library_stream_flag = self.pop_read_data(1)
            if(self.seq_header.library_stream_flag == 1):
                self.seq_header.library_picture_enable_flag = self.pop_read_data(1)
                if(self.seq_header.library_picture_enable_flag==1):
                    self.seq_header.duplicate_seq_header_flag = self.pop_read_data(1)
            self.seq_header.marker_bit = self.pop_read_data(1)
            self.seq_header.horizontal_size = self.pop_read_data(14)
            self.seq_header.marker_bit = self.pop_read_data(1)
            self.seq_header.vertical_size = self.pop_read_data(14)
            self.seq_header.chroma_format = self.pop_read_data(2)
            self.seq_header.sample_precision = self.pop_read_data(3)
            if (self.seq_header.profile_id == 0x22):
                self.seq_header.encoding_precision = self.pop_read_data(3)
            self.seq_header.marker_bit = self.pop_read_data(1)
            self.seq_header.aspect_ratio = self.pop_read_data(4)
            self.seq_header.frame_rate_code = self.pop_read_data(4)
            self.seq_header.marker_bit = self.pop_read_data(1)
            self.seq_header.bit_rate_lower = self.pop_read_data(18)
            self.seq_header.marker_bit = self.pop_read_data(1)
            self.seq_header.bit_rate_upper = self.pop_read_data(12)
            self.seq_header.low_delay = self.pop_read_data(1)
            self.seq_header.temporal_id_enable_flag = self.pop_read_data(1)
            self.seq_header.marker_bit = self.pop_read_data(1)
            self.seq_header.bbv_buffer_size = self.pop_read_data(18)
            self.seq_header.marker_bit = self.pop_read_data(1)
            self.seq_header.max_dpb_minus1 = self.pop_read_data(4)
            self.seq_header.rpl1_idx_exist_flag = self.pop_read_data(1)
            self.seq_header.rpl1_same_as_rpl0_flag = self.pop_read_data(1)
            self.seq_header.marker_bit = self.pop_read_data(4)
            self.seq_header.num_ref_pic_list_set[0] = self.read_ue()
            for i in range(self.seq_header.num_ref_pic_list_set[0]):
                ReferencePictureListSet = reference_picture_list_set(0,i,self.seq_header.library_picture_enable_flag)
                self.List_ReferencePictureListSet.append(ReferencePictureListSet)
            if(self.seq_header.rpl1_same_as_rpl0_flag==0):
                self.seq_header.num_ref_pic_list_set[1] = self.read_ue()
                for i in range(self.seq_header.num_ref_pic_list_set[1]):
                    ReferencePictureListSet = reference_picture_list_set(1,i,self.seq_header.library_picture_enable_flag)
                    self.List_ReferencePictureListSet.append(ReferencePictureListSet)
            self.seq_header.num_ref_default_active_minus1[0] = self.read_ue()
            self.num_ref_default_active_minus1[1] = self.read_ue()
            self.log2_lcu_size_minus2 = self.pop_read_data(3)
            self.log2_min_cu_size_minus2 = self.pop_read_data(2)
            


            
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
