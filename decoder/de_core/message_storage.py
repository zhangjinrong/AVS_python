#This file is a basic file, store video message 

# store sequence_header message, instantiation it and add to main function
# key = sequence_header name, value = sequence_header size,instantiation shuould be changed
sequence_header =  {
    'video_sequence_start_code':32,
    'profile_id': 8,
    '8F': 'patch_end_code',
    'B0': 'video_sequence_start_code',
    'B1': 'video_sequence_end_code',
    'B2': 'user_data_start_code',
    '000001B3': 'intra_picture_start_code',
    'B5': 'extension_start_code',
    'B6': 'inter_picture_start_code',
    'B7': 'video_edit_code',
    'FFFFFFFF': 'bbv_delay'
    }