backgroundPicture = 'scene1.jpg'
lane = 127
lane_start = 15
maxRow = 32
maxColumn = 6
prop = 30
rows = [0,41,73,101,132,161,191,220,250,280,312,340,369,398,426,466,499,533,562,589,618,652,679,708,737,768,799,830,859,889,917,950,976]
columns = [0,50,76,100,150,172,196]
seatsUsed = []
rowBusy = []


def initialize():
    for i in range(33):
        seatsUsed.append([False,False,False,False,False,False,False])
    seatsUsed[1][1] = seatsUsed[1][2] = seatsUsed[1][3] = True

initialize()
print("Scene 1 Loaded!")