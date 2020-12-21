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
    'patch_start_code1':'00000000000000000000000100000000',#00-7F is patch_start_code
    'patch_start_code2':'0000000000000000000000010000007F',#00-7F is patch_start_code
    '8F': 'patch_end_code'
    }

class ctxArray_cell:
    def __init__(self):
        self.mps = 0 #1bit   Least Probable Symbol 0/1 CP
        self.cycno = 0 #2    
        self.lgPmps = 1023 #11

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
 
    def pop_read_data(self,read_length):
        string = self.data_file[self.pointer_position:self.pointer_position+read_length]
        self.pointer_position = self.pointer_position + read_length
        return string

    def get_read_data(self,read_length):
        string = self.data_file[self.pointer_position:self.pointer_position+read_length]
        return string
        #return hex(int(string.hex(),16))
        #return string.hex()
        

#序列头定义
class sequence_header:
    def __init__(self,input_file,pointer_position):
        self.List_ReferencePictureListSet = []
        self.data_file = input_file
        self.pointer_position = pointer_position
        self.video_sequence_start_code=0#0x000001B0
        self.profile_id=0#档次标号
        self.level_id=0#级别标号
        self.progressive_sequence=0
        self.field_coded_sequence=0
        self.library_stream_flag=0#知识位流标志.值为'1'表示当前位流是知识位流;值为'0'表示当前位流是主位流
        self.library_picture_enable_flag=0#知识图像允许标志.值为'1'表示视频序列中可存在使用知识图像作为参考图像的帧间预测图像;值为'0'表示视频序列中不应存在使用知识图像作为参考图像的帧间预测图像。
        self.duplicate_sequence_header_flag=0#知识位流重复序列头标志.
        self.marker_bit1=0
        self.horizontal_size=0
        self.marker_bit2=0
        self.vertical_size=0
        self.chroma_format=0
        self.sample_precision=0
        self.encoding_precision=0
        self.marker_bit3=0
        self.aspect_ratio=0
        self.frame_rate_code=0
        self.marker_bit4=0
        self.bit_rate_lower=0
        self.marker_bit5=0
        self.bit_rate_upper=0
        self.low_delay=0
        self.temporal_id_enable_flag=0
        self.marker_bit6=0
        self.bbv_buffer_size=0
        self.marker_bit7=0
        self.max_dpb_minus1=0
        self.rpl1_idx_exist_flag=0
        self.rpl1_same_as_rpl0_flag=0
        self.marker_bit8=0
        self.num_ref_pic_list_set =[0 for i in range(2)] 
        self.num_ref_default_active_minus1 = [0 for i in range(2)]
        self.log2_lcu_size_minus2=0
        self.log2_min_cu_size_minus2=0
        self.log2_max_part_ratio_minus2=0
        self.max_split_times_minus6=0
        self.log2_min_qt_size_minus2=0
        self.log2_max_bt_size_minus2=0
        self.log2_max_eqt_size_minus3=0
        self.marker_bit9=0
        self.weight_quant_enable_flag=0
        self.load_seq_weight_quant_data_flag=0
        self.secondary_transform_enable_flag=0
        self.sample_adaptive_offset_enable_flag=0
        self.adaptive_leveling_filter_enable_flag=0
        self.affine_enable_flag=0
        self.smvd_enable_flag=0
        self.ipcm_enable_flag=0
        self.amvr_enable_flag=0
        self.num_of_hmvp_cand=0
        self.umve_enable_flag=0
        self.emvr_enable_flag=0
        self.ipf_enable_flag=0
        self.tscpm_enable_flag=0
        self.marker_bit10=0
        self.dt_enable_flag=0
        self.log2_max_dt_size_minus4=0
        self.pbt_enable_flag=0
        self.output_reorder_delay=0
        self.cross_patch_loopfilter_enable_flag=0
        self.ref_colocated_patch_flag =0
        self.stable_patch_flag =0
        self.uniform_patch_flag =0
        self.marker_bit11 =0
        self.patch_width_minus1 =0
        self.patch_height_minus1=0
        self.reserved_bits=0
        # 参考图像队列配置集定义
        self.reference_to_library_enable_flag = 0
        self.library_index_flag=[0 for i in range(2)]
        self.NumOfRefPic = [0 for i in range(2)]
        self.referenced_library_picture_index = [0 for i in range(2)]
        self.abs_delta_doi = [0 for i in range(2)]
        self.sign_delta_doi=[0 for i in range(2)]
        self.WeightQuantMatrix4x4=[[]]
        self.WeightQuantMatrix8x8=[[]]
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
        #片定义
        self.PreviousDeltaQP=0
        self.lcu_qp_delta=0
        self.sao_merge_type_index=0#样值偏移补偿合并方式索引
        self.MergeFlagExist=0
        self.SaoMergeUpAvai=0
        self.SaoMergeLeftAvai=0
        self.sao_interval_offset_sign = 0#样值偏移补偿区间模式偏移值符号值
        self.sao_edge_offset =0#样值偏移补偿边缘模式偏移值
        self.sao_interval_start_pos = 0#样值偏移补偿区间模式起始偏移子区间位置
        self.sao_interval_delta_pos_minus2 = 0#样值偏移补偿区间模式起始偏移子区间位置差
        self.sao_edge_type = 0#样值偏移补偿边缘模式类型
        self.alf_lcu_enable_flag = 0#最大编码单元自适应修正滤波允许标志
        self.aec_lcu_stuffing_bit = 0#熵编码最大编码单元填充位
        self.qt_split_flag=0 #四叉树划分标志
        self.bet_split_flag = 0#二叉树扩展四叉树划分标志
        self.bet_split_type_flag=0#二叉树扩展四叉树划分类型标志
        self.bet_split_dir_flag=0#二叉树扩展四叉树划分方向标志
        self.root_cu_mode = 0#编码单元预测模式
        self.intra_chroma_pred_mode=0#帧内色度预测模式
        self.ctp_u = 0#Cb变换块编码模板
        self.ctp_v = 0#Cr变换块编码模板
        self.skip_flag = 0#跳过模式标志
        self.umve_flag = 0#高级运动矢量表达模式
        self.direct_flag = 0#直接模式标志
        self.affine_flag = 0#仿射模式标志
        self.intra_cu_flag = 0#帧内编码单元标志
        self.dt_split_flag = 0#衍生模式划分标志
        self.dt_split_dir = 0#衍生模式划分方向
        self.dt_split_hqt_flag = 0#水平四叉衍生模式划分标志
        self.dt_split_hadt_flag=0#水平非对称衍生模式标志
        self.dt_split_vqt_flag = 0#垂直四叉衍生模式划分标志
        self.dt_split_vadt_flag=0#垂直非对称衍生模式标志
        self.umve_mv_idx = 0#基础运动矢量索引
        self.umve_step_idx = 0#运动矢量偏移量索引
        self.umve_dir_idx = 0#运动矢量方向索引
        self.cu_affine_cand_idx=0#仿射运动矢量索引
        self.cu_subtype_index=0#编码单元子类型索引
        self.extend_mvr_flag=0#运动矢量精度扩展模式标识
        self.affine_amvr_index=0#仿射自适应运动矢量精度索引
        self.amvr_index=0#自适应运动矢量精度索引
        self.inter_pred_ref_mode=0#预测参考模式
        self.smvd_flag=0#对称运动矢量差标志
        self.pu_reference_index_l0=0#L0预测单元参考索引
        self.mv_diff_x_abs_l0=0#L0运动矢量水平分量差绝对值
        self.mv_diff_x_abs_l1=0#L1运动矢量水平分量差绝对值
        self.mv_diff_y_abs_l0=0#L0运动矢量垂直分量差绝对值
        self.mv_diff_y_abs_l1=0#L1运动矢量垂直分量差绝对值
        self.mv_diff_x_sign_l0=0#L0运动矢量水平分量差符号值
        self.mv_diff_y_sign_l0=0#L0运动矢量垂直分量差符号值
        self.mv_diff_x_sign_l1=0#L1运动矢量水平分量差符号值
        self.mv_diff_y_sign_l1=0#L1运动矢量垂直分量差符号值
        self.mv_diff_x_abs_l0_affine=0#仿射帧间模式L0运动矢量水平分量差绝对值(找不到解码方法)
        self.mv_diff_y_abs_l0_affine=0#仿射帧间模式L0运动矢量垂直分量差绝对值(找不到解码方法)
        self.mv_diff_x_abs_l1_affine=0#仿射帧间模式L1运动矢量水平分量差绝对值(找不到解码方法)
        self.mv_diff_y_abs_l1_affine=0#仿射帧间模式L1运动矢量垂直分量差绝对值(找不到解码方法)
        self.mv_diff_x_sign_l0_affine=0#仿射帧间模式L0运动矢量水平分量差符号值(找不到解码方法)
        self.mv_diff_y_sign_l0_affine=0#仿射帧间模式L0运动矢量垂直分量差符号值(找不到解码方法)
        self.mv_diff_x_sign_l1_affine=0#仿射帧间模式L1运动矢量水平分量差符号值(找不到解码方法)
        self.mv_diff_y_sign_l1_affine=0#仿射帧间模式L1运动矢量垂直分量差符号值(找不到解码方法)
        self.pu_reference_index_l0=0#L0预测单元参考索引
        self.pu_reference_index_l1=0#L1预测单元参考索引
        self.intra_luma_pred_mode=0#帧内亮度预测模式
        self.intra_chroma_pred_mode=0#帧内色度预测模式
        self.ipf_flag=0#帧内预测滤波标志



        #CABAC熵编码解码器
        self.binIdx = -1
        self.rS1 = 0 #如果boundS==254,位宽为8位
        self.rT1 = 0xFF
        self.bFlag = 0 #0或1
        self.cFlag = 0 #0或1
        self.valueS = 0#位宽是大于或等于Log(boundS+1)的最小整数,如果boundS==254,位宽为8位
        self.boundS = 0#位宽是大于或等于Log(boundS+1)的最小整数(记录连续0的数量)
        self.valueT = 0#位宽是9位 read_bits(9)
        self.valueD = 1


        self.BypassFlag = 0
        self.StuffingBitFlag = 0
        self.ctxIdxStart = 0
        self.ctxIdxInc = 0
        self.ctxIdx = 0
        self.ctxIdxW = 0
        self.ctx = ctxArray_cell()
        self.ctxW = ctxArray_cell()
        self.CtxWeight = 0

    def picture_data(self):
        while((self.get_read_data(32) >= dict['patch_start_code1'])&(self.get_read_data(32) <= dict['patch_start_code2'])):#000001+0x00～0x7F(patch_index)
            self.patch()
            print('asdf')
    
    #片定义
    def patch(self):
        self.patch_start_code=self.assign_data('patch_start_code',32)#000001+0x00～0x7F(patch_index)
        if (self.fixed_picture_qp_flag == '0'):
            self.fixed_patch_qp_flag=self.assign_data('fixed_patch_qp_flag',1)
            self.patch_qp=self.assign_data('patch_qp',7)
        if (self.sample_adaptive_offset_enable_flag=='1'):#SaoEnableFlag
            for compIdx in range(3):
                self.patch_sao_enable_flag[compIdx] = self.assign_data('patch_sao_enable_flag[compIdx]',1)
        while (self.byte_aligned()==0):#字节对齐
            self.aec_byte_alignment_bit = self.assign_data('aec_byte_alignment_bit',1)
        print(self.fixed_picture_qp_flag)
        
        while (~self.is_end_of_patch()):
            if (self.fixed_picture_qp_flag=='0'):
                self.lcu_qp_delta = self.read_ae('lcu_qp_delta')
                self.PreviousDeltaQP = lcu_qp_delta
            if (self.sample_adaptive_offset_enable_flag=='1'):
                if ((self.patch_sao_enable_flag[0]=='1') | (self.patch_sao_enable_flag[1]=='1') | (self.patch_sao_enable_flag[2]=='1')):
                    #if('如果当前样本的样值偏移补偿单元E的上边样值偏移补偿单元U存在， 且与E对应的最大编码单元和U对应的最大编码单元处于同一片'):
                    #    self.SaoMergeUpAvai=1
                    #else:
                    #    self.SaoMergeUpAvai=0
                    #if('如果当前样本的样值偏移补偿单元E的左边样值偏移补偿单元L存在， 且与E对应的最大编码单元和L对应的最大编码单元处于同一片'):
                    #    self.SaoMergeLeftAvai=1
                    #else:
                    #    self.SaoMergeLeftAvai=0
                    if(self.SaoMergeUpAvai|self.SaoMergeLeftAvai):
                        MergeFlagExist = 1
                    else:
                        MergeFlagExist = 0
                    if (MergeFlagExist):
                        self.sao_merge_type_index = self.read_ae('sao_merge_type_index')
                    if (self.get_SaoMergeMode() == 'SAO_NON_MERGE'):
                        for compIdx in range(3):
                            if (self.patch_sao_enable_flag[compIdx]):
                                self.sao_mode[compIdx] = self.read_ae('sao_mode')
                                self.SaoMode[compIdx] = self.get_SaoMode(self.sao_mode[compIdx])
                                if (self.SaoMode[compIdx] == 'SAO_Interval'):
                                    for j in range(MaxOffsetNumber):
                                        self.sao_interval_offset_abs[compIdx][j] = self.read_ae('sao_interval_offset_abs')
                                        if (self.sao_interval_offset_abs[compIdx][j]):
                                            self.sao_interval_offset_sign[compIdx][j] = self.read_ae('sao_interval_offset_sign')
                                    self.sao_interval_start_pos[compIdx] = self.read_ae('sao_interval_start_pos')
                                    self.sao_interval_delta_pos_minus2[compIdx] = self.read_ae('sao_interval_delta_pos_minus2')
                                if (self.SaoMode[compIdx] == 'SAO_Edge'):
                                    for j in range(MaxOffsetNumber):
                                        self.sao_edge_offset[compIdx][j] = self.read_ae('sao_edge_offset')
                                    self.sao_edge_type[compIdx] = self.read_ae('sao_edge_type')
            for compIdx in range(3):
                if (self.picture_alf_enable_flag[compIdx] == '1'):
                    self.alf_lcu_enable_flag[compIdx][LcuIndex] = self.read_ae('alf_lcu_enable_flag')
            x0 = (LcuIndex % pictureWidthInLcu) * LcuSize
            y0 = (LcuIndex / pictureWidthInLcu) * LcuSize
            self.coding_unit_tree(x0, y0, 0, 1<<LcuSizeInBit, 1<<LcuSizeInBit, 1, 'PRED_No_Constraint')
            self.aec_lcu_stuffing_bit = self.read_ae('aec_lcu_stuffing_bit')
        next_start_code()
        patch_end_code
    
    #CABAC
    def read_ae(self,str_type):
        self.binIdx = -1
        result_data = ''
        while(~self.flag_anti_bin_method(result_data,str_type)):
            self.binIdx = self.binIdx + 1
            
            if(str_type=='ipf_flag'):
                ctxIdxInc =0
            if(str_type=='intra_chroma_pred_mode'):
                if(self.binIdx ==0):
                    ctxIdxInc =0
                elif((self.tscpm_enable_flag==1)&(self.binIdx==1)):
                    ctxIdxInc =2
                else:
                    ctxIdxInc =1
            if(str_type=='intra_luma_pred_mode'):
                if((self.binIdx==1)&(self.result_data='1')):
                    ctxIdxInc =6
                else:
                    ctxIdxInc =len(self.result_data)
            if(str_type==('pu_reference_index_l1'|'pu_reference_index_l0')):
                if(self.binIdx==0):
                    ctxIdxInc =0
                elif(self.binIdx==1):
                    ctxIdxInc =1
                else:
                    ctxIdxInc =2             

            if(str_type==('mv_diff_x_sign_l0_affine'|'mv_diff_y_sign_l0_affine'|'mv_diff_x_sign_l1_affine'|'mv_diff_y_sign_l1_affine')):

            if(str_type==('mv_diff_x_sign_l0'|'mv_diff_x_sign_l1'|'mv_diff_y_sign_l0'|'mv_diff_y_sign_l1')):
                self.BypassFlag=1
            if(str_type=='mv_diff_x_abs_l0'|'mv_diff_x_abs_l1'|'mv_diff_y_abs_l0'|'mv_diff_y_abs_l1'):
                if(self.binIdx==0):
                    ctxIdxInc =0
                elif(self.binIdx==1):
                    ctxIdxInc =1
                elif(self.binIdx==2):
                    ctxIdxInc =2
                else:
                    BypassFlag=1             
            if(str_type=='pu_reference_index_l0'):
                if(self.binIdx==0):
                    ctxIdxInc =0
                elif(self.binIdx==1):
                    ctxIdxInc =1
                else:
                    ctxIdxInc =2
            if(str_type=='smvd_flag'):
                ctxIdxInc =0
            if(str_type=='inter_pred_ref_mode'):
                if((self.binIdx==0)&(width*height<64)):
                    ctxIdxInc =2
                elif((self.binIdx==0)&(width*height>=64)):
                    ctxIdxInc =0
                else:
                    ctxIdxInc =1

            if(str_type=='amvr_index'):
                ctxIdxInc = self.binIdx
            if(str_type=='affine_amvr_index'):
                ctxIdxInc = self.binIdx
            if(str_type=='extend_mvr_flag'):
                ctxIdxInc = 0
            if(str_type=='cu_subtype_index'):
                ctxIdxInc = self.binIdx
            if(str_type=='cu_affine_cand_idx'):
                ctxIdxInc = self.binIdx
            if(str_type=='umve_dir_idx'):
                ctxIdxInc = self.binIdx
            if(str_type=='umve_step_idx'):
                self.BypassFlag  = 1
                ctxIdxInc = 0
            if(str_type=='umve_mv_idx'):
                self.BypassFlag  = 1
                ctxIdxInc = 0
            if(str_type==('dt_split_hadt_flag'|'dt_split_vadt_flag'|'dt_split_hqt_flag'|'dt_split_vqt_flag')):
                ctxIdxInc = 0
            if(str_type=='dt_split_dir'):
                ctxIdxInc = 0
            if(str_type=='dt_split_flag'):
                ctxIdxInc = 0
            if(str_type=='intra_cu_flag'):
                if()#一大堆呢
            if(str_type=='affine_flag'):
                ctxIdxInc = 0
            if(str_type=='direct_flag'):
                if(如果当前预测块 E 的宽度乘以当前预测块 E 的高度的积小于 64，或当前预测块 E 的宽度大于64， 或当前预测块 E 的高度大于 64):
                    ctxIdxInc = 1
                else:
                    ctxIdxInc = 0

            if(str_type=='umve_flag'):
                ctxIdxInc = 0
            if(str_type=='skip_flag'):
                if(如果当前预测块 E 的宽度乘以当前预测块 E 的高度的积小于 64):
                    ctxIdxInc = 3
                elif(如果当前预测块 E 的左边预测块 A“存在”且 A 是跳过模式，且当前预测块 E 的上边预测块 B“存在”且 B 是跳过模式):
                    ctxIdxInc = 2
                elif(如果当前预测块 E 的左边预测块 A“存在”且 A 是跳过模式，或当前预测块 E 的上边预测块 B“存在”且 B 是跳过模式):
                    ctxIdxInc = 1
                else:
                    ctxIdxInc = 0
            if(str_type==('ctp_u'|'ctp_v')):
                ctxIdxInc = 0
            if(str_type=='intra_chroma_pred_mode'):
                if(self.binIdx==0):
                    ctxIdxInc = 0
                elif((self.tscpm_enable_flag==1)&(self.binIdx==1)):
                    ctxIdxInc = 2
                else:
                    ctxIdxInc = 1
            if(str_type=='root_cu_mode'):
                ctxIdxInc = 0
            if(str_type=='bet_split_dir_flag'):#没有bet_split_dir_flag的反二值法，未完成
                if((width==128)&(height==64)):#E是当前亮度编码块
                    ctxIdxInc = 4
                elif((width==64)&(height==128)):
                    ctxIdxInc = 3
                elif(height>width):
                    ctxIdxInc = 2
                elif(width>height):
                    ctxIdxInc = 1
                else:
                    ctxIdxInc = 0
            if(str_type=='bet_split_type_flag'):
                if(A'存在'且 A 的高度小于 E 的高度，且 B'存在'且 B 的宽度小于 E 的宽度):
                    ctxIdxInc=2
                elif(A'存在'且 A 的高度小于 E 的高度，或 B'存在'且 B 的宽度小于 E 的宽度):
                    ctxIdxInc=1
                else:
                    ctxIdxInc=0
            if(str_type=='bet_split_flag'):
                if(如果 A'存在'且 A 的高度小于 E 的高度，且 B'存在'且 B 的宽度小于 E 的宽度):
                    self.ctxIdxInc = 2
                elif(如果 A'存在'且 A 的高度小于 E 的高度，或块 B'存在'且块 B 的宽度小于 E 的宽度):
                    self.ctxIdxInc = 1
                else:
                    self.ctxIdxInc = 0
                if(E 的宽度乘以 E 的高度的积大于 1024):
                    self.ctxIdxInc =self.ctxIdxInc
                elif(如果 E 的宽度乘以 E 的高度的积大于 256):
                    self.ctxIdxInc = self.ctxIdxInc+3
                else:
                    self.ctxIdxInc = self.ctxIdxInc+6
                

            if(str_type=='qt_split_flag'):
                if(如果当前图像为帧内预测图像且 E 的宽度为 128):
                    self.ctxIdxInc = 3
                elif(如果 A'存在'且 A 的高度小于 E 的高度，且 B'存在'且 B 的宽度小于 E 的宽度):
                    self.ctxIdxInc = 2
                elif(如果 A'存在'且 A 的高度小于 E 的高度，或 B'存在'且 B 的宽度小于 E 的宽度):
                    self.ctxIdxInc = 1
                else:
                    self.ctxIdxInc = 0
                
            if(str_type=='sao_interval_offset_sign'):
                self.BypassFlag = 1
            if(str_type=='sao_interval_offset_abs')&(self.binIdx!=0)):
                self.BypassFlag = 1
                self.ctxIdxInc = 0
            if(str_type=='sao_mode')&(self.binIdx!=0)):
                self.BypassFlag = 1
                self.ctxIdxInc = 0
            if(str_type=='sao_edge_offset'):
                self.BypassFlag = 1
            if(str_type=='sao_interval_start_pos'):
                self.BypassFlag = 1
            if(str_type=='sao_interval_delta_pos_minus2'):
                self.BypassFlag = 1           
            if(str_type=='sao_edge_type'):
                self.BypassFlag = 1      
            if((str_type=='mv_diff_x_sign')|(str_type=='mv_diff_y_sign')):
                self.BypassFlag = 1 
            if(((str_type=='mv_diff_x_abs ')|(str_type=='mv_diff_y_abs'))&( binIdx>=3)):
                self.BypassFlag = 1 
            if(str_type=='coeff_sign'):
                self.BypassFlag = 1   
            if((str_type=='coeff_run')&(binIdx>=16)):
                self.BypassFlag = 1   
            if((str_type=='umve_mv_idx')&(binIdx!=0)):
                self.BypassFlag = 1  
            if((str_type=='umve_step_idx')&(binIdx!=0)):
                self.BypassFlag = 1    
            if((str_type=='coeff_level_minus1')&(binIdx>=8)):
                self.BypassFlag = 1     
            if(str_type=='aec_lcu_stuffing_bit'):
                self.BypassFlag = 0
                self.StuffingBitFlag = 1
            if(str_type=='aec_ipcm_stuffing_bit'):
                self.BypassFlag = 0
                self.StuffingBitFlag = 1
            if(str_type=='coeff_last'):
                self.CtxWeight = 1
            else:
                self.CtxWeight = 0
            if(str_type=='alf_lcu_enable_flag'):
                self.ctxIdxInc =0
            if((str_type=='sao_merge_type_index')&(self.binIdx!=0)):
                self.ctxIdxInc = self.binIdxIdx+self.SaoMergeLeftAvai+self.SaoMergeUpAvai-1
            if(str_type=='lcu_qp_delta'):
                self.BypassFlag = 0
                self.StuffingBitFlag = 0
                if((binIdx==0)&(self.PreviousDeltaQP==0)):
                    self.ctxIdxInc = 0
                elif((binIdx==0)&(self.PreviousDeltaQP!=0)):
                    self.ctxIdxInc = 1
                elif(binIdx==1):
                    self.ctxIdxInc = 2
                else:
                    self.ctxIdxInc = 3
                self.ctxIdxStart = 0
                self.ctxIdx = ctxIdxInc + ctxIdxStart
                self.cFlag = 0
                #self.ctx = 
            binVal = self.decode_decision()
            result_data = result_data + str(binVal)
    
    #判断是否满足反二值化
    def flag_anti_bin_method(self,result_data,str_type):
        flag = False
        if(str_type=='ipf_flag'):
            flag = True
            synElVal=self.str_to_int(result_data)
        if(str_type=='intra_chroma_pred_mode'):
            flag = True
            maxVal=(TscpmEnableFlag ? 5 : 4) 
            if(result_data[-1]=='1'):
                synElVal =len(result_data)-1
        if(str_type=='intra_luma_pred_mode'):
            flag = True
            if(result_data=='10'):
                synElVal = 0
            elif(result_data=='11'):
                synElVal = 1
            elif(len(result_data)==6):
                synElVal = 2+result_data[1]*16+result_data[2]*8+result_data[3]*4+result_data[4]*2+result_data[5]
            else:
                flag = False
        if(str_type==('pu_reference_index_l1')):
            maxVal=NumRefActive[1]-1
            synElVal = self.str_to_int(len(result_data))
        if(str_type==('pu_reference_index_l0')):
            maxVal=NumRefActive[0]-1
            synElVal = self.str_to_int(len(result_data))
        if(str_type==('mv_diff_x_sign_l0'|'mv_diff_x_sign_l1'|'mv_diff_y_sign_l0'|'mv_diff_y_sign_l1')):
            flag = True
            synElVal = self.str_to_int(len(result_data))
        if(str_type==('mv_diff_x_abs_l0'|'mv_diff_x_abs_l1'|'mv_diff_y_abs_l0'|'mv_diff_y_abs_l1')):
            flag = True
            if(result_data=='0'):
                synElVal = 0
            elif(result_data=='10'):
                synElVal = 1
            elif(result_data=='110'):
                synElVal = 2
            elif(result_data[0:3]=='1110'):
                synElVal = self.read_ue() + 3
            elif(result_data[0:3]=='1111'):
                synElVal = self.read_ue() + 4
            else:
                flag = False
        if(str_type=='pu_reference_index_l0'):
            if(len(result_data)==NumRefActive[0]-1):
                flag = True
                synElVal = self.str_to_int(len(result_data))

        if(str_type=='smvd_flag'):
            flag = True
            synElVal = self.str_to_int(result_data)
        if(str_type=='inter_pred_ref_mode'):
            flag = True
            if(result_data=='00'):
                synElVal = 0
            elif(result_data=='01'):
                synElVal = 1
            elif(result_data==('10'|'11')):
                synElVal = 2
            else:
                flag = False
        if(str_type=='amvr_index'):
            if(len(result_data)==4):
                flag = True
                synElVal = self.str_to_int(result_data)        
        if(str_type=='affine_amvr_index'):
            if(len(result_data)==2):
                flag = True
                synElVal = self.str_to_int(result_data)
        if(str_type=='extend_mvr_flag'):
            flag = True
            synElVal = self.str_to_int(result_data)
        if(str_type=='cu_subtype_index'):
            if(len(result_data)=((PictureType == 1) ? (1+ NumOfHmvpCand) :(3+NumOfHmvpCand))):
                flag = True
                synElVal = self.str_to_int(result_data)
        if(str_type=='cu_affine_cand_idx'):
            if(len(result_data)==4):
                flag = True
                synElVal = self.str_to_int(result_data)
        if(str_type=='umve_dir_idx'):
            flag = True
            if(result_data=='00'):
                synElVal = 0
            elif(result_data=='01'):
                synElVal = 1
            elif(result_data=='10'):
                synElVal = 2
            elif(result_data=='11'):
                synElVal = 3
            else:
                flag = False
        if(str_type=='umve_step_idx'):
            if(len(result_data)==4):
                flag = True
                synElVal = self.str_to_int(result_data)
        if(str_type=='umve_mv_idx'):
            flag = True
            synElVal = self.str_to_int(result_data)
            return synElVal
        if(str_type==('ctp_u'|'ctp_v'|'skip_flag'|'umve_flag'|'affine_flag'|'intra_cu_flag'|'dt_split_flag'|'dt_split_dir'|'dt_split_hqt_flag'|'dt_split_hadt_flag'|'dt_split_vqt_flag'|'dt_split_vadt_flag')):
            flag = True
            return self.str_to_int(result_data)
        if(str_type=='intra_chroma_pred_mode'):#未完成
            maxVal=(self.tscpm_enable_flag ? 5 : 4)
            if(result_data[0]=='1'):
                flag = True
                synElVal = len(result_data)-1
        if(str_type=='root_cu_mode'):
            flag = True
            return self.str_to_int(result_data)
        if(str_type=='bet_split_type_flag'):
            flag = True
            return self.str_to_int(result_data)
        if(str_type=='bet_split_flag'):
            flag = True
            return self.str_to_int(result_data)
        if(str_type=='qt_split_flag'):
            flag = True
            return self.str_to_int(result_data)
        if(str_type=='aec_lcu_stuffing_bit'):
            flag = True
            return self.str_to_int(result_data)
        if(str_type=='alf_lcu_enable_flag'):
            flag = True
            return self.str_to_int(result_data)
        if(str_type=='sao_edge_type'):
            if(len(result_data)==2):
               flag = True
               return self.str_to_int(result_data)
            else:
                flag = False
        if(str_type=='sao_interval_delta_pos_minus2'):
            flag = True
            if(result_data=='10'):
                return 0
            elif(result_data=='11'):
                return 1
            elif(result_data=='0100'):
                return 2
            elif(result_data=='0101'):
                return 3
            elif(result_data=='0110'):
                return 4         
            elif(result_data=='0111'):
                return 5
            elif(result_data=='001000'):
                return 6
            elif(result_data=='001001'):
                return 7
            elif(result_data=='001010'):
                return 8
            elif(result_data=='001011'):
                return 9               
            elif(result_data=='001100'):
                return 10
            elif(result_data=='001101'):
                return 11
            elif(result_data=='001110'):
                return 12
            elif(result_data=='001111'):
                return 13
            elif(result_data=='000'):
                return 14
            else:
                flag = False
