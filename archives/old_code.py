# writing out to a file in a pretty way

print(groups_score[0][1])

with open("fake_team.txt", "w") as f:
  f.write(">>> This team had the highest score of {:>50} <<<\n".format(sum(groups_score[0][1])))
  f.write(">>> This team had a content similarity score of {:>50} <<<\n".format(groups_score[0][1][0]))
  f.write(">>> This team had a time window score of {:>50} <<<\n".format(groups_score[0][1][1]))
  f.write(">>> This team had a group early time frame score of {:>50} <<<\n".format(groups_score[0][1][2]))
  for product, reviews in groups_score[0][0]:
    f.write("-"*20+"Product: "+product+"-"*20+"\n")
    for review in reviews:
      f.write(review["reviewText"]+"\n\n")
