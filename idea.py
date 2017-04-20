users = [("U1" , ['A', 'B', 'C', 'D', 'E', 'F']),   
         ("U2" , ['A', 'B', 'C']               ),
         ("U3" ,                ['D', 'E', 'F']),
         ("U4" ,           ['C', 'D', 'E']     ),
         ("U5" , ['A', 'B', 'C']               )]


def group_users(users):
   groups = {}
   for i in range(len(users)-1):
      for j in range(i+1,len(users)):
         common_products = list(set(users[i][1]).intersection(set(users[j][1])))
         if len(common_products) >= 3:
            key = "".join(sorted(common_products))
            if key in groups:
               if users[j][0] not in groups[key]:
                  groups[key].append(users[j][0])
            else:
               groups[key] = [users[i][0], users[j][0]]
   print(groups)

group_users(users)