import requests,json,re,threading,os,time
#通用get请求
def get(url,header):
   r=requests.get(url,headers=header)
   return r.text
   
#多线程下载
class Load(threading.Thread):
   def __init__(self,url,file):
      threading.Thread.__init__(self)
      self.url=url
      if not os.path.exists(os.path.dirname(file)):
         os.makedirs(os.path.dirname(file))
      self.file=file
   def run(self):
      r=requests.get(self.url)
      with open(self.file,"wb") as f:
         f.write(r.content)
         print("ok")
   

#前置登录请求
data = {'fp':'4086852310',
'wos':'Android',
'user.loginType':'0',
'logType':'T',
'user.username':'xxxxxxxx',
'user.password':'xxxxxxxxxxxxxxxx'}
r =requests.post("http://dmj006.51baxue.com:19001/edei/loginAction.action",data)
#登录密钥
coo=r.headers["Set-Cookie"]

#构建学科列表
sub={"语文":101,
"数学":102,
"英语":105,
"日语":131,
"历史":111,
"地理":112,
"生物":110}

for v,k in sub.items():
   stj=json.loads(get("http://dmj006.51baxue.com:19001/edei/ajaxAction!getReportStudent.action?exam=86&school=12&grade=12&cla=99412586508318497&type=0&isHistory=F&islevel=&subCompose=0&subject="+str(k)+"&_=1639195730170",{"Cookie":coo}))
   #遍历结果集
   for i in stj:
      name=i["name"]
      num=i["num"]
      #获取答题卡
      html=get("http://dmj006.51baxue.com:19001/edei/functionadd!getStuImg.action?schoolNum=12&studentId="+num+"&examNum=86&subjectNum="+str(k)+"&gradeNum=12&ziyuan_num=802",{"Cookie":coo})
      #提取答题卡
      res=re.findall(r'<img id="(.*)" src="(.*)"',html)
      #list
      for r in res:
         #组装下载链接
         url="http://dmj006.51baxue.com:19001/edei/"+r[1];
         #丢给线程后台下载
         l=Load(url,"/storage/emulated/0/工作目录/"+name+"/"+v+"/"+r[0][-1:]+".jpg")
         l.start()
         time.sleep(2)
         print("正在下载答题卡:",name,v+r[0][-1:],url)
          