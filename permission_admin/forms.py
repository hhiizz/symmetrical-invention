from django import forms
from django.utils import timezone
from django.core.validators import RegexValidator 

class getjob_form(forms.Form):
    id = forms.IntegerField(error_messages={'required':'id不可為空'})
    jobid = forms.CharField(error_messages={'required':'jobid不可為空'})
    date = forms.DateTimeField(label='爬取時間',error_messages={'required':'爬取時間不可為空'})
    job_type = forms.CharField(label='type',error_messages={'required':'種類不可為空'})    
    website = forms.CharField(label='來源',error_messages={'required':'來源為必填資料'})
    title = forms.CharField(label='標題',error_messages={'required':'標題不可為空'})
    company = forms.CharField(label='公司',error_messages={'required':'公司不可為空'})
    local =  forms.CharField(label='地區',error_messages={'required':'地區不可為空'})
    content = forms.CharField(label='工作內容',error_messages={'required':'工作內容不可為空'})
    salary =forms.CharField(label='薪資',error_messages={'required':'薪資不可為空'})
    href = forms.CharField(label='連結',error_messages={'required':'連結不可為空'})
    experience= forms.CharField(label='經驗',error_messages={'required':'經驗不可為空，沒資料請填不拘'})
    education = forms.CharField(label='學歷',error_messages={'required':'學歷不可為空，沒資料請填不拘'})
    department = forms.CharField(label='系所',error_messages={'required':'系所不可為空，沒資料請填不拘'})
    skill = forms.CharField(label='技能',error_messages={'required':'技能不可為空，沒資料請填不拘'})
    language = forms.CharField(label='技能',error_messages={'required':'語言不可為空，沒資料請填不拘'})
    Additional_conditions = forms.CharField(label='附加條件',error_messages={'required':'附加條件不可為空，沒資料請填不拘'})
    other = forms.CharField(label='其他不可為空',error_messages={'required':'附加條件不可為空，沒資料請填不拘'})
class crawler_log_form(forms.Form):
    id = forms.IntegerField(error_messages={'required':'id不可為空'})
    date = forms.DateTimeField(label='爬取時間',error_messages={'required':'爬取時間不可為空'})
    job_type = forms.CharField(label='type',error_messages={'required':'爬取種類不可為空'})
    website = forms.CharField(label='來源',error_messages={'required':'來源為必填資料'})
    count = forms.IntegerField(label='數量',error_messages={'required':'爬取數量為必填資料'})
    state = forms.BooleanField(label='權限',initial=False,required=False)
    crawler_contents = forms.CharField(label='錯誤內容',required=False)
class crawler_set_form(forms.Form):
    id = forms.IntegerField(error_messages={'required':'id不可為空'})
    job_type = forms.CharField(label='type',error_messages={'required':'抓取類別不可為空'})
    url_1111 = forms.CharField(label='url_1111',error_messages={'required':'url_1111不可為空'})
    url_104 = forms.CharField(label='url_104',error_messages={'required':'url_104不可為空'})
    total_type = forms.CharField(label='所屬總類',error_messages={'required':'所屬總類不可為空'})

class trend_form(forms.Form):
    id = forms.IntegerField(error_messages={'required':'id不可為空'})
    date = forms.CharField(label='type',error_messages={'required':'日期不可為空'})
    skill = forms.CharField(label='url_1111',error_messages={'required':'技能不可為空'})
    count = forms.IntegerField(label='數量',error_messages={'required':'次數不可為空'})
    job_type = forms.CharField(label='url_104',error_messages={'required':'工作類別不可為空'})

class member_admin(forms.Form):
    id = forms.IntegerField(label='id',error_messages={'required':'id不可為空'})
    username = forms.CharField(label='帳號',min_length=6,max_length=16,error_messages={'max_length':'帳號超出最大長度','min_length':'帳號不足6位','required':'帳號不可為空'})
    password = forms.CharField(label='密碼',min_length=6,max_length=16,
    error_messages={'max_length':'密碼超出最大長度','min_length':'密碼不足6位','required':'密碼不可為空'})
    Email = forms.EmailField(label='Email',error_messages={'required':'Email不可為空'})
    datetime = forms.DateField(label='創建日期',error_messages={'required':'日期不可為空'})
    last_login = forms.DateField(required=False,label='上次登入')
    line_userid = forms.CharField(label="line-id",required=False)
    permissions = forms.BooleanField(label='權限',required=False,initial=False)

class like_form(forms.Form):
    id = forms.IntegerField(label='id',error_messages={'required':'id不可為空'})
    username = forms.CharField(label='帳號',error_messages={'required':'帳號不可為空'})
    like_type = forms.CharField(label='類型',error_messages={'required':'類型不可為空'})
    skill = forms.CharField(label='技能',error_messages={'required':'技能不可為空'})
    jobid = forms.CharField(label='jobid',error_messages={'required':'jobid不可為空'})
    date = forms.DateField(label='日期',error_messages={'required':'日期不可為空'})

