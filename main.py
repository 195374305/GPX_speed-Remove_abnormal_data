import gpxpy
import gpxpy.gpx
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame(columns=['lat','lon','speed','elevation','time'])
gpx_file = open('C:\\Users\\Administrator\\Desktop\\20231028登山.gpx','r',encoding='utf-8')

gpx = gpxpy.parse(gpx_file)

for track in gpx.tracks:
    print(track.name)
    for segment in track.segments:
        oldPoint = segment.points[0]
        for point in segment.points:
            print(point.latitude,point.longitude,point.elevation)
            newPoint = point    
            #这个直接计算出速度补全        
            speed = point.speed_between(oldPoint)
            oldPoint = newPoint
            print(speed)
            point.speed = speed #这个补全原来的数据偷懒的话可以直接用这个后保存
            gpx.add_missing_speeds() #这个补全原来的数据偷懒的话可以直接用这个后保存
            
            # 导入到pandas
            df.loc[len(df.index)] =[point.latitude,point.longitude,point.speed,point.elevation,point.time]

# 从pandas去除异常数据
std = df['speed'].std()
threshold = std * 7  # 7为标准差倍数，可以打印出图片 按照图像来修改系数
df = df.drop(df[df['speed'] > threshold].index)
df = df.dropna()


###########
print(df)
# plt.bar(x=df.index,height=df.speed)
plt.scatter(x=df.lon,y=df.lat,c=df.speed,cmap='RdYlBu')
plt.colorbar()
plt.show()



print('GPX:', gpx.to_xml())

# xml = gpx.to_xml()
# # 将XML字符串写入一个新的文件
# with open('new_gpx.gpx', 'w', encoding='utf-8') as f:
#    f.write(xml)


##################################
#生成一个新的gpx文件
# 创建一个新的GPX对象
gpx = gpxpy.gpx.GPX()

# 添加一个新的GPX track
track = gpxpy.gpx.GPXTrack()
gpx.tracks.append(track)

# 添加一个新的GPX segment
segment = gpxpy.gpx.GPXTrackSegment()
track.segments.append(segment)

# 添加一些坐标点
for row in df.itertuples():
    segment.points.append(gpxpy.gpx.GPXTrackPoint(latitude=row.lat, longitude=row.lon, elevation=row.elevation, time=row.time, speed= round(row.speed,8))) #节省文件大小压缩speed小数位

gpx.creator = 'Health'
# 将GPX对象写入文件
with open('new_gpx.gpx', 'w') as f:
   f.write(gpx.to_xml(version='1.0'))


#生成的文件需要修改成  version="1.0" creator="Health"
