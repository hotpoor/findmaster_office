f_int_old=open("version.txt").read()
f_int=int(f_int_old)
f_int = f_int+1
f=open("version.txt","w")
f.write( "%s"%f_int)
f.close()
f=open("version.py","w")
f.write( "version_num=%s"%f_int)
f.close()