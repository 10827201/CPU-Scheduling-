import copy

def ReadInputNum() :
    global num
    try :
        num = int( input( "1執行 0結束 : " ) )
        if ( num != 0 and num != 1 ) :
            print("請輸入0或1")    
            print()
            ReadInputNum()
    except ValueError :
        print("不為數字請重新輸入")    
        print()
        ReadInputNum()
    return num

def inputfilename () :
    global filename
    f = None
    try :
        filename = input("請輸入檔名:")
        f = open( filename+".txt", 'r')
    except FileNotFoundError :
        print ("File not found, try again ")
        inputfilename()
    finally:
        if f is not None :
            f.close()
    return filename

def BubbleSort( A , c ):
	n = len( A )
	for i in range( 0, n - 1 ):
		for j in range( i + 1, n ):
			if A[i][c] > A[j][c]:
				A[i], A[j] = A[j], A[i]
			elif A[i][c] == A[j][c]:
				if A[i][0] > A[j][0]:
					A[i], A[j] = A[j], A[i]

def changeID( numID ) :
    if ( numID >= 10 ) :
        num = numID - 10 
        ID = str( chr(65+num) )
    else :
        ID = str( numID )
    return ID

def Done ( IDlist ) :
    for i in range ( len(IDlist) ):
        if ( IDlist[i][1] > 0 ):
            return False
    return True 

def putintonextProcess ( Process, time, nextProcess ) :
    for i in range ( len(Process) ) :
        if ( Process[i][2] == time ) :
            nextProcess.append( i )
        elif ( Process[i][2] > time ) :
            return

def ResRatio( Process, time ) :
    return ( Process[1]+ time - Process[2] ) / Process[1] 

def findmaxRatio( IDlist, time ) :
    maxID = 0 
    Find = False
    Zero = True 
    for i in range( len(IDlist) ) :
        if ( IDlist[i][2] <= time and IDlist[i][1] != 0 ) :
            if ( IDlist[maxID][1] == 0  ) :
                maxID = i 
            elif ( ResRatio( IDlist[maxID], time ) < ResRatio( IDlist[i],time ) ) : #比較Ratio
                maxID = i 
            elif ( ResRatio( IDlist[maxID], time ) == ResRatio( IDlist[i],time ) and IDlist[maxID][2] ==  IDlist[i][2] ) : #比較Ratio
                if IDlist[maxID][0] > IDlist[i][0] :
                    maxID = i 
            Find = True 
        if ( IDlist[i][1] > 0 ) :
            Zero = False
    
    if Find == False :
        maxID = None
    
    if Zero :
        maxID = "Done" ;
    
    return maxID 

def findminBurst( IDlist, time ) :
    minID = 0 
    Find = False
    Zero = True 
    for i in range( len(IDlist) ) :
        if ( IDlist[i][2] <= time and IDlist[i][1] != 0 ) :
            if ( IDlist[minID][1] == 0  ) : # 目前最小的CPUBrust
                minID = i 
            elif ( IDlist[minID][1] > IDlist[i][1] ) :
                minID = i 
            elif ( IDlist[minID][1] == IDlist[i][1]) :
                if ( IDlist[minID][0] > IDlist[i][0] and IDlist[minID][2] == IDlist[i][2] ) :
                    minID = i
            Find = True 
        if ( IDlist[i][1] > 0 ) :
            Zero = False
    
    if Find == False :
        minID = None
    
    if Zero :
        minID = "Done" ;
    
    return minID 

def findPiroity( IDlist, time ) :
    plist = []
    minID = 0
    
    for i in range( len(IDlist) ) :
        if ( IDlist[i][2] <= time and IDlist[i][1] != 0 ) :
            if ( IDlist[minID][1] == 0  ) : #若已完成
                minID = i
                plist.clear()                
                plist.append(minID)
            elif ( IDlist[minID][3] > IDlist[i][3] ) :
                minID = i 
                plist.clear()
                plist.append(minID)
            elif ( IDlist[minID][3] == IDlist[i][3]) :
                plist.append(i)
    return plist 

