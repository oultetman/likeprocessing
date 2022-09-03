def list_to_2d_list(one_d_liste:list,nb_elements=2)->list[list]:
    if len(one_d_liste)%nb_elements != 0:
        raise Exception(f"Invalid format list: len(list) = {len(one_d_liste)} not multiple of {nb_elements}")
    two_d_list =[]
    for i in range(0,len(one_d_liste)-nb_elements+1,nb_elements):
        l = []
        for j in range(nb_elements):
            l.append(one_d_liste[i+j])
        two_d_list.append(l)
    return two_d_list

if __name__ == '__main__':
    l= [1,2,3,4,5,6,7,8,9,10,11,12]
    print(list_to_2d_list(l))
    print(list_to_2d_list(l,3))
    print(list_to_2d_list(l, 5))