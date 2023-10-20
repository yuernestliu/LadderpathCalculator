"""
==============================
Version 1.3,
Based on 1st stable release. Main functions to calculate ladderpath.
written by Yu Ernest Liu, 2022.06.10.
Add omega_min() and omega_max() to calculate kappa and eta.
Add laddergraph_single(), written by Zecheng Zhang.
2023.06.18
==============================
"""
#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
import random
import os
import graphviz

# ============ associated functions ============
def LongestEqSubstr(str1, str2): 
    # This function finds the longest common substring between two strings.
    # It returns the length of the common substring and its starting index.
    
    # Initialize variables to track the longest common substring.
    iStartOnly = 0     # Starting index of the longest substring.
    substrLenMax = 0   # Length of the longest substring.
    iStart = 0         # Temporary variable to store the starting index of the current substring.
    substrLen = 0      # Temporary variable to store the length of the current substring.
    
    # Iterate through each character and its index in the first string(str1).
    for i, iEle in enumerate(str1):
        if iEle == str2[i]:
            # If the current characters match, update the current substring length and starting index.
            if substrLen == 0:
                iStart = i
            substrLen += 1
        else:
            # If the characters don't match, check if there was a previous substring.
            if substrLen != 0:
                # Update the longest substring if the current one is longer.
                if substrLen > substrLenMax:
                    substrLenMax = substrLen
                    iStartOnly = iStart
                # Reset the current substring length.
                substrLen = 0
    
    # Check for the longest substring at the end of the iteration.
    if substrLen > substrLenMax:
        substrLenMax = substrLen
        iStartOnly = iStart
    
    # Return the length of the longest substring and its starting index.
    return substrLenMax, iStartOnly

def LongestSubstr_Diff(str1, str2): # default str1 is longer
    # This function compares two different strings (with potentially different lengths)
    # and finds the length of the longest substring between them.

    if str1 == str2:
        return len(str1), [0, 0]  # If both strings are identical, the entire string is the longest substring.

    switched = False  # Flag to indicate whether the input strings were switched.
    strLong = str1    # The longer of the two input strings.
    strShort = str2   # The shorter of the two input strings.

    if len(str1) < len(str2):
        switched = True
        strLong = str2
        strShort = str1  # If str1 is shorter than str2, swap the variables.

    substrLenMax = 0   # Length of the longest substring.
    idLong = 0         # Starting index of the longest substring in the longer string.
    idShort = 0        # Starting index of the longest substring in the shorter string.

    lenShort = len(strShort)
    lenLong = len(strLong)

    # Iterate over the range of indices in the longer string to find substrings.
    for i in range(lenLong - 1):
        substrLen, iStart = LongestEqSubstr(strShort[:lenLong - i], strLong[i:i + lenShort])
        if substrLen > substrLenMax:
            substrLenMax = substrLen
            idShort = iStart
            idLong = iStart + i

    # Iterate over the range of indices in the shorter string to find substrings.
    for i in range(lenShort - 2):
        substrLen, iStart = LongestEqSubstr(strShort[lenShort - 2 - i:], strLong[:i + 2])
        if substrLen > substrLenMax:
            substrLenMax = substrLen
            idShort = iStart + lenShort - 2 - i
            idLong = iStart

    # Depending on whether the input strings were switched, return the result accordingly.
    if switched:
        return substrLenMax, [idShort, idLong]
    else:
        return substrLenMax, [idLong, idShort]



def LongestSubstr_Self(str0):
    # This function compares subsequences within the same string and finds the length of the longest common substring.

    lenstr = len(str0)
    ids = list(range(lenstr))
    maxLen, whereStart = 0, None

    # Iterate over the range of indices in the string to find subsequences.
    for i in range(1, lenstr - 1):
        str1, str2 = str0[:lenstr - i], str0[i:]
        id1, id2 = ids[:lenstr - i], ids[i:]

        eqs = [False] * len(str1)  # List to mark positions where characters are equal.
        eqStartEnd = []  # List to store the start and end positions of equal blocks.
        newEq = False

        # Iterate through each character and its index in str1 to find equal blocks.
        for ii, iEle in enumerate(str1):
            if iEle == str2[ii]:
                eqs[ii] = True
                if not newEq:
                    eqStartEnd.append([ii])
                newEq = True
            else:
                if newEq:
                    eqStartEnd[-1].append(ii)
                newEq = False
        
        # Handle the special case where the last character is part of an equal block.
        if len(eqStartEnd) > 0 and len(eqStartEnd[-1]) == 1:
            eqStartEnd[-1].append(len(str1))

        # Iterate through each equal block and resolve conflicts.
        for istart, iend in eqStartEnd:
            if maxLen < iend - istart:  # If there's no possibility of exceeding the current maxLen, skip.
                thisMaxLen = resolveEqConflict(id1[istart: iend], id2[istart: iend])
                if thisMaxLen > maxLen:
                    maxLen = thisMaxLen
                    whereStart = [istart, istart + i]  # [Starting position in the first sequence, starting position in the second sequence]

    return maxLen, whereStart


