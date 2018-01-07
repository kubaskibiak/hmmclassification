from pytube import YouTube


def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

content=[]
with open('filmyNowe3IN.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]
# not necessary, just for demo purposes.
from pprint import pprint
videoToDwownload={}

counter=89
file = open('filmyNowe3OUT.txt','w')
# for i in content:
#     start = i.find('href{') +5
#     stop = start + 43
#     print(i[start:stop])
#
#     start2=findnth(i,'&',4) +1
#     print()
#     stop2=i.find('hline')
#     print (start2)
#     videoToDwownload.update({i[start:stop] : i[start2:stop2].strip()})
#
#     yt = YouTube(i[start:stop])
#
#     yt.set_filename('video_'+str(counter)+"_"+i[start2:stop2].strip())
#
#     file.write('set '+ 'films_table'+'['+str(counter)+'].Name'+ '='+'video_'+str(counter)+"_"+i[start2:stop2].strip()+'.mp4' + '\n')
#     file.write('set ' + 'films_table' + '[' + str(counter) + '].Class' +'='+ i[start2:stop2].strip()+ '\n')
#     video= yt.filter('mp4')[-1]
#
#
#     video.download('downloadedYT')
#     counter+=1
#
#
# file.close()

for i in content:
    start = 0
    stop = 60
    print(i[start:stop])

    start2=67
    print(start2)
    stop2=68
    print(i[start:stop] +  i[start2:stop2].strip())
    videoToDwownload.update({i[start:stop] : i[start2:stop2].strip()})

    yt = YouTube(i[start:stop])

    yt.set_filename('video_'+str(counter)+"_"+i[start2:stop2].strip())

    file.write('set '+ 'films_table'+'['+str(counter)+'].Name'+ '='+'video_'+str(counter)+"_"+i[start2:stop2].strip()+'.mp4' + '\n')
    file.write('set ' + 'films_table' + '[' + str(counter) + '].Class' +'='+ i[start2:stop2].strip()+ '\n')
    video= yt.filter('mp4')[-1]


    video.download('downloadedYT')
    counter+=1


file.close()

