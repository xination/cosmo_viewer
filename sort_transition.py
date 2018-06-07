
class sortTrans(object):
    '''
    sorting the transition probability, make it easier to read. 
    '''
    def __init__(self, trans_info):
        
        Ef_Jf = []
        Ef_id = []
        Ef = []
        mode = []        
        Trans_rate = []
        reduced_rate_B = []
        
        #{1509,  2+(1)}->{   0,  0+(1)}   E2   1.83E+01    7.22E+11    1.00E+00        
        #{5914,1/2+(3)}->{   0,3/2+(1)}   M1   3.93E-03    2.59E+00    4.97E-01
        #01234567890123456789012345678901234567890123456789012345678901234567890
        #                |            |   ||   |      |    |      |    |      |   
        preset = trans_info[0][:16]
        preset_final =[]
        
        # collecting data
        for item in trans_info:
            Ef.append( int( item[17:21] ) )
            Ef_id.append( item[22:29] ) 
            Ef_Jf.append(item[16:30])  
            mode.append( item[33:35] )
            reduced_rate_B.append(float( item[38:46] ) ) 
            Trans_rate.append(float(item[50:58]) )
            


        total_num = len( Ef )
        mode_new = [0] * total_num
        comboRate_T = [0] * total_num

 
 
 
 
        #
        # adding transition rate from the same final states.
        #
        for ix in range( total_num ):
            for iy in range( total_num ):
                if ix < iy and Ef[ix] == Ef[iy]:
                    mode_new[ix] = 'M1+E2'
                    mode_new[iy] = 'NA'
                    comboRate_T[ix] = Trans_rate[ix] + Trans_rate[iy]
                    comboRate_T[iy] = 0
                    pass
                
        for ix in range( total_num ):
            if mode_new[ix]==0:
                mode_new[ix] = mode[ix]
                comboRate_T[ix] = Trans_rate[ix] 


        
        order=[] # soring order, from max to min.
       
        
        comboRate_Tcopy = comboRate_T[:]
        
        #
        # sorting is done here.
        #
        while (1):
             
            maxT = max(comboRate_Tcopy)
                             
            maxidx = comboRate_T.index(maxT)                         
             
            if maxT !=0 : order.append(maxidx)
              
            comboRate_Tcopy.remove(maxT)
             
            if len(comboRate_Tcopy) <1 : break 
            pass
         
             

        print "  Ex_i, J_i   ->  Ex_f, J_f     mode   trans_Prob    ratios  "
        print "----------------------------------------------------------------"
        for ix in  order :
            print "%s%s  %5s   %.2E     %5.1f"%(preset, Ef_Jf[ix],\
                                             mode_new[ix],\
                                             comboRate_T[ix],\
                                             comboRate_T[ix]/comboRate_T[ order[0] ]*100 )
                 
                     
        pass
        temppp = raw_input("\ntype any key to continue..")






# for testing only. 
# trans_info= ["{5914,1/2+(3)}->{   0,3/2+(1)}   M1   3.93E-03    2.59E+00    4.97E-01",\
#              "{5914,1/2+(3)}->{ 815,1/2+(1)}   M1   2.95E-03    1.25E+00    2.40E-01",\
#              "{5914,1/2+(3)}->{2295,3/2+(2)}   M1   1.23E-03    1.85E+00    3.56E-02",\
#              "{5914,1/2+(3)}->{3824,3/2+(3)}   M1   9.51E-03    2.76E+00    5.31E-02",\
#              "{5914,1/2+(3)}->{4493,1/2+(2)}   M1   2.53E-02    2.31E+00    4.44E-02",\
#              "{5914,1/2+(3)}->{5128,3/2+(4)}   M1   8.91E-05    1.38E+00    2.65E-05",\
#              "{5914,1/2+(3)}->{5709,3/2+(5)}   M1   4.33E-03    1.19E+00    2.28E-05",\
#              "{5914,1/2+(3)}->{   0,3/2+(1)}   E2   1.02E+00    5.20E+00    1.00E+00",\
#              "{5914,1/2+(3)}->{1606,5/2+(1)}   E2   2.07E-02    2.18E+00    4.18E-03",\
#              "{5914,1/2+(3)}->{2295,3/2+(2)}   E2   3.24E-02    1.42E+00    2.74E-03",\
#              "{5914,1/2+(3)}->{2870,5/2+(2)}   E2   1.07E+00    1.97E+00    3.79E-02",\
#              "{5914,1/2+(3)}->{3824,3/2+(3)}   E2   6.43E-01    1.81E+00    3.49E-03",\
#              "{5914,1/2+(3)}->{5037,5/2+(3)}   E2   3.76E-01    1.38E+00    2.65E-05",\
#              "{5914,1/2+(3)}->{5128,3/2+(4)}   E2   1.98E+00    4.20E+00    8.07E-05",\
#              "{5914,1/2+(3)}->{5397,5/2+(4)}   E2   6.62E-01    1.73E+00    3.33E-06",\
#              "{5914,1/2+(3)}->{5709,3/2+(5)}   E2   2.96E+00    7.57E+00    1.46E-07",\
#              "{5914,1/2+(3)}->{5764,5/2+(5)}   E2   2.62E-01    1.41E+00    2.71E-09"]
# 
# 
# 
# 
# obj=sortTrans(trans_info)
