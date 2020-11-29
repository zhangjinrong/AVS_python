filepath = 'bin.txt'
w_filepath = 'w_bin.txt'
wf = open(w_filepath,'w')
with open(filepath,'r') as f:
    for a in f.readlines():
        s_a = a.split( )
        if(len(s_a)==16):
            for i in range(8):
                wf.write(s_a[i])
                wf.write(' ')
            wf.write('\n')
            for i in range(8):
                wf.write(s_a[i+8])
                wf.write(' ')
            wf.write('\n')
        else:
            for i in range(len(s_a)):
                wf.write(s_a[i])
                wf.write(' ')
            wf.write('\n')
        
wf.close()