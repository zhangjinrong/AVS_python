# This file is a basic file, store video message 
# store video_sequence message, instantiation it and add to main function
import copy
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
        data_value = self.str_to_int(self.pop_read_data(len_data))
        print(str_value,'  ',hex(data_value))
        if((str_value=='marker_bit')&(data_value==0)):
            print('marker_bit wrong!')
        return data_value
    # 字节是否对齐
    def byte_aligned(self):
        if((self.pointer_position%8)==0):
            return True
        else:
            return False

    #在位流中寻找下一个起始码，将位流指针指向起始码前缀的第一个二进制位。
    def next_start_code(self):
        self.stuffing_bit=self.assign_data('stuffing_bit',1)#1
        while (self.byte_aligned()==False):
            self.stuffing_bit=self.assign_data('stuffing_bit',1)#0
        while (self.get_read_data(24) != '000000000000000000000001'):#起始码前缀
            self.stuffing_byte=self.assign_data('stuffing_byte',8)#0#00000000
    
    #拷贝数据
    def memcpy(self,dest,src):
        dest = copy.deepcopy(src)
    #初始化数据
    def memset(self,dest,src,len):
        for i in range(len):
            dest[i] = src


# 参考图像结构
class rpl:
    def __init__(self):
        self.slice_type=''#slice类型
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
        self.rpl1_index_exist_flag=0#参考图像队列1索引存在标志
        self.rpl1_same_as_rpl0_flag=0#参考图像队列相同标志
        self.num_ref_pic_list_set =[0 for i in range(2)] #参考图像队列配置集数
        self.rpls_l0_num = 0#参考图像队列配置集数
        self.rpls_l1_num = 0#参考图像队列配置集数
        self.num_ref_default_active_minus1 = [0 for i in range(2)]#默认活跃参考图像数
        self.log2_lcu_size_minus2=0#最大编码单元尺寸
        self.log2_min_cu_size_minus2=0#最小编码单元尺寸
        self.log2_max_part_ratio_minus2=0#划分单元最大比例
        self.max_split_times_minus6=0#编码树最大划分次数
        self.log2_min_qt_size_minus2=0#最小四叉树尺寸
        self.log2_max_bt_size_minus2=0#最大二叉树尺寸
        self.log2_max_eqt_size_minus3=0#最大扩展四叉树尺寸
        self.wq_enable=0#加权量化允许标志
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
        self.wq_4x4_matrix= [0 for i in range(0,16)] #4x4加权量化矩阵系数
        self.wq_8x8_matrix= [0 for i in range(0,64)] #8x8加权量化矩阵系数


#帧内预测图像头定义
class intra_picture_header:
    def __init__(self):
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
        self.pic_wq_enable=0
        self.pic_weight_quant_data_index=0
        self.reserved_bits=0
        self.weight_quant_param_index=0
        self.weight_quant_model=0
        self.weight_quant_param_delta1=[0 for i in range(6)]
        self.weight_quant_param_delta2=[0 for i in range(6)]
        self.picture_alf_enable_flag=[0 for i in range(3)]

