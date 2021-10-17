from datetime import datetime
from collections import Counter
import operator
from collections import Counter

class Parser:
    def __init__(self):
        self.numberOfDays = 0 # Count number of days passed
        
        self.startDate = datetime.today()
        self.endDate = datetime.today()
        
        self.fileTypeDict = {} # Contains file extension - file type information
        self.initializeFileType()
        
    def initializeFileType(self):  # Define file types for each file
        self.fileTypeDict["html"] = "HTML"
        self.fileTypeDict["htm"] = "HTML"
        self.fileTypeDict["shtml"] = "HTML"
        self.fileTypeDict["map"] = "HTML"

        self.fileTypeDict["gif"] = "Images"
        self.fileTypeDict["jpeg"] = "Images"
        self.fileTypeDict["jpg"] = "Images"
        self.fileTypeDict["xbm"] = "Images"
        self.fileTypeDict["bmp"] = "Images"
        self.fileTypeDict["rgb"] = "Images"
        self.fileTypeDict["xpm"] = "Images"

        self.fileTypeDict["au"] = "Sound"
        self.fileTypeDict["snd"] = "Sound"
        self.fileTypeDict["wav"] = "Sound"
        self.fileTypeDict["mid"] = "Sound"
        self.fileTypeDict["midi"] = "Sound"
        self.fileTypeDict["lha"] = "Sound"
        self.fileTypeDict["aif"] = "Sound"
        self.fileTypeDict["aiff"] = "Sound"

        self.fileTypeDict["mov"] = "Video"
        self.fileTypeDict["movie"] = "Video"
        self.fileTypeDict["avi"] = "Video"
        self.fileTypeDict["qt"] = "Video"
        self.fileTypeDict["mpeg"] = "Video"
        self.fileTypeDict["mpg"] = "Video"

        self.fileTypeDict["ps"] = "Formatted"
        self.fileTypeDict["eps"] = "Formatted"
        self.fileTypeDict["doc"] = "Formatted"
        self.fileTypeDict["dvi"] = "Formatted"
        self.fileTypeDict["txt"] = "Formatted"

        self.fileTypeDict["cgi"] = "Dynamic"
        self.fileTypeDict["pl"] = "Dynamic"
        self.fileTypeDict["cgi-bin"] = "Dynamic"

    def parse(self, logFile):  # Read each line from the log and process output
        index = 0
        requests = 1
        total_bytes = 0
        count = 0
        list_codes = []
        request_list = []
        local_bytes = 0
        remote_bytes = 0
        filename_list = []
        html = 0
        images = 0
        sound = 0
        video = 0
        formatted = 0
        dynamic = 0
        others = 0
        unique_list = []
        unique_bytes = {}

        for line in logFile:
            elements = line.split()

            # Skip to the next line if this line has an empty string
            if line is '':continue

            # Skip to the next line if this line contains not equal to 9 - 11 elements
            if not (9 <= len(elements) <= 11):continue

            # Corrects a record with a single "-"
            if (len(elements) == 9 and elements[2] != '-'):
                elements.insert(2, '-')

            sourceAddress = elements[0]
            timeStr = elements[3].replace('[', '')
            requestMethod = elements[5]
            requestFileName = elements[6].replace('"', '')
            responseCode = elements[len(elements) - 2]
            replySizeInBytes = elements[len(elements) - 1]
            try:
                total_bytes += int(replySizeInBytes)
            except:
                total_bytes

            responseType = checkResCode(self,responseCode)
            #list_codes.append(responseType)
            if responseType == 'Successful':
                # if sourceAddress == 'local':
                #     try:
                #         local_bytes += int(replySizeInBytes)
                #     except:
                #         total_bytes
                # if sourceAddress == 'remote':
                #     try:
                #         remote_bytes += int(replySizeInBytes)
                #     except:
                #         total_bytes


                filetype = self.getFileType(requestFileName)
                # if (filetype == "HTML"):
                #     html += int(replySizeInBytes)
                # elif (filetype == "Images"):
                #     images += int(replySizeInBytes)
                # elif (filetype == "Sound"):
                #     sound += int(replySizeInBytes)
                # elif (filetype == "Video"):
                #     video += int(replySizeInBytes)
                # elif (filetype == "Formatted"):
                #     formatted += int(replySizeInBytes)
                # elif (filetype == "Dynamic"):
                #     dynamic += int(replySizeInBytes)
                # else:
                #     others += int(replySizeInBytes)

                filename_list.append(filetype)
                filetype2 = requestFileName.split('.',1)
                
                unique_list.append(requestFileName)
                try:
                    unique_bytes[requestFileName] += int(replySizeInBytes)
                except:
                    unique_bytes[requestFileName] = int(replySizeInBytes)

                    

            

            ################## From Here, implement your parser ##################
            # Inside the for loop, do simple variable assignments & modifications
            # Please do not add for loop/s
            # Only the successful requests should be used from question 5 onward

            # Prints assigned elements. Please comment print statement.
            #print('{0} , {1} , {2} , {3} , {4} , {5} '.format(sourceAddress,timeStr,requestMethod,requestFileName,responseCode, replySizeInBytes),end="")
            
            # Assigns & prints format type. Please comment print statement.
            #fileType = self.getFileType(requestFileName)
            #print(' , {0}'.format(fileType))

            # Q1: Write a condition to identify a start date and an end date.
            if requests == 1:
                self.startDate = datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S")
                requests +=1
            else:
                self.endDate = datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S")
                requests +=1
            

            
        # Outside the for loop, generate statistics output
        delta = self.endDate - self.startDate
        #print(delta.days)
        #print(requests/int(delta.days))
        #print(total_bytes)
        #print(html, images, sound, video, formatted, dynamic, others)
        #print(total_bytes/int(delta.days))
        d = {}
        for item in unique_list:
            d[item] = d.get(item, 0) +1
        
        unique_total = 0
        for key, value in d.items():
            if value == 1:
               unique_total += unique_bytes.get(key)
                
        print((unique_total/total_bytes)*100)
        #res = Counter(d.values())
        #print(len(d))
        #print(1901/len(d)*100)
        # bytes_total = 0
        # for item.key() in unique_bytes:
        #     if item.key() == 1:
        #         bytes_total += item.value()

        # print(bytes_total)
        
        # print(1051781504/268176,3951539030/285517,101293073/588,908004217/8288,1788151744/3795,1091007/1827,144407633/232)
        # print(len(filename_list))
        # print('local', (local_bytes/total_bytes)*100)
        # print('remote', (remote_bytes/total_bytes)*100)

    def getFileType(self, URI):
        if URI.endswith('/') or URI.endswith('.') or URI.endswith('..'):
            return 'HTML'
        filename = URI.split('/')[-1]
        if '?' in filename:
            return 'Dynamic'
        extension = filename.split('.')[-1].lower()
        if extension in self.fileTypeDict:
            return self.fileTypeDict[extension]
        return 'Others'

def checkResCode(self, code):
    if code == '200' : return 'Successful'
    if code == '302' : return 'Found'
    if code == '304' : return 'Not Modified'  
    return 'Unsuccessful' 


if __name__ == '__main__':
    logfile = open('access_log', 'r', errors='ignore')
    logParser = Parser()
    logParser.parse(logfile)
    pass