def resolveEqConflict(id1group, id2group):
    # This function resolves conflicts within the same string where equal subsequences overlap.
    # For example, in "ABABA", it should find the longest repeated "AB", not "ABA".

    maxLen = 0
    idsOccupied = [id2group[0]]  # List to store occupied id2 values (used as a standard, cannot use id1)
    broken = False #Used to determine whether a conflict has occurred

    # Iterate through the id1group to resolve conflicts.
    for k in range(1, len(id1group)):
        if id1group[k] in idsOccupied:  # Check if the id2 value is already occupied.
            maxLen = len(idsOccupied)
            broken = True
            break
        else:
            idsOccupied.append(id2group[k])  # Mark the id2 value as occupied.

    if not broken:  # If no conflicts were found (k reached the end without breaking).
        maxLen = len(id1group)

    return maxLen

    
    
    
def LongestSubstrList_Diff(strList1, strList2):
    # This function finds the longest substring between two lists of different strings.
    # It does not necessarily return the first longest substring encountered from left to right.

    maxSubstrLen = 0  
    posWanted = None   
    ijWanted = None    

    # Iterate through each string in strList1.
    for i, istr in enumerate(strList1):
        # Iterate through each string in strList2.
        for j, jstr in enumerate(strList2):
            # Find the longest substring and its position using the LongestSubstr_Diff function.
            SubstrLen, pos = LongestSubstr_Diff(istr, jstr)
            
            # Update the maximum substring length and related information if a longer substring is found.
            if SubstrLen > maxSubstrLen:
                maxSubstrLen = SubstrLen
                posWanted = pos
                ijWanted = [i, j]

    # Return the maximum substring length, its position, and the indices of the strings that produced it.
    return maxSubstrLen, posWanted, ijWanted



def LongestSubstrList_Self(strList0):
    # This function finds the longest substring in strList0.
    # It does not necessarily return the first longest substring encountered from left to right.

    maxSubstrLen = 0  
    posWanted = None   
    ijWanted = None   

    # Iterate through each string in the input list.
    for i, istr in enumerate(strList0):
        for j, jstr in enumerate(strList0):
            if i == j:
                # If the two strings are the same, use LongestSubstr_Self to find the longest substring.
                SubstrLen, pos = LongestSubstr_Self(istr)
            else:
                # If the two strings are different, use LongestSubstr_Diff to find the longest substring.
                SubstrLen, pos = LongestSubstr_Diff(istr, jstr)
            
            # Update the maximum substring length and related information if a longer substring is found.
            if SubstrLen > maxSubstrLen:
                maxSubstrLen = SubstrLen
                posWanted = pos
                ijWanted = [i, j]


    return maxSubstrLen, posWanted, ijWanted



def switchAB(A, B):
    # This function swaps the values of variables A and B.

    temp = A
    A = B
    B = temp
    return A, B


def getLevel(links, Level): 
    # This function computes which hierarchy the ladderon should belong to.

    levelComputed = -1
    # Iterate through each ladder ID in the links list.
    for ladderonID in links:
        thisLinkLevel = Level[ladderonID] # Get the level of the current ladder ID from the Level dictionary.
        if thisLinkLevel is None:
            return None
        else:
            if levelComputed < thisLinkLevel:
                levelComputed = thisLinkLevel
    return levelComputed + 1


