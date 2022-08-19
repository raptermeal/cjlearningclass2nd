def find_nav(save_list_add):
    # save_list_add =         [0.669,	0.873,	3.205,
    #     0.65,	0.117,	3.949,
    #     0.158,	0.098,	1.557,
    #     0.205,	0.594,	1.301,
    #     0.878,	0.685,	3.583] # 1 | attention


    # print(save_list_add[0])
    a = [save_list_add[2],save_list_add[5],save_list_add[8],save_list_add[11],save_list_add[14]]

    smallest = a[0]

    for i in a:
        if i < smallest:
            smallest = i
            
            
    # print(i,smallest)
    # print(min(a))
    # print(a.index(min(a)))

    # print(3*(a.index(min(a)) + 1)-3,3*(a.index(min(a)) + 1)-2,3*(a.index(min(a)) + 1)-1)

    if save_list_add[3*(a.index(min(a)) + 1)-3] > 0.5:
        xxx='right'
    else:
        xxx='left'
        
    if save_list_add[3*(a.index(min(a)) + 1)-2] > 0.5:
        yyy='up'
    else:
        yyy='down'

    # print(xxx,yyy,str(round(min(a),1))+'meter')
    # left up 1.3meter
    return xxx,yyy,str(round(min(a),1))+' meters'