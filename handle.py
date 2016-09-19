#!/usr/bin/python
# coding=utf-8

import sys,os
from hashlib import md5
from optparse import OptionParser

#定义一些常量
#用于过滤项目的标志
FLAG_FILE_NAME="index.android.js"

#编译目标目录
TARGET_PATH="~/projects/client_dasheng/cilent/trunk/"
TARGET_PATH=os.path.expanduser(TARGET_PATH)

#生成目标目录
DEST_PATH="~/projects/TestHotUpdate/public"
DEST_PATH=os.path.expanduser(DEST_PATH)

#切换到文件所在目录
os.chdir(os.path.abspath(sys.path[0]))
os.environ['LANG']="zh_CN.UTF-8"


# 全局变量
g_args_dict={}
g_compile_project_list=[]

# 检查环境
def CheckEnv():
    # 判断生成路径
    global TARGET_PATH
    if TARGET_PATH=="":
        CheckRet(-1, "请设置TARGET_PATH作为打包目标目录")
        pass

    # 判断svn和版本
    ret=os.system("svn --help 1>/dev/null")
    CheckRet(ret, "svn不存在")
    ret=os.popen("svn  --version | grep -E \"1\\.9\.*\" | wc -l").readlines()[0][:-1].strip()
    CheckRet((0 if ret=="1" else -1), "svn版本不正确")
    
    # 判断是否为tag
    #ret=os.popen("svn info | grep /tag | wc -l").readlines()[0][:-1].strip()
    #CheckRet((0 if int(ret)>=1 else -1), "请使用tag，不要使用trunk")
    
    # 检查rsync命令
    #ret=os.system("rsync --help 1>/dev/null")
    #CheckRet(ret, "rsync不存在")
    pass

#检查执行结果
def CheckRet(ret, err_str):
    if int(ret)!=0:
        print err_str
        exit(1)
        pass
    pass

# 检查目录  没有就创建它
def CheckAndCreateDir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        pass
    pass

#对文件做md5
def Md5File(name):
    m = md5()
    fd = open(name, 'rb')
    m.update(fd.read())
    fd.close()
    return m.hexdigest()
    pass

# 解析命令参数
def DoArgParse():
    parser = OptionParser("用法:%prog [-option]")
    
    
    parser.add_option("--sendonly",         dest="op_sendonly", action="store_true",    help="可选参数，仅同步到外网")
    parser.add_option("--sendallonly",      dest="op_sendallonly",  action="store_true",    help="可选参数，仅同步到外网，但包含整个package目录")
    parser.add_option("-f", "--forcedelete",    dest="op_forcedelete",  action="store_true",    help="可选参数，是否强制删除外网相关工程的其他包")
    
    parser.add_option("-c", "--cleanonly",      dest="op_cleanonly",    action="store_true",    help="可选参数，仅清除项目，不编译，不打包")
    parser.add_option("-b", "--buildonly",      dest="op_buildonly",    action="store_true",    help="可选参数，仅编译，不清除，不打包")
    parser.add_option("-p", "--buildpack",      dest="op_buildpack",    action="store_true",    help="可选参数，仅编译打包，不清除")
    parser.add_option("-m", "--md5allonly",         dest="op_md5allonly",   action="store_true",    help="可选参数，仅md5所有包")
    parser.add_option("--md5only",          dest="op_md5only",  action="store_true",    help="可选参数，仅md5包")
    parser.add_option("--onlybundlejs",          dest="op_onlybundlejs",  action="store_true",    help="可选参数，仅生成bundlejs包")
    parser.add_option("--platform", dest="platform",  help="要编译或打包的平台",) 

    (options, args) = parser.parse_args()
    global g_args_dict
    
    if len(args) < 1:
        parser.error("缺少编译项目名，编译全部请写all")
    elif len(args) ==1 and args[0] == "all":
        g_args_dict["project_name"] = "all"
        pass
    else:
        g_args_dict["project_name"] = args
        pass

    if options.op_sendonly == True:
        g_args_dict["sendonly"] = True
        pass
    else:
        g_args_dict["sendonly"] = False
        pass
    
    if options.op_sendallonly == True:
        g_args_dict["sendallonly"] = True
        pass
    else:
        g_args_dict["sendallonly"] = False
        pass
    
    if options.op_forcedelete == True:
        g_args_dict["forcedelete"] = True
        pass
    else:
        g_args_dict["forcedelete"] = False
        pass
    
    if options.op_cleanonly == True:
        g_args_dict["cleanonly"] = True
        pass
    else:
        g_args_dict["cleanonly"] = False
        pass
    
    if options.op_buildonly == True:
        g_args_dict["buildonly"] = True
        pass
    else:
        g_args_dict["buildonly"] = False
        pass
    
    if options.op_buildpack == True:
        g_args_dict["buildpack"] = True
        pass
    else:
        g_args_dict["buildpack"] = False
        pass
    if options.op_onlybundlejs == True:
        g_args_dict["onlybundlejs"] = True
        pass
    else:
        g_args_dict["onlybundlejs"] = False
        pass

    if not options.platform:
        g_args_dict["platform"] = "android|ios"
        pass
    elif options.platform == "ios" or options.platform == "android":
        g_args_dict["platform"] = options.platform
        pass
    else:
        CheckRet(-1, "platform 必需为ios || android")
        pass
    pass