'''
#解码过程的所有信息
class decoder_CTX:
    def __init__(self):
        self.info = com_info()
        self.magic = 0
        self.id = dec()#解码器标识号
        self.core = dec_core()#当前操作的核心信息
        self.bs = 0#当前解码比特流
        self.dpm = com_pm()#解码图像的缓存区管理
        self.cdsc = dec_cdsc()#创建描述符
        self.pic = com_pic()#当前解码图像的缓存区
        self.sbac = sbac_dec()#基于语法元素的并行CABAC编码方案
        self.init_flag = 0
        self.map = com_map()
        self.tree_status = 0
        self.cons_pred_mode = 0

        self.lcu_cnt = 0   #编码一帧图像剩余的LCU
        self.ppbEdgeFilter = [0 for i in range(2)]
        self.pic_sao = com_pic()
        self.saostatData = saostatData()
        self.saoBlkParams = saoBlkParams()
        self.rec_saoBlkParams = saoBlkParams()
        self.pic_alf_Dec = com_pic()
        self.pic_alf_Rec = com_pic()
        self.pic_alf_on = [0 for i in range(3)]
        self.Coeff_all_to_write_ALF = 0
        self.Dec_ALF = DecALFVar()
        self.ctx_flags = [0 for i in range(3)]

        self.slice_num = 0#剩余的slice数量
        self.last_intra_ptr=0#最后解码帧内图像的表示时间参考
        self.dtr = 0#当前图片的解码时间
        self.dtr_prev_low = 0#之前图像的解码时间参考低部分
        self.dtr_prev_high = 0#之前图像的解码时间参考高部分
        self.ptr = 0#当前图片的呈现时间参考
        self.pic_cnt =0#当前解码的图像数
        self.pa = picbuf_allocator()#图像缓存
        self.bs_err = 0#比特流是否有错
        self.refp = [[com_refp() for i in range(2)] for j in range(17)]
        self.use_pic_sign = 0#图像签名使能标志
        self.pic_sign = [0 for i in range(16)]#图片签名(MD5占128位)
        self.pic_sign_exist = 0#指示图片签名是否存在的标志
        self.patch_column_width = [0 for i in range(64)]
        self.patch_row_height = [0 for i in range(128)]
        self.patch = patch()
        self.wq = [0 for i in range(2)]

class com_info:
    def __init__(self):
        self.cnkh = com_cnkh()#当前块头
        self.pic_header = com_pic_header()#当前图片头
        self.shext = com_sh_ext()#当前片头
        self.sqh = com_sqh()#序列头
        self.pic_width=0#解码图像宽度
        self.pic_height=0#解码图像高度
        self.max_cuwh = 0#最大CU的宽度和高度
        self.log2_max_cuwh=0#最大CU宽度和高度的Log2
        self.pic_width_in_lcu=0#LCU单元的图片宽度
        self.pic_height_in_lcu=0#LCU单元的图片高度
        self.f_lcu=0#LCU单元的图片尺寸，w*h
        self.pic_width_in_scu=0#SCU单元的图片宽度

    /* picture height in SCU unit */
    int                     pic_height_in_scu;
    /* picture size in SCU unit (= pic_width_in_scu * h_scu) */
    int                     f_scu;

    int                     bit_depth_internal;
    int                     bit_depth_input;
    int                     qp_offset_bit_depth;
'''

MAX_CU_CNT_IN_LCU=6
NUM_BLOCK_SHAPE=7
MAX_CU_CNT_IN_LCU=1024
ALLOWED_HMVP_NUM=8


#用于解码的核心类
class dec_core:
    def __init__(self):
        self.mod_info_curr = com_mode()
        #帧内预测的相邻像素
        self.nb = [[[0 for i in range(128)] for j in range(2)]for k in range(3)]
        #当前编码单元亮度的QP值
        self.qp_y=0
        #当前编码单元色度的QP值
        self.qp_u=0
        self.qp_v=0
        #当前LCU
        #LCU数量
        self.lcu_num=0
        #当前LCU的X地址
        self.x_lcu=0
        #当前LCU的Y地址
        self.y_lcu=0
        #当前LCU的左侧像素位置
        self.x_pel=0
        #当前LCU的上方像素位置
        self.y_pel=0
        #当前LCU的模式映射
        self.split_mode=[[[0 for i in range(MAX_CU_CNT_IN_LCU)]for j in range(NUM_BLOCK_SHAPE)]for k in range(MAX_CU_DEPTH)]
        #平台特殊数据
        self.pf = 0
        self.motion_cands = [com_motion() for i in range(ALLOWED_HMVP_NUM)]
        self.cnt_hmvp_cands=0


MV_D=2
REFP_NUM=2
class com_motion:
    def __init__(self):
        self.mv = [[0 for i in range(MV_D)]for j in range(REFP_NUM)]
        self.ref_idx[0 for i in range(REFP_NUM)]


#ALFParam
class ALFParam:
    def __init__(self):
        self.alf_flag=0
        self.num_coeff=0
        self.filters_per_group=0
        self.componentID=0
        self.filterPattern=0
        self.coeffmulti=0

