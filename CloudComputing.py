import boto3
import time
from key import AWS_ACCESS_KEY_ID, AWS_SCRET_ACCESS_KEY

s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SCRET_ACCESS_KEY)

region_bucketname = {
    'Mumbal': 'ssmmumbal',
    'Seoul': 'ssmseoul',
    'Singapore': 'ssmsingapor',
    'Sydney': 'ssmsydney',
    'Tokyo': 'ssmdokyo',
    'Canada': 'ssmcanada',
    'Frankfurt': 'ssmfrankfurt',
    'Ireland': 'ssmireland',
    'London': 'ssmlondon',
    'Paris': 'ssmparis',
    'Sao Paulo': 'ssmsaopaulo',
    'Virgina': 'ssmvirgina',
    'Ohio': 'ssmohio',
    'California': 'ssmcalifornia',
    'Oregon': 'ssmoregon',
}

upload_times = []
download_times = []
delete_times = []


def time_average(times):
    sum = 0
    for i in times:
        sum += i
    return round(sum/len(times), 2)


def init(size):
    upload_times = []
    download_times = []
    delete_times = []
    # put get delete 순서로 진행
    for region in region_bucketname:
        for i in range(0, 10):

            # 업로드
            upload_start = time.time()
            s3.upload_file(size, region_bucketname[region], size)
            upload_end = time.time()

            # 다운로드
            download_start = time.time()
            s3.download_file(region_bucketname[region], size, size)
            download_end = time.time()

            # 삭제

            delete_start = time.time()
            s3.delete_object(Bucket=region_bucketname[region], Key=size)
            delete_end = time.time()

            upload_time = upload_end - upload_start
            download_time = download_end - download_start
            delete_time = delete_end - delete_start

            upload_times.append(round(upload_time, 2))
            download_times.append(round(download_time, 2))
            delete_times.append(round(delete_time, 2))

        print(f"지역: {region}")
        print(f"파일크기: {size}")
        print(f"평균 put 시간: {time_average(upload_times)}")
        print(f"평균 get 시간: {time_average(download_times)}")
        print(f"평균 delete 시간: {time_average(delete_times)}")
        print("")
        upload_times = []
        download_times = []
        delete_times = []
    print("")
    print("--------------------------------------")
    print("")

init("1KB")
init("10KB")
init("1MB")
init("10MB")

