import argparse
import io
from fake_headers import Headers
import requests
from bs4 import BeautifulSoup as bs4
import hashlib
import re
import pandas as pd
import imagehash
from PIL import Image

seen_sites = set()


def getPicByText(req, good: dict, find_model, df_my, boook: dict):
    # print(
    #     f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={"+".join(req.split())}&_in_kw=3&_sacat=11450&_sop=12&_ipg=60&_fcid=3')
    headers = Headers(headers=True).generate()
    session = requests.Session()
    session.headers = headers
    session.timeout = (3, 7)

    try:
        ab = session.get(
            f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={"+".join(req.split())}&_in_kw=3&_sacat=11450&_sop=12&_ipg=120&_fcid=3',
            # &LH_TitleDesc=0&_odkw=boots&_osacat=0&LH_PrefLoc=98',
        )
    except:
        headers = Headers(headers=True).generate()
        session.headers = headers
        ab = session.get(
            f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={"+".join(req.split())}&_in_kw=3&_sacat=11450&_sop=12&_ipg=120&_fcid=3',
            # &LH_TitleDesc=0&_odkw=boots&_osacat=0&LH_PrefLoc=98',
        )

    soup = bs4(ab.content, 'html.parser')
    results_div = soup.find('div', {'class': 'srp-river-results clearfix'})
    if results_div is None:
        return dict()
    # extract the href attributes from all the a tags inside the div
    links = [a['href'] for a in results_div.find_all('a', {'data-interactions': True})]

    req_words = set(req.split())

    # print the links
    links = list(set(links))

    # print(len(links))

    headers = Headers(headers=True).generate()
    # good = {}
    k = 1
    total = soup.find('h1', {'class': 'srp-controls__count-heading'})
    if total:
        number = total.find('span', class_='BOLD').text
    if (number.find(" ")):
        number = 120
        try:
            ab = session.get(
                f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={"+".join(req.split())}&_in_kw=4&_sacat=11450&_sop=12&_ipg=120&_fcid=3',
                # &LH_TitleDesc=0&_odkw=boots&_osacat=0&LH_PrefLoc=98',
            )
        except:
            headers = Headers(headers=True).generate()
            session.headers = headers
            ab = session.get(
                f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={"+".join(req.split())}&_in_kw=4&_sacat=11450&_sop=12&_ipg=120&_fcid=3',
                # &LH_TitleDesc=0&_odkw=boots&_osacat=0&LH_PrefLoc=98',
            )
        all = 120
    else:
        number = min(70, int(number))
        all = len(links[:number])

    for link in links[:number]:
        # print(link)
        if (link not in seen_sites):
            seen_sites.add(link)

            try:
                ab = session.get(link,  # &LH_TitleDesc=0&_odkw=boots&_osacat=0',
                                 )
            except:
                headers = Headers(headers=True).generate()
                session.headers = headers
                ab = session.get(link)

            soup2 = bs4(ab.content, 'html.parser')
            # print(soup2)

            # model = "None"
            # print(soup2.prettify())
            # bbr = soup2.select_one('h1', class_='x-item-title__mainTitle')
            # if bbr:
            # Title = bbr.get_text(strip=True)
            # print(Title)
            # tmp = soup2.find('span', class_='tooltip__mask')
            # if (tmp):
            #     tmp = tmp.find('div', class_='x-item-title__infoOverlay_content')
            #     if tmp:
            #         tmp = tmp.find('span', class_='ux-textspans')
            #         model = tmp.text.lower()
            #     else:
            #         continue
            # else:
            #     tmp = soup2.find('div', class_='vi-swc-lsp')
            #     if tmp:
            #         model = tmp.find('span', "ux-textspans ux-textspans--BOLD").text.lower()
            #     else:
            #         continue
            # mod = set(model.split())
            # print(mod)
            # print(mod, req_words, mod.intersection(req_words) == req_words)
            # if (mod.intersection(req_words) != req_words):
            # k += 1
            # print("NO")
            # continue
            # model = req
            # print("OK")
            my_model_tmp = soup2.find("div", {"class": "ux-layout-section ux-layout-section--features"})
            if my_model_tmp:
                my_model_tmp = my_model_tmp.find("span", {"itemprop": "model"})
                if my_model_tmp:
                    my_model_tmp = my_model_tmp.find("span", {"class": "ux-textspans"}).text.lower()
                else:
                    continue
            else:
                continue
            cooon = True
            if my_model_tmp != find_model:
                if len(df_my[df_my.model == my_model_tmp]) > 0:
                    cooon = False
                    print("cooon", find_model, my_model_tmp)
                else:
                    continue
            # else:
            #     print(find_model, my_model_tmp)
            model = str(my_model_tmp)
            fin = re.compile(r"https:\/\/i\.ebayimg\.com\/(?!thumbs\/)images\/g\/[a-zA-Z0-9]*\/s-l500\.jpg").findall(
                str(soup2.contents))  # soup2.find_all(string=)#[0-9]{2,3}.jpg"))
            # print(list(set(fin)))
            for ind, i in enumerate(list(set(fin))):
                try:
                    img_data = session.get(i)
                except:
                    headers = Headers(headers=True).generate()
                    session.headers = headers
                    img_data = session.get(i)

                if (img_data):
                    img_data = img_data.content
                    with Image.open(io.BytesIO(img_data)) as img:
                        tmp = str(imagehash.average_hash(img, 24))
                        # print(tmp)
                    # tmp = hashlib.md5(img_data).hexdigest()
                    if cooon:
                        good[model] = good.get(model, set())
                        if tmp not in good[model]:
                            good[model].add(tmp)
                    else:
                        boook[my_model_tmp] = boook.get(my_model_tmp, set())
                        if tmp not in boook[my_model_tmp]:
                            boook[my_model_tmp].add(tmp)
                else:
                    print(f"!!!!!!!!!!!!!!!!!!!!!!!!!\nurl = {i}")

        print(f"{k} / {all} are done")
        k += 1
    return good, boook