# =====================================
class STRMAT(object):
    def __init__(self, strs):
        # This is the constructor method that initializes the attributes of the class.
        self.strs = None #  Stores the target system.
        self.Head = []   #  Stores the list of strings to be processed.
        self.ID = []     #  the IDs of each character in strMatHead, counted from left to right.
        self.Group = []  #  the group membership of each character in strMatHead (original sequence is 0, 1, 2...).
        self.maxGroup = len(strs) - 1  #  The maximum group number.
        self.targetBook = {} 
        self.ladderonBook = {}  # {ladderon: [Group, [UpperGroup1, iStart1, UpperGroup2, iStart2], ... ]
        self.ladderonBookLevel0 = {}  # Multiple sets of the most basic units
        self.ladderonBookDupsExtra = {} # The sequence of repeats in the original target system (Extra=n,if there are initially n+2 repeats)
        self.index3 = None  # (lambda, omega, S)
        self.POM = []  #  partially ordered multiset representation of ladderpath
        self.omega0Data   = (None, None, None)  # information about omega0,specific to single sequences(omega0, nBase, info)
        self.omegaMaxData = (None, None, None)  # information about omegaMax,specific to single sequences(omegaMax, nBase=None, info)
        self.eta = None  #  Order rate, calculated based on omega0Data and omegaMaxData.

        i = 0
        for k, str0 in enumerate(strs):
            self.Head.append([str0])
            self.ID.append( [list(range(i, i+len(str0)))] )
            self.targetBook[str0] = k
            i += len(str0)
            self.Group.append( [[k]*len(str0)] )
            
        self.compData = []  #  Initialize compData
        for i in range(len(strs)):
            self.compData.append([])
            for j in range(i+1):
                self.compData[i].append( [None,] )
                
                
    def updateCompData(self, ii, jj):
        # This method updates the compData list with information about the longest substring between two sequences.

        if ii == jj:
            # If the indices are the same, compare the sequence with itself using LongestSubstrList_Self.
            substrLen, posWanted, ijWanted = LongestSubstrList_Self(self.Head[ii])
        else:
            # If the indices are different, compare the sequences with each other using LongestSubstrList_Diff.
            substrLen, posWanted, ijWanted = LongestSubstrList_Diff(self.Head[ii], self.Head[jj])
        if substrLen < 2:
            # If the length of the common substring is less than 2, store a value of 0 in the compData list.
            self.compData[ii][jj] = [0,]
        else:
            # If the length of the common substring is 2 or more, store information about it in the compData list.
            self.compData[ii][jj] = [substrLen, posWanted, ijWanted]
            
            
    def splitStrs(self, ii, jj, DupInfo):
        # This method splits strings based on the duplication information (DupInfo) provided.
        substrLen = DupInfo[0]
        if ii == jj:
            if DupInfo[2][0] == DupInfo[2][1]: # If duplicate in the same strList and the same str
                strList, IDList, GroupList = self.Head[ii], self.ID[ii], self.Group[ii]
                iStart1 = DupInfo[1][0]
                iStart2 = DupInfo[1][1]
                if iStart1 > iStart2:
                    iStart1 = DupInfo[1][1]
                    iStart2 = DupInfo[1][0]
                newStrList, newIDList, newGroupList = [], [], []
               # Split the string and update data structures accordingly.
                for i in range(len(strList)):
                    if i == DupInfo[2][0]: # The duplicate found from the number of strings
                        str0splited, IDsplited, GroupSplited, dup, dupInfoComb = self.cut1str2spots(strList[i], IDList[i], GroupList[i], iStart1, iStart2, substrLen)
                        newStrList += str0splited
                        newIDList += IDsplited
                        newGroupList += GroupSplited
                        if dup in self.ladderonBook:
                            self.ladderonBook[dup].append(dupInfoComb[1])
                        else:
                            self.ladderonBook[dup] = dupInfoComb
                    else:
                        newStrList.append(strList[i])
                        newIDList.append(IDList[i])
                        newGroupList.append(GroupList[i])
                        
                # Update the class attributes with the new data.
                self.Head[ii] = newStrList
                self.ID[ii] = newIDList
                self.Group[ii] = newGroupList

            else:  #duplicate in same strList but in different str
                strList, IDList, GroupList = self.Head[ii], self.ID[ii], self.Group[ii]
                newStrList, newIDList, newGroupList = [], [], []
                iFirst, iSecond = 0, 1
                if DupInfo[2][0] > DupInfo[2][1]: # Deal with the first repetition first
                    iFirst, iSecond = 1, 0
                for i in range(len(strList)):
                    if i == DupInfo[2][iFirst]: # The duplicate found from the number of strings
                        str0splited, IDsplited, GroupSplited, dup, dupInfo = self.cut1str1spot(strList[i], IDList[i], GroupList[i], DupInfo[1][iFirst], substrLen, KeepDup=False)
                        newStrList += str0splited
                        newIDList += IDsplited
                        newGroupList += GroupSplited
                        self.add2ladderonBook(dup, dupInfo, True)
                    elif i == DupInfo[2][iSecond]:
                        str0splited, IDsplited, GroupSplited, _, dupInfo = self.cut1str1spot(strList[i], IDList[i], GroupList[i], DupInfo[1][iSecond], substrLen, KeepDup=True)
                        newStrList += str0splited
                        newIDList += IDsplited
                        newGroupList += GroupSplited
                        self.add2ladderonBook(dup, dupInfo, False)
                    else:
                        newStrList.append(strList[i])
                        newIDList.append(IDList[i])
                        newGroupList.append(GroupList[i])
                self.Head[ii] = newStrList
                self.ID[ii] = newIDList
                self.Group[ii] = newGroupList
        else:  # ii != jj:
            if ii > jj:
                ii, jj = switchAB(ii, jj)
                DupInfo[1][0], DupInfo[1][1] = switchAB(DupInfo[1][0], DupInfo[1][1])
                DupInfo[2][0], DupInfo[2][1] = switchAB(DupInfo[2][0], DupInfo[2][1])
            self.Head[ii], self.ID[ii], self.Group[ii], dup, dupInfo = self.cutFunction(self.Head[ii], self.ID[ii], self.Group[ii], substrLen, DupInfo[1][0], DupInfo[2][0], KeepDup=False)
            self.add2ladderonBook(dup, dupInfo, True)
            self.Head[jj], self.ID[jj], self.Group[jj], _, dupInfo = self.cutFunction(self.Head[jj], self.ID[jj], self.Group[jj], substrLen, DupInfo[1][1], DupInfo[2][1], KeepDup=True)
            self.add2ladderonBook(dup, dupInfo, False)
        return dup
    
    
    def add2ladderonBook(self, dup, dupInfo, firstHalf): # firstHalf表明是否新找到一个ladderon
        # This method adds information about a ladderon to the ladderonBook dictionary.

        if dup in self.ladderonBook:
            if firstHalf:
                # firstHalf indicates whether a new ladderon has been found
                self.ladderonBook[dup].append( [dupInfo[1], dupInfo[2]] )
            else:
                self.ladderonBook[dup][-1] += [ dupInfo[1], dupInfo[2] ]
        else:
            self.ladderonBook[dup] = [dupInfo[0], [dupInfo[1], dupInfo[2]] ]
             
    

    def calculatePOM(self):
        if len(self.POM) > 0:
            print('No need to run it again, as it has been calculated.')
        else:
            level0 = []
            for key, val in self.ladderonBookLevel0.items():
                level0.append( (key, val) )
            level0.sort(key=lambda y: (y[1], y[0]))
            pom = [level0]  # The final partially ordered multiset format, organized in layers. This is the first layer.
            if len(self.ladderonBook) == 0: # no ladderon is found
                self.POM = pom
            else:
                # ------ Calculate order information ------
                Id, Level, Links, Multiplicity = {}, {}, {}, {}
                for ladderon, val in self.ladderonBook.items():
                    ladderonID = val[0]
                    Id[ladderonID] = ladderon  # {5: 'ABDED', 6: 'ABD', 7: 'ED', 8: 'AB'}
                    Level[ladderonID] = None  # {5: None, 6: None, 7: None, 8: None}
                    Links[ladderonID] = []  # {5: [6, 7], 6: [8], 7: [], 8: []}
                    if ladderon in self.ladderonBookDupsExtra:
                        nExtra = self.ladderonBookDupsExtra[ladderon][1]
                    else:
                        nExtra = 0
                    Multiplicity[ladderonID] = len(val)-1 + nExtra # {5: 1, 6: 2, 7: 2, 8: 1}    
                
                temp = []  # List to store all ladderon IDs
                for val in self.ladderonBook.values():
                    temp.append(val[0])
                for ladderon, val in self.ladderonBook.items():
                    for upper1, _, upper2, _ in val[1:]:
                        if upper1 in temp and upper1 != val[0]:
                            Links[upper1].append(val[0])
                        if upper2 in temp and upper2 != val[0]:
                            Links[upper2].append(val[0])
                for key, val in Links.items(): # Determine the first layer
                    if len(val) == 0:
                        Level[key] = 1
                finished = False
                while not finished:
                    finished = True
                    for ladderonID, val in Level.items():
                        if val is None:
                            finished = False
                            levelComputed = getLevel(Links[ladderonID], Level)
                            if levelComputed is not None:
                                Level[ladderonID] = levelComputed
                for i in range(1, max(Level.values()) + 1):
                    level0 = []
                    for ladderonID, atlevel in Level.items():
                        if atlevel == i:
                            level0.append( (Id[ladderonID], Multiplicity[ladderonID]) )
                    level0.sort(key=lambda y: (y[1], y[0]))
                    pom.append(level0)
                self.POM = pom



    def getOmegaMaxData(self): # return (omegaMax, nBase=None, info)
        # This function only works for a single sequence
        # Calculate omega as omega_max in A string with all 'A' lengths as the length of this sequence
        if self.omegaMaxData[2] is None:
            st0 = self.strs[0]
            temp = bin(len(st0))[2:] # Calculate the omega_max of a sequence of length S
            lpIdx_most_ordered = len(temp) + temp.count('1') - 1
            omegaMax = len(st0) - lpIdx_most_ordered
            info = 'method_global: This omegaMax = omega of a string of A\'s of the same length'
            self.omegaMaxData = (omegaMax, None, info)
        return self.omegaMaxData
    def clearOmegaMaxData(self):
        # resets the OmegaMaxData attribute to a default state 
        self.omegaMaxData = (None, None, None)
    


    def getOmega0Data(self, nBase=None, DataFilePath='ladderpath_data_omega0/'): # return (omega0, nBase, info)
        # This function only works for a single sequence
        # Read omega_min from the data, using a purely random sequence as a baseline
        if self.omega0Data[2] is None:
            if nBase is None: # The number of categories of base must be told: nBase
                print('! Wrong: nBase has to be given.')
                return
            omega0 = None
            DataFilePath_new = DataFilePath + 'nBase' + str(nBase) + '/'
            datafiles = os.listdir(DataFilePath_new)
            _orderlist = []
            for filename in datafiles:
                temp = filename.split('.')[0][1:]
                try:
                    _orderlist.append(int(temp)) # Add all the serial numbers of the data file
                except:
                    pass
            if len(_orderlist) != 0:
                latestFile = 'v' + str(max(_orderlist)) + '.csv'
                minData = pd.read_csv(DataFilePath_new + latestFile)
                omega0 = float(minData[ minData['size']==len(self.strs[0]) ]['omega0'])
            if omega0 is None:
                print('omega0 data is not available.')
            else:
                info = 'method_global: This omega0 = omega of a random string with nBase. Data source: ' + DataFilePath_new + latestFile
                self.omega0Data = (omega0, nBase, info)
        return self.omega0Data
    def clearOmega0Data(self):
        self.omega0Data = (None, None, None)
    


    def getEta(self, nBase):
        # This function only works for a single sequence
        if len(self.strs) > 1:
            print('! Note that .getEta only works for a single sequence.')
            print('! But here you have multiple sequences. None returned.')
            return None
        else:
            # This method calculates the order rate. First, omegaMin and Max are calculated
            omegaMax = self.getOmegaMaxData()[0]
            if self.omega0Data[1] is None:
                omega0 = self.getOmega0Data(nBase=nBase)[0]
            else:
                if nBase == self.omega0Data[1]:
                    omega0 = self.omega0Data[0]
                else:
                    print('! Wrong: nBase is not the same with the saved data self.omega0Data(omega0, nBase, info)')
                    return
            if omegaMax == omega0:
                print('Warning: omegaMax = omega0, ill-defined.')
            else:
                self.eta = (self.index3[1] - omega0) / (omegaMax - omega0)
            return self.eta
        


    def dispPOM(self):
        # This method is used to display the partially ordered multiset information.
        if len(self.POM) == 0:
            print('Partially ordered multiset of the ladderpath has not been computed. Run self.calculatePOM()')
        else:
            print('{ ', end='')
            
            # Iterate over each level in the POM except the last one.
            for level in self.POM[:-1]:
                # Iterate over each ladderon and its multiplicity in the current level.
                for ladderon, m in level[:-1]:
                    if m == 1:
                        print(ladderon, ', ', sep='', end='')
                    else:
                        print(ladderon, '(', m, '), ', sep='', end='')
                m = level[-1][1]
                if m == 1:
                    print(level[-1][0], ' // ', sep='', end='')
                else:
                    print(level[-1][0], '(', m, ') // ', sep='', end='')
            level = self.POM[-1]
            for ladderon, m in level[:-1]:
                if m == 1:
                    print(ladderon, ', ', sep='', end='')
                else:
                    print(ladderon, '(', m, '), ', sep='', end='')
            m = level[-1][1]
            if m == 1:
                print(level[-1][0], sep='', end='')
            else:
                print(level[-1][0], '(', m, ')', sep='', end='')
            print('}')

    def disp3index(self):
        # This method is used to display and return the 3-index information. 
        print('( Ladderpath-index:', self.index3[0], ',  Order-index:', self.index3[1], ',  Size-index:', self.index3[2], ' )', sep='')
        return self.index3


    def laddergraph_single(self, filename = "G", show_longer_than = 1, style = "ellipse", target_name = "", color = "#808080"):
        # Draw the laddergraph. This function currently only works when the target is a single sequence.
        # "filename" is the file name of the figure.
        # "show_longer_than": When the length of the ladderon > show_longer_than, this ladderon will be displayed.
        #     Note that "show_longer_than" should always be >= 1, and the basic building blocks are also omitted.
        # "style" dictates how the laddergraph is displayed. It can either be "ellipse" (the sequence won't be displayed, 
        #     but the size of the ellipse is positively related to the length of the sequence) 
        #     or "box" (the sequence will be displayed).
        # "target_name" is the text displayed in the target sequence.
        
        binfo = self.ladderonBook
        if binfo == {}:
            print('The required information has not been calculated.')
            print('Most likely, you set CalPOM=False in the function ladderpath.ladderpath(strs, CalPOM=False).')
            print('You could set CalPOM=True, and then draw laddergraph.')
        else:
            seq = self.strs[0] # This function currently only works when the target is a single sequence 
            
            # initialize the graph
            g = graphviz.Digraph('Laddergraph/{}'.format(filename), format = 'png')  
            
            if style == "box":
                # a detailed version, showing ladderons length
                g.attr('node', shape='box')
                g.node('0',label = seq)
            else: # style == "ellipse":
                length = np.sqrt(len(seq))/3
                # a wholistic view of ladder-graph
                g.attr('node', shape='ellipse', style = 'filled')
                g.node('0',label = target_name, **{'width':str(length),'height':str(length/2),'fontsize':'50'}, color = color)


            for key,value in binfo.items():
                
                dict_temp = dict()
                for splice in value[1:]:

                    if len(key) > show_longer_than:

                        if style == "box":
                            g.node(str(value[0]), label = str(key))
                        else:
                            lenk = np.sqrt(len(key))/3
                            g.node(str(value[0]),label = "", **{'width':str(lenk),'height':str(lenk/2)}, color = color)

                        for position in splice[::2]:
                            if position == value[0]:
                                pass
                            else:
                                val,pos = str(value[0]),str(position)
                                dict_temp[val,pos] = dict_temp.get((val,pos),0) + 1

                if style == "box":
                    for vp,times in dict_temp.items():
                        if times > 1:
                            g.edge(vp[0],vp[1],label = str(times))
          
                        else:
                            g.edge(vp[0],vp[1])
                else: # style == "ellipse":
                    for vp,times in dict_temp.items():
                        g.edge(vp[0],vp[1],**{'weight':str(times)}, color = color)
            g.view()



    # =================== Internal function ======================
    def comp3index(self):
        # Calculate the 3-index information.
        sizeIndex = 0
        for block in self.targetBook.keys():
            sizeIndex += len(block)
        if len(self.ladderonBook) == 0:
            self.index3 = (sizeIndex, 0, sizeIndex)
            return

        for ladderon, val in self.ladderonBook.items(): # {ladderon: [Group, [UpperGroup1, iStart1, UpperGroup2, iStart2], ... ]
            if val[1][1] is None: # This is when there are duplicates in the original target system{ladderon: [Group, [Group, None, Group, None], ...]}
                sizeIndex += len(ladderon)
        if len(self.ladderonBookDupsExtra) > 0:
            for dup, val in self.ladderonBookDupsExtra.items():
                sizeIndex += len(dup) * val[1]

        orderIndex = 0
        for ladderon, val in self.ladderonBook.items():
            orderIndex += (len(ladderon)-1) * (len(val)-1)
        if len(self.ladderonBookDupsExtra) > 0:
            for dup, val in self.ladderonBookDupsExtra.items():
                orderIndex += (len(dup)-1) * val[1]

        ladderpathIndex = sizeIndex - orderIndex
        self.index3 = (ladderpathIndex, orderIndex, sizeIndex)


    def cutFunction(self, strList, IDlist, Grouplist, substrLen, iStart, ipos, KeepDup):
        # Cut a substring from the given string list and update the corresponding lists.

        # iStart：From which position of str to repeat; ipos: Which string in the strList is being processed, e.g.
        # strList = strMatHead[ii]
        # iStart = DupInfo[1][0]
        # ipos = DupInfo[2][0]
        newStrList, newIDList, newGroupList = [], [], []
        for i in range(len(strList)):
            if i == ipos: # The duplicate found from the number of strings
                str0splited, IDsplited, GroupSplited, dup, dupInfo = self.cut1str1spot(strList[i], IDlist[i], Grouplist[i], iStart, substrLen, KeepDup)
                newStrList += str0splited
                newIDList += IDsplited
                newGroupList += GroupSplited
            else:
                newStrList.append(strList[i])
                newIDList.append(IDlist[i])
                newGroupList.append(Grouplist[i])
        return newStrList, newIDList, newGroupList, dup, dupInfo


    def cut1str1spot(self, str0, ID0, Group0, iStart, substrLen, KeepDup):
        str0splited, IDsplited, GroupSplited = [], [], []
        # Append the substring before the duplicated block (if any) to the new lists.
        if iStart > 1: # If it is a single character, it is not recorded
            str0splited.append(str0[:iStart])
            IDsplited.append(ID0[:iStart])
            GroupSplited.append(Group0[:iStart])
        # Extract the duplicated block and its associated information.
        dup = str0[iStart : iStart+substrLen]
        if dup in self.ladderonBook:
            dupInfo = [self.ladderonBook[dup][0], Group0[iStart], ID0[iStart]]
        else:
            self.maxGroup += 1
            dupInfo = [self.maxGroup, Group0[iStart], ID0[iStart]]
        if KeepDup:
            str0splited.append(dup)
            IDsplited.append(ID0[iStart : iStart+substrLen])
            GroupSplited.append( [ dupInfo[0] ]*substrLen )
                
        if iStart + substrLen < len(str0) - 1: # If it is a single character, it is not recorded
            str0splited.append(str0[iStart + substrLen :])
            IDsplited.append(ID0[iStart + substrLen :])
            GroupSplited.append(Group0[iStart + substrLen :])
        return str0splited, IDsplited, GroupSplited, dup, dupInfo


    def cut1str2spots(self, str0, ID0, Group0, iStart1, iStart2, substrLen):
        str0splited, IDsplited, GroupSplited = [], [], []
        if iStart1 > 1: # If it is a single character, it is not recorded
            str0splited.append(str0[:iStart1])
            IDsplited.append(ID0[:iStart1])
            GroupSplited.append(Group0[:iStart1])
        dup = str0[iStart1 : iStart1+substrLen]
        if dup in self.ladderonBook:
            dupInfoComb = [self.ladderonBook[dup][0], [Group0[iStart1], ID0[iStart1]] ]
        else:
            self.maxGroup += 1
            dupInfoComb = [self.maxGroup, [Group0[iStart1], ID0[iStart1]] ]
        
        if iStart1 + substrLen < iStart2 - 1:
            str0splited.append(str0[iStart1 + substrLen : iStart2])
            IDsplited.append(ID0[iStart1 + substrLen : iStart2])
            GroupSplited.append(Group0[iStart1 + substrLen : iStart2])

        str0splited.append(dup)
        IDsplited.append(ID0[iStart2 : iStart2+substrLen])
        GroupSplited.append( [ dupInfoComb[0] ]*substrLen )
        dupInfoComb[1] += [Group0[iStart2], ID0[iStart2]]

        if iStart2 + substrLen < len(str0) - 1: # If it is a single character, it is not recorded
            str0splited.append(str0[iStart2 + substrLen :])
            IDsplited.append(ID0[iStart2 + substrLen :])
            GroupSplited.append(Group0[iStart2 + substrLen :])
        return str0splited, IDsplited, GroupSplited, dup, dupInfoComb

    