#图像头
class com_pic_header:
    def __init__(self):
        self.low_delay=0#从SQH拷贝
        self.poc = 0#
        self.rpl_l0_idx=-1#-1指slice没有用RPL0中SPS的RPL
        self.rpl_l1_idx=-1#-1指slice没有用RPL1中SPS的RPL
        self.rpl_l0 = rpl()
        self.rpl_l1 = rpl()
        self.num_ref_idx_active_override_flag=0#
        self.ref_pic_list_sps_flag=[0 for i in range(2)]
        self.dtr = 0#
        self.slice_type = ''#
        self.temporal_id = 0#
        self.loop_filter_disable_flag=0#
        self.bbv_delay=0
        self.bbv_check_times=0
        self.loop_filter_parameter_flag=0
        self.alpha_c_offset=0
        self.beta_offset=0
        self.chroma_quant_param_disable_flag=0
        self.chroma_quant_param_delta_cb=0
        self.chroma_quant_param_delta_cr=0

        #Flag and coeff for ALF
        self.tool_alf_on=0
        self.pic_alf_on=[0 for i in range(3)]
        self.m_alfPictureParam = ALFParam()
        self.fixed_picture_qp_flag=0
        self.random_access_decodable_flag=0
        self.time_code_flag=0
        self.time_code=0
        self.decode_order_index=0
        self.picture_output_delay=0
        self.progressive_frame=0
        self.picture_structure=0
        self.top_field_first=0
        self.repeat_first_field=0
        self.top_field_picture_flag=0
        self.picture_qp=0
        self.affine_subblock_size_idx=0
        self.is_RLpic_flag=0  # only reference libpic
        self.library_picture_index=0
        self.pic_wq_enable=0
        self.pic_wq_data_idx=0
        self.wq_param=0
        self.wq_model=0
        self.wq_param_vector = [0 for i in range(6)]
        self.wq_4x4_matrix = [0 for i in range(16)]
        self.wq_8x8_matrix = [0 for i in range(64)]

class patch_info:
    def __init__(self):
        self.stable = 0
        self.cross_patch_loop_filter =0
        self.ref_colocated=0
        self.uniform=0
        self.height=0
        self.width=0
        self.columns=0
        self.rows=0
        self.idx=0
        #片的左上方像素位置
        self.x_pel=0
        self.y_pel=0
        #片中所有的cu都是skip模式
        self.skip_patch_flag=0
        #每个片的指针位置
        self.width_in_lcu=0
        self.height_in_lcu=0
        #片计数
        self.x_pat=0
        self.y_pat=0
        #定义片边界
        self.left_pel=0
        self.right_pel=0
        self.up_pel=0
        self.down_pel=0
        #所有片的sao使能信息
        self.patch_sao_enable=0
        
class com_sh_ext:
    def __init__(self):
        self.slice_sao_enable = [0 for i in range(3)]
        self.fixed_slice_qp_flag
        self.slice_qp

class dec_sbac:
    def __init__(self):
        self.range=0
        self.value=0
        self.bits_Needed=0
        self.prev_bytes=0
        self.ctx = com_sbac_ctx()

