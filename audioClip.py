from moviepy.editor import AudioFileClip
import os
import soundfile
import shutil
import re
import sys

workpath = './'
support_format = 'mow'
delete_originFile = True
high_quality = None

if len(sys.argv) >= 2:
    workpath = sys.argv[1]

if len(sys.argv) >= 3:
    support_format = sys.argv[2]

if len(sys.argv) >= 4:
    delete_originFile = sys.argv[3] == 'True'

if len(sys.argv) >= 5:
    high_quality = sys.argv[4] or None
    
# print(support_format,type(support_format))
# print(delete_originFile,type(delete_originFile))
support_array = []
for char in support_format:
    if char == 'm':
        support_array.append('.mp3')
        support_array.append('.MP3')
    elif char == 'o':
        support_array.append('.ogg')
        support_array.append('.OGG')
    elif char == 'w':
        support_array.append('.wav')
        support_array.append('.WAV')

print("剪辑格式:",' '.join(support_array))
if delete_originFile:
    print("=================文件剪辑完成后删除")
else:
    print("-----------------不删除原文件")

if high_quality:
    print("-----------输出比特率:",high_quality)

if workpath:
    rootpath = workpath
else:
    rootpath = os.path.split(os.path.abspath(__file__))[0]

print("工作目录：",rootpath)

def getAbsPath(path):
    return os.path.abspath(os.path.join(rootpath,path))

# nowRootPath = getAbsPath(workpath)

def initAudioInfo(file):
    audio,samplerate = soundfile.read(file)

    ret = dict()
    ret.setdefault('fps',samplerate)
    ret.setdefault('buffersize',audio.size)
    ret.setdefault('bytes',audio.nbytes)

    return ret

def parseAudio(file,infopre):
    # audio = AudioFileClip(file,fps=infopre.get('fps'),nbytes=infopre.get('nbytes'),buffersize=infopre.get('buffersize'))
    audio = AudioFileClip(file,fps=infopre.get('fps'))

    audioclip = audio.subclip(1,audio.duration - 1)

    audioclip.set_fps(infopre.get('fps'))
    # audioclip.set
    savetopath = os.path.split(file)[0]
    savetopath = os.path.join(savetopath,'XJ_%s'%filename)
    # savetopath = os.path.join(savetopath,filename)

    if high_quality:
        audioclip.write_audiofile(savetopath,fps=infopre.get('fps'),bitrate=high_quality)
    else:
        audioclip.write_audiofile(savetopath,fps=infopre.get('fps'))
    audioclip.close()
    audio.close()

def automovefile():
    newclipPath = getAbsPath('NewClip')
    oldclipPath = getAbsPath('Clipped')
    if not os.path.exists(newclipPath):
        os.mkdir(newclipPath)
    else:
        if not os.path.exists(oldclipPath):
            os.mkdir(oldclipPath)
        
        for root,dirlist,file in os.walk(newclipPath):
            for fileName in file:
                filePath = os.path.join(root,fileName)
                topath = filePath.replace(newclipPath,oldclipPath)
                shutil.move(filePath,topath)


for root,dir,file in os.walk(rootpath):
    for filename in file:
        file_format = os.path.splitext(filename)[1]
        if file_format in support_array:
            pattern = r'XJ_.*'
            matchclipped = re.match(pattern,filename)
            if not matchclipped:
            # if True:
                filepath = os.path.join(root,filename)

                audioinfo = initAudioInfo(filepath)
                parseAudio(filepath,audioinfo)

                if delete_originFile:
                    os.chmod(filepath,0o755)
                    os.remove(filepath)
                    print(filename+"文件剪辑成功,原文件已删除!")
                else:
                    print(filename+"文件剪辑成功!")