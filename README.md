# CyberGroupPhoto

Language: [English](/README.md) | [中文](/docs/README-zh.md)

## What can it do?
Given a list of Minecraft players, it can automatically retrieve their current skins and generate a group photo like the one shown below.
![](/docs/imgs/example1.png)

Note: The number of avatars per row can be adjusted. In this example, there are 4.

## How to use?

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Provide player list
Fill in the player names in `players`, one per line.

### 3. Adjust avatars per row
Modify the `ROW_COUNT` value in `summon_minecraft_group_photo.py`.

### 4. Run the script
```bash
python summon_minecraft_group_photo.py
```

### 5. View the result
The group photo will be saved as `group_photo.png`.