NUM_SBAC_CTX_SKIP_FLAG=4
NUM_SBAC_CTX_SKIP_IDX=11
NUM_SBAC_CTX_DIRECT_FLAG=2
NUM_SBAC_CTX_UMVE_BASE_IDX=1
NUM_SBAC_CTX_UMVE_STEP_IDX=1
NUM_SBAC_CTX_UMVE_DIR_IDX=2
NUM_INTER_DIR_CTX=3
NUM_INTRA_DIR_CTX=10
NUM_PRED_MODE_CTX=6
NUM_CONS_MODE_CTX=1
NUM_IPF_CTX=1
NUM_REFI_CTX=3
NUM_MVR_IDX_CTX=4
NUM_AFFINE_MVR_IDX_CTX=2
NUM_EXTEND_AMVR_FLAG=1
NUM_MV_RES_CTX=3
NUM_CTP_ZERO_FLAG_CTX=2
NUM_QT_CBF_CTX=3
NUM_TB_SPLIT_CTX=1
NUM_SBAC_CTX_RUN=24
NUM_SBAC_CTX_LAST1=6
NUM_SBAC_CTX_LAST2=12
NUM_SBAC_CTX_LEVEL=24
NUM_SBAC_CTX_SPLIT_FLAG=4
NUM_SBAC_CTX_BT_SPLIT_FLAG=9
NUM_SBAC_CTX_SPLIT_DIR=5
NUM_SBAC_CTX_SPLIT_MODE=3
NUM_SBAC_CTX_AFFINE_FLAG=1
NUM_SBAC_CTX_AFFINE_MRG=4
NUM_SBAC_CTX_SMVD_FLAG=1
NUM_SBAC_CTX_PART_SIZE=6
NUM_SAO_MERGE_FLAG_CTX=3
NUM_SAO_MODE_CTX=1
NUM_SAO_OFFSET_CTX=1
NUM_ALF_LCU_CTX=1
NUM_SBAC_CTX_DELTA_QP=4
MAX_NUM_SAO_CLASSES=32

class com_sbac_ctx:
    def __init__(self):
        self.skip_flag   =    [0 for i in range(NUM_SBAC_CTX_SKIP_FLAG)]
        self.skip_idx_ctx =   [0 for i in range(NUM_SBAC_CTX_SKIP_IDX)]
        self.direct_flag  =   [0 for i in range(NUM_SBAC_CTX_DIRECT_FLAG)]
        self.umve_flag=0
        self.umve_base_idx  = [0 for i in range(NUM_SBAC_CTX_UMVE_BASE_IDX)]
        self.umve_step_idx  = [0 for i in range(NUM_SBAC_CTX_UMVE_STEP_IDX)]
        self.umve_dir_idx   = [0 for i in range(NUM_SBAC_CTX_UMVE_DIR_IDX)]
        self.inter_dir      = [0 for i in range(NUM_INTER_DIR_CTX)]
        self.intra_dir      = [0 for i in range(NUM_INTRA_DIR_CTX)]
        self.pred_mode      = [0 for i in range(NUM_PRED_MODE_CTX)]
        self.cons_mode    =  [0 for i in range(NUM_CONS_MODE_CTX)]
        self.ipf_flag     = [0 for i in range(NUM_IPF_CTX)] 
        self.refi         = [0 for i in range(NUM_REFI_CTX)]   
        self.mvr_idx      = [0 for i in range(NUM_MVR_IDX_CTX)]
        self.affine_mvr_idx = [0 for i in range(NUM_AFFINE_MVR_IDX_CTX)] 
        self.mvp_from_hmvp_flag= [0 for i in range(NUM_EXTEND_AMVR_FLAG)]  
        self.mvd               = [[0 for i in range(NUM_MV_RES_CTX)] for j in range(2)] 
        self.ctp_zero_flag     = [0 for i in range(NUM_CTP_ZERO_FLAG_CTX)]  
        self.cbf               = [0 for i in range(NUM_QT_CBF_CTX)]         
        self.tb_split          = [0 for i in range(NUM_TB_SPLIT_CTX)]       
        self.run               = [0 for i in range(NUM_SBAC_CTX_RUN)]       
        self.run_rdoq          = [0 for i in range(NUM_SBAC_CTX_RUN)]       
        self.last1             = [0 for i in range(NUM_SBAC_CTX_LAST1*2)]   
        self.last2             = [0 for i in range(NUM_SBAC_CTX_LAST2 * 2 - 2)] 
        self.level             = [0 for i in range(NUM_SBAC_CTX_LEVEL)]         
        self.split_flag        = [0 for i in range(NUM_SBAC_CTX_SPLIT_FLAG)]    
        self.bt_split_flag     = [0 for i in range(NUM_SBAC_CTX_BT_SPLIT_FLAG)] 
        self.split_dir         = [0 for i in range(NUM_SBAC_CTX_SPLIT_DIR)]     
        self.split_mode        = [0 for i in range(NUM_SBAC_CTX_SPLIT_MODE)]    
        self.affine_flag       = [0 for i in range(NUM_SBAC_CTX_AFFINE_FLAG)]   
        self.affine_mrg_idx    = [0 for i in range(NUM_SBAC_CTX_AFFINE_MRG)]    
        self.smvd_flag         = [0 for i in range(NUM_SBAC_CTX_SMVD_FLAG)] 
        self.part_size         = [0 for i in range(NUM_SBAC_CTX_PART_SIZE)] 
        self.sao_merge_flag    = [0 for i in range(NUM_SAO_MERGE_FLAG_CTX)] 
        self.sao_mode          = [0 for i in range(NUM_SAO_MODE_CTX)]       
        self.sao_offset        = [0 for i in range(NUM_SAO_OFFSET_CTX)]     
        self.alf_lcu_enable    = [0 for i in range(NUM_ALF_LCU_CTX)]        
        self.delta_qp          = [0 for i in range(NUM_SBAC_CTX_DELTA_QP)]  

