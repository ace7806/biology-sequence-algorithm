import csv
import sys

gapPenalty = -2
matchScore = 1
mismatchScore = -1



def initialize_matrix(a,b):
    '''initializes and populates matrix appropiatly'''
    m = len(a)+1
    n = len(b)+1
    arr = [ [ 0 for x in range(m) ] for x in range(n) ]
    for j in range(m): arr[0][j] = j*gapPenalty 
    for i in range(n): arr[i][0] = i*gapPenalty

    for i in range(1,n):
        for j in range(1,m):
            score = max(scoreMatrix(arr,a,b,i,j))
            arr[i][j] = score 
    return arr


def scoreMatrix(arr,S1,S2,i,j):
    '''takes in matrix (arr), both string sequences(S1,S2) and position your currently at (i,j),
        and calculates scores for the diagonal, left and above element respectively'''
    matchingStringScore = matchScore if (S2[i-1]==S1[j-1]) else mismatchScore
    return (arr[i-1][j-1] + matchingStringScore ,arr[i][j-1] + gapPenalty, arr[i-1][j] + gapPenalty)



def print_arr(arr):
    for x in arr: print(x)

def backtrack(arr,a,b):
    alignmentA = ''
    alignmentB = ''
    i = len(b)
    j = len(a)
    while i > 0 or j>0:
        '''grabs the score of its diagonal, left and above element and merges equal scores in sequence
            so it complys with backtracking rule of choosing which direction to go'''
        scores = scoreMatrix(arr,a,b,i,j)
        mergedScores = {scores[i]:i for i in range(len(scores))}
        gate = mergedScores[max(scores)]
        if gate==0: #diagonal
            alignmentA = a[j-1] + alignmentA
            alignmentB = b[i-1] + alignmentB
            i-=1
            j-=1
        elif gate==1: #left
            alignmentA = a[j-1] + alignmentA
            alignmentB = '-' + alignmentB
            j-=1
        else: #above
            alignmentA = '-' + alignmentA
            alignmentB = b[i-1] + alignmentB
            i-=1
    return alignmentA,alignmentB,arr[-1][-1]

if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as file:
        csvreader = list(csv.reader(file))[1:]
        for row in csvreader:
            arr = initialize_matrix(row[0],row[1])
            Sequence1,Sequence2,Score =  backtrack(arr,row[0],row[1])
            print(Sequence1,Sequence2,Score)
            