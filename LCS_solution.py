
class ComSubstr (object):


    '''
    Calulate lcs, return size of lcs
    '''
    def comSubstring(self, str1, str2):
        l1 = len(str1)
        l2 = len(str2)
        lcs = []
        for i in range(l1 + 1):
            lcs.append([0] * (l2 + 1))
        for i in range(1, l1 + 1):
            for j in range(1, l2 + 1):
                if (str1[i - 1] == str2[j - 1]):
                    lcs[i][j] = lcs[i - 1][j - 1] + 1
                elif str1[i - 1] != str2[j - 1]:
                    lcs[i][j] = max(lcs[i][j - 1], lcs[i - 1][j])

        # for i in range(1, l1 + 1):
        #     for j in range(1, l2 + 1):
        #         print str(lcs[i][j]) + ",",
        #     print("\n")


        max_len = lcs[l1][l2]
        i, j = l1, l2
        comStr = [""] * max_len
        while max_len > 0 and i >= 0 and j >= 0:
            if (lcs[i][j] != lcs[i - 1][j - 1]):
                if (lcs[i - 1][j] == lcs[i][j - 1]):
                    comStr[max_len - 1] = str1[i - 1]
                    max_len -= 1
                    i -= 1
                    j -= 1
                else:
                    if (lcs[i-1][j]>lcs[i][j-1]):
                        i -= 1
                    else:
                        j -= 1

            else:
                i -= 1
                j -= 1

        # print ("Common substring is:")
        # print (comStr)
        # print ("Size is:")
        # print (len(comStr))
        return len(comStr)

if __name__ == "__main__":
    c = ComSubstr()
    s1 = "dasdasdasd"
    s2 = "djasiofhsdiofhsoifeiuhfuivdfuvbdskj"
    c.comSubstring(s1, s2)