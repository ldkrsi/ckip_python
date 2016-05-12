import ConfigParser
import socket
import xml.parsers.expat


my_format = "<?xml version=\"1.0\"?><wordsegmentation version=\"0.1\" charsetcode=\"utf-8\"><option showcategory=\"1\"/>%s<text>%s</text></wordsegmentation>"

config = ConfigParser.ConfigParser()
config.read('config.ini')
authentication_string = "<authentication username=\"%s\" password=\"%s\"/>" % (config.get("Authentication","Username"), config.get("Authentication","Password"))
connect_target = config.get("Server","IP"), int(config.get("Server","Port"))

class parse_xml:
	def __init__(self,input_xml_str):
		self.status_code, self.status_str, self.result = None, '', ''
		self.core = xml.parsers.expat.ParserCreate('utf-8')
		self.core.StartElementHandler = self.start_element
		self.core.EndElementHandler = self.end_element
		self.core.CharacterDataHandler = self.char_data
		self.pointer = None
		self.core.Parse(input_xml_str.strip(),1)
	def start_element(self,name,attrs):
		if name == "processstatus":
			self.status_code = int(attrs['code'])
			self.pointer = name
		elif name == "sentence":
			self.pointer = name
	def end_element(self,name):
		if name == "wordsegmentation":
			self.result = self.result.strip()
	def char_data(self,data):
		if self.pointer is None:
			return None
		if self.pointer == "processstatus":
			self.status_str = data
		elif self.pointer == "sentence":
			self.result+= data
		self.pointer = None


def ckip_client(input_text,output_file=None):
	input_text = input_text.replace('　',' ').strip()
	text = my_format % (authentication_string, input_text)
	if len(text.decode('utf-8')) >= 7900:
		raise ValueError("Your input text is too long.")
	downloaded = ''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(connect_target)
	sock.sendall(text)
	while "</wordsegmentation>" not in downloaded:
		chunk = sock.recv(4096)
		downloaded +=chunk
	result = parse_xml(downloaded)
	if result.status_code == 0:
		if output_file:
			output = open(output_file,'w')
			output.write(result.result.encode('utf-8'))
			output.close()
		return result.result, len(text.decode('utf-8'))
	else:
		class CKIPException(Exception):
			pass
		raise CKIPException("status_code: %d, %s" % (result.status_code, result.status_str))



if __name__ == "__main__":
	#print config.get("Authentication","Username"), config.get("Authentication","Password")
	text = "Facebook 是一個聯繫朋友、工作夥伴、同學或其他社交圈之間的社交工具。你可以利用Facebook 與朋友保持密切聯絡，無限量地上傳相片，分享轉貼連結及影片。"
	ckip_client(text,"output.txt")