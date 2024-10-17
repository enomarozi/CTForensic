from django.shortcuts import render
from django.http import JsonResponse
from .models import ImageFile
from scapy.all import *
import base64

def analisaPCAP(request, id_):
	fileName = ImageFile.objects.get(pk=id_)
	path_file = "uploads/"+fileName.name
	packets = rdpcap(path_file)
	summary_data = str(packets).split(' ')
	context = {
		'id_':id_,
		"title":"Analysis PCAP",
		'metadata':fileName,
		'summary': summary_data[1]+" "+summary_data[2]+" "+summary_data[3]+" "+summary_data[4][:-1],
		'ip': getIP(packets)
	}
	return render(request, 'index/analisa_pcap.html', context)

def getIP(packets):
	IPresultSRCtoDST = []
	for i in packets:
	    if IP in i:
	        iter_ = i[IP].src+"-"+i[IP].dst
	        IPresultSRCtoDST.append(iter_)
	    elif IPv6 in i:
	    	iter_ = i[IPv6].src+"-"+i[IPv6].dst
	    	IPresultSRCtoDST.append(iter_)
	result = {}
	for i in set(IPresultSRCtoDST):
	    result[i] = str(IPresultSRCtoDST.count(i))
	return result

def checkPacket(request):
	if request.method == 'GET':
		ip_address = request.GET.get('ip')
		id_ = request.GET.get('id')
		fileName = ImageFile.objects.get(pk=id_)
		path_file = "uploads/"+fileName.name
		packets = rdpcap(path_file)
		response_data = {
			'type':bytesData(packets,ip_address)[3],
			'sport':bytesData(packets,ip_address)[0],
			'dport':bytesData(packets,ip_address)[1],
			'bytes_data_encode':bytesData(packets,ip_address)[2],
		}
		return JsonResponse(response_data,safe=False)

def bytesData(packets,ip_address):
	result = ""
	ip_src, ip_dst = ip_address.split("-")
	sport, dport, type_ = set(),set(),set()
	for i in packets:
		try:
			if ":" in ip_src or ":" in ip_dst:
				if i[IPv6].src == ip_src and i[IPv6].dst == ip_dst:
					raw_data_base64 = base64.b64encode(i[Raw].load).decode('utf-8')
					sport.add(i[IPv6].sport)
					dport.add(i[IPv6].dport)
					if "TCP" in i[IPv6]:
						type_.add("TCP")
					elif "UDP" in i[IPv6]:
						type_.add("UDP")
					result += raw_data_base64
			elif "." in ip_src or "." in ip_dst:
				if i[IP].src == ip_src and i[IP].dst == ip_dst:
					raw_data_base64 = base64.b64encode(i[Raw].load).decode('utf-8')
					sport.add(i[IP].sport)
					dport.add(i[IP].dport)
					if "TCP" in i[IP]:
						type_.add("TCP")
					elif "UDP" in i[IP]:
						type_.add("UDP")
					result += raw_data_base64

			
		except Exception as e:
			pass
	if len(sport) == 0:
		sport.add("Tidak ada port")
	if len(dport) == 0:
		dport.add("Tidak ada port")
	if len(type_) == 0:
		type_.add("Others")
	return (list(sport)[0],list(dport)[0],result,list(type_))

def getPcap(request):
	file_pcap = ImageFile.objects.all().values('id','name','size','format')
	data = list(file_pcap)
	return JsonResponse(data,safe=False)