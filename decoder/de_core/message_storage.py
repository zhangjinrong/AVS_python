# This file is a basic file, store video message 
# store sequence_header message, instantiation it and add to main function
# name = sequence_header name, value = sequence_header size, instantiation shuould be changed
class sequence_header:
    def __init__(self):
        self.video_sequence_start_code=32
        self.profile_id=8
        self.level_id=8
        self.progressive_sequence=1
        self.field_coded_sequence=1
        self.library_stream_flag=1
        self.library_picture_enable_flag=1
        self.duplicate_sequence_header_flag=1
        self.marker_bit1=1
        self.horizontal_size=14
        self.marker_bit2=1
        self.vertical_size=14
        self.chroma_format=2
        self.sample_precision=3
        self.encoding_precision=3
        self.marker_bit3=1
        self.aspect_ratio=4
        self.frame_rate_code=4
        self.marker_bit4=1
        self.bit_rate_lower=18
        self.marker_bit5=1
        self.bit_rate_upper=12
        self.low_delay=1
        self.temporal_id_enable_flag=1
        self.marker_bit6=1
        self.bbv_buffer_size=18
        self.marker_bit7=1
        self.max_dpb_minus1=4
        self.rpl1_idx_exist_flag=1
        self.rpl1_same_as_rpl0_flag=1
        self.marker_bit8=1
        self.num_ref_pic_list_set[0]=1
        self.num_ref_pic_list_set[1]=1
        self.num_ref_default_active_minus1[0]=1
        self.num_ref_default_active_minus1[1]=1
        self.log2_lcu_size_minus2=3
        self.log2_min_cu_size_minus2=2
        self.log2_max_part_ratio_minus2=2
        self.max_split_times_minus6=3
        self.log2_min_qt_size_minus2=3
        self.log2_max_bt_size_minus2=3
        self.log2_max_eqt_size_minus3=2
        self.marker_bit9=1
        self.weight_quant_enable_flag=1
        self.load_seq_weight_quant_data_flag=1
        self.secondary_transform_enable_flag=1
        self.sample_adaptive_offset_enable_flag=1
        self.adaptive_leveling_filter_enable_flag=1
        self.affine_enable_flag=1
        self.smvd_enable_flag=1
        self.ipcm_enable_flag=1
        self.amvr_enable_flag=1
        self.num_of_hmvp_cand=4
        self.umve_enable_flag=1
        self.emvr_enable_flag=1
        self.ipf_enable_flag=1
        self.tscpm_enable_flag=1
        self.marker_bit10=1
        self.dt_enable_flag=1
        self.log2_max_dt_size_minus4=2
        self.pbt_enable_flag=1
        self.output_reorder_delay=5
        self.cross_patch_loopfilter_enable_flag=1
        self.ref_colocated_patch_flag =1
        self.stable_patch_flag =1
        self.uniform_patch_flag =1
        self.marker_bit11 =1
        self.patch_width_minus1 =1
        self.patch_height_minus1=1
        self.reserved_bits=2
   
    '''
    for (j = 0; j < NumRefPicListSet[0]; j++) 
        {reference_picture_list_set(0, j)}
    if (! Rpl1SameAsRpl0Flag) {
        for (j = 0; j < NumRefPicListSet[1]; j++) 
        {reference_picture_list_set(0, j)}
    }
    参考图像队列配置集定义
    '''
    def rence_picture_list_set(list, rpls):
        if(LibraryPictureEnableFlag):
            reference_to_library_enable_flag
        for i in range(len(NumOfRefPic[list][rpls])):
            if (ReferenceToLibraryEnableFlag):
                if(LibraryIndexFlag[list][rpls][i]):
                    referenced_library_picture_index[list][rpls][i]
                else:
                    abs_delta_doi[list][rpls][i]
                    if(abs_delta_doi[list][rpls][i] > 0):
                        sign_delta_doi[list][rpls][i]

   '''
    if (load_seq_weight_quant_data_flag == '1')
    {weight_quant_matrix()}
    自定义加权量化矩阵定义
    '''
    def weight_quant_matrix():
        for sizeId in range(2):
            WQMSize = 1 << (sizeId+2)
            for i in range(WQMSize):
                for j in range(WQMSize):
                    if(sizeId == 0):
                        WeightQuantMatrix4x4[i][j] = WeightQuantCoeff
                    else:
                        WeightQuantMatrix8x8[i][j] = WeightQuantCoeff
    '''
    扩展和用户数据定义
    '''
    def extension_and_user_data(i):
        while ((next_bits(32) == extension_start_code) | (next_bits(32) == user_data_start_code)):
            if (next_bits(32) == extension_start_code):
                extension_data(i)
            if (next_bits(32) == user_data_start_code)
                user_data()
    '''
    扩展数据定义
    '''
    def extension_data(i):
        while ((next_bits(32) == extension_start_code):
            if(i==0):
                if(next_bits(4)== '0010'):#序列显示扩展 
                    sequence_display_extension()
                else if (next_bits(4) == '0011'): # 时域可伸缩扩展 
                    temporal_scalability_extension()
                else if (next_bits(4) == '0100'): # 版权扩展 
                    copyright_extension()
                else if (next_bits(4) == '0110'): 
                    cei_extension()
                else if (next_bits(4) == '1010'): # 目标设备显示和内容元数据扩展 
                    mastering_display_and_content_metadata_extension()
                else if (next_bits(4) == '1011'): # 摄像机参数扩展 
                    camera_parameters_extension()
                else if (next_bits(4) == '1101'): # 参考知识图像扩展
                    cross_random_access_point_reference_extension()
                else:
                    while (next_bits(24) != '0000 0000 0000 0000 0000 0001')
                        reserved_extension_data_byte
            else:#图像头之后
                if (next_bits(4) == '0100'): # 版权扩展 
                    copyright_extension()
                else if ( next_bits(4) == '0101' ): # 高动态范围图像元数据扩展
                    hdr_dynamic_metadata_extension()
                else if (next_bits(4) == '0111'): # 图像显示扩展
                    picture_display_extension()
                else if (next_bits(4) == '1011'): # 摄像机参数扩展
                    camera_parameters_extension()
                else if (next_bits(4) == '1100'): #感兴趣区域参数扩展
                    roi_parameters_extension()
                else:
                    while (next_bits(24) != '0000 0000 0000 0000 0000 0001'):
                        reserved_extension_data_byte
'''
用户数据定义
'''
class user_data:
    def __init__(self):
        self.user_data_start_code=32
        while (next_bits(24) != '0000 0000 0000 0000 0000 0001'):
            self.user_data=8

'''
序列显示扩展定义
'''
class sequence_display_extension:
    def __init__(self):
        self.extension_id=4
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

    '''
    时域可伸缩扩展定义
    ''' 
    def temporal_scalability_extension():
        extension_id=4
        num_of_temporal_level_minus1=3
        for i in range(num_of_temporal_level_minus1):
            temporal_frame_rate_code[i]=4
            temporal_bit_rate_lower[i]=4
            marker_bit=4
            temporal_bit_rate_upper[i]=4
        
    '''
    版权扩展定义
    '''
class copyright_extension:
    def __init__():
        self.extension_id=4
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
'''
内容加密扩展定义
'''
class  cei_extension:
    def __init__():
        self.extension_id=4
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
 
'''
高动态范围图像扩展定义
'''
class hdr_dynamic_metadata_extension:
    def __init__():
        extension_id=4
        extension_id=4
        while ( next_bits(24) != '0000 0000 0000 0000 0000 0001'):
            extension_data_byte
    
'''
目标设备显示和内容元数据扩展定义
'''
class mastering_display_and_content_metadata_extension:
    def __init__():
        self.extension_id=4
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
'''
摄像机参数扩展定义
'''
class camera_parameters_extension:
    def __init__():
        self.extension_id =4
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
'''
感兴趣区域参数扩展定义
'''
class roi_parameters_extension:
    def __init__():
        self.extension_id=4
        self.current_picture_roi_num=8
        self.roiIndex = 0
        if(PictureType!=0)
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

                    
'''
参考知识图像扩展定义
'''
class cross_random_access_point_reference_extension:
    def __init__():
        self.extension_id
        self.crr_lib_number
        self.marker_bit
        while(i<crr_lib_number):
            crr_lib_pid[i]
            i=i+1
            if( i%2 == 0):
                marker_bit

'''
帧内预测图像头定义
'''
class intra_picture_header:
    def __init__():
        intra_picture_start_code#0x000001B3
        bbv_delay
        time_code_flag
        if (time_code_flag == '1'):
            time_code
        decode_order_index
        if (LibraryStreamFlag):
            library_picture_index
        if (temporal_id_enable_flag == '1'):
            temporal_id
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
            if (NumRefPicListSet[0] > 1):
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
        fixed_picture_qp_flag
        picture_qp
        loop_filter_disable_flag
        if (loop_filter_disable_flag == '0'):
            loop_filter_parameter_flag
        if (loop_filter_parameter_flag):
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
                    weight_quant_model
                    if (weight_quant_param_index == '01'):
                        for i in range(6):
                            weight_quant_param_delta1[i]
                    if (weight_quant_param_index == '10'):
                         for i in range(6):
                            weight_quant_param_delta2[i]
                else if(pic_weight_quant_data_index == '10'):
                    weight_quant_matrix()
        if (AlfEnableFlag):
            for compIdx in range(3):
                picture_alf_enable_flag[compIdx]
            if (PictureAlfEnableFlag[0] == 1 | PictureAlfEnableFlag[1] == 1 | PictureAlfEnableFlag[2] == 1)
                alf_parameter_set()


'''
帧间预测图像头定义
'''
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
        if (! ((picture_coding_type == '10') & (PictureStructure == 1))):
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
                else if (pic_weight_quant_data_index == '10'):
                    weight_quant_matrix()
        if (AlfEnableFlag):
            for compIdx in range(3):
                picture_alf_enable_flag[compIdx]
            if (PictureAlfEnableFlag[0] == 1 | PictureAlfEnableFlag[1] == 1 | PictureAlfEnableFlag[2] == 1):
                alf_parameter_set()
        if (AffineEnableFlag):
            affine_subblock_size_flag
'''
图像显示扩展定义
'''
class picture_display_extension:
    def __init__(seq_data):
        extension_id
        for i in range(NumberOfFrameCentreOffsets):
            picture_centre_horizontal_offset
            marker_bit
            picture_centre_vertical_offset
            marker_bit
'''
图像数据定义
'''
class picture_data:
    def __init__(seq_data):
        patch()
        while(next_bits(32) == patch_start_code):
            patch()
'''
片定义
'''
class patch:
    def __init__(seq_data):
        patch_start_code
        if (fixed_picture_qp_flag == '0') :
            fixed_patch_qp_flag
            patch_qp
        if (SaoEnableFlag):
            for compIdx in range(3):
                patch_sao_enable_flag[compIdx]
        while (! byte_aligned()):
            aec_byte_alignment_bit
        while (! is_end_of_patch()):
            if (! FixedQP):
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

'''
编码树定义
'''
class coding_unit_tree(x0, y0, split, width, height, qt, mode):
    def __init__(seq_data):
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
            else if ((width == 64 & height > 64) | (height == 64 & width > 64)):
                allowSplitBtHor = 1
                allowSplitBtVer = 1
            else if (! rightBoundary & ! bottomBoundary):
                allowSplitQt = 1
            else if (rightBoundary):
                allowSplitBtVer = 1
            else if (bottomBoundary):
                allowSplitBtHor = 1
        else:
            if (((width == 64) & (height > 64)) | ((height == 64) & (width > 64))):
                allowSplitBtHor = 1
                allowSplitBtVer = 1
                allowNoSplit = 1
            else if (split >= MaxSplitTimes):
                allowNoSplit = 1
            else if ((PictureType == 0) & (width == 128) & (height == 128)) :
                allowSplitQt = 1
                allowNoSplit = 1
            else :
                if ((width <= height * MaxPartRatio) & (height <= width * MaxPartRatio)):
                    allowNoSplit = 1
                if ((width > MinQtSize) & qt)
                    allowSplitQt = 1
                if ((width <= MaxBtSize) & (height <= MaxBtSize) & (width > MinBtSize) & (height < MaxPartRatio*width))
                    allowSplitBtVer = 1
                if ((width <= MaxBtSize) & (height <= MaxBtSize) & (height > MinBtSize) & (width <MaxPartRatio*height))
                    allowSplitBtHor = 1
                if ((width <= MaxEqtSize) & (height <= MaxEqtSize) & (height >= MinEqtSize*2) & (width >= MinEqtSize*4) & (height*4 <= MaxPartRatio*width))
                    allowSplitEqtVer = 1
                if ( (width <= MaxEqtSize) & (height <= MaxEqtSize) & (width >= MinEqtSize*2) & (height >= MinEqtSize*4) & (width*4 <= MaxPartRatio*height) )
                    allowSplitEqtHor = 1
        allowSplitBt = allowSplitBtVer | allowSplitBtHor
        allowSplitEqt = allowSplitEqtVer | allowSplitEqtHor
        if (allowSplitQt & (allowNoSplit | allowSplitBt | allowSplitEqt)):
            qt_split_flag
        if (! QtSplitFlag):
            if (allowNoSplit & (allowSplitBt | allowSplitEqt)):
                bet_split_flag
            if (BetSplitFlag):
                if (allowSplitBt & allowSplitEqt):
                    bet_split_type_flag
                if (! BetSplitTypeFlag & allowSplitBtHor & allowSplitBtVer) | (BetSplitTypeFlag &allowSplitEqtHor & allowSplitEqtVer):
                    bet_split_dir_flag
        if ((PictureType != 0) & ((((BetSplitFlag & ! BetSplitTypeFlag) | QtSplitFlag) & (width * height== 64)) | (BetSplitTypeFlag & (width * height == 128)))):
            root_cu_mode
            modeChild = root_cu_mode ? 'PRED_Intra_Only' : 'PRED_Inter_Only'
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
            if ((LumaWidth == width) & (LumaHeight = height) & ChildSizeOccur4):
                coding_unit(x0, y0, width, height, 'PRED_No_Constraint', 'COMPONENT_Chroma')
                Component = 0
        else if (BlockSplitMode == 'SPLIT_BT_VER'):
            x1 = x0 + width / 2
            coding_unit_tree(x0, y0, split+1, width/2, height, 0, modeChild)
            if (x1 < PicWidthInLuma)
                coding_unit_tree(x1, y0, split+1, width/2, height, 0, modeChild)
            if ((LumaWidth == width) & (LumaHeight = height) & ChildSizeOccur4):
                coding_unit (x0, y0, width, height, 'PRED_No_Constraint', 'COMPONENT_Chroma')
                Component = 0
        else if (BlockSplitMode == 'SPLIT_BT_HOR'):
            y1 = y0 + height / 2
            coding_unit_tree(x0, y0, split+1, width, height/2, 0, modeChild)
            if (y1 < PicHeightInLuma)
                coding_unit_tree(x0, y1, split+1, width, height/2, 0, modeChild)
            if ((LumaWidth == width) & (LumaHeight = height) & ChildSizeOccur4) {
                coding_unit(x0, y0, width, height, 'PRED_No_Constraint', 'COMPONENT_Chroma')
                Component = 0
        else if (BlockSplitMode == 'SPLIT_EQT_VER'):
            x1 = x0 + width / 4
            x2 = x0 + (3 * width / 4)
            y1 = y0 + height / 2
            coding_unit_tree(x0, y0, split+1, width/4, height, 0, modeChild)
            coding_unit_tree(x1, y0, split+1, width/2, height/2, 0, modeChild)
            coding_unit_tree(x1, y1, split+1, width/2, height/2, 0, modeChild)
            coding_unit_tree(x2, y0, split+ 1, width/4, height, 0, modeChild)
            if ((LumaWidth == width) & (LumaHeight = height) & ChildSizeOccur4):
                coding_unit(x0, y0, width, height, 'PRED_No_Constraint', 'COMPONENT_Chroma')
                Component = 0
        else if (BlockSplitMode == 'SPLIT_EQT_HOR') :
            x1 = x0 + width / 2
            y1 = y0 + height / 4
            y2 = y0 + (3 * height / 4)
            coding_unit_tree(x0, y0, split+1, width, height/4, 0, modeChild)
            coding_unit_tree(x0, y1, split+1, width/2, height/2, 0, modeChild)
            coding_unit_tree(x1, y1, split+1, width/2, height/2, 0, modeChild)
            coding_unit_tree(x0, y2, split+1, width, height/4, 0, modeChild)
            if ((LumaWidth == width) & (LumaHeight = height) & ChildSizeOccur4) {
                coding_unit(x0, y0, width, height, 'PRED_No_Constraint', 'COMPONENT_Chroma')
                Component = 0
        else:
            if (Component == 0):
                coding_unit(x0, y0, width, height, mode, 'COMPONENT_LUMACHROMA')
            else if (Component == 1):
                coding_unit(x0, y0, width, height, mode, 'COMPONENT_LUMA')
        
'''
编码单元定义
'''
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
                IsPcmMode[i+NumOfTransBlocks–2] = (IntraChromaPredMode == 'Intra_Chroma_PCM')
                IsChroma = 0
                if (i == NumOfTransBlocks -1 | i == NumOfTransBlocks -2):
                    IsChroma = 1
                block(i, width, height, CuCtp, IsChroma, IsPcmMode[i], component)
        else:
            if (PictureType != 0):
                if (mode != 'PRED_Intra_Only'):
                    self.skip_flag = 
                if (self.skip_flag):
                    if (UmveEnableFlag):
                        umve_flag
                    if (AffineEnableFlag & ! UmveFlag & (width >= 16) & (height >= 16)):
                        affine_flag
                if (! SkipFlag):
                    if (mode != 'PRED_Intra_Only'):
                        direct_flag
                    if (DirectFlag):
                        if (UmveEnableFlag):
                            umve_flag
                        if (AffineEnableFlag & ! UmveFlag & (width >= 16) & (height >= 16))
                            affine_flag
                    if (! DirectFlag & (mode == 'PRED_No_Constraint'))
                        intra_cu_flag
            PartSize = 'SIZE_2Mx2N'
            if (DtEnableFlag & IntraCuFlag):
                allowDtHorSplit = (height >= DtMinSize) & (height <= DtMaxSize) & (width / height < 4)& (width <= DtMaxSize)
                allowDtVerSplit = (width >= DtMinSize) & (width <= DtMaxSize) & (height / width < 4)& (height <= DtMaxSize)
                if (allowDtHorSplit | allowDtVerSplit):
                    dt_split_flag
                    if (DtSplitFlag)：
                        if (allowDtHorSplit & allowDtVerSplit):
                            dt_split_dir
                        else if (allowDtHorSplit):
                            DtSplitDir = 1
                        else:
                            DtSplitDir = 0
                    else:
                        dt_split_vqt_flag
                        if (! DtSplitVqtFlag):
                            dt_split_vadt_flag
            if (UmveFlag):
                umve_mv_idx
                umve_step_idx
                umve_dir_idx
            else if ((SkipFlag | DirectFlag) & AffineFlag):
                cu_affine_cand_idx
            else if (SkipFlag | DirectFlag):
                cu_subtype_index
            if (! SkipFlag & ! DirectFlag):
                if (! IntraCuFlag) {
                    if (AffineEnableFlag & (width >= 16) & (height >= 16)):
                        affine_flag
                if (AmvrEnableFlag):
                    if (EmvrEnableFlag & ! AffineFlag):
                        extend_mvr_flag
                    if (AffineFlag):
                        affine_amvr_index
                    else:
                        amvr_index
                if (PictureType == 2):
                    inter_pred_ref_mode
                if (SmvdEnableFlag & SmvdApplyFlag & ! AffineFlag & (InterPredRefMode == 2)& ! ExtendMvrFlag):
                    smvd_flag
                if (MvExistL0):
                    if (! SmvdFlag & NumRefActive[0] > 1):
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
                if (MvExistL1 & ! SmvdFlag):
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
                if (IpfEnableFlag & (PartSize == 'SIZE_2Mx2N') & (! IsPcmMode[0])):
                    ipf_flag
        if (! IntraCuFlag & ! SkipFlag):
            if (! DirectFlag & component == 'COMPONENT_LUMACHROMA'):
                ctp_zero_flag
            CuCtp = 0
            if (! CtpZeroFlag):
                if (PbtEnableFlag & (width / height < 4) & (height / width < 4) & (width >= 8) &(width <= 32)& (height >= 8) & (height <= 32)):
                    pbt_cu_flag
                if (! PbtCuFlag):
                    if (component == 'COMPONENT_LUMACHROMA'):
                        ctp_u
                        ctp_v
                    CuCtp = ctp_u << (NumOfTransBlocks–2)
                    CuCtp += (ctp_v << (NumOfTransBlocks–1))
                    if (((ctp_u != 0) | (ctp_v != 0)) | ( component !='COMPONENT_LUMACHROMA')):
                        ctp_y[0]
                        CuCtp += ctp_y[0]
                    else:
                        CuCtp += ctp_y[0]
                else:
                    if (component == 'COMPONENT_LUMACHROMA'):
                        ctp_u
                        ctp_v
                    CuCtp = ctp_u << (NumOfTransBlocks–2)
                    CuCtp += (ctp_v << (NumOfTransBlocks–1
                    for i in range(NumOfTransBlocks–2):
                        ctp_y[i]
                        CuCtp += (ctp_y[i] << i)
        else if (! SkipFlag):
            CuCtp = 0
            if (! IsPcmMode[0]):
                for i in range(NumOfTransBlocks–2):
                    ctp_y[i]
                    CuCtp += (ctp_y[i] << i)
            if ((component == 'COMPONENT_LUMACHROMA') & (IntraChromaPredMode !='Intra_Chroma_PCM')):
                ctp_u
                ctp_v
            CuCtp += (ctp_u << (NumOfTransBlocks–2))
            CuCtp += (ctp_v << (NumOfTransBlocks–1))
        for i in range(NumOfTransBlocks):
            if (i < NumOfTransBlocks–2):
                blockWidth = ((TransformSplitDirection == 0) | (TransformSplitDirection == 2)) ?width : (TransformSplitDirection == 1 ? width >> 1 : width >> 2)
                blockHeight = ((TransformSplitDirection == 0) | (TransformSplitDirection == 3)) ?eight : (TransformSplitDirection == 1 ? height >> 1 : height >> 2)
                blockX = x0 + (((TransformSplitDirection == 0) | (TransformSplitDirection == 2)) ? 0 :TransformSplitDirection == 1 ? ((blockWidth >> 1) * (i % 2)) : ((blockWidth >> 2) * i)))
                blockY = y0 + (((TransformSplitDirection == 0) | (TransformSplitDirection == 3)) ? 0 :TransformSplitDirection == 1 ? ((blockHeight >> 1) * (i / 2)) : ((blockHeight >> 2) * i)))
                IsChroma = 0
                if (i == NumOfTransBlocks -1 | i == NumOfTransBlocks -2):
                    IsChroma = 1
                block(i, blockWidth, blockHeight, CuCtp, IsChroma, IsPcmMode[i], component)

'''
变换块定义
'''
class block:
    def __init__(i, blockWidth, blockHeight, CuCtp, isChroma, isPcm, component):
        M1 = blockWidth
        M2 = blockHeight
        for x in range(M1):
            for y in range(M2):
                QuantCoeffMatrix[x][y] = 0
        if (! isPcm):
            if (CuCtp & (1 << i)):
                blockWidth = isChroma ? blockWidth / 2 : blockWidth
                blockHeight = isChroma ? blockHeight / 2 : blockHeight
                idxW = Log(blockWidth) – 1
                idxH = Log(blockHeight) – 1
                NumOfCoeff = blockWidth * blockHeight
                ScanPosOffset = 0
                while (! coeff_last)
                    coeff_run
                    coeff_level_minus1
                    coeff_sign



AbsLevel = coeff_level_minus1 + 1
ScanPosOffset = ScanPosOffset + coeff_run
PosxInBlk = InvScanCoeffInBlk[idxW][idxH][ScanPosOffset][0]
PosyInBlk = InvScanCoeffInBlk[idxW][idxH][ScanPosOffset][1]
QuantCoeffMatrix[PosxInBlk][PosyInBlk] = coeff_sign ? –AbsLevel : AbsLevel
if (ScanPosOffset >= NumOf Coeff – 1) {
break
}
coeff_last
ScanPosOffset = ScanPosOffset + 1

class next_start_code:
    def __init__(seq_data):