# 筛选编译项目
def FilterCompilePrj():
    global g_compile_project_list
    global g_args_dict
    tmp_prj_list=[]
    for prj in os.listdir(TARGET_PATH):
        tmp_cnf_file = "%s/%s/%s"%(TARGET_PATH, prj, FLAG_FILE_NAME)
        if(os.path.isfile(tmp_cnf_file)):
            tmp_prj_list.append(prj)
            pass
        pass

    if g_args_dict["project_name"] == "all":
        g_compile_project_list=tmp_prj_list
        return
    else:
        g_compile_project_list=[]
        for prj in g_args_dict["project_name"]:
            if prj in tmp_prj_list :
                g_compile_project_list.append(prj)
                pass
            else:
                print "project[%s]不存在"%prj
                exit(1)
                pass
            pass
        pass
    pass

#生成IOS的ipa包
def PackIos(prj, app_name, target_path, version_name):
    print "##############开始生成IPA##############"
    build_dir="%s%s/ios/build/Debug-iphoneos/"%(TARGET_PATH, prj)
    print build_dir  

    cmd="cd %s; rm -rf Payload; mkdir Payload; cp -r %s.app Payload/; zip -r %s.ipa Payload; "%(build_dir, prj, app_name)
    ret=os.system(cmd)
    CheckRet(ret, "项目【%s】打包失败"%prj)
    
    cmd="cd %s; rm -rf %s.app.dSYM.zip; zip -r %s.app.dSYM.zip %s.app.dSYM; "%(build_dir, app_name, app_name, prj)
    ret=os.system(cmd)
    CheckRet(ret, "项目【%s】打包失败"%prj)
    
    cmd="mkdir -p %s/; "%(target_path)
    ret=os.system(cmd)
    CheckRet(ret, "项目【%s】打包失败"%prj)
    
    cmd="cd %s; mv -v %s.ipa %s/; "%(build_dir, app_name, target_path)
    ret=os.system(cmd)
    CheckRet(ret, "项目【%s】打包失败"%prj)

    cmd="cd %s; mv -v %s.app.dSYM.zip %s/; "%(build_dir, app_name, target_path)
    ret=os.system(cmd)
    CheckRet(ret, "项目【%s】打包失败"%prj)
    print "##############结束生成IPA##############"
    pass

#生成android的apk包
def PackAndroid(prj, app_name, target_path, version_name):
    print "##############开始生成APK##############"
    build_dir="%s%s/android/app/build/outputs/apk"%(TARGET_PATH, prj)
    cmd="mkdir -p %s/; "%(target_path)
    ret=os.system(cmd)
    CheckRet(ret, "项目【%s】打包失败"%prj)

    cmd="cd %s; mv -v app-release-unsigned.apk %s/%s.apk; "%(build_dir, target_path, app_name)
    print cmd
    ret=os.system(cmd)
    CheckRet(ret, "项目【%s】打包失败"%prj)
    print "##############结束生成APK##############"
    pass


