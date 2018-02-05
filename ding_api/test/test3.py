import json
#一个把list处理为string作为sql语句的函数
#问题list中嵌套list+dict时引号重复
def list2string(sqlist, types):
    string=''
    #type为keys表示键，values表示值。键加``值加""。
    if types == 'keys': 
        for i in range(len(sqlist)):
            if i != len(sqlist)-1: #最后一个特殊处理
                if type(sqlist[i]) == bool:
                    string = string + '`%d`,' % sqlist[i]
                elif type(sqlist[i]) == unicode:
                    string = string + '`%s`,'% sqlist[i]
                else:
                    string = string + '`' + str(sqlist[i]) + '`,'
            else:
                if type(sqlist[i]) == bool:
                    string = string + '`%d`' % sqlist[i]
                elif type(sqlist[i]) == unicode:
                    string = string + '`%s`'% sqlist[i]
                else:
                    string = string + '`' + str(sqlist[i]) + '`'        
    elif types == 'values':
        for i in range(len(sqlist)):
            if i != len(sqlist)-1: #最后一个特殊处理
                if type(sqlist[i]) == bool:
                    string = string + '\'%d\',' % sqlist[i]
                elif type(sqlist[i]) == unicode:
                    string = string + '\'%s\','% sqlist[i]
                elif type(sqlist[i]) == dict:
                    string = string + '\'' + json.dumps(sqlist[i], ensure_ascii=False) + '\','
                elif type(sqlist[i]) == list:
                    string = string + '\'[' + list2string(sqlist[i], types='no_wrapper') + ']\','
                else:
                    string = string + '\'' + str(sqlist[i]) + '\', '
            else:
                if type(sqlist[i]) == bool:
                    string = string + '\'%d\'' % sqlist[i]
                elif type(sqlist[i]) == unicode:
                    string = string + '\'%s\''% sqlist[i]
                elif type(sqlist[i]) == dict:
                    string = string + '\'' + json.dumps(sqlist[i], ensure_ascii=False) + '\''
                elif type(sqlist[i]) == list:
                    string = string + '\'[' + list2string(sqlist[i], types='no_wrapper') + ']\''
                else:
                    string = string + '\'' + str(sqlist[i]) + '\''
    elif types == 'no_wrapper':
        for i in range(len(sqlist)):
            if i != len(sqlist)-1: #最后一个特殊处理
                if type(sqlist[i]) == bool:
                    string = string + '%d,' % sqlist[i]
                elif type(sqlist[i]) == unicode:
                    string = string + '%s,' % sqlist[i]
                elif type(sqlist[i]) == dict:
                    string = string + json.dumps(sqlist[i], ensure_ascii=False) + ','
                elif type(sqlist[i]) == list:
                    string = string + list2string(sqlist[i], types='no_wrapper') + ','
                else:
                    string = string + str(sqlist[i]) + ','
            else:
                if type(sqlist[i]) == bool:
                    string = string + '%d' % sqlist[i]
                elif type(sqlist[i]) == unicode:
                    string = string + '%s'% sqlist[i]
                elif type(sqlist[i]) == dict:
                    string = string + json.dumps(sqlist[i], ensure_ascii=False)
                elif type(sqlist[i]) == list:
                    string = string + list2string(sqlist[i], types='no_wrapper')
                else:
                    string = string + str(sqlist[i])
    else:
        string = string + ''
    return string



def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input




dicts = {u'tel': u'', u'isLeaderInDepts': u'{56590897:false}', u'dingId': u'$:LWCP_v1:$3zK1mwC5mQy3T+kzXPur0g==', u'openId': u'viiaNUkmcIdZVvKmHysTHxgiEiE', u'isAdmin': True, u'department': [56590897], u'email': u'', u'stateCode': u'86', u'extattr': {}, u'isBoss': True, u'workPlace': u'', u'active': True, u'remark': u'', u'name': u'\u9ad8\u9e4f', u'roles': [{u'groupName': u'\u9ed8\u8ba4', u'id': 271298995, u'name': u'\u8d1f\u8d23\u4eba'}, {u'groupName': u'\u9ed8\u8ba4', u'id': 271298993, u'name': u'\u4e3b\u7ba1\u7406\u5458'}], u'orderInDepts': u'{56590897:176400858992700512}', u'mobile': u'13126672772', u'unionid': u'viiaNUkmcIdZVvKmHysTHxgiEiE', u'userid': u'13570206541269367', u'isHide': False, u'avatar': u'', u'position': u'', u'isSenior': True, u'jobnumber': u''}

print list2string(dicts.values(),'values')
#print byteify(dicts)