def findnextRR( IDlist, nextRR, plist ) :
    for i in range ( len(nextRR) ) :
        if ( IDlist[nextRR[i][0]][3] == IDlist[ plist[0]][3] ) :
            if ( len(nextRR[i]) < len(plist) ):
                for j in range( len(plist) ):
                    find = False
                    for k in range ( len(nextRR[i]) ):
                        if ( nextRR[i][k] == plist[j] ):
                            find = True
                    if find != True :
                        nextRR[i].append(plist[j])
            return nextRR[i], i
    return plist, None

def FindArrivaltime( IDlist, time ) :
    for i in range ( len(IDlist) ): 
        if ( time == IDlist[i][2] ) :
            return True
    
    return False

def FCFS( IDlist ) :
    Gantt = []
    Waiting = []
    Turnaround = [] 
    i = 0 ;
    while i < len(IDlist) :
        if ( IDlist[i][2] > len(Gantt) ) : # 現在時間 > arrival time 
            Gantt.append("-")
        else :
            Waiting.append( [ IDlist[i][0], len(Gantt)-IDlist[i][2] ] )
            for j in range( IDlist[i][1] ): # CPU Brust 
                Gantt.append( changeID(IDlist[i][0]) ) # 轉換ID 0-9 A-Z
            Turnaround.append( [ IDlist[i][0], len(Gantt)-IDlist[i][2] ] )
            i += 1 
    return Gantt, Waiting, Turnaround

def RR( IDlist, time_slice ) :
    Process = copy.deepcopy(IDlist)
    Gantt = []
    Waiting = []
    Turnaround = [] 
    nextProcess = []
    i = 0 
    
    if ( FindArrivaltime ( Process, len(Gantt) ) ):
        putintonextProcess( Process, len(Gantt), nextProcess )     
        
    while ( not Done( Process ) ) :
        if ( len( nextProcess ) == 0 ) :
            Gantt.append("-")
            if ( FindArrivaltime ( Process, len(Gantt) ) ):
                putintonextProcess( Process, len(Gantt), nextProcess ) 
        else  :
            j = 0 ;
            ID = nextProcess[0]
            nextProcess.pop(0)
            while( j < time_slice and Process[ID][1] > 0 ) :
                Gantt.append( changeID(Process[ID][0]) )
                if ( FindArrivaltime ( Process, len(Gantt) ) ):
                    putintonextProcess( Process, len(Gantt), nextProcess )
                Process[ID][1] -= 1
                j += 1
            if ( Process[ID][1] > 0 ) :
                nextProcess.append( ID )
            elif (Process[ID][1] == 0 ) :
               Turnaround.append( [ Process[ID][0], len(Gantt)-Process[ID][2] ] ) #登記Turnaround time
               Waiting.append( [ Process[ID][0], len(Gantt)-Process[ID][2]-IDlist[ID][1] ] ) # waiting = turnaround time - brust
    return Gantt, Waiting, Turnaround

def SRTF( IDlist ) :
    Process = copy.deepcopy(IDlist)
    Gantt = []
    Waiting = []
    Turnaround = [] 
    
    minID = findminBurst( Process, 0 )
    while ( minID != "Done" ) :
        #print (minID)
        if ( minID == None ):
            Gantt.append( "-" ) 
            minID = findminBurst( Process, len(Gantt) )
        elif ( FindArrivaltime( Process, len(Gantt) ) ) : #有新的process進入
            minID = findminBurst( Process, len(Gantt) )
            if ( minID == "Done" ):
                break
            elif( minID == None ) :
                Gantt.append("-")
                minID = findminBurst( Process, len(Gantt) )
            else :                
                Gantt.append( changeID( Process[minID][0] ) )
                Process[minID][1] -= 1
        elif Process[minID][1] > 0 : #還沒有新的process原本的繼續執行
            Gantt.append( changeID( Process[minID][0] ) )
            Process[minID][1] -= 1
        
        if minID != None and Process[minID][1] == 0 :
           Turnaround.append( [ Process[minID][0], len(Gantt)-Process[minID][2] ] ) #登記Turnaround time
           Waiting.append( [ Process[minID][0], len(Gantt)-Process[minID][2]-IDlist[minID][1] ] ) # waiting = turnaround time - brust
           minID = findminBurst( Process, len(Gantt) ) #找新的process
        
    return Gantt, Waiting, Turnaround
    
