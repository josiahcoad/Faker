from __future__ import print_function
with open("scores.txt") as f:
   all_scores = eval(f.read())

def curve(x, minn, maxx):
   return (x-minn/)

mins = []
maxs = []
for i in range(8):
   mins.append( min(score_list[i] for score_list in all_scores) )
   maxs.append( max(score_list[i] for score_list in all_scores) )


