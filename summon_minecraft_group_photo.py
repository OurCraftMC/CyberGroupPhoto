import requests
import json
import base64
from PIL import Image
import os
import math
# 每行数量
# Column count for each row
ROW_COUNT = 4
# 放大倍数
# Scale
SCALE = 60


def get_player_data_by_name(name):
    url = f"https://api.mojang.com/users/profiles/minecraft/{name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_skin_url_by_uuid(uuid):
    url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
    response = requests.get(url)
    if response.status_code == 200:
        j = response.json()
        properties = j["properties"]
        for p in properties:
            if p["name"] == "textures":
                p = p["value"]
                d = base64.b64decode(p)
                d = json.loads(d)

                return d["textures"]["SKIN"]["url"]
    else:
        return None


def get_player_skin_face(img: Image):
    img = img.crop((8, 8, 16, 16))
    return img


def get_player_skin_helm(img: Image):
    img = img.crop((40, 8, 48, 16))
    return img


def mix_skin(img: Image, helm: Image):
    # put helm on face
    r, g, b, a = helm.split()
    for i in range(0, 8):
        for j in range(0, 8):
            if r.getpixel((i, j)) == 0 and g.getpixel((i, j)) == 0 and b.getpixel((i, j)) == 0:
                a.putpixel((i, j), 0)
    helm = Image.merge("RGBA", (r, g, b, a))
    img.paste(helm, (0, 0), mask=a)
    return img


def get_player_skin_face_with_helm(name):
    if os.path.exists(f"skins/{name}.png"):
        img = Image.open(f"skins/{name}.png")
    else:
        player_data = get_player_data_by_name(name)
        if player_data is None:
            print(f"Failed to get player data of {name}")
            return None

        uuid = player_data["id"]
        skin_url = get_skin_url_by_uuid(uuid)
        if skin_url is None:
            print(f"Failed to get skin url of {name}")
            return None

        resp = requests.get(skin_url)
        if resp.status_code != 200:
            print(f"Failed to get skin of {name}")
            return None

        img = Image.open(requests.get(skin_url, stream=True).raw)
        img.save(f"skins/{name}.png")
    face = get_player_skin_face(img)
    helm = get_player_skin_helm(img)
    return mix_skin(face, helm)


def get_list_of_players():
    with open("players", "r") as f:
        return f.read().splitlines()


def get_list_of_players_face():
    players = get_list_of_players()
    ret = []
    for player in players:
        player = player.strip()
        print(f"Getting face of {player}")
        a = get_player_skin_face_with_helm(player)
        if a is None:
            raise Exception(f"Failed to get face of " +
                            f"{player}, maybe the player name is wrong")
        a = a.resize((a.width * SCALE, a.height * SCALE), Image.NEAREST)
        ret.append(a)

    return ret


if __name__ == "__main__":
    os.makedirs("skins", exist_ok=True)
    faces = get_list_of_players_face()
    if faces is None:
        print("Failed to get faces")
    else:
        width = faces[0].width
        height = faces[0].height
        new_img = Image.new(
            "RGBA", (width * ROW_COUNT, height * math.ceil(len(faces) / ROW_COUNT)))

        for i in range(len(faces)):
            x = i % ROW_COUNT
            y = i // ROW_COUNT
            new_img.paste(faces[i], (x * width, y * height))

        new_img.save("group_photo.png")
        print("Done")