#######################
        if(str_type=='sao_interval_start_pos'):
            if(len(result_data)==5):
                flag = True
                return self.str_to_int(result_data)
            else:
                flag = False

        if(str_type=='sao_edge_offset'):
            flag = True
            if(result_data=='1'):
                self.sao_edge_offset[compIdx][0] = 1
                self.sao_edge_offset[compIdx][3] = -1
            elif(result_data=='01'):  
                self.sao_edge_offset[compIdx][0] = 0
                self.sao_edge_offset[compIdx][3] = 0  
            elif(result_data=='001'):
                self.sao_edge_offset[compIdx][0] = 2
                self.sao_edge_offset[compIdx][3] = -2
            elif(result_data=='0001'):  
                self.sao_edge_offset[compIdx][0] = -1
                self.sao_edge_offset[compIdx][3] = 1  
            elif(result_data=='00001'):
                self.sao_edge_offset[compIdx][0] = 3
                self.sao_edge_offset[compIdx][3] = -3
            elif(result_data=='000001'):  
                self.sao_edge_offset[compIdx][0] = 4
                self.sao_edge_offset[compIdx][3] = -4 
            elif(result_data=='0000001'):
                self.sao_edge_offset[compIdx][0] = 5
                self.sao_edge_offset[compIdx][3] = -5
            elif(result_data=='00000001'):  
                self.sao_edge_offset[compIdx][0] = 6
                self.sao_edge_offset[compIdx][3] = -6 
            else:
                flag = False
            if(flag == True):
                if(result_data[0]=='0'):
                    self.sao_edge_offset[compIdx][1] = 1
                    self.sao_edge_offset[compIdx][2] = -1
                if(result_data[0]=='1'):
                    self.sao_edge_offset[compIdx][1] = 0
                    self.sao_edge_offset[compIdx][2] = 0

        if(str_type=='sao_interval_offset_sign'):
            flag =  True
            return self.str_to_int(result_data)
        if(str_type=='sao_interval_offset_abs'):
            if(result_data[-1]=='1'):
                flag =  True
                return len(result_data)-1
            else:
                flag =  False

        if(str_type=='lcu_qp_delta'):
            if(result_data[-1]=='1'):
                synElVal = len(result_data)-1
                if(synElVal%2==0):
                    cu_qp_delta = -(synElVal / 2)
                else:
                    cu_qp_delta = (synElVal / 2)
                return cu_qp_delta
                flag =  True
            else:
                flag = False

        if(str_type=='sao_mode'):
            if(result_data[-1]=='1'):
                return = len(result_data)-1
                flag =  True
            else:
                flag = False
            
        if(str_type=='sao_merge_type_index'):
            flag =  True
            if((self.SaoMergeLeftAvai==1)&(self.SaoMergeUpAvai==0)&(self.binIdx==0)&(result_data=='0')):
                self.sao_merge_type_index = 0
            if((self.SaoMergeLeftAvai==1)&(self.SaoMergeUpAvai==0)&(self.binIdx==1)&(result_data=='0')):
                self.sao_merge_type_index = 1
            if((self.SaoMergeLeftAvai==0)&(self.SaoMergeUpAvai==1)&(self.binIdx==0)&(result_data=='0')):
                self.sao_merge_type_index = 0  
            if((self.SaoMergeLeftAvai==1)&(self.SaoMergeUpAvai==0)&(self.binIdx==1)&(result_data=='0')):
                self.sao_merge_type_index = 1
            if((self.SaoMergeLeftAvai==1)&(self.SaoMergeUpAvai==1)&(self.binIdx==0)&(result_data=='00')):
                self.sao_merge_type_index = 0
            if((self.SaoMergeLeftAvai==1)&(self.SaoMergeUpAvai==1)&(self.binIdx==0)&(result_data[0]=='1')):
                self.sao_merge_type_index = 1
            if((self.SaoMergeLeftAvai==1)&(self.SaoMergeUpAvai==1)&(self.binIdx==0)&(result_data=='01')):
                self.sao_merge_type_index = 2
        return flag

    def get_SaoMode(self,n):
        if(n==0):
            return 'SAO_Off'
        if(n==1):
            return 'SAO_Interval'
        if(n==2):
            return 'SAO_Edge'

    def get_SaoMergeMode(self):
        if((SaoMergeTypeIndex==1)&(self.SaoMergeLeftAvai==1)&(self.SaoMergeUpAvai==0)):
            SaoMergeMode = 'SAO_MERGE_LEFT'
        elif((SaoMergeTypeIndex==1)&(self.SaoMergeLeftAvai==0)&(self.SaoMergeUpAvai==1)):
            SaoMergeMode = 'SAO_MERGE_UP'
        elif((SaoMergeTypeIndex==1)&(self.SaoMergeLeftAvai==1)&(self.SaoMergeUpAvai==1)):
            SaoMergeMode = 'SAO_MERGE_LEFT'
        elif((SaoMergeTypeIndex==2)&(self.SaoMergeLeftAvai==1)&(self.SaoMergeUpAvai==1)):
            SaoMergeMode = 'SAO_MERGE_UP'
        else:
            SaoMergeMode = 'SAO_NON_MERGE'
        return SaoMergeMode

    #在位流中检测是否已达到片的结尾，如果已到达片的结尾，返回TRUE，否则返回FALSE
    def is_end_of_patch(self):
        if(self.byte_aligned()):
            if (self.str_to_int(self.get_read_data(32)) == 0x80000001):
                return True#片结束
        else:
            if ((self.str_to_int(self.byte_aligned_next_bits(24)) == 0x000001) & self.is_stuffing_pattern()):
                return True #片结束
        return False

    def byte_aligned_next_bits(self,n):
        while((self.pointer_position%8)!=0):
            self.pointer_position = self.pointer_position + 1
        return self.get_read_data(n)

    # 字节是否对齐
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
            self.extension_start_code = self.assign_data('intra_picture_start_code',32)
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
        self.user_data_start_code=self.assign_data('user_data_start_code',32)
        while (self.get_read_data(24) != '000000000000000000000001'):
            self.user_data=self.assign_data('user_data',8)

    #帧内预测图像头定义
    def intra_picture_header(self):
        print('intra_picture_header begin begin begin begin begin begin begin begin begin begin begin begin begin')
        self.intra_picture_start_code = self.assign_data('intra_picture_start_code',32)
        self.bbv_delay = self.assign_data('bbv_delay',32)
        self.time_code_flag = self.assign_data('time_code_flag',1)
        if (self.time_code_flag == '1'):
            self.time_code = self.assign_data('time_code',24)
        self.decode_order_index = self.assign_data('decode_order_index',8)
        
        if (self.library_stream_flag=='1'):
            self.library_picture_index = self.read_ue()
        if (self.temporal_id_enable_flag == '1'):
            self.temporal_id = self.assign_data('temporal_id',3)
            
        if (self.low_delay == '0'):
            self.picture_output_delay=self.read_ue()
        if (self.low_delay == '1'):
            self.bbv_check_times=self.read_ue()
            
        self.progressive_frame = self.assign_data('progressive_frame',1)
        if (self.progressive_frame == '0'):
            self.picture_structure= self.assign_data('picture_structure',1)
        self.top_field_first= self.assign_data('top_field_first',1)
        self.repeat_first_field= self.assign_data('repeat_first_field',1)
        if (self.field_coded_sequence == '1'):
            self.top_field_picture_flag= self.assign_data('top_field_picture_flag',1)
            self.reserved_bits= self.assign_data('reserved_bits',1)
            
        self.ref_pic_list_set_flag[0]= self.assign_data('ref_pic_list_set_flag[0]',1)
        if ( self.ref_pic_list_set_flag[0]=='1'):
            if (int(self.num_ref_pic_list_set[0]) > 1):
                self.ref_pic_list_set_idx[0]=self.read_ue()
        else:
            self.reference_picture_list_set(0, self.num_ref_pic_list_set[0])
        if (self.rpl1_idx_exist_flag=='1'):
            self.ref_pic_list_set_flag[1]= self.assign_data('ref_pic_list_set_flag[1]',1)
        if (self.ref_pic_list_set_flag[1]=='1'):
            if ((self.rpl1_idx_exist_flag=='1') & (int(self.num_ref_pic_list_set[1]) > 1)):
                self.ref_pic_list_set_idx[1]=self.read_ue()
        else:
            self.reference_picture_list_set(1, self.num_ref_pic_list_set[1])
        self.fixed_picture_qp_flag= self.assign_data('fixed_picture_qp_flag',1)
        self.picture_qp= self.assign_data('picture_qp',7)
        self.loop_filter_disable_flag= self.assign_data('loop_filter_disable_flag',1)
        if (self.loop_filter_disable_flag == '0'):
            self.loop_filter_parameter_flag= self.assign_data('loop_filter_parameter_flag',1)
            if (self.loop_filter_parameter_flag=='1'):
                self.alpha_c_offset=self.read_se()
                self.beta_offset=self.read_se()
        self.chroma_quant_param_disable_flag= self.assign_data('chroma_quant_param_disable_flag',1)
        
        if (self.chroma_quant_param_disable_flag == '0'):
            self.chroma_quant_param_delta_cb=self.read_se()
            self.chroma_quant_param_delta_cr=self.read_se()
             
        if (self.weight_quant_enable_flag=='1'):
            self.pic_weight_quant_enable_flag= self.assign_data('pic_weight_quant_enable_flag',1)
            if (self.pic_weight_quant_enable_flag=='1'):
                self.pic_weight_quant_data_index= self.assign_data('pic_weight_quant_data_index',2)
                if (self.pic_weight_quant_data_index == '01'):
                    self.reserved_bits= self.assign_data('reserved_bits',1)
                    self.weight_quant_param_index = self.assign_data('weight_quant_param_index',2)
                    self.weight_quant_model = self.assign_data('weight_quant_model',2)
                    if (self.weight_quant_param_index == '01'):
                        for i in range(6):
                            self.weight_quant_param_delta1[i] = self.read_se()
                    if (self.weight_quant_param_index == '10'):
                         for i in range(6):
                            weight_quant_param_delta2[i] = self.read_se()
                elif(self.pic_weight_quant_data_index == '10'):
                    self.weight_quant_matrix()
        if (self.adaptive_leveling_filter_enable_flag=='1'):#AlfEnableFlag
            for compIdx in range(3):
                self.picture_alf_enable_flag[compIdx] = self.assign_data('self.picture_alf_enable_flag[compIdx]',1)
            if (self.picture_alf_enable_flag[0] == '1' | self.picture_alf_enable_flag[1] == '1' | self.picture_alf_enable_flag[2] == '1'):#picture_alf_enable_flag
                self.alf_parameter_set()
        #self.next_start_code()
        print('position....................',self.pointer_position)

    def run(self):
        if(self.get_read_data(32)==dict['video_sequence_start_code']):
            print('position....................',self.pointer_position)
            self.video_sequence_start_code = self.assign_data('video_sequence_start_code',32)
            self.profile_id = self.assign_data('profile_id',8)
            self.level_id = self.assign_data('level_id',8)
            self.progressive_sequence = self.assign_data('progressive_sequence',1)
            self.field_coded_sequence = self.assign_data('field_coded_sequence',1)
            self.library_stream_flag = self.assign_data('library_stream_flag',1)
            if(self.library_stream_flag == '0'):
                self.library_picture_enable_flag = self.assign_data('library_picture_enable_flag',1)
                if(self.library_picture_enable_flag=='1'):
                    self.duplicate_seq_header_flag = self.assign_data('duplicate_seq_header_flag',1)
            self.marker_bit = self.assign_data('marker_bit',1)
            self.horizontal_size = self.assign_data('horizontal_size',14)
            self.marker_bit = self.assign_data('marker_bit',1)
            self.vertical_size = self.assign_data('vertical_size',14)
            self.chroma_format = self.assign_data('chroma_format',2)
            self.sample_precision = self.assign_data('sample_precision',3)
            if ((self.profile_id) == '22'):
                self.encoding_precision = self.assign_data('encoding_precision',3)
            self.marker_bit = self.assign_data('marker_bit',1)
            self.aspect_ratio = self.assign_data('aspect_ratio',4)
            self.frame_rate_code = self.assign_data('frame_rate_code',4)
            self.marker_bit = self.assign_data('marker_bit',1)
            self.bit_rate_lower = self.assign_data('bit_rate_lower',18)
            self.marker_bit = self.assign_data('marker_bit',1)
            self.bit_rate_upper = self.assign_data('bit_rate_upper',12)
            self.low_delay = self.assign_data('low_delay',1)
            self.temporal_id_enable_flag = self.assign_data('temporal_id_enable_flag',1)
            self.marker_bit = self.assign_data('marker_bit',1)
            self.bbv_buffer_size = self.assign_data('bbv_buffer_size',18)
            self.marker_bit = self.assign_data('marker_bit',1)
            self.max_dpb_minus1 = self.assign_data('max_dpb_minus1',4)
            self.rpl1_idx_exist_flag = self.assign_data('rpl1_idx_exist_flag',1)
            self.rpl1_same_as_rpl0_flag = self.assign_data('rpl1_same_as_rpl0_flag',1)
            self.marker_bit = self.assign_data('marker_bit',1)
            self.num_ref_pic_list_set[0] = self.read_ue()
            
            print('position1....................',self.pointer_position)
            print('num_ref_pic_list_set[0]  ',((self.num_ref_pic_list_set[0])))
            self.NumOfRefPic[0] = [0 for i in range(self.num_ref_pic_list_set[0])]
            #=======================================
            for i in range(int(self.num_ref_pic_list_set[0])):
                self.reference_picture_list_set(0,i)
            if(self.rpl1_same_as_rpl0_flag=='0'):
                self.num_ref_pic_list_set[1] = self.read_ue()
                print('num_ref_pic_list_set[1]    ',self.num_ref_pic_list_set[1])
                self.NumOfRefPic[1] = [0 for i in range(self.num_ref_pic_list_set[1])]
                for i in range(int(self.num_ref_pic_list_set[1])):
                    self.reference_picture_list_set(1,i)
            
            self.num_ref_default_active_minus1[0] = self.read_ue()
            print('num_ref_default_active_minus1[0]  ',((self.num_ref_default_active_minus1[0])))
            self.num_ref_default_active_minus1[1] = self.read_ue()
            print('num_ref_default_active_minus1[1]  ',((self.num_ref_default_active_minus1[1])))
            self.log2_lcu_size_minus2 = self.assign_data('log2_lcu_size_minus2',3)
            self.log2_min_cu_size_minus2 = self.assign_data('log2_min_cu_size_minus2',2)
            self.log2_max_part_ratio_minus2 = self.assign_data('log2_max_part_ratio_minus2',2)
            self.max_split_times_minus6 = self.assign_data('max_split_times_minus6',3)
            self.log2_min_qt_size_minus2 = self.assign_data('log2_min_qt_size_minus2',3)
            self.log2_max_bt_size_minus2 = self.assign_data('log2_max_bt_size_minus2',3)
            self.log2_max_eqt_size_minus3 = self.assign_data('log2_max_eqt_size_minus3',2)
            self.marker_bit = self.assign_data('marker_bit',1)
            self.weight_quant_enable_flag = self.assign_data('weight_quant_enable_flag',1)
            
            if(self.weight_quant_enable_flag=='1'):
                self.load_seq_weight_quant_data_flag = self.assign_data('load_seq_weight_quant_data_flag',1)
                if(self.load_seq_weight_quant_data_flag=='1'):
                    self.weight_quant_matrix()
            self.secondary_transform_enable_flag = self.assign_data('secondary_transform_enable_flag',1)
            self.sample_adaptive_offset_enable_flag = self.assign_data('sample_adaptive_offset_enable_flag',1)
            self.adaptive_leveling_filter_enable_flag = self.assign_data('adaptive_leveling_filter_enable_flag',1)
            self.affine_enable_flag = self.assign_data('affine_enable_flag',1)
            self.smvd_enable_flag = self.assign_data('smvd_enable_flag',1)
            self.ipcm_enable_flag = self.assign_data('ipcm_enable_flag',1)
            self.amvr_enable_flag = self.assign_data('amvr_enable_flag',1)
            self.num_of_hmvp_cand = self.assign_data('num_of_hmvp_cand',4)
            self.umve_enable_flag = self.assign_data('umve_enable_flag',1)
            if((self.num_of_hmvp_cand=='1') & (self.amvr_enable_flag=='1')):
                self.emvr_enable_flag = self.assign_data('emvr_enable_flag',1)
            self.ipf_enable_flag = self.assign_data('ipf_enable_flag',1)
            self.tscpm_enable_flag = self.assign_data('tscpm_enable_flag',1)
            self.marker_bit = self.assign_data('marker_bit',1)
            self.dt_enable_flag = self.assign_data('dt_enable_flag',1)
            if(self.dt_enable_flag=='1'):
                self.log2_max_dt_size_minus4 = self.assign_data('log2_max_dt_size_minus4',2)
            self.pbt_enable_flag = self.assign_data('pbt_enable_flag',1)
            if(self.low_delay=='0'):
                self.output_reorder_delay = self.assign_data('output_reorder_delay',5)
            self.cross_patch_loopfilter_enable_flag = self.assign_data('cross_patch_loopfilter_enable_flag',1)
            self.ref_colocated_patch_flag = self.assign_data('ref_colocated_patch_flag',1)
            self.stable_patch_flag = self.assign_data('stable_patch_flag',1)
            if(self.stable_patch_flag=='1'):
                self.uniform_patch_flag = self.assign_data('uniform_patch_flag',1)
                if(self.uniform_patch_flag=='1'):
                    self.marker_bit = self.assign_data('marker_bit',1)
                    self.patch_width_minus1 = self.read_ue()
                    print('patch_width_minus1  ',((self.patch_width_minus1)))
                    self.patch_height_minus1 = self.read_ue()
                    print('patch_height_minus1  ',((self.patch_height_minus1)))
            self.reserved_bits = self.assign_data('reserved_bits',2)
            print('position....................',self.pointer_position)
            self.pop_read_data(12)
            self.intra_picture_header()
            print('position....................',self.pointer_position)
            self.pop_read_data(32)
            self.extension_and_user_data(1)
            self.picture_data()

    # 参考图像队列配置集定义
    def reference_picture_list_set(self,mlist,rpls):
        print('in func reference_picture_list_set')
        if(self.library_picture_enable_flag=='1'):
            self.reference_to_library_enable_flag = self.assign_data('reference_to_library_enable_flag',1)
        self.NumOfRefPic[mlist][rpls] = self.read_ue()
        print('NumOfRefPic[mlist][rpls]  ',(self.NumOfRefPic[mlist][rpls]))
        #==================malloc array
        self.library_index_flag[mlist] = [[0 for k in range(self.NumOfRefPic[mlist][rpls])] for j in range(self.num_ref_pic_list_set[mlist])]
        self.referenced_library_picture_index[mlist] = [[0 for k in range(self.NumOfRefPic[mlist][rpls])] for j in range(self.num_ref_pic_list_set[mlist])]
        self.abs_delta_doi[mlist] = [[0 for k in range(self.NumOfRefPic[mlist][rpls])] for j in range(self.num_ref_pic_list_set[mlist])]
        self.sign_delta_doi[mlist] = [[0 for k in range(self.NumOfRefPic[mlist][rpls])] for j in range(self.num_ref_pic_list_set[mlist])]
        
        for i in range((self.NumOfRefPic[mlist][rpls])):
            if (self.reference_to_library_enable_flag=='1'):
                self.library_index_flag[mlist][rpls][i] = int(self.assign_data('library_index_flag[mlist][rpls][i]',1))
            if(self.library_index_flag[mlist][rpls][i]==1):
                self.referenced_library_picture_index[mlist][rpls][i] = self.read_ue()
                print('referenced_library_picture_index[mlist][rpls][i]   ',self.referenced_library_picture_index[mlist][rpls][i])
            else:
                self.abs_delta_doi[mlist][rpls][i] = self.read_ue()
                print('abs_delta_doi[mlist][rpls][i]   ',self.abs_delta_doi[mlist][rpls][i])
                if(int(self.abs_delta_doi[mlist][rpls][i]) > 0):
                    self.sign_delta_doi[mlist][rpls][i] = self.assign_data('sign_delta_doi[mlist][rpls][i]',1)
        print('out func reference_picture_list_set')        

    # 自定义加权量化矩阵定义
    def weight_quant_matrix(self):
        print('in func weight_quant_matrix')
        for sizeId in range(2):
            WQMSize = 1 << (sizeId+2)
            self.WeightQuantMatrix4x4= [[0 for j in range(0,WQMSize)] for i in range(0,WQMSize)]
            self.WeightQuantMatrix8x8= [[0 for j in range(0,WQMSize)] for i in range(0,WQMSize)]
            for i in range(WQMSize):
                for j in range(WQMSize):
                    weight_quant_coeff = self.read_ue()
                    if(sizeId == 0):
                        self.WeightQuantMatrix4x4[i][j] = weight_quant_coeff
                    else:
                        self.WeightQuantMatrix8x8[i][j] = weight_quant_coeff
        print('out func weight_quant_matrix')
    
    def is_stuffing_pattern(self):
        n = self.pointer_position%8
        if (self.str_to_int(self.get_read_data(8-n)) == (1<<(7-n))): # n=0～7，为位流指针在当前字节的位置偏移， n为0时位流指针指向当前字节最高位
            return True
        else:
            return False

    def pop_read_data(self,read_length):
        string = self.data_file[self.pointer_position:self.pointer_position+read_length]
        self.pointer_position = self.pointer_position + read_length
        return string

    def get_read_data(self,read_length):
        string = self.data_file[self.pointer_position:self.pointer_position+read_length]
        return string
    
      
    def decode_aec_stuffing_bit(self):
        ctx0.lgPmps=4
        ctx0.mps=0
        cFlag=0
        return self.decode_decision()

    def decode_bypass(self):
        ctx.lgPmps = 1024
        ctx.mps = 0
        cFlag=0
        return self.decode_decision()

    def decode_decision(self):
        if (self.CtxWeight == 0):
            predMps = self.ctx.mps
            lgPmps = self.ctx.lgPmps >> 2
        else:
            if(self.ctx.mps == self.ctxW.mps):
                predMps = self.ctx.mps
                lgPmps = ( self.ctx.lgPmps + self.ctxW.lgPmps ) >> 1
            else:
                if(self.ctx.lgPmps < self.ctxW.lgPmps):
                    predMps = self.ctx.mps
                    lgPmps = 1023 – ((self.ctxW.lgPmps - self.ctx.lgPmps ) >> 1 )
                else:
                    predMps = self.ctxW.mps
                    lgPmps = 1023 – ((self.ctx.lgPmps – self.ctxW.lgPmps ) >> 1 )
            lgPmps = lgPmps >> 2
        if (self.valueD | (self.bFlag == 1 & self.rS1 == self.boundS) ):
            self.rS1 = 0
            self.valueS = 0
            while (self.valueT < 0x100 & self.valueS < self.boundS ):
                self.valueS = self.valueS + 1
                self.valueT = (self.valueT << 1) | self.pop_read_data(1)#read_bits(1)
            if ( self.valueT < 0x100 ):
                self.bFlag = 1
            else:
                self.bFlag = 0
            self.valueT = self.valueT & 0xFF
        if( self.rT1 >= lgPmps ):
            self.rS2 = self.rS1
            self.rT2 = self.rT1 - lgPmps
            sFlag = 0
        else:
            self.rS2 = self.rS1 + 1
            self.rT2 = 256 + self.rT1 - lgPmps
            sFlag = 1
        if (( self.rS2 > self.valueS | (self.rS2 == self.valueS & self.valueT >= self.rT2)) & self.bFlag == 0 ):
            binVal = ! predMps
            if ( sFlag == 0 ):
                tRlps = lgPmps
            else:
                tRlps = rT1 + lgPmps
            if ( self.rS2 == self.valueS ):
                valueT = valueT - rT2
            else:
                valueT = 256 + ((valueT << 1 ) | read_bits(1)) - rT2
            while ( tRlps < 0x100 ):
                tRlps = tRlps << 1
                valueT = (valueT << 1 ) | read_bits(1)
            rT1 = tRlps & 0xFF
            valueD = 1
        else:
            binVal = predMps
            self.rS1 = self.rS2
            self.rT1 = self.rT2
            valueD = 0
        if(self.cFlag):  
            if (self.CtxWeight == 0 ) :
                self.ctx = self.update_ctx( self.binVal, self.ctx )
            else:
                self.ctx = self.update_ctx( self.binVal, self.ctx )
                self.ctxW = self.update_ctx( self.binVal, self.ctxW )
        return (self.binVal)

    def update_ctx(self,binVal,ctx):
        if (ctx.cycno <= 1 ):
            cwr = 3
        elif ( ctx.cycno == 2 ):
            cwr = 4
        else:
            cwr = 5
        if ( binVal != ctx.mps ):
            if ( ctx.cycno <= 2 ):
                ctx.cycno = ctx.cycno + 1
            else:
                ctx.cycno = 3
        elif ( ctx.cycno == 0):
            ctx.cycno = 1
        if ( binVal == ctx.mps ):
            ctx.lgPmps = ctx.lgPmps – (ctx.lgPmps >> cwr) - (ctx.lgPmps >> (cwr+2))
        else :
            if ( cwr == 3 ):
                ctx.lgPmps = ctx.lgPmps + 197
            elif ( cwr == 4 ):
                ctx.lgPmps = ctx.lgPmps + 95
            else:
                ctx.lgPmps = ctx.lgPmps + 46
            if ( ctx.lgPmps > 1023 ) :
                ctx.lgPmps = 2047 - ctx.lgPmps
        return ctx

    def read_ue(self):
        string_size=1
        while(self.get_read_data(1)=='0'):
            string_size = string_size+1
            self.pop_read_data(1)
        return (self.str_to_int(self.pop_read_data(string_size))-1)
    def read_se(self):
        string_size=1
        while(self.get_read_data(1)=='0'):
            string_size = string_size+1
            self.pop_read_data(1)
        code_num = self.str_to_int(self.pop_read_data(string_size))-1
        if(code_num%2==0):
            return 0-code_num/2
        else:
            return code_num/2+1

    def str_to_int(self,str):
        data = 0
        for i in range(len(str)):
            data = data*2 + int(str[i])
        return data

    def str_to_hex(self,str_input):
        data_string=''
        if(((len(str_input)%4)==0)&(len(str_input)>0)):
            for i in range(int(len(str_input)/4)):
                data = hex(int(str_input[i*4:i*4+4],2))
                data_string = data_string + data[-1]
        else:
            data_string = str_input
        return data_string
    def assign_data(self,str_value,len_data):
        data_value = self.str_to_hex(self.pop_read_data(len_data))
        print(str_value,'  ',data_value)
        return data_value
    
    #编码树定义
    def coding_unit_tree(self,x0, y0, split, width, height, qt, mode,seq_data):
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
            self.qt_split_flag = self.read_ae('qt_split_flag')
        if (QtSplitFlag==0):
            if (allowNoSplit & (allowSplitBt | allowSplitEqt)):
                self.bet_split_flag = self.read_ae('bet_split_flag')
            if (BetSplitFlag):
                if (allowSplitBt & allowSplitEqt):
                    self.bet_split_type_flag = self.read_ae('bet_split_type_flag')
                if ((BetSplitTypeFlag==0) & allowSplitBtHor & allowSplitBtVer) | (BetSplitTypeFlag &allowSplitEqtHor & allowSplitEqtVer):
                    self.bet_split_dir_flag= self.read_ae('bet_split_dir_flag')
        if ((PictureType != 0) & ((((BetSplitFlag & (BetSplitTypeFlag==0)) | QtSplitFlag) & (width * height== 64)) | (BetSplitTypeFlag & (width * height == 128)))):
            self.root_cu_mode = self.read_ae('root_cu_mode')
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
            self.coding_unit_tree(x0, y0, split+1, QtWidth, QtHeight, 1, modeChild)
            if (x1 < PicWidthInLuma):
                self.coding_unit_tree(x1, y0, split+1, QtWidth, QtHeight, 1, modeChild)
            if (y1 < PicHeightInLuma):
                self.coding_unit_tree(x0, y1, split+1, QtWidth, QtHeight, 1, modeChild)
            if ((x1 < PicWidthInLuma) & (y1 < PicHeightInLuma)):
                self.coding_unit_tree(x1, y1, split+1, QtWidth, QtHeight, 1, modeChild)
            if ((LumaWidth == width) & (LumaHeight == height) & ChildSizeOccur4):
                self.coding_unit(x0, y0, width, height, 'PRED_No_Constraint', 'COMPONENT_Chroma')
                Component = 0
        elif (BlockSplitMode == 'SPLIT_BT_VER'):
            x1 = x0 + width / 2
            self.coding_unit_tree(x0, y0, split+1, width/2, height, 0, modeChild)
            if (x1 < PicWidthInLuma):
                self.coding_unit_tree(x1, y0, split+1, width/2, height, 0, modeChild)
            if ((LumaWidth == width) & (LumaHeight == height) & ChildSizeOccur4):
                self.coding_unit (x0, y0, width, height, 'PRED_No_Constraint', 'COMPONENT_Chroma')
                Component = 0
        elif (BlockSplitMode == 'SPLIT_BT_HOR'):
            y1 = y0 + height / 2
            self.coding_unit_tree(x0, y0, split+1, width, height/2, 0, modeChild)
            if (y1 < PicHeightInLuma):
                self.coding_unit_tree(x0, y1, split+1, width, height/2, 0, modeChild)
            if ((LumaWidth == width) & (LumaHeight == height) & ChildSizeOccur4):
                self.coding_unit(x0, y0, width, height, 'PRED_No_Constraint', 'COMPONENT_Chroma')
                Component = 0
        elif (BlockSplitMode == 'SPLIT_EQT_VER'):
            x1 = x0 + width / 4
            x2 = x0 + (3 * width / 4)
            y1 = y0 + height / 2
            self.coding_unit_tree(x0, y0, split+1, width/4, height, 0, modeChild)
            self.coding_unit_tree(x1, y0, split+1, width/2, height/2, 0, modeChild)
            self.coding_unit_tree(x1, y1, split+1, width/2, height/2, 0, modeChild)
            self.coding_unit_tree(x2, y0, split+ 1, width/4, height, 0, modeChild)
            if ((LumaWidth == width) & (LumaHeight == height) & ChildSizeOccur4):
                self.coding_unit(x0, y0, width, height, 'PRED_No_Constraint', 'COMPONENT_Chroma')
                Component = 0
        elif (BlockSplitMode == 'SPLIT_EQT_HOR') :
            x1 = x0 + width / 2
            y1 = y0 + height / 4
            y2 = y0 + (3 * height / 4)
            self.coding_unit_tree(x0, y0, split+1, width, height/4, 0, modeChild)
            self.coding_unit_tree(x0, y1, split+1, width/2, height/2, 0, modeChild)
            self.coding_unit_tree(x1, y1, split+1, width/2, height/2, 0, modeChild)
            self.coding_unit_tree(x0, y2, split+1, width, height/4, 0, modeChild)
            if ((LumaWidth == width) & (LumaHeight == height) & ChildSizeOccur4):
                self.coding_unit(x0, y0, width, height, 'PRED_No_Constraint', 'COMPONENT_Chroma')
                Component = 0
        else:
            if (Component == 0):
                self.coding_unit(x0, y0, width, height, mode, 'COMPONENT_LUMACHROMA')
            elif (Component == 1):
                self.coding_unit(x0, y0, width, height, mode, 'COMPONENT_LUMA')

    #编码单元定义
    def coding_unit(self,x0, y0, width, height, mode, component):
        if (component == 'COMPONENT_Chroma'):
            if ((priorCuMode == 1) & (chroma_format != '00')):
                self.intra_chroma_pred_mode = self.read_ae('intra_chroma_pred_mode')
            NumOfTransBlocks = 3
            ctp_y[0] = 0
            CuCtp += ctp_y[0]
            if (IntraChromaPredMode != 'Intra_Chroma_PCM'):
                self.ctp_u = self.read_ae('ctp_u')
                CuCtp += (ctp_u << 1)
                self.ctp_v = self.read_ae('ctp_v')
                CuCtp += (ctp_v << 2)
            for i in range(2):
                IsPcmMode[i-2+NumOfTransBlocks] = (IntraChromaPredMode == 'Intra_Chroma_PCM')
                IsChroma = 0
                if (i == NumOfTransBlocks -1 | i == NumOfTransBlocks -2):
                    IsChroma = 1
                self.block(i, width, height, CuCtp, IsChroma, IsPcmMode[i], component)
        else:
            if (PictureType != 0):
                if (mode != 'PRED_Intra_Only'):
                    self.skip_flag = self.read_ae('skip_flag')
                if (self.skip_flag):
                    if (UmveEnableFlag):
                        self.umve_flag = self.read_ae('umve_flag')
                    if (AffineEnableFlag & (UmveFlag==0)  & (width >= 16) & (height >= 16)):
                        self.affine_flag = self.read_ae('affine_flag')
                if (~SkipFlag):
                    if (mode != 'PRED_Intra_Only'):
                        self.direct_flag = self.read_ae('direct_flag')
                    if (DirectFlag):
                        if (UmveEnableFlag):
                            self.umve_flag = self.read_ae('umve_flag')
                        if (AffineEnableFlag & (UmveFlag==0)  & (width >= 16) & (height >= 16)):
                            self.affine_flag = self.read_ae('affine_flag')
                    if (~DirectFlag & (mode == 'PRED_No_Constraint')):
                        self.intra_cu_flag = self.read_ae('intra_cu_flag')
            PartSize = 'SIZE_2Mx2N'
            if (DtEnableFlag & IntraCuFlag):
                allowDtHorSplit = (height >= DtMinSize) & (height <= DtMaxSize) & (width / height < 4)& (width <= DtMaxSize)
                allowDtVerSplit = (width >= DtMinSize) & (width <= DtMaxSize) & (height / width < 4)& (height <= DtMaxSize)
                if (allowDtHorSplit | allowDtVerSplit):
                    self.dt_split_flag = self.read_ae('dt_split_flag')
                    if (DtSplitFlag):
                        if (allowDtHorSplit & allowDtVerSplit):
                            self.dt_split_dir = self.read_ae('dt_split_dir')
                        elif (allowDtHorSplit):
                            DtSplitDir = 1
                        else:
                            DtSplitDir = 0
                        if(DtSplitDir):
                            self.dt_split_hqt_flag = self.read_ae('dt_split_hqt_flag')
                            if (~self.dt_split_hqt_flag):
                                self.dt_split_hadt_flag = self.read_ae('dt_split_hadt_flag')
                        else:
                            self.dt_split_vqt_flag = self.read_ae('dt_split_vqt_flag')
                            if (~self.dt_split_vqt_flag):
                                self.dt_split_vadt_flag = self.read_ae('dt_split_vadt_flag')
            if (UmveFlag):
                self.umve_mv_idx = self.read_ae('umve_mv_idx')
                self.umve_step_idx = self.read_ae('umve_step_idx')
                self.umve_dir_idx = self.read_ae('umve_dir_idx')
            elif ((SkipFlag | DirectFlag) & AffineFlag):
                self.cu_affine_cand_idx = self.read_ae('cu_affine_cand_idx')
            elif (SkipFlag | DirectFlag):
                self.cu_subtype_index = self.read_ae('cu_subtype_index')
            if ((SkipFlag==0)  & (DirectFlag==0)):
                if (IntraCuFlag==0):
                    if (AffineEnableFlag & (width >= 16) & (height >= 16)):
                        self.affine_flag = self.read_ae('affine_flag')
                if (AmvrEnableFlag):
                    if (EmvrEnableFlag & ~AffineFlag):
                        self.extend_mvr_flag = self.read_ae('extend_mvr_flag')
                    if (AffineFlag):
                        self.affine_amvr_index = self.read_ae('affine_amvr_index')
                    else:
                        self.amvr_index = self.read_ae('amvr_index')
                if (PictureType == 2):
                    self.inter_pred_ref_mode = self.read_ae('inter_pred_ref_mode')
                if (SmvdEnableFlag & SmvdApplyFlag & ~AffineFlag & (InterPredRefMode == 2)& ~ExtendMvrFlag):
                    self.smvd_flag = self.read_ae('smvd_flag')
                if (MvExistL0):
                    if ((SmvdFlag==0) & NumRefActive[0] > 1):
                        self.pu_reference_index_l0 = self.read_ae('pu_reference_index_l0')
                    self.mv_diff_x_abs_l0 = self.read_ae('mv_diff_x_abs_l0')
                    if (MvDiffXAbsL0):
                        self.mv_diff_x_sign_l0 = self.read_ae('mv_diff_x_sign_l0')
                    self.mv_diff_y_abs_l0 = self.read_ae('mv_diff_y_abs_l0')
                    if (MvDiffYAbsL0):
                        self.mv_diff_y_sign_l0 = self.read_ae('mv_diff_y_sign_l0')
                    if (AffineFlag):
                        self.mv_diff_x_abs_l0_affine = self.read_ae('mv_diff_x_abs_l0')#找不到解码方法
                        if (MvDiffXAbsL0Affine):
                            self.mv_diff_x_sign_l0_affine = self.read_ae('mv_diff_x_sign_l0')
                        self.mv_diff_y_abs_l0_affine = self.read_ae('mv_diff_y_abs_l0')
                        if (MvDiffYAbsL0Affine):
                            self.mv_diff_y_sign_l0_affine = self.read_ae('mv_diff_y_sign_l0')
                if (MvExistL1 &  (SmvdFlag==0)):
                    if (NumRefActive[1] > 1):
                        self.pu_reference_index_l1 = self.read_ae('pu_reference_index_l1')
                    self.mv_diff_x_abs_l1 = self.read_ae('mv_diff_x_abs_l1')
                    if (MvDiffXAbsL1):
                        self.mv_diff_x_sign_l1 = self.read_ae('mv_diff_x_sign_l1')
                    self.mv_diff_y_abs_l1 = self.read_ae('mv_diff_y_abs_l1')
                    if (MvDiffYAbsL1):
                        self.mv_diff_y_sign_l1 = self.read_ae('mv_diff_y_sign_l1')
                    if (AffineFlag):
                        self.mv_diff_x_abs_l1_affine = self.read_ae('mv_diff_x_abs_l1')
                        if (MvDiffXAbsL1Affine):
                            self.mv_diff_x_sign_l1_affine = self.read_ae('mv_diff_x_sign_l1')
                        self.mv_diff_y_abs_l1_affine = self.read_ae('mv_diff_y_abs_l1')
                        if (MvDiffYAbsL1Affine):
                            self.mv_diff_y_sign_l1_affine = self.read_ae('mv_diff_y_sign_l1')
            else:
                TuOrder = 0
                for i in range(NumOfIntraPredBlock):
                    self.intra_luma_pred_mode = self.read_ae('intra_luma_pred_mode')
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
                    self.intra_chroma_pred_mode = self.read_ae('intra_chroma_pred_mode')
                    IsPcmMode[TuOrder+1] = (IntraChromaPredMode == 'Intra_Chroma_PCM')
                    IsPcmMode[TuOrder+2] = (IntraChromaPredMode == 'Intra_Chroma_PCM')
                if (IpfEnableFlag & (PartSize == 'SIZE_2Mx2N') & (~IsPcmMode[0])):
                    self.ipf_flag = self.read_ae('ipf_flag')
        if ((IntraCuFlag==0) & (SkipFlag==0)):
            if ((DirectFlag==0) & component == 'COMPONENT_LUMACHROMA'):
                self.ctp_zero_flag = self.read_ae()
            CuCtp = 0
            if ((CtpZeroFlag==0)):
                if (PbtEnableFlag & (width / height < 4) & (height / width < 4) & (width >= 8) &(width <= 32)& (height >= 8) & (height <= 32)):
                    self.pbt_cu_flag = self.read_ae()
                if (PbtCuFlag==0):
                    if (component == 'COMPONENT_LUMACHROMA'):
                        self.ctp_u = self.read_ae('ctp_u')
                        self.ctp_v = self.read_ae('ctp_v')
                    CuCtp = ctp_u << (NumOfTransBlocks)
                    CuCtp = CuCtp>>2
                    CuCtp += (ctp_v << (NumOfTransBlocks))
                    CuCtp = CuCtp>>1
                    if (((ctp_u != 0) | (ctp_v != 0)) | ( component !='COMPONENT_LUMACHROMA')):
                        self.ctp_y[0] = self.read_ae()
                        CuCtp += ctp_y[0]
                    else:
                        CuCtp += ctp_y[0]
                else:
                    if (component == 'COMPONENT_LUMACHROMA'):
                        self.ctp_u = self.read_ae('ctp_u')
                        self.ctp_v = self.read_ae('ctp_v')
                    CuCtp = ctp_u << (NumOfTransBlocks)
                    CuCtp = CuCtp>>2
                    CuCtp += (ctp_v << (NumOfTransBlocks))
                    CuCtp = CuCtp>>1
                    for i in range((NumOfTransBlocks-2)):
                        self.ctp_y[i] = self.read_ae()
                        CuCtp += (ctp_y[i] << i)
        elif (~ SkipFlag):
            CuCtp = 0
            if (~ IsPcmMode[0]):
                for i in range(NumOfTransBlocks-2):
                    self.ctp_y[i] = self.read_ae()
                    CuCtp += (ctp_y[i] << i)
            if ((component == 'COMPONENT_LUMACHROMA') & (IntraChromaPredMode !='Intra_Chroma_PCM')):
                self.ctp_u = self.read_ae('ctp_u')
                self.ctp_v = self.read_ae('ctp_v')
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
                self.block(i, blockWidth, blockHeight, CuCtp, IsChroma, IsPcmMode[i], component)
    

    #变换块定义
    def block(self,i, blockWidth, blockHeight, CuCtp, isChroma, isPcm, component):
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
                    self.coeff_run = self.read_ae()
                    self.coeff_level_minus1 = self.read_ae()
                    self.coeff_sign = self.read_ae()
                    AbsLevel = coeff_level_minus1 + 1
                    ScanPosOffset = ScanPosOffset + coeff_run
                    PosxInBlk = InvScanCoeffInBlk[idxW][idxH][ScanPosOffset][0]
                    PosyInBlk = InvScanCoeffInBlk[idxW][idxH][ScanPosOffset][1]
                    QuantCoeffMatrix[PosxInBlk][PosyInBlk] = (~AbsLevel) if coeff_sign else AbsLevel
                    #QuantCoeffMatrix[PosxInBlk][PosyInBlk] = coeff_sign ? –AbsLevel : AbsLevel
                    if (ScanPosOffset >= NumOfCoeff - 1):
                        break
                    self.coeff_last = self.read_ae()
                    ScanPosOffset = ScanPosOffset + 1
        elif ((component != 'COMPONENT_CHROMA' & i == 0) | (component =='COMPONENT_CHROMA' & i == 1)):
            self.aec_ipcm_stuffing_bit = self.read_ae()
            while (~byte_aligned()):
                self.aec_byte_alignment_bit0 = self.read_ae()
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
                        self.pcm_coeff = self.read_ae()
                        QuantCoeffMatrix[x+xStep*xMin][y + yStep*yMin] = pcm_coeff

    #自适应修正滤波参数定义
    def alf_parameter_set(self):
        if (PictureAlfEnableFlag[0] == 1):
            self.alf_filter_num_minus1 = self.read_ue()
            for i in range(alf_filter_num_minus1+1):
                if ((i > 0) & (alf_filter_num_minus1 != 15)):
                    self.alf_region_distance[i] = self.read_ue()
                for j in range(9):
                    self.alf_coeff_luma[i][j] = self.read_se()
        if(PictureAlfEnableFlag[1] == 1):
            for j in range(9):
                self.alf_coeff_chroma[0][j] = self.read_se()
        if (PictureAlfEnableFlag[2] == 1):
            for j in range(9):
                self.alf_coeff_chroma[1][j] = self.read_se()

    #在位流中寻找下一个起始码，将位流指针指向起始码前缀的第一个二进制位。
    def next_start_code(self):
        self.stuffing_bit=self.assign_data('stuffing_bit',1)#1
        while (~ self.byte_aligned()):
            self.stuffing_bit=self.assign_data('stuffing_bit',1)#0
        while (self.get_read_data(24) != '000000000000000000000001'):#起始码前缀
            self.stuffing_byte=self.assign_data('stuffing_byte',8)#0#00000000



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

'''