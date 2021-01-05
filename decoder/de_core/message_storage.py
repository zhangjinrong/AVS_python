# This file is a basic file, store video message 
# store video_sequence message, instantiation it and add to main function

from  de_core.file_rw  import  *

#视频序列定义,这是整个视频解码的最高层
dict =  {
    'video_sequence_start_code':'00000000000000000000000110110000',#0x000001B0,#视频序列起始码
    'video_sequence_end_code':'00000000000000000000000110110001',#0x000001B1,
    'user_data_start_code':'00000000000000000000000110110010',#0x000001B2,
    'intra_picture_start_code':'00000000000000000000000110110011',#0x000001B3,
    'extension_start_code':'00000000000000000000000110110101',#0x000001B5,
    'inter_picture_start_code':'00000000000000000000000110110110',#0x000001B6,
    'video_edit_code':'00000000000000000000000110110111',#0x000001B7,
    'bbv_delay':'11111111111111111111111111111111',#0xFFFFFFFF,
    'patch_start_code1':'00000000000000000000000000000000',#00-7F is patch_start_code
    'patch_start_code2':'0000000000000000000000000000007F',#00-7F is patch_start_code
    '8F': 'patch_end_code'
    }

#暂时无用
class video_sequence:
    def __init__(self,input_file):
        self.data_file = input_file
        self.pointer_position = 0
        self.run()
    def run(self):
        #if(self.get_read_data(32) == dict['video_sequence_start_code']):
        #    print('good')
        SH = sequence_header(self.data_file,self.pointer_position)
        SH.run()
        #extension_and_user_data(0,self.data_file,self.pointer_position)
        '''
        while((self.get_read_data(32) != dict['video_sequence_end_code']) & (self.get_read_data(32) != dict['video_edit_code'])):
            sequence_header(self.data_file,self.pointer_position)
            extension_and_user_data(0)
            while((self.get_read_data(32) == dict['inter_picture_start_code']) | (self.get_read_data(32) == dict['intra_picture_start_code'])):
                if (next_bits(32) == dict['intra_picture_start_code']):#0x000001B3
                    intra_picture_header()
                else:
                    inter_picture_header()
                extension_and_user_data(1)
                picture_data()
        if (pop_read_data(32) == dict['intra_picture_start_code']):#0x000001B3
            video_sequence_end_code#0x000001B1
        if (pop_read_data(32) == dict['intra_picture_start_code']):
            video_edit_code #0x000001B7
        '''
 
#比特流信息
class bitstream_data:
    def __init__(self,input_decoder_file):
        self.pointer_position = 0
        self.data_file = input_decoder_file

    def pop_read_data(self,read_length):
        string = self.data_file[self.pointer_position:self.pointer_position+read_length]
        self.pointer_position = self.pointer_position + read_length
        return string

    def get_read_data(self,read_length):
        string = self.data_file[self.pointer_position:self.pointer_position+read_length]
        return string

    def read_ue(self,str_value):
        string_size=1
        while(self.get_read_data(1)=='0'):
            string_size = string_size+1
            self.pop_read_data(1)
        data_value=self.str_to_int(self.pop_read_data(string_size))-1
        print(str_value,'  ',data_value)
        return data_value

    def read_se(self,str_value):
        string_size=1
        while(self.get_read_data(1)=='0'):
            string_size = string_size+1
            self.pop_read_data(1)
        code_num = self.str_to_int(self.pop_read_data(string_size))-1
        if(code_num%2==0):
            data_value = 0-code_num/2
        else:
            data_value = code_num/2+1
        print(str_value,'  ',data_value)
        return data_value

    def str_to_int(self,str):
        data = 0
        for i in range(len(str)):
            data = data*2 + int(str[i])
        return data

    def assign_data(self,str_value,len_data):
        data_value = self.str_to_int(self.get_read_data(len_data))
        data_value = hex(data_value)
        print(str_value,'  ',data_value)
        if((str_value=='marker_bit')&(data_value==0)):
            print('marker_bit wrong!')
        return data_value
    
    #在位流中寻找下一个起始码，将位流指针指向起始码前缀的第一个二进制位。
    def next_start_code(self):
        self.stuffing_bit=self.assign_data('stuffing_bit',1)#1
        while (~ self.byte_aligned()):
            self.stuffing_bit=self.assign_data('stuffing_bit',1)#0
        while (self.get_read_data(24) != '000000000000000000000001'):#起始码前缀
            self.stuffing_byte=self.assign_data('stuffing_byte',8)#0#00000000

# 参考图像结构
class rpl:
    def __init__(self):
        self.slice_type=0#slice类型
        self.poc=0
        self.tid=0
        self.ref_pic_num=0#参考图像数
        self.ref_pic_active_num=0
        self.ref_pics=[0 for i in range(17)]
        self.ref_pics_ddoi=[0 for i in range(17)]#被参考的知识图像索引
        self.ref_pics_doi=[0 for i in range(17)]
        self.reference_to_library_enable_flag = 0#参考知识图像标志
        self.library_index_flag=[0 for i in range(17)]#知识图像索引标志
        self.NumOfRefPic = [0 for i in range(2)]#参考图像数
        self.referenced_library_picture_index = [0 for i in range(2)]#被参考的知识图像索引
        self.abs_delta_doi = [0 for i in range(2)]#参考图像DOI差值绝对值,DOI为图像头中的解码顺序索引
        self.sign_delta_doi=[0 for i in range(2)]#参考图像DOI差值符号,DOI为图像头中的解码顺序索引

        self.WeightQuantMatrix4x4= [[0 for j in range(0,4)] for i in range(0,4)]#4x4加权量化矩阵系数
        self.WeightQuantMatrix8x8= [[0 for j in range(0,8)] for i in range(0,8)]#8x8加权量化矩阵系数
