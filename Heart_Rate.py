import cv2
import multiprocessing
from PIL import Image , ImageStat
import os


class Heart_Rate():
    from matplotlib import pyplot
    # use python 2.7

    def video_capture(self):
        video = cv2.VideoCapture('Heart_Sample.MOV')
        c=1

        if video.isOpened():
            rval , frame = video.read()
        else:
            rval = False

        while rval:
            rval, frame = video.read()
            cv2.imwrite('images/ ' + str(c) + '.jpg',frame)
            c = c + 1
            cv2.waitKey(1)
        video.release()


    global brigtness



    def find_brightness(i):
        i = int(i)
        global brightness


        img = Image.open('images/ ' + str(i) + '.jpg').convert('RGBA')
        stat = ImageStat.Stat(img)


        return (stat.mean[0])




    def find_all_dips(self):
        global brigthness
        dips= []
        for i in range(1, len(brigthness)-1):

             if(brigthness[i-1] > brigthness[i] and brigthness[i+1] > brigthness[i]):
                 dips.append(brigthness[i])
        return dips
    def find_big_dips(self):
        global brigthness
        dips= []
        for i in range(1, len(brigthness)-1):
            a = False
            for j in range(1,10):
                if(i-j < 0):
                    if (brigthness[0] > brigthness[i] and brigthness[i + j] > brigthness[i]):
                        a = True
                    else:
                        a = False
                        break
                elif(i+j >= len(brigthness)):
                    if (brigthness[i - j] > brigthness[i] and brigthness[len(brigthness)-1] > brigthness[i]):
                        a = True
                    else:
                        a = False
                        break
                else:
                    if(brigthness[i-j] > brigthness[i] and brigthness[i+j] > brigthness[i]):
                     a = True
                    else:
                        a = False
                        break


            if(a == True):
                dips.append(brigthness[i])
        return dips
    def main(self):
        self.video_capture()

        counter = 0
        for e in os.listdir('images'):
            if ('.jpg' in e):
                counter += 1

        counter -=1
        print counter
        pool = multiprocessing.Pool(processes=8)

        result = pool.map(self.find_brightness, (('%d' % i) for i in range(1,counter)))
        brigthness = result
        max_val = 0
        min_val = 255
        for i in range(len(brigthness)):
            if(brigthness[i] < min_val):
                min_val = brigthness[i]
            if(brigthness[i]> max_val):
                max_val = brigthness[i]
            print(str(i ) + '  :  '+ str(brigthness[i]))
        print ("min : " + str(min_val))
        print ("max : " + str(max_val))
        for i in range(len(brigthness)):
            brigthness[i] -= min_val
            tmp = max_val-min_val
            brigthness[i] *= 100/tmp
            print(str(i) + '  :  ' + str(brigthness[i]))

        dips = len(self.find_big_dips())
        print dips

        duration = ((counter+1) / 29)
        print duration
        bpm = dips*(60/duration)
        print bpm

    # pyplot.plot(brigthness)
    # pyplot.show()




