import requests
import json
import time
from PIL import Image
from io import BytesIO
import os
import json


class imageInjection:

	def __init__(self):
		self.folderPath=None
		self.subfolders=None
		self.csvFile=None
		self.counter=0
		self.setSubscriptionVar()

	def setSubscriptionVar(self):
		self.subscription_key = <#your subscription key>
		assert self.subscription_key
		self.vision_base_url = "https://westus.api.cognitive.microsoft.com/vision/v2.0/"
		self.analyze_url = self.vision_base_url + "analyze"

	def readImageGetData(self,imagePath):
		image_data = open(imagePath, "rb").read()
		headers    = {'Ocp-Apim-Subscription-Key': self.subscription_key,
		              'Content-Type': 'application/octet-stream'}
		params     = {'visualFeatures': 'Categories,Description,Tags,Objects'}
		response = requests.post(self.analyze_url, headers=headers, params=params, data=image_data)
		response.raise_for_status()
		return response.json()

	def getPath(self):
		self.folderPath=os.getcwd() #your path
		self.csvFile=open(os.getcwd()+"#your csv file name", "w")

	def getImageNo(self,imageList,subFolder):
		for image in imageList:
			print("For Image: ",image)
			if image.split('.')[1] == 'jpg':
				imagePath=subFolder+'/'+image
				analysis=self.readImageGetData(imagePath)
				self.fileWrprintite(analysis,image,subFolder)
				self.counter+=1

				if self.counter > 19:
					time.sleep(62)
					self.counter=0

	def fileWrite(self,analysis,image,subFolder):
		jsonPath=subFolder+'/'+image.split('.')[0]+'.json'

		with open(jsonPath, 'w') as fp:
			json.dump(analysis, fp, indent=4)


	def getSubFoldersList(self):
		self.getPath()
		self.subfolders = [f.path for f in os.scandir(self.folderPath) if f.is_dir()]

	def getImageList(self):
		abc=os.listdir(self.folderPath)
		#for subFolder in self.subfolders:
		for subFolder in abc:
			imageList=os.listdir(self.folderPath+"/"+subFolder)
			full=self.folderPath+subFolder
			self.getJSONNo(imageList,subFolder,full)
			
	def getJSONFromFile(self,subFolder,jshonPath,fullPath):
		with open(fullPath) as file:
			data = json.load(file)

			for i in data["tags"]:
				if i["name"]==subFolder:
					if i["confidence"] > 0.8:
						line=jshon+","+i['name']+","+"1"+","+"0"+","+"0"+","+"0"+","+","+str(i['confidence'])
					elif i["confidence"] > 0.6:
						line=jshon+","+i['name']+","+"0"+","+"1"+","+"0"+","+"0"+","+","+str(i['confidence'])
					elif i["confidence"] > 0.4:
						line=jshon+","+i['name']+","+"0"+","+"0"+","+"1"+","+"0"+","+","+str(i['confidence'])
					elif i["confidence"] > 0.15:
						line=jshon+","+i['name']+","+"0"+","+"0"+","+"0"+","+"1"+","+","+str(i['confidence'])
					else:
						line=jshon+","+i['name']+","+"0"+","+"0"+","+"0"+","+"0"+","+","+str(i['confidence'])
					print("ithe")
					self.csvFile.write(line+"\n")

	def getJSONNo(self,imageList,subFolder,fullPath):
		for jshon in imageList:
			if jshon.split('.')[1] == 'json':
				jshonPath=subFolder+'/'+jshon
				self.getJSONFromFile(subFolder,jshonPath,fullPath)

	def getJSONData(self):
		self.getSubFoldersList()
		self.getImageList()
		
if __name__ == '__main__':
	imageObject=imageInjection()
	imageObject.getSubFoldersList()
	imageObject.getImageList()
	#imageObject.getJSONData()