#序列头定义
class sequence_header:
    def __init__(self,bitstream_data):
        self.bsd = bitstream_data
        self.video_sequence_start_code=0#序列头起始码
        self.profile_id=0#档次标号
        self.level_id=0#级别标号
        self.progressive_sequence=0#逐行序列标志
        self.field_coded_sequence=0#场图像序列标志
        self.library_stream_flag=0#知识位流标志.值为'1'表示当前位流是知识位流;值为'0'表示当前位流是主位流
        self.library_picture_enable_flag=0#知识图像允许标志.值为'1'表示视频序列中可存在使用知识图像作为参考图像的帧间预测图像;值为'0'表示视频序列中不应存在使用知识图像作为参考图像的帧间预测图像。
        self.duplicate_sequence_header_flag=0#知识位流重复序列头标志.
        self.horizontal_size=0#水平尺寸
        self.vertical_size=0#垂直尺寸
        self.chroma_format=0#色度格式
        self.sample_precision=0#样本精度
        self.encoding_precision=0#编码样本精度
        self.aspect_ratio=0#宽高比
        self.frame_rate_code=0#帧率代码
        self.bit_rate_lower=0#比特率低位
        self.bit_rate_upper=0#比特率高位
        self.low_delay=0#低延迟
        self.temporal_id_enable_flag=0#时间层标识允许标志
        self.bbv_buffer_size=0#位流缓冲区尺寸
        self.max_dpb_minus1=0#最大解码图像缓冲区大小
        self.rpl1_idx_exist_flag=0#参考图像队列1索引存在标志
        self.rpl1_same_as_rpl0_flag=0#参考图像队列相同标志
        self.num_ref_pic_list_set =[0 for i in range(2)] #参考图像队列配置集数
        self.num_ref_default_active_minus1 = [0 for i in range(2)]#默认活跃参考图像数
        self.log2_lcu_size_minus2=0#最大编码单元尺寸
        self.log2_min_cu_size_minus2=0#最小编码单元尺寸
        self.log2_max_part_ratio_minus2=0#划分单元最大比例
        self.max_split_times_minus6=0#编码树最大划分次数
        self.log2_min_qt_size_minus2=0#最小四叉树尺寸
        self.log2_max_bt_size_minus2=0#最大二叉树尺寸
        self.log2_max_eqt_size_minus3=0#最大扩展四叉树尺寸
        self.weight_quant_enable_flag=0#加权量化允许标志
        self.load_seq_weight_quant_data_flag=0#加权量化矩阵加载标志
        self.secondary_transform_enable_flag=0#二次变换允许标志
        self.sample_adaptive_offset_enable_flag=0#样值偏移补偿允许标志
        self.adaptive_leveling_filter_enable_flag=0#自适应修正滤波允许标志
        self.affine_enable_flag=0#仿射运动补偿允许标志
        self.smvd_enable_flag=0#对称运动矢量差模式允许标志
        self.ipcm_enable_flag=0#脉冲编码调制模式允许标志
        self.amvr_enable_flag=0#自适应运动矢量精度允许标志
        self.num_of_hmvp_cand=0#候选历史运动信息数
        self.umve_enable_flag=0#高级运动矢量表达模式允许标志
        self.emvr_enable_flag=0#运动矢量精度扩展模式允许标志
        self.ipf_enable_flag=0#帧内预测滤波允许标志
        self.tscpm_enable_flag=0#色度两步预测模式允许标志
        self.dt_enable_flag=0#帧内衍生模式允许标志
        self.log2_max_dt_size_minus4=0#衍生模式待划分边长最大尺寸
        self.max_dt_size=0#衍生模式待划分边长最大尺寸
        self.pbt_enable_flag=0#基于位置的变换允许标志
        self.output_reorder_delay=0#图像重排序延迟
        self.cross_patch_loopfilter_enable_flag=0#跨片环路滤波允许标志
        self.ref_colocated_patch_flag =0#参考同位置片标志
        self.stable_patch_flag =0#片划分一致性标志
        self.uniform_patch_flag =0#统一片大小标志
        self.patch_width_minus1 =0#片宽度
        self.patch_height_minus1=0#片高度
        self.reserved_bits=0#
        self.marker_bit =0#

        # 参考图像队列配置集定义
        self.rpls_l0=[rpl() for i in range(32)]
        self.rpls_l1=[rpl() for i in range(32)]

    def run(self):
        if(self.bsd.get_read_data(32)==dict['video_sequence_start_code']):
            self.video_sequence_start_code = self.bsd.assign_data('video_sequence_start_code',32)
            self.profile_id = self.bsd.assign_data('profile_id',8)
            self.level_id = self.bsd.assign_data('level_id',8)
            self.progressive_sequence = self.bsd.assign_data('progressive_sequence',1)
            self.field_coded_sequence = self.bsd.assign_data('field_coded_sequence',1)
            self.library_stream_flag = self.bsd.assign_data('library_stream_flag',1)
            if(self.library_stream_flag == 0):
                self.library_picture_enable_flag = self.bsd.assign_data('library_picture_enable_flag',1)
                if(self.library_picture_enable_flag==1):
                    self.duplicate_seq_header_flag = self.bsd.assign_data('duplicate_seq_header_flag',1)
            self.marker_bit = self.bsd.assign_data('marker_bit',1)
            self.horizontal_size = self.bsd.assign_data('horizontal_size',14)
            self.marker_bit = self.bsd.assign_data('marker_bit',1)
            self.vertical_size = self.bsd.assign_data('vertical_size',14)
            self.chroma_format = self.bsd.assign_data('chroma_format',2)
            self.sample_precision = self.bsd.assign_data('sample_precision',3)
            if (self.profile_id == 0x22):
                self.encoding_precision = self.bsd.assign_data('encoding_precision',3)
            self.marker_bit = self.bsd.assign_data('marker_bit',1)
            self.aspect_ratio = self.bsd.assign_data('aspect_ratio',4)
            self.frame_rate_code = self.bsd.assign_data('frame_rate_code',4)
            self.marker_bit = self.bsd.assign_data('marker_bit',1)
            self.bit_rate_lower = self.bsd.assign_data('bit_rate_lower',18)
            self.marker_bit = self.bsd.assign_data('marker_bit',1)
            self.bit_rate_upper = self.bsd.assign_data('bit_rate_upper',12)
            self.low_delay = self.bsd.assign_data('low_delay',1)
            self.temporal_id_enable_flag = self.bsd.assign_data('temporal_id_enable_flag',1)
            self.marker_bit = self.bsd.assign_data('marker_bit',1)
            self.bbv_buffer_size = self.bsd.assign_data('bbv_buffer_size',18)
            self.marker_bit = self.bsd.assign_data('marker_bit',1)
            self.max_dpb_minus1 = self.bsd.assign_data('max_dpb_minus1',4)
            self.rpl1_idx_exist_flag = self.bsd.assign_data('rpl1_idx_exist_flag',1)
            self.rpl1_same_as_rpl0_flag = self.bsd.assign_data('rpl1_same_as_rpl0_flag',1)
            self.marker_bit = self.bsd.assign_data('marker_bit',1)
            self.num_ref_pic_list_set[0] = self.bsd.read_ue('num_ref_pic_list_set[0]')
            #self.NumOfRefPic[0] = [0 for i in range(self.num_ref_pic_list_set[0])]
            #=======================================
            for i in range(int(self.num_ref_pic_list_set[0])):
                self.reference_picture_list_set(self.rpls_l0[i])
            if(self.rpl1_same_as_rpl0_flag==0):
                self.num_ref_pic_list_set[1] = self.bsd.read_ue('num_ref_pic_list_set[1]')
                #self.NumOfRefPic[1] = [0 for i in range(self.num_ref_pic_list_set[1])]
                for i in range(int(self.num_ref_pic_list_set[1])):
                    self.reference_picture_list_set(self.rpls_l1[i])
            else:#rpl1_same_as_rpl1和rpl1_same_as_rpl0的值一样
                self.num_ref_pic_list_set[1] = self.num_ref_pic_list_set[0] 
                for i in range(int(self.num_ref_pic_list_set[1])):
                    sqh.rpls_l1[i].reference_to_library_enable_flag = sqh.rpls_l0[i].reference_to_library_enable_flag
                    sqh.rpls_l1[i].ref_pic_num = sqh.rpls_l0[i].ref_pic_num
                    for j in range(sqh.rpls_l1[i].ref_pic_num):
                        sqh.rpls_l1[i].library_index_flag[j] = sqh.rpls_l0[i].library_index_flag[j]
                        sqh.rpls_l1[i].ref_pics_ddoi[j] = sqh.rpls_l0[i].ref_pics_ddoi[j]

            self.num_ref_default_active_minus1[0] = self.bsd.read_ue('num_ref_default_active_minus1[0]')
            self.num_ref_default_active_minus1[1] = self.bsd.read_ue('num_ref_default_active_minus1[1]')
            self.log2_lcu_size_minus2 = self.bsd.assign_data('log2_lcu_size_minus2',3)
            self.log2_min_cu_size_minus2 = self.bsd.assign_data('log2_min_cu_size_minus2',2)
            self.log2_max_part_ratio_minus2 = self.bsd.assign_data('log2_max_part_ratio_minus2',2)
            self.max_split_times_minus6 = self.bsd.assign_data('max_split_times_minus6',3)
            self.log2_min_qt_size_minus2 = self.bsd.assign_data('log2_min_qt_size_minus2',3)
            self.log2_max_bt_size_minus2 = self.bsd.assign_data('log2_max_bt_size_minus2',3)
            self.log2_max_eqt_size_minus3 = self.bsd.assign_data('log2_max_eqt_size_minus3',2)
            self.marker_bit = self.bsd.assign_data('marker_bit',1)
            self.weight_quant_enable_flag = self.bsd.assign_data('weight_quant_enable_flag',1)
            if(self.weight_quant_enable_flag==1):
                self.load_seq_weight_quant_data_flag = self.bsd.assign_data('load_seq_weight_quant_data_flag',1)
                if(self.load_seq_weight_quant_data_flag==1):
                    self.weight_quant_matrix()
                else:
                    self.copy_weight_quant_matrix()
            self.secondary_transform_enable_flag = self.bsd.assign_data('secondary_transform_enable_flag',1)
            self.sample_adaptive_offset_enable_flag = self.bsd.assign_data('sample_adaptive_offset_enable_flag',1)
            self.adaptive_leveling_filter_enable_flag = self.bsd.assign_data('adaptive_leveling_filter_enable_flag',1)
            self.affine_enable_flag = self.bsd.assign_data('affine_enable_flag',1)
            self.smvd_enable_flag = self.bsd.assign_data('smvd_enable_flag',1)
            self.ipcm_enable_flag = self.bsd.assign_data('ipcm_enable_flag',1)
            self.amvr_enable_flag = self.bsd.assign_data('amvr_enable_flag',1)
            self.num_of_hmvp_cand = self.bsd.assign_data('num_of_hmvp_cand',4)
            self.umve_enable_flag = self.bsd.assign_data('umve_enable_flag',1)
            if((self.num_of_hmvp_cand==1) & (self.amvr_enable_flag==1)):
                self.emvr_enable_flag = self.bsd.assign_data('emvr_enable_flag',1)
            self.ipf_enable_flag = self.bsd.assign_data('ipf_enable_flag',1)
            self.tscpm_enable_flag = self.bsd.assign_data('tscpm_enable_flag',1)
            self.marker_bit = self.bsd.assign_data('marker_bit',1)
            self.dt_enable_flag = self.bsd.assign_data('dt_enable_flag',1)
            if(self.dt_enable_flag==1):
                self.log2_max_dt_size_minus4 = self.bsd.assign_data('log2_max_dt_size_minus4',2)
                self.max_dt_size = (1 << (self.log2_max_dt_size_minus4 + 4)); 
            self.pbt_enable_flag = self.bsd.assign_data('pbt_enable_flag',1)
            if(self.low_delay==0):
                self.output_reorder_delay = self.bsd.assign_data('output_reorder_delay',5)
            else:
                self.output_reorder_delay = 0
            self.cross_patch_loopfilter_enable_flag = self.bsd.assign_data('cross_patch_loopfilter_enable_flag',1)
            self.ref_colocated_patch_flag = self.bsd.assign_data('ref_colocated_patch_flag',1)
            self.stable_patch_flag = self.bsd.assign_data('stable_patch_flag',1)
            if(self.stable_patch_flag==1):
                self.uniform_patch_flag = self.bsd.assign_data('uniform_patch_flag',1)
                if(self.uniform_patch_flag==1):
                    self.marker_bit = self.bsd.assign_data('marker_bit',1)
                    self.patch_width_minus1 = self.bsd.read_ue('patch_width_minus1  ')
                    self.patch_height_minus1 = self.bsd.read_ue('patch_height_minus1  ')
            self.reserved_bits = self.bsd.assign_data('reserved_bits',2)
            self.bsd.next_start_code()
    
    # 参考图像队列配置集定义
    def reference_picture_list_set(self,rpl):
        print('in func reference_picture_list_set')
        if(self.library_picture_enable_flag==1):
            rpl.reference_to_library_enable_flag = self.bsd.assign_data('reference_to_library_enable_flag',1)
        rpl.ref_pic_num = self.bsd.read_ue('ref_pic_num')
        #self.NumOfRefPic[mlist][rpls] = self.bsd.read_ue('NumOfRefPic[mlist][rpls]')
        #==================malloc array
        #self.library_index_flag[mlist] = [[0 for k in range(self.NumOfRefPic[mlist][rpls])] for j in range(self.num_ref_pic_list_set[mlist])]
        #self.referenced_library_picture_index[mlist] = [[0 for k in range(self.NumOfRefPic[mlist][rpls])] for j in range(self.num_ref_pic_list_set[mlist])]
        #self.abs_delta_doi[mlist] = [[0 for k in range(self.NumOfRefPic[mlist][rpls])] for j in range(self.num_ref_pic_list_set[mlist])]
        #self.sign_delta_doi[mlist] = [[0 for k in range(self.NumOfRefPic[mlist][rpls])] for j in range(self.num_ref_pic_list_set[mlist])]
        ddoi_base=0
        if(rpl.ref_pic_num>0):
            if((self.library_picture_enable_flag)&(rpl.reference_to_library_enable_flag)):
                rpl.library_index_flag[0] = self.bsd.assign_data('library_index_flag',1)
            if(self.library_picture_enable_flag & rpl.library_index_flag[0]):
                rpl.ref_pics_ddoi[0] = self.bsd.read_ue()
            else:
                rpl.ref_pics_ddoi[0] = self.bsd.read_ue()
                if (rpl.ref_pics_ddoi[0] != 0):
                    rpl.ref_pics_ddoi[0] *= 1 - (self.bsd.assign_data('ref_pics_ddoi',1) << 1)
                ddoi_base = rpl.ref_pics_ddoi[0]

        for i in range(rpl.ref_pic_num-1):
            if (self.reference_to_library_enable_flag& rpl.reference_to_library_enable_flag):
                rpl.library_index_flag[i+1] = (self.bsd.assign_data('library_index_flag',1))
 
            if(self.library_picture_enable_flag&rpl.library_index_flag[i+1]):
                rpl.ref_pics_ddoi[i+1] = self.bsd.read_ue('ref_pics_ddoi')
                                          
            else:
                deltaRefPic = self.bsd.read_ue('deltaRefPic')
                #self.abs_delta_doi[mlist][rpls][i] = self.bsd.read_ue('abs_delta_doi[mlist][rpls][i]')
                if(deltaRefPic>0):
                    sign_delta_doi = self.bsd.assign_data('sign_delta_doi',1)
                    deltaRefPic = deltaRefPic*(1-(sign_delta_doi<<1))
                rpl.ref_pics_ddoi[i+1] = ddoi_base + deltaRefPic
                ddoi_base = rpl.ref_pics_ddoi[i+1]
                #if(int(self.abs_delta_doi[mlist][rpls][i]) > 0):
                #    self.sign_delta_doi[mlist][rpls][i] = self.bsd.assign_data('sign_delta_doi[mlist][rpls][i]',1)
        print('out func reference_picture_list_set')        


    # 默认的加权量化矩阵
    def copy_weight_quant_matrix(self):
        tab_WqMDefault4x4[16] =   [64, 64, 64, 68, 64, 64, 68, 72,64, 68, 76, 80,72, 76, 84, 96] 
        tab_WqMDefault8x8[64] =   [64,  64,  64,  64,  68,  68,  72,  76, 64,  64,  64,  68,  72,  76,  84,  92, 64,  64,  68,  72,  76,  80,  88, 100, 64,  68,  72,  80,  84,  92, 100, 112, 68,  72,  80,  84,  92, 104, 112, 128, 76,  80,  84,  92, 104, 116, 132, 152, 96, 100, 104, 116, 124, 140, 164, 188, 104, 108, 116, 128, 152, 172, 192, 216]

        for i in range(4):
            for j in range(4):
                self.WeightQuantMatrix4x4[i][j]= tab_WqMDefault4x4[i*4+j]
        for i in range(8):
            for j in range(8):
                self.WeightQuantMatrix8x8[i][j]= tab_WqMDefault8x8[i*8+j]

    # 自定义加权量化矩阵定义
    def weight_quant_matrix(self):
        print('in func weight_quant_matrix')
        for i in range(4):
            for j in range(4):
                self.WeightQuantMatrix4x4[i][j]= self.bsd.read_ue('weight_quant_coeff4x4')
        for i in range(8):
            for j in range(8):
                self.WeightQuantMatrix8x8[i][j]= self.bsd.read_ue('weight_quant_coeff8x8')
        #for sizeId in range(2):
        #    WQMSize = 1 << (sizeId+2)
        #    for i in range(WQMSize):
        #        for j in range(WQMSize):
        #            weight_quant_coeff = self.bsd.read_ue('weight_quant_coeff')
        #            if(sizeId == 0):
        #                self.WeightQuantMatrix4x4[i][j] = weight_quant_coeff
        #            else:
        #                self.WeightQuantMatrix8x8[i][j] = weight_quant_coeff
        print('out func weight_quant_matrix')

