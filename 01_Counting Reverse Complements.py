####################
# Helper Functions #
####################

# Create i-th quaternary string of length n
def intToQuat(integer,length):
    quatString = ""
    for i in range(length):
        place = integer//(4**(length-i-1))
        quatString += str(place)
        integer -= (4**(length-i-1))*place
    return quatString

# Return reverse-complement
def quatToRC(string):
    RCstrand = ""
    for i in range(len(string)):
        RCstrand += str((int(string[i])+2)%4)
    return(RCstrand[::-1])

# Return number of unique letters in the strand
def numUniqueLetters(string):
    letters = set()
    for i in range(len(string)):
        letters.add(string[i])
    return len(letters)
        

############################################################
# The base code for finding strands counted by r_{n,delta} #
############################################################

# Range over all desired strand lengths (n)
for n in range(3,6):
    # Range over the possible maximal r-c lengths (delta)
    for delta in range(1,n//2+1):
        # count is for individual choice of n and delta, will reset if either iterates
        count = 0

        # Check all possible quaternary strands of length n
        for number in range(4**n):

            # Convert number to n-length quaternary strand
            strand = intToQuat(number,n)

            # flagA is set to TRUE if a strand is found to have a delta-length reverse-complement
            flagA = False
            # flagB is set to FALSE if a strand is found to have a delta+1-length reverse-complement
            flagB = True

            # kmers holds all the k-length windows in the strand. Even if there are repeats, we care about where they occur.
            kmers = []
            for index in range(n-delta+1):
                kmers.append(strand[index:index+delta])
            # Check if r-c is in kmers and no overlap
            for index in range(n-delta+1):
                # Find the r-c of the current strand
                strandRC = quatToRC(strand[index:index+delta])
                # Check if it's in kmers...
                if strandRC in kmers:
                    # ... and then check if the r-c overlaps with the strand
                    for i in range(n-delta+1):
                        # If the r-c both exists and does not overlap...
                        if strandRC == kmers[i] and i >= index + delta:
                            # flagA is set to TRUE and we don't need to check the rest of the strand.
                            flagA = True
                            break
        
            # If a strand was found to have a delta r-c, we check for a delta+1 r-c.
            if flagA:
                # Same process as above...
                kmers = []
                for ind in range(n-delta):
                    kmers.append(strand[ind:ind+delta+1])
                for ind in range(n-delta):
                    strandRC = quatToRC(strand[ind:ind+delta+1])
                    if strandRC in kmers:
                        for i in range(n-delta):
                            if strandRC == kmers[i] and i >= ind + delta+1:
                                # Except if we find a delta+1 r-c, we don't want to count this strand, so flagB is set to FALSE
                                flagB = False
                                break
                        # Break out of the outer loop as well if we've found a delta+1 r-c 
                        if not flagB:
                            break

            # Only those strands that do have a delta r-c (flagA) but do not have a delta+1 r-c (flagB) are counted
            if flagA and flagB:
                count+=1
        print("For n equal to " + str(n) + " and Delta equal to " + str(delta) + " the count is " + str(count)) 

