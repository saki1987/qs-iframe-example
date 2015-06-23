#coding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext

#hashlib类库
import hashlib
from Crypto.Cipher import AES
 
# 引入我们创建的表单类
from .forms import AddForm
from .forms import UserForm 
from models import User

from binascii import b2a_hex, a2b_hex
from decimal import Decimal

#requests类库
import requests

def decrypt(text, private_key):
    """
    decrypt the Request_Key.
    用AES算法根据私钥在MODE_ECB模式下进行解密。因为加密后是以十六进制传输，
    所以要先按十六进制解码，再去掉以'\0'补全的数据（在AES加密时必须是十六位
    或者十六位的倍数长加密，不足的以'\0'补全）
    """
    cryptor = AES.new(private_key, AES.MODE_ECB)
    plain_text = cryptor.decrypt(text.decode('hex'))
    return plain_text.rstrip('\0')


def encrypt(text, private_key):
    # cryptor = AES.new(self.key, self.mode, b'0000000000000001')
    cryptor = AES.new(private_key, AES.MODE_ECB)
    # 这里密钥key 长度必须为16（AES-128）,
    # 24（AES-192）,或者32 （AES-256）Bytes 长度
    # 目前AES-128 足够目前使用
    length = 16
    count = len(text)
    if count < length:
        add = (length-count)
        # \0 backspace
        text = text + ('\0' * add)
    elif count > length:
        add = (length-(count % length))
        text = text + ('\0' * add)
    ciphertext = cryptor.encrypt(text)
    # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
    # 所以这里统一把加密后的字符串转化为16进制字符串
    return b2a_hex(ciphertext)



def index(request):
    if request.method == 'POST':# 当提交表单时
     
        form = AddForm(request.POST) # form 包含提交的数据
         
        if form.is_valid():# 如果提交的数据合法
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(str(int(a) + int(b)))
     
    else:# 当正常访问时
        form = AddForm()
    return render(request, 'index.html', {'form': form})

def register(request):
	if request.method == 'POST':
		uf = UserForm(request.POST)
		if uf.is_valid():
			#数据有效则获取用户数据
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			email	 = uf.cleaned_data['email']
			phone	 = uf.cleaned_data['phone']
			#数据同步导数据库
			User.objects.create(username=username,password=password,email=email,phone=phone)
			return HttpResponse('注册成功！')

	else:
		uf = UserForm()

	return render_to_response('register.html',{'uf':uf},context_instance = RequestContext(request))

def login(request):
	if request.method == 'POST':
		uf = UserForm(request.POST)
		if uf.is_valid():
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			email	 = uf.cleaned_data['email']
			phone	 = uf.cleaned_data['phone']
			user = User.objects.filter(username__exact = username,password__exact = password)
			if user:
				uid = user.values('id')[0]['id']
				#发现存在当前用户，则跳转到index.html
				response = HttpResponseRedirect('/learn/index')
				#获取用户ID
				uid = user.values('id')[0]['id']
				#把用户信息写入到cookie中
				response.set_cookie('username',username,3600)
				response.set_cookie('email',email,3600)
				response.set_cookie('phone',phone,3600)
				response.set_cookie('uid',uid,3600)
				return response
			else:
				return HttpResponseRedirect('/learn/login_error/')
	else:
		uf = UserForm()
	return render_to_response('login.html',{'uf':uf},context_instance = RequestContext(request))

#登陆成功
def index(request):
	url 	 = 'http://qs.qsmind.com/api/home/agent-user-login/'
	username = request.COOKIES.get('username','')
	email	 = request.COOKIES.get('email','')
	phone	 = request.COOKIES.get('phone','')
	uid	 	 = request.COOKIES.get('uid','')
	#进行认证
	PrivateKey = '11036491134911e58513600308a8dcb2'
	iv 		= "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"; 
	params	= "email=%s&phone=%s&uid=%s&uname=%s" % (email,phone,uid,username)
	sign 	= hashlib.md5('%s%s' % (params, PrivateKey)).hexdigest()
	signed_request = "%s.%s" % (sign, encrypt(params, PrivateKey))
	print signed_request
	data 	= {'signed_request': signed_request}
	r = requests.post(url, data=data)
	res = r.json()
	response = render_to_response('index.html',{'username':username})
	response.set_cookie(key='pk', value=res.get('pk', ''))
	return response
	

#退出
def logout(request):
	response = HttpResponse('登出系统！')
	#清理cookie
	response.delete_cookie('username')
	return response

def login_error(request):
	return render_to_response('login_error.html')

def qsProxy(request,a):
	return render_to_response('qsProxy.html')


#支付
def fetch_alipay(request):
	PrivateKey = '11036491134911e58513600308a8dcb2'
	print request.POST
	return 




















