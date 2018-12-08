#!/usr/bin/python
#
####################################################################################
#[S] SCRIP : Cloudump                                                              #
#[J]   JOB : identifying real IP of CloudFlare protected website.                  #
#[A]Codedby: Oseid Aldary                                                          #
####################################################################################
##
##Modlues
try:
        import mechanize,re,socket,urllib2,json,sys
        from os import system as sy
        from time import sleep
        sy("")
except ImportError, e:
        e = e[0][16:]
        if e =="json":
                e = "simplejson"
        print("\n[!] Error: Please Install [ "+e+" ] Library And Try Again !!!\n[*] Use This Command For Install It: pip install "+e)
	exit(1)

####=COLORS=########
wi = '\033[1;37m' ##>>White
rd = '\033[1;31m' ##>Red
gr = '\033[1;32m' ##>Green
yl = '\033[1;33m' ##>Yallow
bl = '\033[1;34m' ##>Blue
pu = '\033[1;35m' ##>Purple
cy = '\033[1;36m' ##>Cyan
####################
class DumpIP:
        def cnet(self):
                try:
                        ip = socket.gethostbyname("www.google.com")
			con = socket.create_connection((ip,80),2)
			return True
		except socket.error:
			pass
		return False
	def dumpIP(self, url):
		if self.cnet() !=True:
                        print(rd+"\n["+yl+"!"+rd+"]"+yl+" Error: Please Check Your Internet Connection "+rd+"!!!")
                        exit(1)
                if url[:7] =="http://" or url[:8] =="https://":
                        curl = url[7:] if url[:7] =="http://" else url[8:]
                        curl = curl.lower()
                        curl = curl.strip("/")
                        try:
                                colIP = socket.gethostbyname(curl)
                        except socket.error:
                                print(rd+"["+yl+"!"+rd+"]"+yl+" ERRORCode["+rd+"404"+yl+"]: Server Not Found!")
                                print(rd+"["+yl+"!"+rd+"]"+wi+" Please Check Your URL !")
                                exit(1)
                                
                        url = url.strip("/")
                else:
                        try:
                                colIP = socket.gethostbyname(url)
                        except socket.error:
                                print(rd+"["+yl+"!"+rd+"]"+yl+" ERRORCode["+rd+"404"+yl+"]: Server Not Found!")
                                print(rd+"["+yl+"!"+rd+"]"+wi+" Please Check Your URL !")
                                exit(1)
                        except socket.gaierror:
                                print(rd+"["+yl+"!"+rd+"]"+yl+" Error: Please Check Your URL[ "+rd+url+yl+" ]"+rd+" !!!")
                                exit(1)

                        url = "http://"+url
                try:
                        print(yl+"\n["+wi+"~"+yl+"]"+gr+" Analysis "+yl+"Website[ "+wi+url+yl+" ]"+rd+"...")
                        br = mechanize.Browser()
                        br.set_handle_robots(False)
                        br.addheaders = [ ('user-agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36" ) ]
                        br.open("http://www.crimeflare.cc:82/cfs.html")
                        br.select_form(nr=0)
                        br["cfS"]=url
                        res = br.submit()
                        data = res.get_data()
                        print(wi+"======================"+"="*len(url)+"=====")
                        if "No working nameservers are registered." in data:
                                print(rd+"  ["+yl+"!"+rd+"]"+yl+" ERRORCode["+rd+"404"+yl+"]: Server Not Found!")
                                print(rd+"  ["+yl+"!"+rd+"]"+wi+" Please Check Your URL !")
                        if "these are not CloudFlare-user nameservers" in data and "No working nameservers are registered." not in data:
                                print(rd+"  ["+yl+"!"+rd+"]"+yl+" CloudFlare "+wi+"STATUS: "+rd+" Disabled"+yl+"!")
                                print(rd+"  ["+yl+"!"+rd+"]"+yl+" Error: This Website Not Using "+rd+"CloudFlare"+yl+" Security"+rd+" !!!"+wi)
                        if "Sorry, but the domain name must contain one or two dots." in data:
                                print(rd+"  ["+yl+"!"+rd+"] "+yl+"Sorry,"+wi+" but the domain name must contain one or two dots."+rd+" !!!"+wi)
                        if "A direct-connect IP address was found:" in data:
                                ips =  re.findall( r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",data)
                                print(wi+"  ["+gr+">"+wi+"]"+yl+" CloudFlare "+wi+" STATUS:"+gr+" Enabled")
                                print(wi+"  ["+gr+">"+wi+"]"+gr+" CloudFlare IP Is: "+wi+colIP)
                                print(yl+"  ======================"+"="*len(colIP))
                                print(gr+"  ["+wi+"+"+gr+"]"+wi+" Real IP Is: "+gr+ips[0])
                                print(yl+"  ================"+"="*len(ips[0]))
                                try:
                                        url = "http://ip-api.com/json/"
                                        response = urllib2.urlopen(url + str(ips[0]))
                                        name = response.read()
                                        labs = json.loads(name.decode("utf-8"))
                                        region = labs['regionName']
                                        print(rd+"     GeoIP INFO"+gr+":["+wi+str(ips[0])+gr+"]===:")
                                        sleep(0.10)
                                        print(gr + "\t\t IP: " +wi+ labs['query'])
                                        sleep(0.10)
                                        print(gr+ "\t\t Status: " +wi+ labs['status'])
                                        sleep(0.10)
                                        print(gr+ "\t\t Region: "+wi+"{}".format(region))
                                        sleep(0.10)
                                        print(gr + "\t\t Country: " +wi+ labs['country'])
                                        sleep(0.10)
                                        print(gr + "\t\t City: " +wi+ labs['city'])
                                        sleep(0.10)
                                        print(gr + "\t\t ISP: "+wi + labs['isp'])
                                        sleep(0.10)
                                        print(gr + "\t\t Lat,Lon: "+wi + str(labs['lat']) + "," + str(labs['lon']))
                                        sleep(0.10)
                                        print(gr + "\t\t ZIPCODE: "+wi + labs['zip'])
                                        sleep(0.10)
                                        print(gr + "\t\t TimeZone: " +wi+ labs['timezone'])
                                        sleep(0.10)
                                        print(gr + "\t\t AS: " +wi+ labs['as'])
                                        sleep(0.10)
                                        print(pu+"===============================\n"+wi)
                                except Exception, e:
                                     print(rd+"\t\t ["+yl+"!"+rd+"]"+yl+" Something Went Wrong"+rd+" !!!"+wi)
                        if "No direct-connect IP address was found for this domain." in data:
                                print(rd+"  ["+yl+"!"+rd+"] "+yl+"Sorry,"+wi+" I Can't Find The Real IP Address Of This Website"+yl+"!"+rd+" :("+wi)
                         
                                
                except KeyboardInterrupt:
                        print(" ")
                        exit(1)
dumpIP = DumpIP()
if len(sys.argv) !=2:
        print("""

###########################################################################\ 
###  [S] SCRIP : Cloudump                                                   \ 
###  [J]   JOB : Identifying Real IP Of CloudFlare Protected Website.       #> 
###  [A] AUTHOR: Oseid Aldary                                               /     
###########################################################################/ 
""")
        print("[*]====> Let's Bypass CloudFlare <====[*]")
        try:
                url = raw_input("\nSite URL: ")
                while url=="" or url is None:
                        url = raw_input("Site URL: ")
                dumpIP.dumpIP(url)
        except KeyboardInterrupt:
                print(cy+"\n~"+gr+"GoodBye"+yl+" :)")
                exit(1)
else:
   url = sys.argv[1]
   if url in ["-h","--help","-hh","?","/?","help","HELP","-H","--HELP","-HH"]:
           print("Usage: python cloudump.py <Website URL>\nEx: python cloudump.py http://www.example.com")
           exit(1)
   else:
            dumpIP.dumpIP(url)
##############################################################
##################### 		     #########################
#####################   END OF TOOL  #########################
#####################                #########################
##############################################################
#This Tool by Oseid Aldary
#Have a nice day :)
#GoodBye