# =====================================
def ladderpath(strsInput, CalPOM=True):
# strsInput = ['ABCAB', 'BACAX', 'BACAX'] or strsInput = {'ABCAB': 2, 'BACAX': 1, 'BACAX': 1}
    hasDup = False # Indicates whether there are duplicates in the target component
    if type(strsInput) == list:
        countStrs = {}  # Stores the number of each target component in the target system
        for str0 in strsInput:
            if str0 in countStrs:
                hasDup = True
                countStrs[str0] += 1
            else:
                countStrs[str0] = 1
        if hasDup:
            strs = list(countStrs.keys())
        else:
            strs = strsInput
    elif type(strsInput) == dict:
        countStrs = strsInput
        strs = list(strsInput.keys())
        if max(strsInput.values()) > 1:
            hasDup = True
    else:
        print('Error: the type of strs is wrong, must be list or dict.')
        return

    strMat = STRMAT(strs)
    # First pick out the repetitive structures in the original target system
    if hasDup: # If the target component already has a duplicate
        for block, ndup in countStrs.items():
            if ndup > 1:
                Group = strMat.targetBook[block]
                strMat.ladderonBook[block] = [Group, [Group, None, Group, None]]
                strMat.ladderonBookDupsExtra[block] = [Group, ndup-2]
        strMat.strs = strs
    else:
        strMat.strs = strs

    # The following program can already handle a distinct target system of strings. Primary program:
    lenStrs = len(strs)
    for i in range(lenStrs):
        for j in range(i+1):
            #Initialize compData to record the maximum number of duplicate substrings
            strMat.updateCompData(i, j)

    maxLen = 1
    while maxLen > 0:
        maxLen = 0
        imax, jmax = 0, 0
        for i in range(lenStrs): # Finds the length of the longest repeating substring
            for j in range(i+1):
                if maxLen < strMat.compData[i][j][0]:
                    maxLen = strMat.compData[i][j][0]
                    imax, jmax = i, j
        if maxLen > 0:
            thisDupInfo = strMat.compData[imax][jmax]
                # thisDupInfo means: repeat sequence length, (the same starting position in the sequence), (between the number of subsequences in the sequence)
            strMat.splitStrs(imax, jmax, thisDupInfo)

            if imax > jmax: #Make sure imax is smaller than jmax 
                temp = imax
                imax = jmax
                jmax = temp
            for k in range(imax): # row in All comparisons
                strMat.updateCompData(imax, k)
            for k in range(imax, lenStrs):
                strMat.updateCompData(k, imax) 

            for k in range(jmax): # column in All comparisons
                if k != imax:
                    strMat.updateCompData(jmax, k)
            for k in range(jmax, lenStrs):
                strMat.updateCompData(k, jmax) 
    
    # ------ Computes information about Level 0 ------
    countLetters0 = {} # in the original blocks0, the number of each letter
    for target0 in strMat.targetBook.keys():
        if target0 in strMat.ladderonBookDupsExtra: #Extra when there is an initial duplication
            nExtra = strMat.ladderonBookDupsExtra[target0][1] + 1 #Only there's one more
        else:
            nExtra = 0
        for x in target0:
            if x in countLetters0:
                countLetters0[x] += 1 + nExtra
            else:
                countLetters0[x] = 1 + nExtra

    Multiplicity = {}
    countLetters = {} # among all the ladderons, the number of each letter
    for ladderon, val in strMat.ladderonBook.items():
        if ladderon in strMat.ladderonBookDupsExtra:
            nExtra = strMat.ladderonBookDupsExtra[ladderon][1]
        else:
            nExtra = 0

        ladderonId = val[0]
        Multiplicity[ladderonId] = len(val) - 1 + nExtra  # {5: 1, 6: 2, 7: 2, 8: 1}  
        for x in ladderon:
            if x in countLetters:
                countLetters[x] += Multiplicity[ladderonId]
            else:
                countLetters[x] = Multiplicity[ladderonId]

    for key, val in countLetters0.items(): # Level 0, multiple sets of the underlying components
        if key in countLetters:
            strMat.ladderonBookLevel0[key] = val - countLetters[key]
        else:
            strMat.ladderonBookLevel0[key] = val

    strMat.comp3index()
    if CalPOM:
        strMat.calculatePOM()

    return strMat