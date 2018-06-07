#!/usr/bin/python
import subprocess           
import sys
import os
import copy                 # for copy the list
import xml.dom.minidom
import sort_transition
from  xml.dom.minidom import parse, parseString
import math



class view_comso( object ):
    def __init__(self):
        self.__orbits = []
        self.file_database = []
        self.fileList = self.get_fileList()
        pass
    
    def run(self):
                        
        self.first_time = True
        
        while True:
           
           
           # by default, to load all xml files in the folder, 
           # and then go to the 'V' option 
           
           if(self.first_time): self.add_xml_files()
           
           if(self.first_time):  opt = 'V' # default action            
           
           
           if opt == 'A': os.system('clear'); self.add_xml_files()
           
           if opt == 'E': os.system('clear'); self.eliminate_item_in_database()
           
           if opt == 'P': os.system('clear'); self.print_current_database_withhold()
           
           if opt == 'V': os.system('clear'); self.veiwCosmo_submenu()
           
           
           
           if opt == 'X': self.clean_out_when_exit(); sys.exit(0)
           
           self.first_time = False
           
           
           
           opt = self.show_xml_menu() 
           opt = opt.capitalize()
           
           pass 
        pass




    
    def veiwCosmo_submenu(self):
        
        #
        # prepare the data_list
        #
        self.cp_xml_files()
        data_list = self.parse_xml()
        
        
        while True:
            os.system('clear');
            menu="""
            -- veiw cosmo menu --
                    
        (1) Combine two xmls (positive + negative parity)
        (2) View occupation of a given state in the active xml
        (3) Compare occupation between two states   
        (4) View the transition 
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        (U) go to xml files menu
        (H) Author's Note
        (X) Exit
"""
            print menu
            opt = raw_input( 'Your option: ' )

            if opt == '1': os.system('clear'); self.show_combine_two_xml(data_list)

            if opt == '2': os.system('clear'); self.view_occupation( data_list)
            
            if opt == '3': os.system('clear'); self.compare_occup_two_state(data_list)
            
            if opt == '4': os.system('clear'); self.show_transition( data_list)

            if opt.capitalize() == 'U': break
            
            if opt.capitalize() == 'H': os.system('clear'); self.author_note()

            if opt.capitalize() == 'X': self.clean_out_when_exit(); sys.exit( 0 )
        
        pass


        


    def show_xml_menu(self):
        
        os.system('clear');
        
        #
        # the xml files menu
        #   
        menu="""
         -- xml file menu --
         
        (A) Add the xml files into database 
        (E) Eliminate xml files in database
        (P) Print the current xml database
        - - - - - - - - - - - - - - - - - - 
        (V) View cosmo
        (X) Exit the program
        """
        print menu   
        opt = raw_input( 'Your option: ')
        opt = opt.capitalize()
        while True:
            if opt in ('A','E','P','V','X'):
                return opt
                break
            else:
                opt = raw_input( 'Your option: ')
                opt = opt.capitalize()     
        pass
        #----------------------------------------------------------# end

    
    def author_note(self):
        message ="""
        Last update: 2015 Nov. 1 written by Pei-Luan Tai
        
        To use this program:
        run the XSHLJT  program to get state info 
        run the XSHLAO  program to get occupation info
        run the XSHLEMB program to get transition info
        
        go to the xml menu, 
        it will automatically refresh the change in xml files.
        
        transition rates and Wesskopf unit is calculated by the formula 
        in the Appendix B of the book of Ring and Schuck  
        
"""
        print message
        tempp = raw_input("\n\ntype any key to continue. ")

    def get_fileList(self):
        p = subprocess.Popen("ls *.xml", shell=True,  stdout=subprocess.PIPE )    
        (result,err) = p.communicate()    
        fileList = result.split()
        if len(fileList) ==0:
         print "No xml files in the current folders!!!"
         sys.exit(0)
        return fileList
    

    def add_xml_files( self ):
        
        '''
        adding the xml files into the database
        '''
        #
        # by default, at the first time, we don't print information.
        #
        if( not self.first_time ):
            #
            # print our current database
            #
            self.print_current_database()
            if len( self.file_database ) == len( self.fileList ):
                #
                # in the case, we have loaded all the files.
                #
                print " \n   Aleady loaded all the xml files"
                tempp = raw_input("\n\ntype any key to continue. ")
                return self.file_database
            else:
                #
                # print out the possible selection
                #
                print "\nThe xml files in the current folders: \n"
                for i in range( len( self.fileList ) ):
                    print "(" + str( i + 1 ) + "):  " + self.fileList[i]
                print "\n"


            print "add the files into your database"
            print "use '0' to end the process"
        total_num = len( self.fileList )
        
        
        while True:

             if( not self.first_time ): option = input( "[1~" + str( total_num ) + "]: " ) 
             
             #
             # At the first time, we load all xml files.
             #
             if(self.first_time): option = 0
              
                
             if option < 0 or option > total_num:
                 #
                 # invalid input range
                 #
                 print "No such files"
             else:
                 #
                 # Valid input range
                 #
                 if option == 0 :
                     if( not self.first_time ): print " End of input"
                     break

                 print self.fileList[option - 1]
                 #
                 # we only add a new one to the database
                 #
                 if self.fileList[option - 1] not in self.file_database:
                     self.file_database.append( self.fileList[option - 1] )
                 #
                 # when database has all the files in the list, we exit.
                 #
                 if len( self.file_database ) == len( self.fileList ):
                     print "\n    Loaded all the xml files in current folder"
                     tempp = raw_input("\n\ntype any key to continue. ")
                     break
        #
        # in case we don't have any input.
        # then we load all the xml files
        #
        if len( self.file_database ) == 0:
           self.file_database = copy.deepcopy( self.fileList ) 
     
         
    def eliminate_item_in_database(self):
        
        #
        # print our database status
        #
        print "    ____________________________    "
        if len(self.file_database) ==0:
            print "    current database is empty"
        else:
            print "The xml files in our database: "    
            for i in range( len( self.file_database) ):
                print "("+str(i+1)+"):  "+ self.file_database[i]                
        print "    ____________________________    "
        
        
        print "substract the files in your database"
        print "use '0' to end the process"
        
        
        while True:
            option = input("[1~" + str(len(self.file_database)) + "]: ")
            
            if option <0 or option>len(self.file_database):
                print "No such files"
            else: 
                #
                # Valid input range
                #
                if option == 0 :
                    print " End of process"
                    break 
            
                del self.file_database[option-1] 
                
                self.print_current_database()
                
                
                if len(self.file_database) == 0: break
        pass
        #----------------------------------------------------------------------# end
    



                 

    def write_occup_diff_xg_data(self, occup_diff, outputFilename='data_diff.dat'):
        '''
        occup_diff = [ (terms), (terms), ... ]
        terms = ( orbit_name, Pdiff, Ndiff )
        '''
        writeout = open(outputFilename,'w')
        
        write_order_list = ('0s1','0p3','0p1',\
                      '0d5','1s1','0d3',\
                      '0f7','1p3','0f5','1p1',\
                      '0g9','0g7','1d5','1d3','2s1','0h11' )
        
        

        str1  = "# Bar char data. (x,y=height)\n"
           
        #
        # proton part: P_occup
        #
        index = 1
        str1 += '\n# proton diff \n'
        for i in range( len( write_order_list ) ):
            for j in range( len( occup_diff ) ):
                if occup_diff[j][0] == write_order_list[i]:
                    
                    P_occup = occup_diff[j][1]
                    str1 += str(index) + "\t" + str("%4.3f"%P_occup) + "\n"
                    index += 1
        
        #
        # neutron part: N_occup
        #
        index = 1
        str1 += "\n# neuton diff \n"
        for i in range( len( write_order_list ) ):
            for j in range( len( occup_diff ) ):
                if occup_diff[j][0] == write_order_list[i]:
                    
                    N_occup = occup_diff[j][2] 
                    str1 += str(index) + "\t" + str("%4.3f"%N_occup) + "\n"
                    index += 1
        writeout.write(str1)
        writeout.close()        
        pass


    def write_occup_xg_data(self, data_list, \
                            active_xml, active_state, \
                            outputFilename='data.dat'):
        """
        to write out the occupation to data.dat for bar char
        then call xmgrace to plot
        """
        
        current_xml = data_list[active_xml]
        occupation =  current_xml['occup'][active_state]
        
        # STEP 1: prepare the output filename.
        # write out data
        writeout = open(outputFilename,'w')
        str1  = "# Bar char data. (x,y=height)\n"

        
        # STEP2:
        # control what should we write out
        # we only want the occupation for the sd-shell or fp-shell
        #
        write_order_list = ('0s1','0p3','0p1',\
                      '0d5','1s1','0d3',\
                      '0f7','1p3','0f5','1p1',\
                      '0g9','0g7','1d5','1d3','2s1','0h11' )
        
        self.__orbits = [] # clear out
        

        #
        # proton part: P_occup
        #
        index = 1
        str1 += '\n# proton part\n'
        for i in range( len( write_order_list ) ):
            for j in range( len( current_xml['orbit_name'] ) ):
                if current_xml['orbit_name'][j] == write_order_list[i]:
                   
                    P_occup = float( occupation[j][1] )
                    str1 += str(index) + "\t" + str("%4.3f"%P_occup) + "\n"
                    index += 1

        #
        # neutron part: N_occup
        #
        index = 1
        str1 += '\n# neutron part\n'
        for i in range( len( write_order_list ) ):
            for j in range( len( current_xml['orbit_name'] ) ):
                if current_xml['orbit_name'][j] == write_order_list[i]:
                    
                    N_occup = float( occupation[j][0] )
                    str1 += str(index) + "\t" + str("%4.3f"%N_occup) + "\n"
                    index += 1
                    self.__orbits.append( current_xml['orbit_name'][j] )
        
        
                    
        # STEP3
        #  write out the results.
        #
        writeout.write(str1)
        writeout.close()
        
        #------------------------------------------------# end

 

    def print_occup(self, data_list, active_xml, active_state):
        """
        To print the occupation of a given state in a given xml file.
        """
        
        current_xml = data_list[active_xml]
        
        occupation =  current_xml['occup'][active_state]
        
        order_list = ('0s1','0p3','0p1',\
                      '0d5','1s1','0d3',\
                      '0f7','1p3','0f5','1p1',\
                      '0g9','0g7','1d5','1d3','2s1','0h11' )
        
        #
        # We use two loops to control the output follow the shell-model orbit order.
        #
        strOuts = []
        occup_info = []
        sumP = 0.
        sumN = 0.
        print "orbit\t P \t N" 
        for i in range( len( order_list ) ):            
            for j in range( len( current_xml['orbit_name'] ) ):  
                if current_xml['orbit_name'][j] == order_list[i]:
              
                  N_occup = float( occupation[j][0] )
                  P_occup = float( occupation[j][1] )
                  
                  sumN += N_occup
                  sumP += P_occup

                  s =  "%3s\t%4.2f\t%4.2f" \
                  %( current_xml['orbit_name'][j], P_occup, N_occup)
                  strOuts.append( s )

                  occup_info.append( (P_occup, N_occup) )
                  #
                  # set up the separation line.
                  #
                  ss = "---------------------"
                  if order_list[i] == '0p1' :strOuts.append( ss )
                  if order_list[i] == '0d3' :strOuts.append( ss )
                  if order_list[i] == '1p1' :strOuts.append( ss )
                  if order_list[i] == '2s1' :strOuts.append( ss )
          
       
        for i in range( len(strOuts) ):
          print "%s" %strOuts[-i-1]
        
         
        print "\n%3s\t%4.f\t%4.f" %( "sum",  sumP, sumN )

        return occup_info


    def print_occup_diff(self, data_list, active_xml, active_state):
        
        current_xml1 = data_list[ active_xml[0] ]
        current_xml2 = data_list[ active_xml[1] ]
        

        occupation1 =  current_xml1['occup'][active_state[0]]
        occupation2 =  current_xml2['occup'][active_state[1]]
        
        order_list = ('0s1','0p3','0p1',\
                      '0d5','1s1','0d3',\
                      '0f7','1p3','0f5','1p1',\
                      '0g9','0g7','1d5','1d3','2s1','0h11' )
        occup_diff = []
        
        print "diff = state_1 - state_2"
        print "orbit\t Pdiff \t Ndiff" 
        strOuts = []
        
         
        if len( current_xml1['orbit_name'] )  ==  len( current_xml2['orbit_name'] ):     
            for i in range( len( order_list ) ):            
                for j in range( len( current_xml1['orbit_name'] ) ):
                    for k in range( len( current_xml2['orbit_name'] ) ):
                     
                        if current_xml1['orbit_name'][j] == order_list[i] and\
                           current_xml2['orbit_name'][k] == order_list[i] :
                             
                            N_occup1 = float( occupation1[j][0] )
                            P_occup1 = float( occupation1[j][1] )
                            
                            
                            N_occup2 = float( occupation2[k][0] )
                            P_occup2 = float( occupation2[k][1] )
                            
                            s = "%3s\t%5.2f\t%5.2f" \
                              %( order_list[i], P_occup1 - P_occup2, \
                                                N_occup1- N_occup2 )
                            strOuts.append( s )
                            #
                            # set up the separation line.
                            #
                            ss = "---------------------"
                            if order_list[i] == '0p1':strOuts.append( ss )
                            if order_list[i] == '0d3':strOuts.append( ss )
                            if order_list[i] == '1p1':strOuts.append( ss )
                            if order_list[i] == '2s1':strOuts.append( ss )
                            
                             
                            #
                            # prepare for xmgrace
                            #
                            _info = ( order_list[i], \
                                      P_occup1-P_occup2, \
                                      N_occup1-N_occup2)
                            occup_diff.append( _info )
            
            
        else :
           #
           # get the difference in valence space. ex. cmp usd vs. WBP-a
           #

           diff_orbit=[]

           # if state1 in pf-sd-sp, state2 in sd ==> diff_orbit = pf
           # if state1 in sd, state2 in pf-sd-sp ==> diff_orbit = none
           for j in range( len( current_xml1['orbit_name'] ) ):
              if  current_xml1['orbit_name'][j] not in current_xml2['orbit_name'] \
              and current_xml1['orbit_name'][j] not in ('0s1', '0p3', '0p1' ):
                   diff_orbit.append(current_xml1['orbit_name'][j])
                    
                    
           # the second loop is necessary 
           # if state2 in pf-sd-sp, state1 in sd ==> diff_orbit = pf
           # if state2 in sd, state1 in pf-sd-sp ==> diff_orbit = none
           for k in range( len( current_xml2['orbit_name'] ) ):    
               if  current_xml2['orbit_name'][k] not in current_xml1['orbit_name'] \
               and current_xml2['orbit_name'][k] not in ('0s1', '0p3', '0p1' ):
                   diff_orbit.append(current_xml2['orbit_name'][k])
                    
           
            
           #
           # start to analyze
           #
           for i in range( len( order_list ) ):            
                for j in range( len( current_xml1['orbit_name'] ) ):
                    for k in range( len( current_xml2['orbit_name'] ) ):
                        if  current_xml1['orbit_name'][j] not in diff_orbit \
                        and current_xml2['orbit_name'][k] not in diff_orbit\
                        and current_xml1['orbit_name'][j] == order_list[i] \
                        and current_xml2['orbit_name'][k] == order_list[i]:
                        
                        # common orbits for both state1 and state2.

                            N_occup1 = float( occupation1[j][0] )
                            P_occup1 = float( occupation1[j][1] )
                            
                            
                            N_occup2 = float( occupation2[k][0] )
                            P_occup2 = float( occupation2[k][1] )
                             
                            s = "%3s\t%5.2f\t%5.2f" \
                            %( order_list[i], P_occup1-P_occup2, \
                                              N_occup1- N_occup2 )
                            strOuts.append( s )
                            ss = "---------------------"
                            if order_list[i] == '0p1':strOuts.append( ss )
                            if order_list[i] == '0d3':strOuts.append( ss )
                            if order_list[i] == '1p1':strOuts.append( ss )
                            if order_list[i] == '2s1':strOuts.append( ss )

                            _info = ( order_list[i],\
                                      P_occup1 - P_occup2, \
                                      N_occup1 - N_occup2)
                            
                            occup_diff.append(  _info )
                            pass
                        
                        elif current_xml1['orbit_name'][j] in diff_orbit\
                        and  current_xml1['orbit_name'][j] == order_list[i] \
                        and k==0:
                            # orbits that only state1 has.
                            N_occup1 = float( occupation1[j][0] )
                            P_occup1 = float( occupation1[j][1] )
                            N_occup2 = 0
                            P_occup2 = 0
                          
                            s = "%3s\t%5.2f\t%5.2f" \
                              %(  order_list[i], \
                                  P_occup1 - P_occup2, \
                                  N_occup1- N_occup2 )
                            strOuts.append( s )
                            ss = "---------------------"
                            if order_list[i] == '0p1':strOuts.append( ss )
                            if order_list[i] == '0d3':strOuts.append( ss )
                            if order_list[i] == '1p1':strOuts.append( ss )
                            if order_list[i] == '2s1':strOuts.append( ss )
                          
                            _info = ( order_list[i],\
                                    P_occup1 - P_occup2, \
                                    N_occup1 - N_occup2)                            
                            occup_diff.append(  _info )

                        elif current_xml2['orbit_name'][k] in diff_orbit\
                        and  current_xml2['orbit_name'][k] == order_list[i] \
                        and j==0 :
                            # orbits that only state2 has.
                            N_occup1 = 0
                            P_occup1 = 0
                            N_occup2 = float( occupation2[k][0] )
                            P_occup2 = float( occupation2[k][1] )
                             
                            s = "%3s\t%5.2f\t%5.2f" \
                              %(  order_list[i], \
                                  N_occup1 - N_occup2, \
                                  P_occup1 - P_occup2 )
                            strOuts.append( s )
                            
                            ss = "---------------------"
                            if order_list[i] == '0p1':strOuts.append( ss )
                            if order_list[i] == '0d3':strOuts.append( ss )
                            if order_list[i] == '1p1':strOuts.append( ss )
                            if order_list[i] == '2s1':strOuts.append( ss )

                            _info = ( order_list[i],\
                                    P_occup1 - P_occup2, \
                                    N_occup1 - N_occup2)                            
                            occup_diff.append(  _info )
                            pass

        for i in range( len(strOuts) ):
            print "%s" %strOuts[-i-1]   

        option = raw_input("to visualize occupation in xmgrace [y/N]: ")
        if option.capitalize() == 'Y': 

            self.write_occup_xg_data( data_list, \
                                      active_xml[0], active_state[0], \
                                      outputFilename='data_state1.dat')
            
            self.write_occup_xg_data( data_list, \
                                      active_xml[1], active_state[1],\
                                      outputFilename='data_state2.dat')
            
            self.write_occup_diff_xg_data(  occup_diff, \
                                            outputFilename='data_diff.dat')
            
            self.write_occup_diff_xg_script(  occup_diff,\
                                              outputFilename='.xmgrace.script' )
            
            # cmd = './plot_bar_diff.sh &'
            cmd = 'xmgrace -batch .xmgrace.script -saveall result_diff.agr &'
            subprocess.call(cmd,shell=True)
            temppp = raw_input("\ntype any key to continue..") 
        pass
        #------------------------------------------------------------------------# end
        




    def write_occup_xg_script(self, occup_info, outputFilename ):
      '''
      write out .xmgrace.script for the occup case for a single state.
      '''

      orbitN = len( self.__orbits ) # x2.
      # note: __orbits is updated at write_occup_xg_data()

      # the highest capacity of the orbit.
      highest_capacity = 0  # y2
      for orbit in self.__orbits:
        orbit_capacity = int( orbit[2:] ) + 1
        # note: if orbit = "0d5", 
        # then capacity = 5+1 = 6
        if orbit_capacity > highest_capacity : 
          highest_capacity = orbit_capacity
      
      #===========================================  
      outStr=""
      outStr+='g0 type Chart\n'
      # read input file.
      outStr+='READ BAR "data.dat"\n'
      outStr +="world 0, -1, %d, %d\n" %(orbitN+2, highest_capacity)
      outStr+='frame type 1\n'
      
      #Set appearance
      outStr+='s0 legend  "Proton"\n'
      outStr+='s1 legend  "Neutron"\n'
      outStr+='s0 line type 0\n'
      outStr+='s1 line type 0\n'
      outStr+='s0 symbol color 2\n'
      outStr+='s1 symbol color 4\n'
      outStr+='s0 symbol fill color 2\n'
      outStr+='s1 symbol fill color 4\n'
      outStr+='s0 symbol fill pattern 5\n'
      outStr+='s1 symbol fill pattern 24\n'
      
      # x,y axis
      outStr+='yaxis  ticklabel char size 0.750000\n'
      outStr+='yaxis  tick place normal\n'
      outStr+='yaxis  tick major grid on\n'
      outStr+='yaxis  tick major linestyle 2\n'
      outStr+='xaxis  tick place normal\n'
      outStr+='xaxis  tick off\n'
      outStr+='\n'
      
      # for special labels
      outStr +="xaxis  tick spec type both \n"
      outStr +="xaxis  tick spec %d \n" %(orbitN)  
       
      for idx, orbit in zip( range(orbitN), self.__orbits):
          # make 7/2 to be \s7/2, which is subscripted.
          orbit_front = orbit[:2]
          orbit_capacity = "%s/2" %orbit[2:] 
          tick = "%s\s%s" %( orbit_front, orbit_capacity )
          outStr += "xaxis  tick major %d, %d\n" %(idx, idx+1)
          outStr += 'xaxis  ticklabel  %d, "%s"\n' %(idx, tick )
        
      with open( outputFilename , "w") as f: 
        f.write(outStr)    
 
      pass


    def write_occup_diff_xg_script(self, occup_diff, outputFilename ):
      '''
      write out .xmgrace.script for the occup_diff case for two states.
       
      '''

      orbitN = len( self.__orbits ) # x2.
      # note: __orbits is updated at write_occup_xg_data()

      # the highest capacity of the orbit.
      highest_capacity = 0  # y2
      for orbit in self.__orbits:
        orbit_capacity = int( orbit[2:] ) + 1
        # note: if orbit = "0d5", 
        # then capacity = 5+1 = 6
        if orbit_capacity > highest_capacity : 
          highest_capacity = orbit_capacity


      # check the largest occup_diff
      # occup_diff = [ (orbit_name, Pdiff, Ndiff), (), (),...]
      npdiffs = []
      for terms in occup_diff:
        npdiffs.append( terms[1] )
        npdiffs.append( terms[2] )
      diff_max = max( npdiffs )
      diff_max += 1 # for some room.
      diff_max = int(diff_max)
      del npdiffs


      #===========================================  
      outStr = ""
      outStr +="arrange (3,1,0.1,0,0,ON,ON,ON)\n"

      outStr +="With G2\n"
      outStr +="g2 type Chart\n"
      #input file
      outStr +='READ BAR "data_state1.dat"\n'
      outStr +="world 0, -1, %d, %d\n" %(orbitN+2, highest_capacity)
      outStr +='frame type 1\n'
      outStr +='subtitle "diff = state1-state2"\n'
      
      #set appearance.
      outStr +='s0 legend  "state1 Proton"\n' 
      outStr +='s1 legend  "state1 Neutron"\n' 
      outStr +='s0 line type 0\n' 
      outStr +='s1 line type 0\n' 
      outStr +='legend 0.95, 0.87\n' 
      outStr +='s0 symbol color 2\n' 
      outStr +='s1 symbol color 4\n' 
      outStr +='s0 symbol fill color 2\n' 
      outStr +='s1 symbol fill color 4\n' 
      outStr +='s0 symbol fill pattern 5\n' 
      outStr +='s1 symbol fill pattern 24\n' 
      
      
      # xy axis
      outStr +='yaxis  ticklabel char size 0.750000\n' 
      outStr +='yaxis  tick place normal\n' 
      outStr +='yaxis  tick major 2\n' 
      outStr +='yaxis  tick major grid on\n' 
      outStr +='yaxis  tick major linestyle 2\n' 
      outStr +='xaxis  tick off\n' 
      outStr +='xaxis  ticklabel off\n' 
      outStr +='\n' 
      outStr +='\n'





      outStr +="#############################\n"
      outStr +="With G1\n"
      outStr +="g1 type Chart\n"
      #input file
      outStr +='READ BAR "data_state2.dat"\n' 
      outStr +="world 0, -1, %d, %d\n" %(orbitN+2, highest_capacity)
      outStr +='frame type 1\n' 
      
      #set appearance. 
      outStr +='s0 line type 0\n' 
      outStr +='s1 line type 0\n' 
      outStr +='legend 0.95, 0.62\n'  
      outStr +='s0 legend  "state2 Proton"\n' 
      outStr +='s1 legend  "state2 Neutron"\n' 
      outStr +='s0 symbol color 2\n' 
      outStr +='s1 symbol color 4\n'  
      outStr +='s0 symbol fill color 2\n' 
      outStr +='s1 symbol fill color 4\n' 
      outStr +='s0 symbol fill pattern 5\n' 
      outStr +='s1 symbol fill pattern 24\n' 

      # xy axis
      outStr +='yaxis  ticklabel char size 0.750000\n' 
      outStr +='yaxis  tick place normal\n' 
      outStr +='yaxis  tick major 2\n' 
      outStr +='yaxis  tick major grid on\n' 
      outStr +='yaxis  tick major linestyle 2\n' 
      outStr +='xaxis  tick off\n' 
      outStr +='xaxis  ticklabel off\n'  
      outStr +='\n' 
      outStr +='\n' 
      
      outStr +="#############################\n"  
      outStr +="With G0\n"
      outStr +="g0 type Chart\n"
      #input file
      outStr +='READ BAR "data_diff.dat"\n' 
      outStr +="world 0, %d, %d, %d\n" %(-diff_max,orbitN+2,diff_max)
      outStr +='frame type 1\n' 
      
      #set appearance; s0 = proton, s1 = neutron
      outStr +='s0 legend  "Pdiff"\n' 
      outStr +='s1 legend  "Ndiff"\n' 
      outStr +='s0 line type 0\n' 
      outStr +='s1 line type 0\n' 
      outStr +='legend 0.95, 0.34\n'  
      
      outStr +='s0 symbol color 2\n' 
      outStr +='s1 symbol color 4\n' 
      outStr +='s0 symbol fill color 2\n'
      outStr +='s1 symbol fill color 4\n'
      outStr +='s1 symbol fill pattern 24\n' 
      outStr +='s0 symbol fill pattern 5\n' 
      outStr +='\n' 

      # xy axis 
      outStr +='yaxis  ticklabel char size 0.750000\n' 
      outStr +='yaxis  tick place normal\n' 
      outStr +='yaxis  tick major 1\n' 
      outStr +='yaxis  tick major grid on\n'    
      outStr +='yaxis  tick major linestyle 2\n'
      outStr +='xaxis  tick off\n'     
  
      # for special labels for x axis
      outStr +="xaxis  tick spec type both \n"
      outStr +="xaxis  tick spec %d \n" %(orbitN)  
      
      for idx, orbit in zip( range(orbitN), self.__orbits):
          # make 7/2 to be \s7/2, which is subscripted.
          orbit_front = orbit[:2]
          orbit_capacity = "%s/2" %orbit[2:] 
          tick = "%s\s%s" %( orbit_front, orbit_capacity )
          outStr += "xaxis  tick major %d, %d\n" %(idx, idx+1)
          outStr += 'xaxis  ticklabel  %d, "%s"\n' %(idx, tick )
        
      with open( outputFilename , "w") as f: 
        f.write(outStr)

      pass







    def compare_occup_two_state(self, data_list):
        
        self.print_current_database()
        active_xml1 = int( input( "\n    set active xml_1: " ) ) - 1

        self.print_states( data_list, active_xml1 )
        state1 = int( input( " select state_1: " ) ) - 1

        self.print_current_database()
        active_xml2 = int( input( "\n    set active xml_2: " ) ) - 1

        self.print_states( data_list, active_xml2 )
        state2 = int( input( " select state_2: " ) ) - 1

        # print user's input
        self.print_selected_2states( data_list, \
                                active_xml1, active_xml2,\
                                state1, state2 )
        
        #
        # show the diff in occupation number
        #
        active_xml = (active_xml1, active_xml2)
        active_state = ( state1,  state2 )
        self.print_occup_diff( data_list, active_xml, active_state)
        
    
    def view_occupation(self, data_list):
        
        active_xml = self.set_active_xml()
        
          
        current = data_list[active_xml]
        total_states = len(current['Ex'])
        
        while True:
            
            #
            # show the states, so that we can pick one
            #
            self.print_states(data_list, active_xml)
            
             
            
            opt = raw_input( "'x' to end, 'number' to pick a state: " )
            
            if opt.capitalize() == 'X': break
            
            elif opt.isdigit() and int(opt) <= total_states :
                active_state = int( opt )- 1
                print "\n(%i): %4i\t%4s %3s\n" \
                % ( int(active_state)+1, \
                    int( float(current['Ex'][active_state])*1000 ), \
                    current['state_id'][active_state][:-3],\
                    current['state_id'][active_state][-3:]  )
                
                occup_info = \
                self.print_occup( data_list, active_xml, active_state )
                
                opt_plot = raw_input("to visualize data in xmgrace? [y/N]:")
                
                if opt_plot.capitalize() == 'Y' :
                    #
                    # call methods to plot.
                    #
                    self.write_occup_xg_data(data_list, active_xml, active_state)
                    
                    self.write_occup_xg_script( occup_info, ".xmgrace.script")  

                    cmd = 'xmgrace -batch .xmgrace.script -saveall result_single.agr &' 

                    subprocess.call(cmd,shell=True)  
                    pass
        pass
        #------------------------------------------------------# end
  
  
  
  
    def print_selected_2states(self, data_list, \
        active_xml1, active_xml2, idx1, idx2 ):

        current = data_list[ active_xml1 ]
        state_info = " %4i %5s" \
          % ( int( float(current['Ex'][idx1])*1000 ), \
              current['state_id'][idx1][:-3] ) 
        print "state1: %s from %s " \
          %( state_info, self.file_database[active_xml1]  )

        current = data_list[ active_xml2 ]
        state_info = " %4i %5s" \
          % ( int( float(current['Ex'][idx2])*1000 ), \
              current['state_id'][idx2][:-3] ) 
        print "state2: %s from %s \n" \
          %( state_info, self.file_database[active_xml2]  )

        pass
  
    def print_current_database_withhold(self):
        print "    ____________________________    "
        print "    Database:     "
        if len(self.file_database) == 0:
            print "    current database is empty"
        else:
            for i in range( len(self.file_database) ):
                print "    (" + str( i + 1 ) + "):  "+self.file_database[i]
        print "    ____________________________    "
        tempp = raw_input("\n\ntype any key to continue. ")
    
    
    def print_current_database(self):
        print "    ____________________________    "
        print "    Database:     "
        if len(self.file_database) == 0:
            print "    current database is empty"
        else:
            for i in range( len(self.file_database) ):
                print "    (" + str( i + 1 ) + "):  "+self.file_database[i]
        print "    ____________________________    "
        

    def print_states(self, data_list, active_xml):
        
        '''
        print the state information
        '''
        
        current = data_list[active_xml]
        print "\n  -  -  -  -   -  -  -  -\n"
        for i in range( len(current['Ex']) ):
            print " (%i):\t%4i\t%5s %3s" % ( int(i)+1, \
                                             int( float(current['Ex'][i])*1000 ), \
                                             current['state_id'][i][:-3],\
                                             current['state_id'][i][-3:] )
        print "\n  -  -  -  -   -  -  -  -\n"
        pass

  
    def set_active_xml(self):
        
        self.print_current_database()
        
        active_xml = int(input("    set active xml: "))-1 
        
        #
        # print active xml
        #
        print "    ____________________________    "
        print "    Active xml:     "
        print "    "+self.file_database[active_xml]
        print "    ____________________________    "
        
                
        return active_xml
    
    
    
    
    

    def B_Weisskopf_unit(self, BCosmo, EMLmode, A ):
        
        '''
        Convert reduced rate B in comso in Weisskopf unit,
        
        return B in W.U unit
        '''
        B_wu = 0
        #
        #  Egamma in unit of MeV. ( not keV) 
        #
        L = int( EMLmode[1] )

        b = 1.0045 * A**( float( 1 ) / 6 )
        BE = BCosmo * b**( 2 * L )
        BM = BCosmo * b**( 2 * L - 2 )
        
        BEL = 0.0796 * ( 1.2 )**(2*L) * ( 3.0 / (L+3) )** 2 * A**( 2 * float(L)/3 )

        BML = 3.1831 * (1.2)**(2*L-2) * ( 3.0/(L+3) )**2 * A**( (2*float(L)-2)/ 3 ) 

        
                        
        if EMLmode[0] == 'E':
            B_wu = BE/BEL 
            
                            
        elif EMLmode[0] == 'M':
            B_wu = BM/BML 
        
        return  B_wu
        pass

    
    def trans_prob(self, Egamma, BCosmo, EMLmode, A ):
        '''
        return the transition probability in unit of 1/sec.
        '''
        
        #
        #  Egamma in unit of MeV. ( not keV) 
        #
       
        L = int( EMLmode[1] )
        
        # b = 1.0045* A ** ( float(1)/6 ); # this is the older formula        
        b = 6.4289*( 45*A**(- float(1)/3) - 25*A**(- float(2)/3) )** (- float(1)/2)  # rebeca told me, this is an updated one.
        
        BE = BCosmo* b**(2*L);
        BM = BCosmo* b**(2*L-2);
        
        trans_prob = 0
        mode = 0
        
        if EMLmode[0] == 'E':
            if L == 1:
                trans_prob = 1.587*10**15 * (Egamma)**3 *BE
            elif L == 2:
                trans_prob = 1.223*10**9 * (Egamma)**5  *BE
            elif L == 3:
                trans_prob = 5.698*10**2 * (Egamma)**7  *BE
                
        elif EMLmode[0] == 'M':
            if L == 1:
                trans_prob = 1.779*10**13 * (Egamma)**3 *BM
            elif L == 2:
                trans_prob = 1.371*10**7  * (Egamma)**5 *BM;
            elif L == 3:
                trans_prob = 6.387*10     * (Egamma)** 7*BM;
        
        return trans_prob
        pass

    
    def show_transition(self, data_list):
        
        self.print_current_database()
        
        active_xml = int( input( "\n    set active xml: " ) ) - 1
        
        current_xml = data_list[ active_xml ]
        
        total_states =len(current_xml['Ex'])
        
        
        
        while True:
            
            #
            # show the states, so that we can pick one
            #
            self.print_states(data_list, active_xml)
            
            output_string = []
            
            opt = raw_input( "'x' to exit or 'num' to pick a state: " )
            
            if opt.capitalize() == 'X': break
            
            elif opt.isdigit() and int(opt) <= total_states :
                
                active_state = int( opt )- 1
                
                transitions_list = current_xml['transition'][active_state]
                
                
                initial_Ex   = current_xml['Ex'][active_state]
                initial_Ex    = int(float(initial_Ex)*1000)
                inital_id  = current_xml['state_id'][active_state][:-3]
                inital_id2 = current_xml['state_id'][active_state]
                
                atomic_massA = current_xml['A']
                
                
                
                
                #
                # to set up the ratios for trans_prob 
                #
                ratios_trans = []
                for trans_info in transitions_list:
                    mode = trans_info[0][2:-1]
                    final_id = trans_info[1]
                    B = float( trans_info[2] )
                    
                
                    final_index = -1
                    final_Ex = 0;
                    #
                    # find out the final state energy
                    #
                    for i in range( total_states ):
                        if current_xml['state_id'][i] == final_id:

                            final_index = i
                            final_Ex = current_xml['Ex'][final_index]
                            final_Ex = int( float( final_Ex ) * 1000 )


                    
                    if initial_Ex > final_Ex:
                        Egamma = float( initial_Ex - final_Ex ) / 1000  # in unit of MeV
                        trans_prob = self.trans_prob( Egamma, B, mode, atomic_massA )
                        ratios_trans.append(trans_prob)
                        
                
                max_trans = max(ratios_trans )
                for i in range( len(ratios_trans) ):
                    ratios_trans[i] = float(ratios_trans[i])/ max_trans 
                    
                    
                    
                #
                #    print the final results
                #
                print "  Ex_i, J_i   ->  Ex_f, J_f     mode    B(W.U.)   trans_Prob    ratios  "
                print "-----------------------------------------------------------------------"
                ratio_idx = 0
                
                for trans_info in transitions_list:
                    mode = trans_info[0][2:-1]
                    final_id = trans_info[1]
                    B = float( trans_info[2] )


                    final_index = -1
                    final_Ex = 0;
                    for i in range( total_states ):
                        if current_xml['state_id'][i] == final_id:

                            final_index = i
                            final_Ex = current_xml['Ex'][final_index]

                            final_Ex = int( float( final_Ex ) * 1000 )


                            
                    
                    if initial_Ex > final_Ex:

                        Egamma = float( initial_Ex - final_Ex ) / 1000  # in unit of MeV


                        trans_prob = self.trans_prob( Egamma, B, mode, atomic_massA )
                        B_wu = self.B_Weisskopf_unit(B, mode, atomic_massA )



                        print "{%4i,%7s}->{%4i,%7s}   %2s   %.2E    %.2E       %5.1f" \
                        %(initial_Ex, inital_id2, final_Ex, str( final_id ), mode, \
                        B_wu, trans_prob, ratios_trans[ratio_idx]*100 )
                        
                                                
                        # dont change the format!!! for tempstr
                        tempstr = "{%4i,%7s}->{%4i,%7s}   %2s   %.2E    %.2E    %.2E" \
                        %(initial_Ex, inital_id2, final_Ex, str( final_id ), mode, \
                        B_wu, trans_prob, ratios_trans[ratio_idx] )
                        
                        output_string.append(tempstr)
                                                
                        ratio_idx += 1
                        

                    
                if ratio_idx >1:   temppp = raw_input("\ntype s to sort, or other key to continue..")
                if ratio_idx == 1: temppp = raw_input("\ntype any key to continue..")
                
                if temppp.lower() == 's' and ratio_idx >1:                   
                    sorting = sort_transition.sortTrans(output_string)
                    pass  
                
            
        pass





    def show_combine_two_xml( self, data_list ):
        self.print_current_database()
        active_xml1 = int( input( "\n    set active xml_1: " ) ) - 1
        active_xml2 = int( input( "    set active xml_2: " ) ) - 1
        current_xml1 = data_list[ active_xml1 ]
        current_xml2 = data_list[ active_xml2 ]

        #
        # find out the min binding energy
        #
        min_binging = 0  
        
        
        if current_xml1['binding'][0] < current_xml2['binding'][0]:
            min_binging = current_xml1['binding'][0]
        else: 
            min_binging = current_xml2['binding'][0]

        list=[]
        
        for i in range( len(current_xml1['binding'])   ):           
            temp = (current_xml1['binding'][i] - min_binging, current_xml1['state_id'][i]  )
            list.append( temp  )
            
        for i in range( len(current_xml2['binding'])   ):
            temp = (current_xml2['binding'][i] - min_binging, current_xml2['state_id'][i]  )
            list.append( temp  )
        
        
        #
        # sort by binding energy
        #
        list.sort( key= lambda x: x[0] )
        
        
        print "\n    Ex\tspin"
        for i in range( len(list)   ):
            print " %4i\t%5s %3s" %(int(list[i][0]*1000+0.5), list[i][1][:-3], list[i][1][-3:])
        
        temppp = raw_input("type any key to continue..")    

        pass



    def clean_out_when_exit(self):
      '''
      remove files such as .xxx_copy
      '''
      cmd = "rm .*_copy .xmgrace.script 2>/dev/null"
      subprocess.call(cmd,shell=True)
    
    def cp_xml_files(self):  
        
        '''
        to make a copy of original xml files
        '''
        
        # adding the root tag for the xml
        # modify the original xml file.
        
        for i in range( len(self.file_database) ):
            infile = open(       self.file_database[i]  ,'r')
            oufile = open( "." + self.file_database[i] +"_copy",'w')
            #file_database[i] = "."+ self.file_database[i] +"_copy"
              
            lines = infile.readlines()
            lines = lines[1:]
          
            head="""\
<?xml version="1.0"?>
<root>
        """
            tail="</root>"+"\n"
            good_one = []
            good_one.append(head) 
            good_one += lines 
            good_one.append(tail)     
            infile.close()
             
            for line in good_one:
                oufile.write( line )
            oufile.close()
            
            
    def parse_xml(self):
        
        """
        To extract the xml file, and arrange into a data_list[ {state1},{state2},{state3} ]
        
        data_list is a array, and each element is a dictrionary.
		
		    to see the xml1: data_list[0]
        
        to see the xml1 first state's energy: data_list[0]['Ex'][0]
        to see the xml1 second state's energy: data_list[0]['Ex'][1]        
        """
        
        
        data_list = [] # the total result

        for i in range( len(self.file_database) ):
            
            # create the Document object from parse() method.
            doc = parse( open("." + self.file_database[i] +"_copy" ) )
        
            temp_dic = {}
            temp_dic['Ex']   =[]
            temp_dic['spin'] =[]
            temp_dic['binding']=[]
            temp_dic['occup'] = []
            temp_dic['orbit_name'] = []
            temp_dic['transition'] = []
            temp_dic['state_id'] = []
            temp_dic['A'] = 0
            
            
            # get atomic mass
            tag_system = doc.getElementsByTagName("system")
            temp_dic['A'] = int(tag_system[0].getAttribute( 'A' ) )
            
            
            
            # get a list of all the tag "state"
            tag_state_list = doc.getElementsByTagName("state")  
            

            
            
            
            
            for state in tag_state_list: ##
                #
                # the list of < occupation > tag under a <state>
                # <occupation name="0f5" N="0.0260252" Z="0.0053174"/>
                # <occupation name="1p3" N="0.055295" Z="0.00611222"/>
                # <occupation name="1p1" N="0.00486805" Z="0.00280927"/>
                #
                tag_occupation_list =state.getElementsByTagName("occupation")
                 
                single_state_occup = []
                
                
                for k in range ( len(tag_occupation_list) ): ###
                     
                    orbit = str( tag_occupation_list[k].getAttribute('name') )
                    N_occup = tag_occupation_list[k].getAttribute('N')
                    P_occup = tag_occupation_list[k].getAttribute('Z')                     
                    single_state_occup.append(  (N_occup, P_occup) ) 
                    pass ###
                
                temp_dic['occup'].append(single_state_occup)
                pass ##         
                
            
            for state in tag_state_list: ##
                
                #
                # <transition name="B(E2)" final="0+(1)" B="8.90153"/>
                #
                tag_transition_list =state.getElementsByTagName("transition")
                 
                single_state_transition = []
                
                
                for k in range ( len(tag_transition_list) ): ###
                     
                    mode        = str( tag_transition_list[k].getAttribute('name') )
                    final_state =      tag_transition_list[k].getAttribute('final')
                    reduceB     =      tag_transition_list[k].getAttribute('B')  
                    
                    single_state_transition.append(  (mode, final_state, reduceB) ) 
                    pass ###
                
                temp_dic['transition'].append(single_state_transition)
                pass ##         
            
    
            
            
            ### extract data and fill in
            # <state J="0" P="+" T="0" E="-87.0896" name="0+(1)" Ex="0">
            for item in tag_state_list:
                # print("this is Ex: ", item.getAttribute('Ex') )
                Ex = item.getAttribute( 'Ex' )
                spin = str( item.getAttribute( 'J' ) ) + str( item.getAttribute( 'P' ) )
                binding = float( item.getAttribute( 'E' ) )
                id = item.getAttribute( 'name' )
                
                temp_dic['Ex'].append( Ex )
                temp_dic['spin'].append( spin )
                temp_dic['binding'].append( binding )
                temp_dic['state_id'].append( id )

                pass
            
            # get the orbit name in the model space.
            valencespace = doc.getElementsByTagName("valencespace")
            orbit_list = valencespace[0].getElementsByTagName("orbital")
            
            for k in range ( len( orbit_list ) ):

                orbit = str( orbit_list [k].getAttribute( 'name' ) )
                temp_dic['orbit_name'].append(orbit)
                pass                            
            
            
            data_list.append(temp_dic )
        if(0): print( data_list[0] )
        return data_list
        pass  
    






    

 

    


    
obj = view_comso()
obj.run()    