def parse(start_from, misc_id):
    classes = pd.read_csv(r"D:\Kaggle\CleanCodeCup\2023\2023\classes.csv")
    misc_df = pd.read_csv(fr"D:\Kaggle\CleanCodeCup\2023\2023\everything_ebay\all_csv\middle\misc{misc_id}.csv", index_col=False)

    STATE = "old"  # new
    OLD_ID = start_from
    if STATE == "new":
        df = pd.DataFrame(columns=["brand", "hash"])
    else:
        df = pd.read_csv(rf"D:\Kaggle\CleanCodeCup\2023\2023\everything_ebay\all_csv\middle\temp_result_fin_avg{OLD_ID}.csv")

    for index, row in classes.iterrows():
        if index <= start_from:
            continue
        # print(classes.at[index, "model"])
        if classes.at[index, "brand"] in classes.at[index, "model"]:
            result = classes.at[index, "model"]
        else:
            result = classes.at[index, "brand"] + " " + classes.at[index, "model"]
        try:
            # print(classes.at[index, "model"])
            data, boook = getPicByText(result, dict(), classes.at[index, "model"], classes, dict())
            df1 = pd.DataFrame(data.items(), columns=["brand", "hash"])
            if len(boook) != 0:
                if index % 3 == 0:
                    df1_misc = pd.DataFrame(boook.items(), columns=["brand", "hash"])
                    misc_df = pd.concat([misc_df, df1_misc])
                    misc_df.to_csv(f"D:/Kaggle/CleanCodeCup/2023/2023/everything_ebay/all_csv/middle/misc{index}.csv",
                                   index=False)
            df1['idx'] = index
            df = pd.concat([df, df1])
            # if index % 1 == 0:
            df.to_csv(f"D:/Kaggle/CleanCodeCup/2023/2023/everything_ebay/all_csv/middle/temp_result_fin_avg{index}.csv",
                      index=False)
        except:
            data, boook = getPicByText(result, dict(), classes.at[index, "model"], classes, dict())
            df1 = pd.DataFrame(data.items(), columns=["brand", "hash"])
            if len(boook) != 0:
                if index % 5 == 0:
                    df1_misc = pd.DataFrame(boook.items(), columns=["brand", "hash"])
                    misc_df = pd.concat([misc_df, df1_misc])
                    misc_df.to_csv(f"D:/Kaggle/CleanCodeCup/2023/2023/everything_ebay/all_csv/middle/misc{index}.csv",
                                   index=False)
            df1['idx'] = index
            df = pd.concat([df, df1])
            # if index % 1 == 0:
            df.to_csv(f"D:/Kaggle/CleanCodeCup/2023/2023/everything_ebay/all_csv/middle/temp_result_fin_avg{index}.csv",
                      index=False)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--start', help='start_id', required=True, default=400)
parser.add_argument('--misc', help='misc', required=True, default=627)
args = parser.parse_args()
print(args)
parse(int(args.start), int(args.misc))