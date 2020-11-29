s_a_dict =  {
    '000001':'start_code',#起始码前缀
    '00': 'patch_start_code',#00-7F is patch_start_code
    '8F': 'patch_end_code',
    'B0': 'video_sequence_start_code',#视频序列起始码
    'B1': 'video_sequence_end_code',
    'B2': 'user_data_start_code',
    '000001B3': 'intra_picture_start_code',
    'B5': 'extension_start_code',
    'B6': 'inter_picture_start_code',
    'B7': 'video_edit_code',
    'FFFFFFFF': 'bbv_delay'
    }
global state = "start_code"
'''
    This function analysis state, decided what state used.
    Analysis s_a_dict and logic to achieve this function.
    
'''
def state_analysis(file_string):
    sub_start=0
    sub_end=6
    sub_string = file_string[sub_start:sub_end]
    global state
    if(s_a_dict[sub_string]=='start_code'&state == 'start_code')
        state = 'start_code'
    if(s_a_dict[sub_string]=='video_sequence_start_code'&state = 'start_code')
        state = 'video_sequence_start_code'
        get_sequence_header()
    #video_sequence_code begin
    if(s_a_dict[sub_string]=='video_sequence_end_code'&state = 'video_sequence_start_code')
        state = ''#
    if(s_a_dict[sub_string]!='video_sequence_end_code'&state = 'video_sequence_start_code')
        video_sequence_code_state_analysis(sub_string)
    

'''
    video_sequence_code analysis flow
'''
def get_sequence_header():
    pass

'''
    video_sequence_code analysis flow
'''
def video_sequence_code_state_analysis(sub_string):
    if(s_a_dict[sub_string]=='user_data_start_code')
        pass
    if(s_a_dict[sub_string]=='intra_picture_start_code')
        pass
    if(s_a_dict[sub_string]=='inter_picture_start_code')
        pass
    if(s_a_dict[sub_string]=='user_data_start_code')
        pass
    if(s_a_dict[sub_string]=='extension_start_code')
        pass
    
