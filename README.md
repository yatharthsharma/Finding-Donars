Insight Data Engineering Coding Challenge

Language used : Python, Version - 2.7.6
Tested on Ubuntu 16.04

# Execution Time:

1. Input size = 10 records , time taken: 0.005 secs
2. Input size = 242890 records, time taken: 2.31 secs
3. Input size = 1976566, time taken : 11.89 secs


How to Run: ./run.sh

# Table of Contents

1. [Data Structure](README.md#Data-Structure)
2. [Implementation Details](README.md#Implementation-Details)

# Data Structure

    The following Data Structures were used:
    *   Hash: TO store all the unique cmte+zip and cmte+date combinations

        hash[cmte] = {
                        {zipCode:{"minH": [],"maxH": [],"nTrans":0,"tAmt": 0},
                        {dateCode: {"median":[],"nTrans":0,"tAmt": 0,"date":0} 
                    } 

    * Heap - MinHeap, MaxHeap for calculting the running median



# Implementation Details

    Main driver code can be found in find_political_donors.py. The code can be divided into 2 calculations

    * MedianValBy_Zip
    * MedianValBy_Date    


1. medianVal by Zip:
    
    In order to calculate the running median value by CMTE ID and ZipCode, 2 heaps were used per CMTE ID and ZipCode combination. While iterating through the input file, the transaction amount was added to the heap based on the following algorithm:

    * if the transaction amount < the median, add it to the max heap,
    * if the transaction amount > the median, add it to the min heap,
    * make sure to maintain the size difference between the heap atmost 1
    * median is the average of the min and max heap if the size is same, else pick the value from the bigger heap

    This algorithm insures that we can get the running median in  o(1) time. Moreover, the adding to head take o(logn) which is quite fast

    * Other things that were tried but didn't give better performance:
        1. Maintaining a sorted array while inserting every new element. Took a lot of time (used bisect library)
        2. using a trie to store the value of key, Hashing using current dictionary had better performance

2. medianVal by Date:

    In order to calculate the median by CMTE ID and Date while also maintainin the sorted order, a hash as follows:

    * change date from mmddyyyy to yyyymmdd (this will make sure the date is sorted in chronological order)
    * create a hash with key as  cmteID+Date (in yyyymmdd format)
    * appen median values in another hash which is by cmte id and date  (see definition in Data Structure topic)
    * sort the hash key and while traversing the sorted hash key, sort median array
    * get the median


    * Other things that were tried but didn't give better performance:
        1. Used heap as in part 1, but performance was not good
        2. used tries to store the key as it will be automatically sorted while doing traversal, but poor performance

# Output

You can see the output files, medianvals_by_zip.txt and medianvals_by_date.txt in the output folder