#生成bundlejs差异
def DiffPackage(des_bundle_path, bunlde_ver_list, new_bundle_ver, platform):
    print "##############开始[%s]生成差异文件##############"%platform
    tmp_file_name="index.%s.bundle"% platform
    #遍历每一个版本生成bundle的差异包
    tmp_new_bundle_ver_bundle_path="%s%s"%(des_bundle_path, new_bundle_ver)
    for bundle_ver in bunlde_ver_list:
        tmp_bundle_ver_file="%s%s/%s"%(des_bundle_path, bundle_ver, tmp_file_name)
        tmp_new_bundle_ver_bundle_file="%s/%s"%(tmp_new_bundle_ver_bundle_path, tmp_file_name)
        tmp_patch_file="%s/bundle_%s_%s.patch"%(tmp_new_bundle_ver_bundle_path, new_bundle_ver, bundle_ver)
        #开始生成差异
        ret=os.system("bsdiff %s %s %s"%(tmp_bundle_ver_file, tmp_new_bundle_ver_bundle_file, tmp_patch_file))
        CheckRet(ret, "生成[%s] patch 失败"%tmp_patch_file)
    
    print "##############生成[%s]差异文件结束##############"%platform
    pass


# 生成 android bundle.js打包
def PackBundleJs(prj, app_version, platform):
    print "##############开始[%s]生成bundlejs文件##############"%platform
    tmp_target_path=("%s/package/%s/%s/%s/"%(DEST_PATH, prj, platform, app_version))
    #生成bundle包目录
    tmp_des_bundle_path=("%sdiff/"%(tmp_target_path))
    print tmp_des_bundle_path
    CheckAndCreateDir(tmp_des_bundle_path)
    #删除生成的临时包
    cmd="cd %s; rm -rf tmp; mkdir tmp;"%tmp_target_path
    ret=os.system(cmd)
    CheckRet(ret, "打BundleJs包失败")

    #获取已经生成最高版本号
    tmp_bunlde_ver_list=[]
    for v in os.listdir(tmp_des_bundle_path):
        if v[0]!=".":
            tmp_bunlde_ver_list.append(v)
            pass
        pass
    tmp_bunlde_ver_list.sort(reverse=True)

    #打android js 包
    cmd="cd %s%s; react-native bundle —minify --entry-file index.%s.js  --platform %s  --dev false --bundle-output %s/tmp/index.%s.bundle"%(TARGET_PATH, prj, platform, platform, tmp_target_path, platform)
    ret=os.system(cmd)
    CheckRet(ret, "打BundleJs包失败")
    
    #新版本号如果没有默认值
    tmp_new_bundle_ver="1.0.0"
    #用最新生成的包的md5码对比已经生成的最高版本号
    if(len(tmp_bunlde_ver_list) != 0) :
        tmp_new_bundle_md5=Md5File("%s/tmp/index.%s.bundle"%(tmp_target_path, platform))
        last_bundle_md5=Md5File("%s/%s/index.%s.bundle"%(tmp_des_bundle_path, tmp_bunlde_ver_list[0], platform))
        #不相等时，创建新bundle版本号
        if(tmp_new_bundle_md5!=last_bundle_md5) :
            tmp_last_ver_list=tmp_bunlde_ver_list[0].split('.');
            tmp_last_ver=int(tmp_last_ver_list[2])+1
            tmp_last_ver_list[2]=str(tmp_last_ver)
            #生成最新版本号
            tmp_new_bundle_ver='.'.join(tmp_last_ver_list)
            pass
        else: 
            print "##############版本号为[%s]的index.%s.bundle已经是最新##############"%(tmp_bunlde_ver_list[0], platform)
            return
            pass
        pass

    tmp_new_bundle_ver_path="%s%s"%(tmp_des_bundle_path, tmp_new_bundle_ver)

    CheckAndCreateDir(tmp_new_bundle_ver_path)
    cmd="cd %s; mv -v tmp/index.%s.bundle %s%s/; "%(tmp_target_path, platform, tmp_des_bundle_path, tmp_new_bundle_ver)
    ret=os.system(cmd)
    CheckRet(ret, "打BundleJs包失败")

    print "##############结束[%s]生成bundlejs文件##############"%platform
    #生成bundlejs差异包
    DiffPackage(tmp_des_bundle_path, tmp_bunlde_ver_list, tmp_new_bundle_ver, platform)
    pass