def PPRR( IDlist, time_slice ) :
    Process = copy.deepcopy(IDlist)
    Gantt = []
    Waiting = []
    Turnaround = [] 
    plist = []
    nextProcess = []
    nextRR = []
    i = 0 
    piroity = 0 
    print ( IDlist )
    if ( FindArrivaltime ( Process, len(Gantt) ) ):
        plist = findPiroity( Process , len(Gantt) )
        piroity = Process[ plist[0] ][3]
        nextProcess = plist 

    while ( not Done( Process ) ) :
        if ( len(plist) == 0 ) :
            Gantt.append("-")
            if ( FindArrivaltime ( Process, len(Gantt) ) ):
                plist = findPiroity( Process , len(Gantt) )
                piroity = Process[ plist[0] ][3]
                nextProcess, rr = findnextRR( Process, nextRR, plist )
                if ( rr != None) :
                    nextRR.pop(rr)
        else :
            change = False
            j = 0 ;
            print (nextProcess)
            ID = nextProcess[0]
            nextProcess.pop(0)
            while( j < time_slice and Process[ID][1] > 0 ) :
                Gantt.append( changeID(Process[ID][0]) )
                Process[ID][1] -= 1
                if ( FindArrivaltime ( Process, len(Gantt) ) ):
                    plist = findPiroity( Process, len(Gantt) )
                    if ( Process[plist[0]][3] == piroity ) :
                        for k in range ( len( Process ) ) :
                            if ( Process[k][2] == len(Gantt) and Process[k][3] == Process[ID][3] ) :
                                nextProcess.append(k)
                    else :
                        change = True
                        if ( len(nextProcess) > 0  ) :
                            nextRR.append(copy.deepcopy(nextProcess))
                        nextProcess.clear()
                        nextProcess, rr = findnextRR( Process, nextRR, plist )
                        if ( rr != None ) :
                            nextRR.pop(rr)
                        break
                        
                j += 1
                
            if ( Process[ID][1] > 0 and change == False ) :
                nextProcess.append( ID )
            
            if ( Process[ID][1] == 0 ) :
                Turnaround.append( [ Process[ID][0], len(Gantt)-Process[ID][2] ] ) #登記Turnaround time
                Waiting.append( [ Process[ID][0], len(Gantt)-Process[ID][2]-IDlist[ID][1] ] ) # waiting = turnaround time - brust
                if change == False and len(nextProcess) == 0:
                   plist = findPiroity( Process, len(Gantt) )
                   nextProcess, rr = findnextRR( Process, nextRR, plist )
                   if ( rr != None ) :
                        nextRR.pop(rr)

    return Gantt, Waiting, Turnaround

def HRRN( IDlist ) :
    Process = copy.deepcopy(IDlist)
    Gantt = []
    Waiting = []
    Turnaround = [] 
    
    maxID = findmaxRatio( Process, 0 )
    while ( maxID != "Done" ) :
        if ( maxID == None ): #輪空
            Gantt.append( "-" ) 
            maxID = findmaxRatio( Process, len(Gantt) )
        else:
            while ( Process[maxID][1] > 0 ):
                Gantt.append( changeID( Process[maxID][0] ) )
                Process[maxID][1] -= 1
            Turnaround.append( [ Process[maxID][0], len(Gantt)-Process[maxID][2] ] ) #登記Turnaround time
            Waiting.append( [ Process[maxID][0], len(Gantt)-Process[maxID][2]-IDlist[maxID][1] ] ) # waiting = turnaround time - brust
            maxID = findmaxRatio( Process, len(Gantt) ) #找新的process
        
    return Gantt, Waiting, Turnaround
    
def Savelist ( Glist, Wlist, Tlist, G, W, T ):
    BubbleSort(W, 0)
    BubbleSort(T, 0)    
    Glist.append(G)
    Wlist.append(W)
    Tlist.append(T)

def PrintGantt( Gantt, outfile, case ):
    outfile.write( '=={:>12s}==\n'.format(case))
    for j in range ( len(Gantt) ) :
        outfile.write("%s" %Gantt[j]) 
    outfile.write("\n")