class recommend_log_form(forms.Form):
    id = forms.IntegerField(label='id',error_messages={'required':'id不可為空'})
    username = forms.CharField(label='帳號',error_messages={'required':'帳號不可為空'})
    date = forms.DateTimeField(label='日期',error_messages={'required':'日期不可為空'})
    count = forms.IntegerField(label='數量',error_messages={'required':'推送數量不可為空'})
    state = forms.BooleanField(label='權限',initial=False,required=False)
    content = forms.CharField(label='錯誤內容',required=False)

class recommend_form(forms.Form):
    id = forms.IntegerField(label='id',error_messages={'required':'id不可為空'})
    username = forms.CharField(label='帳號',error_messages={'required':'帳號不可為空'})
    open_recommend = forms.BooleanField(label='開啟推送',initial=False,required=False)
    job_type = forms.CharField(label='推送類別',error_messages={'required':'推送類別不可為空'})
    skill = forms.CharField(label='篩選技能',error_messages={'required':'篩選技能不可為空'})
    local = forms.CharField(label="篩選地區",initial="",required=False,error_messages={'required':'篩選地區不可為空'})
    fraction = forms.CharField(label='標準',error_messages={'required':'推送篩選分數不可為空'})
    count = forms.CharField(label='數量', validators=[
            RegexValidator(r'^\d+|max$', "數量格式錯誤"), 
        ],
        error_messages={'required':'推送數量不可為空'})
    notice_Email = forms.BooleanField(label='開啟Email通知',initial=False,required=False)

class notice_form(forms.Form):
    id = forms.IntegerField(label='id',error_messages={'required':'id不可為空'})
    username = forms.CharField(label='帳號',error_messages={'required':'帳號不可為空'})
    title = forms.CharField(label='標題',error_messages={'required':'標題不可為空'})
    content = forms.CharField(label='內容',error_messages={'required':'內容不可為空'})
    date = forms.DateTimeField(label='日期',error_messages={'required':'日期不可為空'})
    look_bool = forms.BooleanField(label='是否查看',initial=False,required=False)

class hot_search_form(forms.Form):
    id = forms.IntegerField(label='id',error_messages={'required':'id不可為空'})
    job_type = forms.CharField(label='技能類別',error_messages={'required':'技能類別不可為空'})
    skill = forms.CharField(label='熱門技能',error_messages={'required':'熱門技能不可為空'})
    count = forms.CharField(label='次數',error_messages={'required':'次數不可為空'})

class opinion_form(forms.Form):
    id = forms.IntegerField(label='id',error_messages={'required':'id不可為空'})
    date = forms.DateTimeField(label='日期',error_messages={'required':'日期不可為空'})
    username = forms.CharField(label='帳號',error_messages={'required':'帳號不可為空'})
    opinion_type =  forms.CharField(label='類型',error_messages={'required':'類型不可為空'})
    content = forms.CharField(label='內容',error_messages={'required':'內容不可為空'})
    response  = forms.CharField(label='回覆id',required=False)

class response_form(forms.Form):
    id = forms.IntegerField(label='id',error_messages={'required':'id不可為空'})
    username = forms.CharField(label='帳號',error_messages={'required':'帳號不可為空'})
    title = forms.CharField(label='標題',error_messages={'required':'標題不可為空'})
    content = forms.CharField(label='內容',error_messages={'required':'內容不可為空'})

class popular_job_form(forms.Form):
    id = forms.IntegerField(label='id',error_messages={'required':'id不可為空'})
    username = forms.CharField(label='帳號',error_messages={'required':'帳號不可為空'})
    jobid = forms.CharField(label='jobid',error_messages={'required':'jobid不可為空'})

class total_type_form(forms.Form):
    id = forms.IntegerField(label='id',error_messages={'required':'id不可為空'})
    total_type = forms.CharField(label='總類名稱',error_messages={'required':'總類名稱不可為空'})

class tesk_form(forms.Form):
    id = forms.CharField(label='id',error_messages={'required':'id不可為空'})
    trigger = forms.CharField(label='總類名稱',error_messages={'required':'触发器类型不可為空'})
    time = forms.CharField(label='總類名稱',error_messages={'required':'触发時間不可為空'})
    state = forms.BooleanField(label='狀態',initial=False,required=False)

class tesk_log_form(forms.Form):
    id = forms.IntegerField(label='id',error_messages={'required':'id不可為空'})
    job_id = forms.CharField(label='job_id',error_messages={'required':'job_id不可為空'})
    run_time = forms.DateTimeField(label='啟動時間',error_messages={'required':'執行時間不可為空'})
    duration = forms.FloatField(label='執行時間',error_messages={'required':'執行時間不可為空'})