# 编译IOS项目
def CompilePrjIos():
    global g_compile_project_list
    global g_args_dict
    for prj in g_compile_project_list:
        print prj
        # 获取项目版本号
        cmd="/usr/libexec/PlistBuddy -c \"Print CFBundleShortVersionString\" %s%s/ios/%s/Info.plist "%(TARGET_PATH, prj, prj)
        tmp_version=os.popen(cmd).readlines()[0][:-1]

        #只编译生成bundlejs包
        if not g_args_dict["onlybundlejs"] == True:
            #清理项目
            # if not g_args_dict["buildonly"] and not g_args_dict["buildpack"] :
            #     ret=os.system("xcodebuild -project %s%s/ios/%s.xcodeproj -configuration Debug clean"%(TARGET_PATH, prj, prj))
            #     CheckRet(ret, "project[%s] clean 失败"%prj)
                
            #     if g_args_dict["cleanonly"] == True:
            #         print "项目【%s】清理完成"%(prj)
            #         continue
            #     pass
            # pass

            #开始编译项目
            print ("xcodebuild -project %s%s/ios/%s.xcodeproj -configuration Debug build -sdk iphoneos"%(TARGET_PATH, prj, prj))
            ret=os.system("xcodebuild -archive %s%s/ios/%s.xcodeproj -configuration Debug build -sdk iphoneos"%(TARGET_PATH, prj, prj))
            CheckRet(ret, "project[%s] build 失败"%prj)

            #开始打包app
            if not g_args_dict["buildonly"] :
                #包名称
                tmp_target_name=("%s_%s"%(prj, tmp_version))
                tmp_target_path=("%s/package/%s/%s"%(DEST_PATH, prj, tmp_version))
                PackIos(prj, tmp_target_name, tmp_target_path, tmp_version)
                pass
            pass

        #生成jsbundle
        PackBundleJs(prj, tmp_version, "ios")
    pass

# 编译ANDROID项目
def CompilePrjAndroid():
    global g_compile_project_list
    global g_args_dict
    for prj in g_compile_project_list:
        
        # 获取项目版本号
        cmd="grep -E \"versionName.* .*0\" %s%s/android/app/build.gradle"%(TARGET_PATH, prj)
        tmp_version=os.popen(cmd).readlines()[0][:-1].strip().split()[1].strip('\"')

        #只编译生成bundlejs包
        if not g_args_dict["onlybundlejs"] == True:
            #清理项目
            if not g_args_dict["buildonly"] and not g_args_dict["buildpack"] :
                ret=os.system("cd %s%s/android; ./gradlew clean"%(TARGET_PATH, prj))
                CheckRet(ret, "project[%s] clean 失败"%prj)
                
                if g_args_dict["cleanonly"] == True:
                    print "项目【%s】清理完成"%(prj)
                    continue
                pass
            pass

            #设置metadata.android.json的版本号
            ret=os.system("sed -i '' 's#minContainerVersion.*,#minContainerVersion\": \"%s\",#g' %s/%s/android/app/src/main/assets/metadata.android.json"%(tmp_version, TARGET_PATH, prj))
            CheckRet(ret, "项目[%s]metadata.android.json配置修改失败"%prj)

            #开始编译项目
            ret=os.system("cd %s%s/android; ./gradlew assembleRelease"%(TARGET_PATH, prj))
            CheckRet(ret, "project[%s] build 失败"%prj)
            
            #开始打包app
            if not g_args_dict["buildonly"] :
                #包名称
                tmp_target_name=("%s_%s"%(prj, tmp_version))
                tmp_target_path=("%s/package/%s/android/%s/"%(DEST_PATH, prj, tmp_version))
                PackAndroid(prj, tmp_target_name, tmp_target_path, tmp_version)
                pass
            pass
        #生成jsbundle
        PackBundleJs(prj, tmp_version, "android")
    pass


if __name__ == "__main__":
    CheckEnv()
    DoArgParse()
    if g_args_dict["buildonly"] or g_args_dict["buildpack"] or g_args_dict["onlybundlejs"]:
        FilterCompilePrj()
        pass
    if g_args_dict["platform"] == "android|ios":
        CompilePrjIos()
        CompilePrjAndroid()
        pass
    elif g_args_dict["platform"] == "android":
        CompilePrjAndroid()
        pass
    else:
        CompilePrjIos()
        pass
   
    pass