'''
#序列头定义
class sequence_header:
    def __init__(self,input_file,pointer_position):
        self.data_file = input_file
        self.pointer_position = pointer_position
        self.video_sequence_start_code=0#0x000001B0

        
        #帧内预测图像头定义
        self.intra_picture_start_code=0
        self.bbv_delay=0
        self.time_code_flag=0
        self.time_code=0
        self.decode_order_index=0
        self.library_picture_index=0
        self.temporal_id=0
        self.picture_output_delay=0
        self.bbv_check_times=0
        self.progressive_frame=0
        self.picture_structure=0
        self.top_field_first=0
        self.repeat_first_field=0
        self.top_field_picture_flag=0
        self.reserved_bits=0
        self.ref_pic_list_set_flag=[0 for i in range(2)] 
        self.ref_pic_list_set_idx=[0 for i in range(2)] 
        self.fixed_picture_qp_flag=0
        self.picture_qp=0
        self.loop_filter_disable_flag=0
        self.loop_filter_parameter_flag=0
        self.alpha_c_offset=0
        self.beta_offset=0
        self.chroma_quant_param_disable_flag=0
        self.chroma_quant_param_delta_cb=0
        self.chroma_quant_param_delta_cr=0
        self.pic_weight_quant_enable_flag=0
        self.pic_weight_quant_data_index=0
        self.reserved_bits=0
        self.weight_quant_param_index=0
        self.weight_quant_model=0
        self.weight_quant_param_delta1=[0 for i in range(6)]
        self.weight_quant_param_delta2=[0 for i in range(6)]
        self.picture_alf_enable_flag=[0 for i in range(3)]
        #图像数据定义
        self.patch_start_code=0
        self.patch_sao_enable_flag = [0 for i in range(3)]

    def picture_data(self):
        while((self.get_read_data(32) >= dict['patch_start_code1'])&(self.get_read_data(32) <= dict['patch_start_code2'])):#000001+0x00～0x7F(patch_index)
            self.patch()
    
    #片定义
    def patch(self):
        self.patch_start_code=self.bsd.assign_data('patch_start_code',32)#000001+0x00～0x7F(patch_index)
        if (self.fixed_picture_qp_flag == '0'):
            self.fixed_patch_qp_flag=self.bsd.assign_data('fixed_patch_qp_flag',1)
            self.patch_qp=self.bsd.assign_data('patch_qp',7)
        if (self.sample_adaptive_offset_enable_flag=='1'):#SaoEnableFlag
            for compIdx in range(3):
                self.patch_sao_enable_flag[compIdx] = self.bsd.assign_data('patch_sao_enable_flag[compIdx]',1)
        while (self.byte_aligned()==0):#字节对齐
            self.aec_byte_alignment_bit = self.bsd.assign_data('aec_byte_alignment_bit',1)
        while (is_end_of_patch()==0):
            if (FixedQP==0):
                lcu_qp_delta
                PreviousDeltaQP = lcu_qp_delta
            if (SaoEnableFlag):
                if (PatchSaoEnableFlag[0] | PatchSaoEnableFlag[1] | PatchSaoEnableFlag[2]):
                    if (MergeFlagExist):
                        sao_merge_type_index
                    if (SaoMergeMode == 'SAO_NON_MERGE') :
                        for compIdx in range(3):
                            if (PatchSaoEnableFlag[compIdx]) :
                                sao_mode[compIdx]
                                if (SaoMode[compIdx] == 'SAO_Interval'):
                                    for j in range(MaxOffsetNumber):
                                        sao_interval_offset_abs[compIdx][j]
                                        if (SaoIntervalOffsetAbs[compIdx][j]):
                                            sao_interval_offset_sign[compIdx][j]
                                    sao_interval_start_pos[compIdx]
                                    sao_interval_delta_pos_minus2[compIdx]
                                if (SaoMode[compIdx] == 'SAO_Edge'):
                                    for j in range(MaxOffsetNumber):
                                        sao_edge_offset[compIdx][j]
                                    sao_edge_type[compIdx]
            for compIdx in range(3):
                if (PictureAlfEnableFlag[compIdx] == 1):
                    alf_lcu_enable_flag[compIdx][LcuIndex]
            x0 = (LcuIndex % pictureWidthInLcu) * LcuSize
            y0 = (LcuIndex / pictureWidthInLcu) * LcuSize
            coding_unit_tree(x0, y0, 0, 1<<LcuSizeInBit, 1<<LcuSizeInBit, 1, 'PRED_No_Constraint')
            aec_lcu_stuffing_bit
        next_start_code( )
        patch_end_code

    #在位流中检测是否已达到片的结尾，如果已到达片的结尾，返回TRUE，否则返回FALSE
    def is_end_of_patch(self):
        if(self.byte_aligned()):
            if (self.get_read_data(32) == 0x80000001):
                return True#片结束
        else:
            if ((byte_aligned_next_bits(24) == 0x000001) & is_stuffing_pattern( )):
                return True #片结束
        return False

    # 字节是否
    def byte_aligned(self):
        if((self.pointer_position%8)==0):
            return 1
        else:
            return 0
    
    # 扩展和用户数据定义
    def extension_and_user_data(self,i):
        while ((self.get_read_data(32) == dict['extension_start_code']) | (self.get_read_data(32) == dict['user_data_start_code'])):
            if (self.get_read_data(32) == dict['extension_start_code']):#0x000001B5
                self.extension_data(i)
            if (self.get_read_data(32) == dict['user_data_start_code']):#0x000001B2
                self.user_data()
    
    #扩展数据定义
    def extension_data(self,i):
        print('extension_data begin')
        '''
        while ((self.get_read_data(32) == "extension_start_code")):#0x000001B5
            self.extension_start_code = self.bsd.assign_data('intra_picture_start_code',32)
            if(i==0):
                if(self.get_read_data(4)== '0010'):#序列显示扩展 
                    self.sequence_display_extension()
                elif (self.get_read_data(4) == '0011'): # 时域可伸缩扩展 
                    self.temporal_scalability_extension()
                elif (self.get_read_data(4) == '0100'): # 版权扩展 
                    self.copyright_extension()
                elif (self.get_read_data(4) == '0110'): # 内容加密扩展
                    self.cei_extension()
                elif (self.get_read_data(4) == '1010'): # 目标设备显示和内容元数据扩展 
                    self.mastering_display_and_content_metadata_extension()
                elif (self.get_read_data(4) == '1011'): # 摄像机参数扩展 
                    self.camera_parameters_extension()
                elif (self.get_read_data(4) == '1101'): # 参考知识图像扩展
                    self.cross_random_access_point_reference_extension()
                else:
                    while (self.get_read_data(24) != '000000000000000000000001'):
                        self.reserved_extension_data_byte
            else:#图像头之后
                if (self.get_read_data(4) == '0100'): # 版权扩展 
                    self.copyright_extension()
                elif ( self.get_read_data(4) == '0101' ): # 高动态范围图像元数据扩展
                    self.hdr_dynamic_metadata_extension()
                elif (self.get_read_data(4) == '0111'): # 图像显示扩展
                    self.picture_display_extension()
                elif (self.get_read_data(4) == '1011'): # 摄像机参数扩展
                    self.camera_parameters_extension()
                elif (self.get_read_data(4) == '1100'): #感兴趣区域参数扩展
                    self.roi_parameters_extension()
                else:
                    while (self.get_read_data(24) != '0000 0000 0000 0000 0000 0001'):
                        self.reserved_extension_data_byte
        '''
    #用户数据定义
    def user_data(self):
        print('user_data begin')
        self.user_data_start_code=self.bsd.assign_data('user_data_start_code',32)
        while (self.get_read_data(24) != '000000000000000000000001'):
            self.user_data=self.bsd.assign_data('user_data',8)

    #帧内预测图像头定义
    def intra_picture_header(self):
        print('intra_picture_header begin begin begin begin begin begin begin begin begin begin begin begin begin')
        self.intra_picture_start_code = self.bsd.assign_data('intra_picture_start_code',32)
        self.bbv_delay = self.bsd.assign_data('bbv_delay',32)
        self.time_code_flag = self.bsd.assign_data('time_code_flag',1)
        if (self.time_code_flag == '1'):
            self.time_code = self.bsd.assign_data('time_code',24)
        self.decode_order_index = self.bsd.assign_data('decode_order_index',8)
        
        if (self.library_stream_flag=='1'):
            self.library_picture_index = self.bsd.read_ue()
        if (self.temporal_id_enable_flag == '1'):
            self.temporal_id = self.bsd.assign_data('temporal_id',3)
            
        if (self.low_delay == '0'):
            self.picture_output_delay=self.bsd.read_ue()
        if (self.low_delay == '1'):
            self.bbv_check_times=self.bsd.read_ue()
            
        self.progressive_frame = self.bsd.assign_data('progressive_frame',1)
        if (self.progressive_frame == '0'):
            self.picture_structure= self.bsd.assign_data('picture_structure',1)
        self.top_field_first= self.bsd.assign_data('top_field_first',1)
        self.repeat_first_field= self.bsd.assign_data('repeat_first_field',1)
        if (self.field_coded_sequence == '1'):
            self.top_field_picture_flag= self.bsd.assign_data('top_field_picture_flag',1)
            self.reserved_bits= self.bsd.assign_data('reserved_bits',1)
            
        self.ref_pic_list_set_flag[0]= self.bsd.assign_data('ref_pic_list_set_flag[0]',1)
        if ( self.ref_pic_list_set_flag[0]=='1'):
            if (int(self.num_ref_pic_list_set[0]) > 1):
                self.ref_pic_list_set_idx[0]=self.bsd.read_ue()
        else:
            self.reference_picture_list_set(0, self.num_ref_pic_list_set[0])
        if (self.rpl1_idx_exist_flag=='1'):
            self.ref_pic_list_set_flag[1]= self.bsd.assign_data('ref_pic_list_set_flag[1]',1)
        if (self.ref_pic_list_set_flag[1]=='1'):
            if ((self.rpl1_idx_exist_flag=='1') & (int(self.num_ref_pic_list_set[1]) > 1)):
                self.ref_pic_list_set_idx[1]=self.bsd.read_ue()
        else:
            self.reference_picture_list_set(1, self.num_ref_pic_list_set[1])
        self.fixed_picture_qp_flag= self.bsd.assign_data('fixed_picture_qp_flag',1)
        self.picture_qp= self.bsd.assign_data('picture_qp',7)
        self.loop_filter_disable_flag= self.bsd.assign_data('loop_filter_disable_flag',1)
        if (self.loop_filter_disable_flag == '0'):
            self.loop_filter_parameter_flag= self.bsd.assign_data('loop_filter_parameter_flag',1)
            if (self.loop_filter_parameter_flag=='1'):
                self.alpha_c_offset=self.bsd.read_se()
                self.beta_offset=self.bsd.read_se()
        self.chroma_quant_param_disable_flag= self.bsd.assign_data('chroma_quant_param_disable_flag',1)
        
        if (self.chroma_quant_param_disable_flag == '0'):
            self.chroma_quant_param_delta_cb=self.bsd.read_se()
            self.chroma_quant_param_delta_cr=self.bsd.read_se()
             
        if (self.weight_quant_enable_flag=='1'):
            self.pic_weight_quant_enable_flag= self.bsd.assign_data('pic_weight_quant_enable_flag',1)
            if (self.pic_weight_quant_enable_flag=='1'):
                self.pic_weight_quant_data_index= self.bsd.assign_data('pic_weight_quant_data_index',2)
                if (self.pic_weight_quant_data_index == '01'):
                    self.reserved_bits= self.bsd.assign_data('reserved_bits',1)
                    self.weight_quant_param_index = self.bsd.assign_data('weight_quant_param_index',2)
                    self.weight_quant_model = self.bsd.assign_data('weight_quant_model',2)
                    if (self.weight_quant_param_index == '01'):
                        for i in range(6):
                            self.weight_quant_param_delta1[i] = self.bsd.read_se()
                    if (self.weight_quant_param_index == '10'):
                         for i in range(6):
                            weight_quant_param_delta2[i] = self.bsd.read_se()
                elif(self.pic_weight_quant_data_index == '10'):
                    self.weight_quant_matrix()
        if (self.adaptive_leveling_filter_enable_flag=='1'):#AlfEnableFlag
            for compIdx in range(3):
                self.picture_alf_enable_flag[compIdx] = self.bsd.assign_data('self.picture_alf_enable_flag[compIdx]',1)
            if (self.picture_alf_enable_flag[0] == '1' | self.picture_alf_enable_flag[1] == '1' | self.picture_alf_enable_flag[2] == '1'):#picture_alf_enable_flag
                self.alf_parameter_set()
        #self.next_start_code()
        print('position....................',self.pointer_position)

    
            self.intra_picture_header()
            print('position....................',self.pointer_position)
            self.pop_read_data(32)
            self.extension_and_user_data(1)

'''
'''
#序列显示扩展定义

class sequence_display_extension:
    def __init__(self):
        self.extension_id=4#0010,不同的值有不同的含义
        self.video_format=3
        self.sample_range=1
        self.colour_description=1
        if (self.colour_description):
            self.colour_primaries=8
            self.transfer_characteristics=8
            self.matrix_coefficients=8
        self.display_horizontal_size=14
        self.marker_bit=1
        self.display_vertical_size=14
        self.td_mode_flag=1
        if (self.td_mode_flag == '1'):
            self.td_packing_mode=8
            self.view_reverse_flag=1

    #时域可伸缩扩展定义  
class temporal_scalability_extension():
    def __init__():
        extension_id=4#0010
        num_of_temporal_level_minus1=3
        for i in range(num_of_temporal_level_minus1):
            temporal_frame_rate_code[i]=4
            temporal_bit_rate_lower[i]=4
            marker_bit=4
            temporal_bit_rate_upper[i]=4
        
    
    #版权扩展定义
    
class copyright_extension:
    def __init__():
        self.extension_id=4#0010
        self.copyright_flag=1
        self.copyright_id=8
        self.original_or_copy=1
        self.reserved_bits=7
        self.marker_bit1=1
        self.copyright_number_1=20
        self.marker_bit2=1
        self.copyright_number_2=22
        self.marker_bit=1
        self.copyright_number_3=22
        next_start_code()    

#内容加密扩展定义

class  cei_extension:
    def __init__():
        self.extension_id=4#0010
        self.content_encryption_algorithm=8
        self.content_encryption_method=8
        self.original_or_copy=1
        self.marker_bit1=1
        self.cek_id_len=8
        self.marker_bit2=1
        self.cek_id_number_1=18
        self.marker_bit3=1
        self.cek_id_number_2=22
        self.marker_bit4=1
        self.cek_id_number_3=22
        self.marker_bit5=1
        self.cek_id_number_4=22
        self.marker_bit6=1
        self.cek_id_number_5=22
        self.marker_bit7=1
        self.cek_id_number_6=22
        self.marker_bit8=1
        self.iv_len=8
        self.marker_bit9=1
        self.iv_number_1=18
        self.marker_bit10=1
        self.iv_number_2=22
        self.marker_bit11=1
        self.iv_number_3=22
        self.marker_bit12=1
        self.iv_number_4=22
        self.marker_bit13=1
        self.iv_number_5=22
        self.marker_bit14=1
        self.iv_number_6=22
        self.marker_bit15=1
        self.reserved_bits=5
 

#高动态范围图像扩展定义

class hdr_dynamic_metadata_extension:
    def __init__():
        extension_id=4#0010
        extension_id=4#0010
        while ( next_bits(24) != '0000 0000 0000 0000 0000 0001'):
            extension_data_byte
    

#目标设备显示和内容元数据扩展定义

class mastering_display_and_content_metadata_extension:
    def __init__():
        self.extension_id=4#0010
        for i in range(3):
            self.display_primaries_x[i]=16
            self.marker_bit=1
            self.display_primaries_y[i]=16
            self.marker_bit=1
            self.white_point_x =16
            self.marker_bit =1
            self.white_point_y =16
            self.marker_bit =1
            self.max_display_mastering_luminance =16
            self.marker_bit =1
            self.min_display_mastering_luminance =16
            self.marker_bit 
            self.max_content_light_level =16
            self.marker_bit 
            self.max_picture_average_light_level =16
            self.marker_bit 
            self.reserved_bits =16

#摄像机参数扩展定义

class camera_parameters_extension:
    def __init__():
        self.extension_id =4#0010
        self.reserved_bits =1
        self.camera_id =7
        self.marker_bit =1
        self.height_of_image_device =22
        self.marker_bit =1
        self.focal_length =22
        self.marker_bit =1
        self.f_number =22
        self.marker_bit =1
        self.vertical_angle_of_view =22
        self.marker_bit =1
        self.camera_position_x_upper =16
        self.marker_bit =1
        self.camera_position_x_lower =16
        self.marker_bit =1
        self.camera_position_y_upper =16
        self.marker_bit =1
        self.camera_position_y_lower =16
        self.marker_bit =1
        self.camera_position_z_upper =16
        self.marker_bit =1
        self.camera_position_z_lower =16
        self.marker_bit =1
        self.camera_direction_x =22
        self.marker_bit =1
        self.camera_direction_y =22
        self.marker_bit =1
        self.camera_direction_z =22
        self.marker_bit =1
        self.image_plane_vertical_x =22
        self.marker_bit =1
        self.image_plane_vertical_y =22
        self.marker_bit =1
        self.image_plane_vertical_z =22
        self.marker_bit =1
        self.reserved_bits =16

#感兴趣区域参数扩展定义

class roi_parameters_extension:
    def __init__():
        self.extension_id=4#0010
        self.current_picture_roi_num=8
        self.roiIndex = 0
        if(PictureType!=0):
            self.prev_picture_roi_num=8
            for i in range(self.prev_picture_roi_num):
                self.roi_skip_run
                if (roi_skip_run != '0'):
                    for j in range(self.roi_skip_run):
                        self.skip_roi_mode[i+j]=1
                        if (j % 22 == 0):
                            marker_bit
                        if (skip_roi_mode == '1'):
                            ROIInfo[roiIndex].asisx = PrevROIInfo[i+j] .asisx
                            ROIInfo[roiIndex].asisy = PrevROIInfo[i+j] .asisy
                            ROIInfo[roiIndex].width = PrevROIInfo[i+j] .width
                            ROIInfo[roiIndex].height = PrevROIInfo[i+j].height
                            roiIndex = roiIndex+1
                    i=i+j
                    marker_bit
                else:
                    roi_axisx_delta
                    marker_bit
                    roi_axisy_delta
                    marker_bit
                    roi_width_delta
                    marker_bit
                    roi_height_delta
                    marker_bit
                    ROIInfo[roiIndex].asisx = PrevROIInfo[i+j] .asisx + ROIAxisxDelta
                    ROIInfo[roiIndex].asisy = PrevROIInfo[i+j] .asisy + ROIAxisyDelta
                    ROIInfo[roiIndex].width = PrevROIInfo[i+j] . width + ROIWidthDelta
                    ROIInfo[roiIndex].height = PrevROIInfo[i+j]. height + ROIHeightDelta
                    roiIndex=roiIndex+1
            for i in range(current_picture_roi_num):
                roi_axisx
                marker_bit
                roi_axisy
                marker_bit
                roi_width
                marker_bit
                roi_height
                marker_bit
                ROIInfo[roiIndex].asisx = roi_axisx
                ROIInfo[roiIndex].asisy = roi_axisy
                ROIInfo[roiIndex].width = roi_width
                ROIInfo[roiIndex].height = roi_height
                roiIndex = roiIndex+1
        for i in range(roiIndex): 
            PrevROIInfo[i].asisx = ROIInfo[i].asisx
            PrevROIinfo[i].asisy = ROIInfo[i].asisy
            PrevROIinfo[i].width = ROIInfo[i].width
            PrevROIinfo[i].height = ROIInfo[i].height

                    

#参考知识图像扩展定义

class cross_random_access_point_reference_extension:
    def __init__():
        self.extension_id#0010
        self.crr_lib_number
        self.marker_bit
        while(i<crr_lib_number):
            crr_lib_pid[i]
            i=i+1
            if( i%2 == 0):
                marker_bit




#帧间预测图像头定义

class inter_picture_header:
    def __init__(seq_data):
        self.inter_picture_start_code=32#0x000001B6
        self.random_access_decodable_flag=1
        self.bbv_delay=32
        self.picture_coding_type=2
        self.decode_order_index=8
        if (temporal_id_enable_flag == '1'):
            temporal_id=3
        if (low_delay == '0'):
            picture_output_delay
        if (low_delay == '1'):
            bbv_check_times
            progressive_frame
        if (progressive_frame == '0'):
            picture_structure
        top_field_first
        repeat_first_field
        if (field_coded_sequence == '1'):
            top_field_picture_flag
            reserved_bits
        ref_pic_list_set_flag[0]
        if (RefPicListSetFlag[0]):
            if ( NumRefPicListSet[0] > 1 ):
                ref_pic_list_set_idx[0]
        else:
            reference_picture_list_set(0, NumRefPicListSet[0])
        if (Rpl1IdxExistFlag):
            ref_pic_list_set_flag[1]
        if (RefPicListSetFlag[1]):
            if (Rpl1IdxExistFlag & NumRefPicListSet[1] > 1):
                ref_pic_list_set_idx[1]
        else:
            reference_picture_list_set(1, NumRefPicListSet[1])
        self.num_ref_active_override_flag=1
        if (num_ref_active_override_flag == '1'):
            num_ref_active_minus1[0]
            if (picture_coding_type == '10'):
                num_ref_active_minus1[1]
        fixed_picture_qp_flag
        picture_qp
        if ((((picture_coding_type == '10') & (PictureStructure == 1)))==0):
            reserved_bits
        loop_filter_disable_flag
        if (loop_filter_disable_flag == '0'):
            loop_filter_parameter_flag
            if (loop_filter_parameter_flag == '1'):
                alpha_c_offset
                beta_offset
        chroma_quant_param_disable_flag
        if (chroma_quant_param_disable_flag == '0'):
            chroma_quant_param_delta_cb
            chroma_quant_param_delta_cr
        if (WeightQuantEnableFlag):
            pic_weight_quant_enable_flag
            if (PicWeightQuantEnableFlag):
                pic_weight_quant_data_index
                if (pic_weight_quant_data_index == '01'):
                    reserved_bits
                    weight_quant_param_index
                    if (weight_quant_param_index == '01'):
                        for i in range(6):
                            weight_quant_param_delta1[i]
                    if (weight_quant_param_index == '10'):
                        for i in range(6):
                            weight_quant_param_delta2[i]
                elif (pic_weight_quant_data_index == '10'):
                    weight_quant_matrix()
        if (AlfEnableFlag):
            for compIdx in range(3):
                picture_alf_enable_flag[compIdx]
            if (PictureAlfEnableFlag[0] == 1 | PictureAlfEnableFlag[1] == 1 | PictureAlfEnableFlag[2] == 1):
                alf_parameter_set()
        if (AffineEnableFlag):
            affine_subblock_size_flag

#图像显示扩展定义

class picture_display_extension:
    def __init__(seq_data):
        extension_id#0010
        for i in range(NumberOfFrameCentreOffsets):
            picture_centre_horizontal_offset
            marker_bit
            picture_centre_vertical_offset
            marker_bit


#编码树定义

class coding_unit_tree():
    def __init__(self,x0, y0, split, width, height, qt, mode,seq_data):
        isBoundary = ((x0+width) > PicWidthInLuma) | ((y0+height) > PicHeightInLuma)
        rightBoundary = ((x0+width) > PicWidthInLuma) & ((y0+height) <= PicHeightInLuma)
        bottomBoundary = ( (x0 + width) <= PicWidthInLuma ) & ( (y0 + height) > PicHeightInLuma)
        allowNoSplit = 0
        allowSplitQt = 0
        allowSplitBtVer = 0
        allowSplitBtHor = 0
        allowSplitEqtVer = 0
        allowSplitEqtHor = 0
        if (isBoundary):
            allowNoSplit = 0
            if ((PictureType == 0) & (width > 64) & (height > 64)):
                allowSplitQt = 1
                allowNoSplit = 1
            elif ((width == 64 & height > 64) | (height == 64 & width > 64)):
                allowSplitBtHor = 1
                allowSplitBtVer = 1
            elif ((rightBoundary==0) & (bottomBoundary==0)):
                allowSplitQt = 1
            elif (rightBoundary):
                allowSplitBtVer = 1
            elif (bottomBoundary):
                allowSplitBtHor = 1
        else:
            if (((width == 64) & (height > 64)) | ((height == 64) & (width > 64))):
                allowSplitBtHor = 1
                allowSplitBtVer = 1
                allowNoSplit = 1
            elif (split >= MaxSplitTimes):
                allowNoSplit = 1
            elif ((PictureType == 0) & (width == 128) & (height == 128)) :
                allowSplitQt = 1
                allowNoSplit = 1
            else :
                if ((width <= height * MaxPartRatio) & (height <= width * MaxPartRatio)):
                    allowNoSplit = 1
                if ((width > MinQtSize) & qt):
                    allowSplitQt = 1
                if ((width <= MaxBtSize) & (height <= MaxBtSize) & (width > MinBtSize) & (height < MaxPartRatio*width)):
                    allowSplitBtVer = 1
                if ((width <= MaxBtSize) & (height <= MaxBtSize) & (height > MinBtSize) & (width <MaxPartRatio*height)):
                    allowSplitBtHor = 1
                if ((width <= MaxEqtSize) & (height <= MaxEqtSize) & (height >= MinEqtSize*2) & (width >= MinEqtSize*4) & (height*4 <= MaxPartRatio*width)):
                    allowSplitEqtVer = 1
                if ( (width <= MaxEqtSize) & (height <= MaxEqtSize) & (width >= MinEqtSize*2) & (height >= MinEqtSize*4) & (width*4 <= MaxPartRatio*height)):
                    allowSplitEqtHor = 1
        allowSplitBt = allowSplitBtVer | allowSplitBtHor
        allowSplitEqt = allowSplitEqtVer | allowSplitEqtHor
        if (allowSplitQt & (allowNoSplit | allowSplitBt | allowSplitEqt)):
            qt_split_flag
        if (QtSplitFlag==0):
            if (allowNoSplit & (allowSplitBt | allowSplitEqt)):
                bet_split_flag
            if (BetSplitFlag):
                if (allowSplitBt & allowSplitEqt):
                    bet_split_type_flag
                if ((BetSplitTypeFlag==0) & allowSplitBtHor & allowSplitBtVer) | (BetSplitTypeFlag &allowSplitEqtHor & allowSplitEqtVer):
                    bet_split_dir_flag
        if ((PictureType != 0) & ((((BetSplitFlag & (BetSplitTypeFlag==0)) | QtSplitFlag) & (width * height== 64)) | (BetSplitTypeFlag & (width * height == 128)))):
            root_cu_mode
            if(root_cu_mode):
                modeChild = 'PRED_Intra_Only'
            else:
                modeChild = 'PRED_Inter_Only'
            
        else:
            modeChild = mode
        if (ChildSizeOccur4):
            if (Component == 0):
                LumaWidth = width
                LumaHeight = height
                Component = 1
        if (BlockSplitMode == 'SPLIT_QT'):
            QtWidth = width / 2
            QtHeight = height / 2
            x1 = x0 + QtWidth
            y1 = y0 + QtHeight
            coding_unit_tree(x0, y0, split+1, QtWidth, QtHeight, 1, modeChild)
            if (x1 < PicWidthInLuma):
                coding_unit_tree(x1, y0, split+1, QtWidth, QtHeight, 1, modeChild)
            if (y1 < PicHeightInLuma):
                coding_unit_tree(x0, y1, split+1, QtWidth, QtHeight, 1, modeChild)
            if ((x1 < PicWidthInLuma) & (y1 < PicHeightInLuma)):
                coding_unit_tree(x1, y1, split+1, QtWidth, QtHeight, 1, modeChild)
            if ((LumaWidth == width) & (LumaHeight == height) & ChildSizeOccur4):
                coding_unit(x0, y0, width, height, 'PRED_No_Constraint', 'COMPONENT_Chroma')
                Component = 0
        elif (BlockSplitMode == 'SPLIT_BT_VER'):
            x1 = x0 + width / 2
            coding_unit_tree(x0, y0, split+1, width/2, height, 0, modeChild)
            if (x1 < PicWidthInLuma):
                coding_unit_tree(x1, y0, split+1, width/2, height, 0, modeChild)
            if ((LumaWidth == width) & (LumaHeight == height) & ChildSizeOccur4):
                coding_unit (x0, y0, width, height, 'PRED_No_Constraint', 'COMPONENT_Chroma')
                Component = 0
        elif (BlockSplitMode == 'SPLIT_BT_HOR'):
            y1 = y0 + height / 2
            coding_unit_tree(x0, y0, split+1, width, height/2, 0, modeChild)
            if (y1 < PicHeightInLuma):
                coding_unit_tree(x0, y1, split+1, width, height/2, 0, modeChild)
            if ((LumaWidth == width) & (LumaHeight == height) & ChildSizeOccur4):
                coding_unit(x0, y0, width, height, 'PRED_No_Constraint', 'COMPONENT_Chroma')
                Component = 0
        elif (BlockSplitMode == 'SPLIT_EQT_VER'):
            x1 = x0 + width / 4
            x2 = x0 + (3 * width / 4)
            y1 = y0 + height / 2
            coding_unit_tree(x0, y0, split+1, width/4, height, 0, modeChild)
            coding_unit_tree(x1, y0, split+1, width/2, height/2, 0, modeChild)
            coding_unit_tree(x1, y1, split+1, width/2, height/2, 0, modeChild)
            coding_unit_tree(x2, y0, split+ 1, width/4, height, 0, modeChild)
            if ((LumaWidth == width) & (LumaHeight == height) & ChildSizeOccur4):
                coding_unit(x0, y0, width, height, 'PRED_No_Constraint', 'COMPONENT_Chroma')
                Component = 0
        elif (BlockSplitMode == 'SPLIT_EQT_HOR') :
            x1 = x0 + width / 2
            y1 = y0 + height / 4
            y2 = y0 + (3 * height / 4)
            coding_unit_tree(x0, y0, split+1, width, height/4, 0, modeChild)
            coding_unit_tree(x0, y1, split+1, width/2, height/2, 0, modeChild)
            coding_unit_tree(x1, y1, split+1, width/2, height/2, 0, modeChild)
            coding_unit_tree(x0, y2, split+1, width, height/4, 0, modeChild)
            if ((LumaWidth == width) & (LumaHeight == height) & ChildSizeOccur4):
                coding_unit(x0, y0, width, height, 'PRED_No_Constraint', 'COMPONENT_Chroma')
                Component = 0
        else:
            if (Component == 0):
                coding_unit(x0, y0, width, height, mode, 'COMPONENT_LUMACHROMA')
            elif (Component == 1):
                coding_unit(x0, y0, width, height, mode, 'COMPONENT_LUMA')
        

#编码单元定义

class coding_unit:
    def __init__(x0, y0, width, height, mode, component):
        if (component == 'COMPONENT_Chroma'):
            if ((priorCuMode == 1) & (chroma_format != '00')):
                intra_chroma_pred_mode
            NumOfTransBlocks = 3
            ctp_y[0] = 0
            CuCtp += ctp_y[0]
            if (IntraChromaPredMode != 'Intra_Chroma_PCM'):
                ctp_u
                CuCtp += (ctp_u << 1)
                ctp_v
                CuCtp += (ctp_v << 2)
            for i in range(2):
                IsPcmMode[i-2+NumOfTransBlocks] = (IntraChromaPredMode == 'Intra_Chroma_PCM')
                IsChroma = 0
                if (i == NumOfTransBlocks -1 | i == NumOfTransBlocks -2):
                    IsChroma = 1
                block(i, width, height, CuCtp, IsChroma, IsPcmMode[i], component)
        else:
            if (PictureType != 0):
                if (mode != 'PRED_Intra_Only'):
                    self.skip_flag 
                if (self.skip_flag):
                    if (UmveEnableFlag):
                        umve_flag
                    if (AffineEnableFlag & (UmveFlag==0)  & (width >= 16) & (height >= 16)):
                        affine_flag
                if (~SkipFlag):
                    if (mode != 'PRED_Intra_Only'):
                        direct_flag
                    if (DirectFlag):
                        if (UmveEnableFlag):
                            umve_flag
                        if (AffineEnableFlag & (UmveFlag==0)  & (width >= 16) & (height >= 16)):
                            affine_flag
                    if (~DirectFlag & (mode == 'PRED_No_Constraint')):
                        intra_cu_flag
            PartSize = 'SIZE_2Mx2N'
            if (DtEnableFlag & IntraCuFlag):
                allowDtHorSplit = (height >= DtMinSize) & (height <= DtMaxSize) & (width / height < 4)& (width <= DtMaxSize)
                allowDtVerSplit = (width >= DtMinSize) & (width <= DtMaxSize) & (height / width < 4)& (height <= DtMaxSize)
                if (allowDtHorSplit | allowDtVerSplit):
                    dt_split_flag
                    if (DtSplitFlag):
                        if (allowDtHorSplit & allowDtVerSplit):
                            dt_split_dir
                        elif (allowDtHorSplit):
                            DtSplitDir = 1
                        else:
                            DtSplitDir = 0
                    else:
                        dt_split_vqt_flag
                        if (~DtSplitVqtFlag):
                            dt_split_vadt_flag
            if (UmveFlag):
                umve_mv_idx
                umve_step_idx
                umve_dir_idx
            elif ((SkipFlag | DirectFlag) & AffineFlag):
                cu_affine_cand_idx
            elif (SkipFlag | DirectFlag):
                cu_subtype_index
            if ((SkipFlag==0)  & (DirectFlag==0)):
                if (IntraCuFlag==0):
                    if (AffineEnableFlag & (width >= 16) & (height >= 16)):
                        affine_flag
                if (AmvrEnableFlag):
                    if (EmvrEnableFlag & ~AffineFlag):
                        extend_mvr_flag
                    if (AffineFlag):
                        affine_amvr_index
                    else:
                        amvr_index
                if (PictureType == 2):
                    inter_pred_ref_mode
                if (SmvdEnableFlag & SmvdApplyFlag & ~AffineFlag & (InterPredRefMode == 2)& ~ExtendMvrFlag):
                    smvd_flag
                if (MvExistL0):
                    if ((SmvdFlag==0) & NumRefActive[0] > 1):
                        pu_reference_index_l0
                    mv_diff_x_abs_l0
                    if (MvDiffXAbsL0):
                        mv_diff_x_sign_l0
                    mv_diff_y_abs_l0
                    if (MvDiffYAbsL0):
                        mv_diff_y_sign_l0
                    if (AffineFlag):
                        mv_diff_x_abs_l0_affine
                    if (MvDiffXAbsL0Affine):
                        mv_diff_x_sign_l0_affine
                    mv_diff_y_abs_l0_affine
                    if (MvDiffYAbsL0Affine):
                        mv_diff_y_sign_l0_affine
                if (MvExistL1 &  (SmvdFlag==0)):
                    if (NumRefActive[1] > 1):
                        pu_reference_index_l1
                    mv_diff_x_abs_l1
                    if (MvDiffXAbsL1):
                        mv_diff_x_sign_l1
                    mv_diff_y_abs_l1
                    if (MvDiffYAbsL1):
                        mv_diff_y_sign_l1
                    if (AffineFlag):
                        mv_diff_x_abs_l1_affine
                        if (MvDiffXAbsL1Affine):
                            mv_diff_x_sign_l1_affine
                        mv_diff_y_abs_l1_affine
                        if (MvDiffYAbsL1Affine):
                            mv_diff_y_sign_l1_affine
            else:
                TuOrder = 0
                for i in range(NumOfIntraPredBlock):
                    intra_luma_pred_mode
                if (PartSize == 'SIZE_2Mx2N'):
                    IsPcmMode[TuOrder] = (IntraLumaPredMode == 'Intra_Luma_PCM')
                    TuOrder=TuOrder+1
                else:
                    IsPcmMode[0] = 0
                    IsPcmMode[1] = 0
                    IsPcmMode[2] = 0
                    IsPcmMode[3] = 0
                    TuOrder=3
                if (IntraCuFlag & (chroma_format != '00') & (component=='COMPONENT_LUMACHROMA')):
                    intra_chroma_pred_mode
                    IsPcmMode[TuOrder+1] = (IntraChromaPredMode == 'Intra_Chroma_PCM')
                    IsPcmMode[TuOrder+2] = (IntraChromaPredMode == 'Intra_Chroma_PCM')
                if (IpfEnableFlag & (PartSize == 'SIZE_2Mx2N') & (~IsPcmMode[0])):
                    ipf_flag
        if ((IntraCuFlag==0) & (SkipFlag==0)):
            if ((DirectFlag==0) & component == 'COMPONENT_LUMACHROMA'):
                ctp_zero_flag
            CuCtp = 0
            if ((CtpZeroFlag==0)):
                if (PbtEnableFlag & (width / height < 4) & (height / width < 4) & (width >= 8) &(width <= 32)& (height >= 8) & (height <= 32)):
                    pbt_cu_flag
                if (PbtCuFlag==0):
                    if (component == 'COMPONENT_LUMACHROMA'):
                        ctp_u
                        ctp_v
                    CuCtp = ctp_u << (NumOfTransBlocks)
                    CuCtp = CuCtp>>2
                    CuCtp += (ctp_v << (NumOfTransBlocks))
                    CuCtp = CuCtp>>1
                    if (((ctp_u != 0) | (ctp_v != 0)) | ( component !='COMPONENT_LUMACHROMA')):
                        ctp_y[0]
                        CuCtp += ctp_y[0]
                    else:
                        CuCtp += ctp_y[0]
                else:
                    if (component == 'COMPONENT_LUMACHROMA'):
                        ctp_u
                        ctp_v
                    CuCtp = ctp_u << (NumOfTransBlocks)
                    CuCtp = CuCtp>>2
                    CuCtp += (ctp_v << (NumOfTransBlocks))
                    CuCtp = CuCtp>>1
                    for i in range((NumOfTransBlocks-2)):
                        ctp_y[i]
                        CuCtp += (ctp_y[i] << i)
        elif (~ SkipFlag):
            CuCtp = 0
            if (~ IsPcmMode[0]):
                for i in range(NumOfTransBlocks-2):
                    ctp_y[i]
                    CuCtp += (ctp_y[i] << i)
            if ((component == 'COMPONENT_LUMACHROMA') & (IntraChromaPredMode !='Intra_Chroma_PCM')):
                ctp_u
                ctp_v
            CuCtp += (ctp_u << (NumOfTransBlocks-2))
            CuCtp += (ctp_v << (NumOfTransBlocks-1))
        for i in range(NumOfTransBlocks):
            if (i < NumOfTransBlocks-2):
                if((TransformSplitDirection == 0) | (TransformSplitDirection == 2)):
                    blockWidth = width
                elif(TransformSplitDirection==1):
                    blockWidth=width >> 1
                else:
                    blockWidth=width >> 2
                #
                if((TransformSplitDirection == 0) | (TransformSplitDirection == 3)):
                    blockHeight = height
                elif(TransformSplitDirection==1):
                    blockHeight = height >> 1
                else:
                    blockHeight = height >> 2
                #
                if((TransformSplitDirection == 0) | (TransformSplitDirection == 2)):
                    blockX = 0
                elif(TransformSplitDirection==1):
                    blockX = (blockWidth >> 1) * (i % 2)
                else:
                    blockX = (blockWidth >> 2) * i
                #
                if((TransformSplitDirection == 0) | (TransformSplitDirection == 3)):
                    blockY = 0
                elif(TransformSplitDirection==1):
                    blockY = (blockHeight >> 1) * (i / 2)
                else:
                    blockY = (blockHeight >> 2) * i
                #blockWidth = ((TransformSplitDirection == 0) | (TransformSplitDirection == 2)) ?width : (TransformSplitDirection == 1 ? width >> 1 : width >> 2)
                #blockHeight = ((TransformSplitDirection == 0) | (TransformSplitDirection == 3)) ?height : (TransformSplitDirection == 1 ? height >> 1 : height >> 2)
                #blockX = x0 + (((TransformSplitDirection == 0) | (TransformSplitDirection == 2)) ? 0 :TransformSplitDirection == 1 ? ((blockWidth >> 1) * (i % 2)) : ((blockWidth >> 2) * i)))
                #blockY = y0 + (((TransformSplitDirection == 0) | (TransformSplitDirection == 3)) ? 0 :TransformSplitDirection == 1 ? ((blockHeight >> 1) * (i / 2)) : ((blockHeight >> 2) * i)))
                IsChroma = 0
                if (i == NumOfTransBlocks -1 | i == NumOfTransBlocks -2):
                    IsChroma = 1
                block(i, blockWidth, blockHeight, CuCtp, IsChroma, IsPcmMode[i], component)


#变换块定义

class block:
    def __init__(i, blockWidth, blockHeight, CuCtp, isChroma, isPcm, component):
        M1 = blockWidth
        M2 = blockHeight
        for x in range(M1):
            for y in range(M2):
                QuantCoeffMatrix[x][y] = 0
        if (~isPcm):
            if (CuCtp & (1 << i)):
                blockWidth = blockWidth / 2 if isChroma else blockWidth
                blockHeight = blockHeight / 2 if isChroma else blockHeight
                #blockWidth = isChroma ? blockWidth / 2 : blockWidth
                #blockHeight = isChroma ? blockHeight / 2 : blockHeight
                idxW = Log(blockWidth) -1
                idxH = Log(blockHeight) -1
                NumOfCoeff = blockWidth * blockHeight
                ScanPosOffset = 0
                while (~coeff_last):
                    coeff_run
                    coeff_level_minus1
                    coeff_sign
                    AbsLevel = coeff_level_minus1 + 1
                    ScanPosOffset = ScanPosOffset + coeff_run
                    PosxInBlk = InvScanCoeffInBlk[idxW][idxH][ScanPosOffset][0]
                    PosyInBlk = InvScanCoeffInBlk[idxW][idxH][ScanPosOffset][1]
                    QuantCoeffMatrix[PosxInBlk][PosyInBlk] = (~AbsLevel) if coeff_sign else AbsLevel
                    #QuantCoeffMatrix[PosxInBlk][PosyInBlk] = coeff_sign ? –AbsLevel : AbsLevel
                    if (ScanPosOffset >= NumOfCoeff - 1):
                        break
                    coeff_last
                    ScanPosOffset = ScanPosOffset + 1
        elif ((component != 'COMPONENT_CHROMA' & i == 0) | (component =='COMPONENT_CHROMA' & i == 1)):
            aec_ipcm_stuffing_bit
            while (~byte_aligned()):
                aec_byte_alignment_bit0
        M1 = blockWidth / 2 if isChroma else blockWidth
        M2 = blockHeight / 2 if isChroma else blockHeight
        #M1 = isChroma ? blockWidth / 2 : blockWidth
        #M2= isChroma ? blockHeight / 2 : blockHeight
        xMin = Min(32, M1)
        yMin = Min(32, M2)
        for yStep in range(M2/yMin):
            for xStep in range(M1/xMin):
                for y in range(yMin):
                    for x in range(xMin):
                        pcm_coeff
                        QuantCoeffMatrix[x+xStep*xMin][y + yStep*yMin] = pcm_coeff



#自适应修正滤波参数定义

class alf_parameter_set:
    def __init__(seq_data):
        if (PictureAlfEnableFlag[0] == 1):
            alf_filter_num_minus1
            for i in range(alf_filter_num_minus1+1):
                if ((i > 0) & (alf_filter_num_minus1 != 15)):
                    alf_region_distance[i]
                for j in range(9):
                    alf_coeff_luma[i][j]
        if(PictureAlfEnableFlag[1] == 1):
            for j in range(9):
                alf_coeff_chroma[0][j]
        if (PictureAlfEnableFlag[2] == 1):
            for j in range(9):
                alf_coeff_chroma[1][j]

                





#在位流中检测当前字节中剩下的位或在字节对齐时下一个字节是否是片结尾填充的二进制位，如
#果是，则返回TRUE，否则返回FALSE。此函数不修改位流指针

class is_stuffing_pattern:
    def __init__(n):
        if (next_bits(8-n) == (1<<(7-n))): # n=0～7，为位流指针在当前字节的位置偏移， n为0时位流指针指向当前字节最高位
            return True
        else:
            return False


'''