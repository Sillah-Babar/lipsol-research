# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import glob


def makePath(datapath,rangee):
    new_path=''
    for i in range(rangee):
        new_path+=datapath[i]+'\\'


    return new_path


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path=r'D:\Downloads\dataset\13\13\*\*'
    vid_count=1
    align_count=1
    count=1

    for video_path in glob.glob(path):
        datapaths=video_path.split('\\')

        # print(datapaths)
        # print(datapaths[6])
        # new_path=datapaths[6].split('.')
        if(datapaths[6]=='align'):
           print(video_path)
           #print(video_path)
           with open(video_path,'r',encoding="utf-8") as file:
               for item in file:
                   item=item.strip()
                   new_array=item.split(' ')
                   print(new_array)

                   if(len(new_array)>5):

                       if new_array[0]== 'چھے':
                           new_array[0]='چھ'
                       if new_array[0] == 'نوں':
                           new_array[0] = 'نو'
                   new_str=""
                   print(len(new_array))
                   for i in range(len(new_array)):
                        if(new_array[i]==''):
                            new_str+=" "
                        else:
                            new_str+=new_array[i]
                   print(new_str)
                   new_str+='\n'
                   # #print(new_array)
                   # check=False
                   # word_array=new_array[0].split('  ')
                   # for i in range(len(roman_urdu)):
                   #      if(word_array[0]==roman_urdu[i]):
                   #          word_array[0]=data_into_list[i]
                   #          if(len(new_array)==2):
                   #              new_string+=word_array[0]+" "+word_array[1]+" "+new_array[1]+'\n'
                   #
                   #              check=True
                   # if (len(new_array) == 2 and check==False):
                   #      new_string += new_array[0] + " " + new_array[1]+"\n"
                   #
                   #
                   # print("new_String: ",new_string)
                   newarr=makePath(datapaths, 6)
                   new_ap=newarr+str(count)+'.txt'
                   print(new_ap)
                   # print(new_ap)
                   file = open(new_ap, "a",encoding='utf-8')
                   a = file.write(new_str)
               file.close()
           count += 1
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