class SAOBlkParam:
    def __init__(self):
        self.modeIdc=0 #NEW, MERGE, OFF
        self.typeIdc=0 #NEW: EO_0, EO_90, EO_135, EO_45, BO. MERGE: left, above
        self.startBand=0 #BO: starting band index
        self.startBand2=0
        self.deltaband=0
        self.offset = [0 for i in range(MAX_NUM_SAO_CLASSES)]

MAX_CU_DIM = 128*128
N_C = 3
MAX_NUM_TB = 4
MAX_NUM_PB = 4
#模式决策结构
class com_mode:
    def __init__(self):
        self.x_scu = 0#SCU单元的CU位置X
        self.y_scu = 0#SCU单元的CU位置Y
        self.cud = 0#当前CU深度
        self.cu_width = 0#当前CU宽度
        self.cu_height = 0#当前CU高度
        self.cu_width_log2=0#log2 of cu_width
        self.cu_height_log2=0#log2 of cu_height
        self.x_pos = 0#CU的位置
        self.y_pos = 0#CU的位置
        self.scup=0#SCU单元中当前帧CU的位置
        self.cu_mode=0
        self.pb_part=0
        self.tb_part=0
        self.pb_info=com_part_info()
        self.tb_info=com_part_info()
        self.rec = [[0 for i in range(MAX_CU_DIM)] for j in range(N_C)]
        self.coef = [[0 for i in range(MAX_CU_DIM)] for j in range(N_C)]
        self.pred = [[0 for i in range(MAX_CU_DIM)] for j in range(N_C)]
        self.num_nz = [[0 for i in range(N_C)] for j in range(MAX_NUM_TB)]
        self.refi = [0 for i in range(REFP_NUM)]#参考指数
        self.mvr_idx = 0#MVR指数
        self.umve_flag=0
        self.umve_idx=0
        self.skip_idx=0
        self.mvp_from_hmvp_flag=0
        self.mvd = [[0 for i in range(MV_D)] for j in range(REFP_NUM)]#运动不同
        self.mv = [[0 for i in range(MV_D)] for j in range(REFP_NUM)]#运动信息
        self.affine_flag=0
        self.affine_mv = [[[0 for i in range(MV_D)] for j in range(VER_NUM)]for k in range(REFP_NUM)]
        self.affine_mvd = [[[0 for i in range(MV_D)] for j in range(VER_NUM)]for k in range(REFP_NUM)]
        self.smvd_flag=0
        #帧内预测模式
        self.mpm = [[0 for i in range(2)] for j in range(MAX_NUM_PB)]
        self.ipm = [[0 for i in range(2)] for j in range(MAX_NUM_PB)]   
        self.ipf_flag = 0


class com_part_info:
    def __init__(self):
        self.u8 num_sub_part=0
        self.sub_x = [0 for i in range(MAX_NUM_PB)]
        self.sub_y = [0 for i in range(MAX_NUM_PB)]
        self.sub_w = [0 for i in range(MAX_NUM_PB)]
        self.sub_h = [0 for i in range(MAX_NUM_PB)]
        self.sub_scup = [0 for i in range(MAX_NUM_PB)]
  