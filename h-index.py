my_list = [33, 99, 22, 14, 6, 2, 2, 0, 1, 15, 9, 11]
my_list.sort(reverse=True)
def get_h_index():
    my_dict = {}
    count = 0
    for i in my_list:
        count +=1
        my_dict[count] = i
    h_list= []
    for key in my_dict.keys():
        if key <= my_dict[key]:
            h_list.append(key)
    h_index = ("h-index is: " + str(h_list[-1]))
    return(h_index)
