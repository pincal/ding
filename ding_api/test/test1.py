from dingding_sdk import config
from dingding_sdk import auth
from dingding_sdk import user
from dingding_sdk import department
from dingding_sdk import utils

##access_token = dingding_sdk.auth.get_access_token(dingding_sdk.config.CorpID,dingding_sdk.config.secret)
##if access_token[0] != True:
##    print 'get access_token error!'
##department_list = dingding_sdk.department.get_department_list(access_token[1]['access_token'], False, 56590897)
##if department_list[0] != True:
##    print 'get department_list error!'


is_success, result = auth.get_access_token(config.CorpID, config.Secret)
if is_success == True:
    access_token = result.get('access_token')
else:
    print 'access_token error!'


#is_success, result = department.create_department(access_token,u'钉钉测试1',1)

#is_success, result = department.update_department(access_token, u'钉钉测试2', 59057510, 1, u'59071175')

#is_success, result = department.delete_department(access_token,u'59071175')

#is_success, result = department.get_department_detail(access_token, u'56590897')

#is_success, result = department.get_parent_depts_by_dept(access_token, u'59057510')

#is_success, result = department.get_parent_depts_by_user(access_token, u'13570206541269367') #这里必须是uniconde

#is_success, result = user.get_department_simple_userlist(access_token, u'56590897')
#print result.get('userlist')[0].get('name')

#info = user.get_department_simple_userlist(access_token, u'56590897',u'1', u'10')
#info = user.get_department_simple_userlist(access_token, u'56590897')

#info = user.get_department_detail_userlist(access_token, u'56590897')
info = user.get_department_detail_userlist(access_token, u'56590897',u'1', u'10')

#is_success, result = user.get_user(access_token, u'13570206541269367')

#is_success, result = user.delete_user(access_token, u'135665061520924093')

#is_success, result = user.create_user(access_token, None, u'测试汪',(u'59057510',), u'13263339686',u'test@test.com',u'测试职位2')

#is_success, result = user.update_user(access_token, u'135665061528025280', u'测试miao',(u'59057510',), u'13263339686',u'test@test.com',u'测试职位2')



#is_success, result = department.create_department(access_token,u'测试111',u'1')

#is_success, result = department.create_department_kw(access_token,u'测试333',u'1',deptHiding=True)

#is_success, result = department.update_department_kw(access_token,u'58970743',deptHiding=False)

#is_success, result = department.update_department(access_token,u'58970743',deptHiding=True)

#is_success, result = user.create_user(access_token, None, u'测试汪',(u'59057510',), u'13263339686',u'test@test.com',u'测试职位2')
#is_success, result = user.create_user(access_token, None, u'测试汪',(u'59057510',), u'13263339686',email=u'test@test.com',position=u'测试职位2')



print is_success, result
