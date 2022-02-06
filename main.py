import pprint, requests, os, json

CLIENT_ID = ""
CLIENT_SECRET = ""
REFRESH_TOKEN = ''

def refresh(client_id, client_secret, refresh_token):
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    access_token = requests.post(url="https://www.googleapis.com/oauth2/v4/token",
                                 data=data).text

    pprint.pp(access_token)
    print()
    print()

    access_token = access_token.split('ya')[1]
    access_token = access_token.split('"')[0]
    access_token = "ya" + access_token

    print(access_token)
    return access_token


active = True
while active:
    try:
        file = "img.jpg"
        url = "https://api.opensea.io/api/v1/assets?order_direction=desc&offset=0&limit=50"
        web = requests.get('https://drive.google.com/drive/folders/1EjU5QTv4Z58y14LVtwjGuM2S9o7G9x88?usp=sharing').text


        def upload(file, name):
            token = access_token
            headers = {
                "Authorization": f"Bearer {token}"}  # put ur access token after the word 'Bearer '
            para = {
                "name": f"{name}",  # NAME OF UPLOAD
                "parents": ["1EjU5QTv4Z58y14LVtwjGuM2S9o7G9x88"]
                # make a folder on drive in which you want to upload files; then open that folder; the last thing in present url will be folder id
            }
            files = {
                'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
                'file': ('application/zip', open(f"./{file}", "rb"))
                # replace 'application/zip' by 'image/png' for png images; similarly 'image/jpeg' (also replace your file name)
            }
            r = requests.post(
                "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                headers=headers,
                files=files
            )
            r = r.text
            print(r)

            r = r.split()


        response = requests.request("GET", url)
        response = response.text
        response = response.split('null,"image_url":"')

        n = 0
        for i in range(50):
            jpg_link = (response[1 + n])
            jpg_link = jpg_link.split('"', 1)
            jpg_link = str(jpg_link[0])
            print(jpg_link)

            try:
                page = requests.get(jpg_link)

                f_ext = os.path.splitext(jpg_link)[-1]
                f_name = "img.jpg".format(f_ext)
                with open(f_name, 'wb') as f:
                    f.write(page.content)

            except Exception:
                pass

            response = requests.request("GET", url)
            response = response.text

            token_id = response.split('"token_id":"')
            token_id = str(token_id[1 + n])
            token_id = token_id.split('",')
            token_id = str(token_id[0])
            print(token_id)

            if f'data-tooltip="{token_id}"' in web:
                print(f"{token_id} already in drive")

            if f'data-tooltip="{token_id}"' not in web:
                if len(token_id) < 50:
                    print("character error")

                if len(token_id) >= 50:
                    try:
                        upload(file, token_id)
                        print(f"uploaded {token_id} to drive")

                    except Exception:
                        pass

            else:
                print("something went wrong")

            n += 1
            continue

        access_token = refresh(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)

        continue

    except Exception:
        access_token = refresh(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
        continue