def PrintList ( listname, case, List, outfile ) :
    if( case != 6 ) : 
        outfile.write("ID\t%s\n" %listname)
        outfile.write("===========================================================\n")
        for i in range( len(List[case-1]) ) :
            outfile.write("%d\t%d\n" % ( List[case-1][i][0],List[case-1][i][1] ) )
    else :
        outfile.write("ID\tFCFS\tRR\tSRTF\tPPRR\tHRRN\n")
        outfile.write("===========================================================\n")
        for i in range( len( List[0] ) ) :
            outfile.write("%d\t%d\t%d\t%d\t%d\t%d\n" %( List[0][i][0],List[0][i][1], List[1][i][1],List[2][i][1],List[3][i][1],List[4][i][1]))
    outfile.write("===========================================================\n")

def PrintALL( outfile, name, case, Glist, Wlist, Tlist ):
    outfile.write("%s\n" %name )
    if ( case != 6 ):
        PrintGantt( Glist[case-1], outfile, name )
    else :  
        PrintGantt( Glist[0], outfile, "FCFS" )
        PrintGantt( Glist[1], outfile, "RR" )
        PrintGantt( Glist[2], outfile, "SRTF" )
        PrintGantt( Glist[3], outfile, "PPRR" )
        PrintGantt( Glist[4], outfile, "HRRN" )        
    outfile.write("===========================================================\n")
    outfile.write("\nWaiting Time\n")
    PrintList ( name, case, Wlist, outfile )
    outfile.write("\nTurnaround Time\n")
    PrintList ( name, case, Tlist, outfile )

if __name__ == '__main__' :
    
    ID = []
    IDlist = []
    Wlist = []
    Glist = []
    Tlist = []
    work =  ReadInputNum()
    while ( work != 0 ) :
        filename = inputfilename ()
        f = open(filename+'.txt', 'r')
        
        line = f.readline().split()
        line = list( map( int, line ) )
        case = line[0]
        time_slice = line[1]
        
        line = f.readline()
        line = f.readline()
        
        while line :
            ID = line.split()
            ID = list( map( int, ID ) )
            if ( len(ID) != 0  ) :
                IDlist.append(ID)
            line = f.readline()

        BubbleSort( IDlist, 2 ) #以arrival_time進行排序
        
        Gantt,Waiting, Turnaround = FCFS( IDlist )
        Savelist( Glist, Wlist, Tlist, Gantt, Waiting, Turnaround )
        
        Gantt,Waiting, Turnaround = RR( IDlist, time_slice )
        Savelist( Glist, Wlist, Tlist, Gantt, Waiting, Turnaround )
        
        Gantt,Waiting, Turnaround = SRTF( IDlist )
        Savelist( Glist, Wlist, Tlist, Gantt, Waiting, Turnaround )
        
        Gantt,Waiting, Turnaround = PPRR( IDlist, time_slice )
        Savelist( Glist, Wlist, Tlist, Gantt, Waiting, Turnaround )
        
        Gantt,Waiting, Turnaround = HRRN( IDlist )
        Savelist( Glist, Wlist, Tlist, Gantt, Waiting, Turnaround )
        
        outname = "out_"+ filename + ".txt" 
        outfile = open( outname, "w" )
        if ( case == 1 ) :
            PrintALL(outfile, "FCFS", case, Glist, Wlist, Tlist )
        elif case == 2 :
            PrintALL(outfile, "RR", case, Glist, Wlist, Tlist )
        elif case == 3 :
            PrintALL(outfile, "SRTF", case, Glist, Wlist, Tlist )
        elif case == 4 :
            PrintALL(outfile, "PPRR", case, Glist, Wlist, Tlist )
        elif case == 5 :
            PrintALL(outfile, "HRRN", case, Glist, Wlist, Tlist )
        elif case == 6 :
            PrintALL(outfile, "All", case, Glist, Wlist, Tlist )          
        outfile.close()
        
        work =  ReadInputNum()
        IDlist.clear()
        Glist.clear()
        Wlist.clear()
        Tlist.clear()