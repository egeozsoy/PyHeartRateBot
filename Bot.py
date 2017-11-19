import telegram
import telegram.ext
from telegram.ext import Updater
from telegram.ext import messagehandler
from telegram.ext import CommandHandler
import logging
import time
from PIL import Image


bot = telegram.Bot(token = '359232501:AAE9aLujYtNzHrhGZJeRwdHBT-urJdxHGsg')
#print(bot.getMe())



def start(bot, update):

    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


updater = Updater(token = '351083444:AAFwqjMx8s_s6ZfjWCdup3rAhLaIUmcu3cA')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)






start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


#updater.start_polling()
offset = 0
updates = []
while(True):

        if (len(updates) > 0):



            offset = bot.getUpdates()[-1].update_id + 1
            # to reset
            # updates = bot.getUpdates(offset=offset)

            for u in updates:


                # offset = bot.getUpdates()[-1].update_id + 1
                if (u.message.text == '/start'):
                    start(bot, u)
                elif (u.message.video):

                    file_id = (u.message.video.file_id)
                    print file_id
                    newFile = bot.getFile(file_id)
                    print newFile
                    newFile.download('Heart_Sample'+ file_id+'.MOV')
                    time.sleep(8)
                   # bot code
                    import cv2
                    import multiprocessing
                    from PIL import Image, ImageStat
                    import os

                    from matplotlib import pyplot

                    # use python 2.7
                    video = cv2.VideoCapture('Heart_Sample'+ file_id+'.MOV')
                    c = 1

                    if video.isOpened():
                        rval, frame = video.read()
                    else:
                        rval = False
                    name ='images'+ file_id
                    try:
                        os.makedirs(name)
                    except OSError:
                        pass
                    while rval:
                        rval, frame = video.read()

                        cv2.imwrite(name+ '/ ' + str(c) + '.jpg', frame)
                        c = c + 1
                        cv2.waitKey(1)
                    video.release()

                    global brigtness


                    def find_brightness(i):
                        i = int(i)
                        global brightness

                        img = Image.open(name+'/ ' + str(i) + '.jpg').convert('RGBA')
                        stat = ImageStat.Stat(img)

                        return (stat.mean[0])


                    counter = 0
                    for e in os.listdir(name):
                        if ('.jpg' in e):
                            counter += 1


                    def find_all_dips():
                        global brigthness
                        dips = []
                        for i in range(1, len(brigthness) - 1):

                            if (brigthness[i - 1] > brigthness[i] and brigthness[i + 1] > brigthness[i]):
                                dips.append(brigthness[i])
                        return dips


                    def find_big_dips():
                        global brigthness
                        dips = []
                        for i in range(1, len(brigthness) - 1):
                            a = False
                            for j in range(1, 10):
                                if (i - j < 0):
                                    if (brigthness[0] > brigthness[i] and brigthness[i + j] > brigthness[i]):
                                        a = True
                                    else:
                                        a = False
                                        break
                                elif (i + j >= len(brigthness)):
                                    if (brigthness[i - j] > brigthness[i] and brigthness[len(brigthness) - 1] > brigthness[
                                        i]):
                                        a = True
                                    else:
                                        a = False
                                        break
                                else:
                                    if (brigthness[i - j] > brigthness[i] and brigthness[i + j] > brigthness[i]):
                                        a = True
                                    else:
                                        a = False
                                        break

                            if (a == True):
                                dips.append(brigthness[i])
                        return dips


                    counter -= 1
                    print counter
                    pool = multiprocessing.Pool(processes=8)
                    result = pool.map(find_brightness, (('%d' % i) for i in range(1, counter)))
                    brigthness = result
                    max_val = 0
                    min_val = 255
                    for i in range(len(brigthness)):
                        if (brigthness[i] < min_val):
                            min_val = brigthness[i]
                        if (brigthness[i] > max_val):
                            max_val = brigthness[i]
                        # print(str(i) + '  :  ' + str(brigthness[i]))
                    # print ("min : " + str(min_val))
                    # print ("max : " + str(max_val))
                    for i in range(len(brigthness)):
                        brigthness[i] -= min_val
                        tmp = max_val - min_val
                        brigthness[i] *= 100 / tmp
                        # print(str(i) + '  :  ' + str(brigthness[i]))

                    dips = len(find_big_dips())
                    print ('beats counted' + str(dips))

                    duration = ((counter + 1) / 29)
                    if(duration is not 0):

                        bpm = dips * (60 / duration)
                    else:
                        bpm = "you dieded"
                    print ('your bpm is ' + str(bpm))



                    pyplot.plot(brigthness)
                    pyplot.savefig(name+'/ yourgraph.jpg' )
                    pyplot.close()

                    bot.send_photo(chat_id=u.message.chat.id,  photo=(open(name+'/ yourgraph.jpg', 'rb')))
                    # bot.sendDocument(chat_id=u.message.chat.id, document=open(name+'/ yourgraph.jpg', 'rb'))

                    bot.sendMessage(chat_id=u.message.chat.id, text=('your BPM is ' +
                                                                     str(bpm)))

                    # pyplot.show()

            updates = bot.getUpdates(offset=offset)
        else:
            updates = bot.getUpdates()
            for u in updates:
                offset = bot.getUpdates()[-1].update_id + 1









