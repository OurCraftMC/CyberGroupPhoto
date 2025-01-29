# CyberGroupPhoto
## 他能做什么？
提供Minecraft玩家名单的情况下，他能自动获取玩家当前的皮肤并生成一张如下图的合照。
![](/docs/imgs/example1.png)

注：每行头像的数量可以调整，这里是4个。

## 如何使用？

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 填写玩家名单
在`players`中填写玩家名单，每行一个。

### 3. 调整每行头像数量

在`summon_minecraft_group_photo.py`中修改`ROW_COUNT`的值即可。

### 4. 运行
```bash
python summon_minecraft_group_photo.py
```

### 5. 查看结果

合照会保存在`group_photo.png`中。