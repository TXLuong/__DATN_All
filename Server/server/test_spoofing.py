path_data_fake = "/home/luong/Desktop/real_and_fake_face/training_fake/"
path_data_real = "/home/luong/Desktop/real_and_fake_face/training_real/"
list_data_fake = os.listdir(path_data_fake)
easy_data_fake = [i for i in list_data_fake if "easy" in i]
easy_data_fake = [path_data_fake + i for i in easy_data_fake]
res_fake = []
for file in easy_data_fake :
    res_fake.append(check_spoofing(file))
print("res-fake", res_fake)
f = open("/home/luong/Desktop/easy_fake.txt", "a")
f.write(res_fake)
f.close()

# ---- real----
list_data_real = os.listdir(path_data_real)
easy_data_real = [path_data_real+ i for i in list_data_real]
res_real = []
for i in range(len(easy_data_real)):
    res_real.append(check_spoofing(easy_data_real[i]))
f = open("/home/luong/Desktop/easy_real.txt","a")
print(check_spoofing("/home/luong/Pictures/Webcam/2021-06-15-165120.jpg"))
print(res_real)
f.write(" ".join([str(i) for i in res_real]))
f.close()