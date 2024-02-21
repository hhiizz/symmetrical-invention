import datetime
import random
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackTemplateAction,
    CarouselTemplate, CarouselColumn,
)
from myApp.models import Job_type

from mysql_member.models import Member
from python_email.recommend_Email import recmooemd_email
from user.models import Like, Recommend
from django.db.models import Sum,Count

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookParser(settings.LINE_CHANNEL_SECRET)
user_states = {}
user_values = {}
user_Email = {}
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = handler.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            try:
                if isinstance(event, MessageEvent):
                    user_id = event.source.user_id
                    if(Member.objects.filter(line_user_id = user_id).exists()):
                        if(event.message.text =="幫助"):
                            try:
                                buttons_template_1 = TemplateSendMessage(
                                    alt_text='Buttons template 1',
                                    template=ButtonsTemplate(
                                        title='可用的功能',
                                        text='可以輸入或點及按鈕來使用功能!!',
                                        actions=[
                                            MessageTemplateAction(
                                                label='關閉推送通知',
                                                text='關閉推送通知',
                                            ),
                                            MessageTemplateAction(
                                                label='關閉推送職缺',
                                                text='關閉推送職缺',
                                            ),
                                            MessageTemplateAction(
                                                label='清除綁定',
                                                text='清除綁定',
                                            ),
                                        ]
                                    )
                                )
                                buttons_template_3 = TemplateSendMessage(
                                    alt_text='Buttons template 3',
                                    template=ButtonsTemplate(
                                        title='可用的功能清空',
                                        text='可以輸入或點及按鈕來使用功能!!',
                                        actions=[
                                            MessageTemplateAction(
                                                label='清空收藏',
                                                text='清空收藏',
                                            ),
                                            MessageTemplateAction(
                                                label='清空我的最愛',
                                                text='清空我的最愛',
                                            ),
                                            MessageTemplateAction(
                                                label='清空推送',
                                                text='清空推送',
                                            ),
                                        ]
                                    )
                                )
                                buttons_template_2 = TemplateSendMessage(
                                    alt_text='Buttons template 3',
                                    template=ButtonsTemplate(
                                        title='查看工作職缺',
                                        text='您可以在此查看推送或熱門職缺!!',
                                        actions=[
                                            MessageTemplateAction(
                                                label='查看推送職缺',
                                                text='查看推送職缺',
                                            ),
                                            MessageTemplateAction(
                                                label='當周熱門工作',
                                                text='當周熱門工作',
                                            )
                                        ]
                                    )
                                )

                                line_bot_api.reply_message(event.reply_token, [buttons_template_1,buttons_template_3,buttons_template_2])
                            except Exception as e:
                                line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=str(e))
                                )
                        elif(event.message.text == "清空收藏"):
                            Like.objects.filter(like_user_name = Member.objects.get(line_user_id = user_id)).delete()
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text="\u2714刪除收藏完成")
                            )
                        elif(event.message.text == "清空我的最愛"):
                            Like.objects.filter(like_user_name = Member.objects.get(line_user_id = user_id),like_type ="like").delete()
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text="\u2714刪除我的最愛完成")
                            )
                        elif(event.message.text == "清空推送"):
                            Like.objects.filter(like_user_name = Member.objects.get(line_user_id = user_id),like_type ="recommend").delete()
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text="\u2714刪除推送職缺完成")
                            )
                        elif event.message.text == "關閉推送職缺":
                            user_recommend =  Recommend.objects.get(recom_user_name = Member.objects.get(line_user_id = user_id))
                            user_recommend.recom_open = False
                            user_recommend.save()
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text="您已關閉推送職缺，如需開啟請至網站中的用戶中心開啟!!!")
                            )
                        elif(event.message.text == "關閉推送通知"):
                            line_bot_api.reply_message(  # 回復傳入的訊息文字
                                event.reply_token,
                                TemplateSendMessage(
                                    alt_text='Buttons template',
                                    template=ButtonsTemplate(
                                        title='關閉通知',
                                        text='請選擇關閉的通知',
                                        actions=[
                                            PostbackTemplateAction(
                                                label='Email',
                                                text='Email',
                                                data='Email'
                                            ),
                                            PostbackTemplateAction(
                                                label='Line-Bot',
                                                text='Line-Bot',
                                                data='Line-Bot'
                                            ),
                                            PostbackTemplateAction(
                                                label='兩者都關閉',
                                                text='兩者都關閉',
                                                data='2'
                                            )
                                        ]
                                    )
                                )
                            )
                        elif event.message.text == "帳號綁定":
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text='您已完成綁定，如果需要更改綁定用戶，請輸入"清除綁定"即可\u2757\u2757\u2757')
                            )
                        elif event.message.text == "清除綁定":
                            user = Member.objects.get(line_user_id = user_id)
                            user.line_user_id = None
                            user.save()
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text='\u2714您已成功清除綁定，請您重新綁定帳戶\u2757')
                            )
                        elif event.message.text == "查看推送職缺":
                            try:
                                button_list = [
                                    PostbackTemplateAction(
                                        label='當日推送職缺',
                                        text='當日推送職缺',
                                        data=0,
                                    ),
                                    PostbackTemplateAction(
                                        label='昨日推送職缺',
                                        text='昨日推送職缺',
                                        data=1,
                                    ),
                                    PostbackTemplateAction(
                                        label='3天前推送職缺',
                                        text='3天前推送職缺',
                                        data=3,
                                    ),
                                    PostbackTemplateAction(
                                        label='一周前推送職缺',
                                        text='一周前推送職缺',
                                        data=7,
                                    )
                                ]
                                line_bot_api.reply_message(  # 回復傳入的訊息文字
                                    event.reply_token,
                                    [TemplateSendMessage(
                                        alt_text='選擇查看推送職缺的時間',
                                        template=ButtonsTemplate(
                                            title='選擇查看推送工作時間',
                                            text='選擇查看推送工作時間',
                                            actions=button_list
                                        )
                                    )]
                                )
                            except Exception as e:
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(text=str(e))
                                )

                        
                        elif event.message.text == "當周熱門工作":
                            try:
                                button_list = []
                                job_type =list(Job_type.objects.values_list('type_name',flat=True))
                                for i in job_type:
                                    button_list.append(
                                        PostbackTemplateAction(
                                            label=i,
                                            text=i,
                                            data=i
                                        )
                                    )
                                line_bot_api.reply_message(  # 回復傳入的訊息文字
                                    event.reply_token,
                                    [TemplateSendMessage(
                                        alt_text='Buttons template',
                                        template=ButtonsTemplate(
                                            title='選擇工作類',
                                            text='選擇每周的工作類',
                                            actions=button_list[0:4]
                                        )
                                    ),TemplateSendMessage(
                                        alt_text='Buttons template',
                                        template=ButtonsTemplate(
                                            title='選擇工作類',
                                            text='選擇每周的工作類',
                                            actions=button_list[4:8]
                                        )
                                    ),TemplateSendMessage(
                                        alt_text='Buttons template',
                                        template=ButtonsTemplate(
                                            title='選擇工作類',
                                            text='選擇每周的工作類',
                                            actions=button_list[8:12]
                                        )
                                    )]

                                )
                            except Exception as e:
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(text=str(e))
                                )
                        else:
                            name =  line_bot_api.get_profile(user_id).display_name
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=name+'用戶請輸入您想要什麼呢?\n如果您不知道可以輸入"幫助"來查看功能。\n \U0001F449 https://140.128.88.181/\n \U0001F4E8 vu56032613@gmail.com')
                            )
                    else:
                        if event.message.text == "帳號綁定":
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text="請輸入您帳戶對應的Email:")
                            )
                            user_states[user_id] = "帳號綁定"
                        elif user_id in user_states and user_states[user_id] == "帳號綁定":
                            if(Member.objects.filter(Email=event.message.text).exists()):
                                if(Member.objects.filter(Email=event.message.text,line_user_id__isnull=True).exists()):
                                    vertical = ''
                                    list_ch = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','z','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
                                    for i in range(0,6):
                                        vertical += random.choice(list_ch)
                                    recmooemd_email(event.message.text,vertical)
                                    line_bot_api.reply_message(
                                        event.reply_token,
                                        TextSendMessage(text="請輸入Email驗證碼進行綁定:")
                                    )
                                    user_values[user_id] = vertical
                                    user_Email[user_id] = event.message.text
                                    user_states[user_id] = "Email驗證"
                                else:
                                    line_bot_api.reply_message(
                                        event.reply_token,
                                        TextSendMessage(text="該用戶以綁定，請查看帳戶是否正確，如果還是沒能解決的問題，請與我們聯繫!!!\n \1F449 https://140.128.88.181/\n \1F4E7 vu56032613@gmail.com")
                                    )
                                    try:
                                        del user_states[user_id]
                                    except KeyError :
                                        print("No such key")
                            else:
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(text="\u274CEmail不存在請您查看Email是否正確\u2757\u2757")
                                )
                                try:
                                    del user_states[user_id]
                                except KeyError :
                                    print("No such key")
                        elif user_id in user_states and user_states[user_id] == "Email驗證":
                            if(user_values[user_id] == event.message.text ):
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(text="\u2714恭喜您綁定成功!!")
                                )
                                user_now = Member.objects.get(Email =user_Email[user_id])
                                user_now.line_user_id = user_id
                                user_now.save()
                                try:
                                    del user_states[user_id]
                                except KeyError :
                                    print("No such key")
                                try:
                                    del user_values[user_id]
                                except KeyError :
                                    print("No such key")
                                try:
                                    del user_Email[user_id]
                                except KeyError :
                                    print("No such key")
                            else:
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(text="\u274CEmail驗證碼錯誤請重新驗證\u2757")
                                )
                                try:
                                    del user_states[user_id]
                                except KeyError :
                                    print("No such key")
                                try:
                                    del user_values[user_id]
                                except KeyError :
                                    print("No such key")
                                try:
                                    del user_Email[user_id]
                                except KeyError :
                                    print("No such key")

                        elif(event.message.text =="幫助"):
                            buttons_template_1 = TemplateSendMessage(
                                    alt_text='Buttons template 1',
                                    template=ButtonsTemplate(
                                        title='可用的功能關閉',
                                        text='可以輸入或點及按鈕來使用功能!!',
                                        actions=[
                                            MessageTemplateAction(
                                                label='關閉推送通知',
                                                text='關閉推送通知',
                                            ),
                                            MessageTemplateAction(
                                                label='關閉推送職缺',
                                                text='關閉推送職缺',
                                            ),
                                        ]
                                    )
                                )
                            buttons_template_3 = TemplateSendMessage(
                                alt_text='Buttons template 3',
                                template=ButtonsTemplate(
                                    title='可用的功能 清空',
                                    text='可以輸入或點及按鈕來使用功能!!',
                                    actions=[
                                        MessageTemplateAction(
                                            label='清空收藏',
                                            text='清空收藏',
                                        ),
                                        MessageTemplateAction(
                                            label='清空我的最愛',
                                            text='清空我的最愛',
                                        ),
                                        MessageTemplateAction(
                                            label='清空推送',
                                            text='清空推送',
                                        ),
                                        MessageTemplateAction(
                                            label='帳號綁定',
                                            text='帳號綁定',
                                        ),
                                    ]
                                )
                            )

                            line_bot_api.reply_message(event.reply_token, [buttons_template_1,buttons_template_3])
                        else:
                            name =  line_bot_api.get_profile(user_id).display_name
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=name+'用戶您尚未綁定帳戶，請您先輸入"帳號綁定"進行綁定\u2757\u2757\u2757')
                            )
                elif isinstance(event, PostbackEvent):
                    user_id = event.source.user_id
                    if event.postback.data == "Email":
                        user_recom = Recommend.objects.get(recom_user_name = Member.objects.get(line_user_id = user_id))
                        user_recom.recom_email_open = False
                        user_recom.save()
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='\u2714已關閉Email通知')
                        )
                    elif(event.postback.data == "Line-Bot"):
                        user_recom = Recommend.objects.get(recom_user_name = Member.objects.get(line_user_id = user_id))
                        user_recom.recom_line_bot = False
                        user_recom.save()
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='\u2714已關閉Line-Bot通知')
                        )
                    elif(event.postback.data == "2"):
                        user_recom = Recommend.objects.get(recom_user_name = Member.objects.get(line_user_id = user_id))
                        user_recom.recom_email_open = False
                        user_recom.recom_line_bot = False
                        user_recom.save()
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text='\u2714已關閉Email和Line-Bot通知')
                        )
                    elif(event.postback.data == '0' or event.postback.data == '1' or event.postback.data == '3' or event.postback.data == '7'):
                        try:
                            first_key_5 = list(get_recommend_skill(user_name=Member.objects.get(line_user_id = user_id),day=int(event.postback.data)).keys())[:5]
                            if(len(first_key_5) !=0):
                                list_text = []
                                for first_key in first_key_5 :
                                    if(len(first_key.like_jobid.content)>150):
                                        content_key = first_key.like_jobid.content[:150]+'...'
                                    else:
                                        content_key = first_key.like_jobid.content
                                    list_text.append(TextSendMessage(text="\u2757\u27A1"+first_key.like_jobid.title+"\u2B05\u2757\n"+
                                                    content_key+'\n'+
                                                    "工作技能:"+first_key.like_jobid.skill+'\n'+
                                                    "更新時間:"+str(first_key.like_jobid.date)+'\n'+
                                                    "工作薪資:"+first_key.like_jobid.salary+'\n'+
                                                    "工作連結:"+first_key.like_jobid.href
                                                    ))
                                # list_text.append(TextSendMessage(
                                #     text= '如果您想查看更多職缺請到\n \U0001F449 https://140.128.88.181/ 會員中心進行查看\u2757'
                                # ))
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    list_text
                                )
                            else:
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(text="\u2757\u2757您今日尚無推送職缺\u2757\u2757")
                                )
                        except Exception as e :
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=str(e))
                            )
                    else:
                        try:
                            first_key_5  = Like.objects.filter(like_type='like',like_date__gte=(datetime.date.today() - datetime.timedelta(weeks=1)),like_jobid__type =event.postback.data).values('like_jobid__company','like_jobid__title','like_jobid__skill','like_jobid__local','like_jobid__salary',"like_jobid__href",'like_jobid__content','like_jobid__date').annotate(count=Count('like_jobid')).order_by('-count')[:5]
                            if(len(first_key_5) != 0):
                                list_text = []
                                for first_key in first_key_5 :
                                    if(len(first_key['like_jobid__content'])>150):
                                        content_key = first_key['like_jobid__content'][:150]+'...'
                                    else:
                                        content_key = first_key['like_jobid__content']
                                    list_text.append(TextSendMessage(text="\u2757\u27A1"+first_key['like_jobid__title']+"\u2B05\u2757\n"+
                                                    content_key+'\n'+
                                                    "工作技能:"+first_key['like_jobid__skill']+'\n'+
                                                    "更新時間:"+str(first_key['like_jobid__date'])+'\n'+
                                                    "工作薪資:"+first_key['like_jobid__salary']+'\n'+
                                                    "工作地點:"+first_key['like_jobid__local']+'\n'+
                                                    "工作連結:"+first_key['like_jobid__href']
                                                    ))
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    list_text
                                )
                            else:
                                line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(text=str('該工作類目前沒有資料!請稍後再嘗試。'))
                                )
                        except Exception as e :
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text=str(e))
                            )
                    return HttpResponse()
                else:
                    return HttpResponseBadRequest()
            except Exception as e:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="系統繁忙中")
                )
                return HttpResponse()


def get_recommend_skill(user_name,day):
    recommend_job = {}
    today = datetime.datetime.now()-datetime.timedelta(days=day)
    today = today.strftime('%Y-%m-%d')
    skill_now = Like.objects.filter(like_user_name=user_name,like_type = 'recommend',like_date__gte = today)
    for i in range(0,len(skill_now)):
        fraction = 0
        job =skill_now[i]
        user_skill = skill_now[i].like_user_skill.lower().split("、")
        job_skill = job.like_jobid.skill.split("、")
        for x in job_skill:
            if(x.lower() in user_skill):
                fraction +=1
            elif x =='不拘' or x =='無':
                fraction = -100000
            else:
                fraction -=20
        recommend_job[job] = fraction
    recommend_job = dict(sorted(recommend_job.items(),key=lambda y:(y[1]),reverse=True))
    return recommend_job
