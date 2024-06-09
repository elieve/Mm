################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

import os
import re
import time
from datetime import timedelta
from time import time
from urllib.parse import urlparse

import requests
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL

from Mix import Emojik, cgr, get_cgr, ky, nlx, progress

__modles__ = "Download"
__help__ = get_cgr("help_download")


async def download_youtube(link, as_video=True):
    ydl_opts = {
        "format": "bestvideo+bestaudio/best" if as_video else "bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "merge_output_format": "mp4" if as_video else "mp3",
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=True)
        print(f"info_dict")
        file_name = ydl.prepare_filename(info_dict)
        title = info_dict.get("title", None)
        url = info_dict.get("webpage_url", None)
        duration = info_dict.get("duration", 0)
        views = info_dict.get("view_count", 0)
        channel = info_dict.get("uploader", None)
        thumb = info_dict.get("thumbnail", None)
        data_ytp = (
            "**Type: `{}`**\n"
            "**Title: `{}`**\n"
            "**Duration: `{}`**\n"
            "**Views: `{}`**\n"
            "**Channel: `{}`**\n"
            "**URL: [url]({})**\n"
            "**Downloaded by: {}**"
        )
    return file_name, title, url, duration, views, channel, thumb, data_ytp


def download_thumbnail(url):
    thumb_path = "thumbnail.jpg"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(thumb_path, "wb") as f:
            f.write(response.content)
    else:
        thumb_path = None
    return thumb_path


@ky.ubot("vtube", sudo=True)
async def _(c, m):
    em = Emojik()
    em.initialize()
    if len(m.command) < 2:
        return await m.reply(cgr("down_1").format(em.gagal, m.command))
    pros = await m.reply(cgr("proses").format(em.proses))
    query = m.text.split(None, 1)[1]
    if re.match(r"^https?://", query):
        link = query
    else:
        try:
            search = VideosSearch(query, limit=1).result()["result"][0]
            link = f"https://youtu.be/{search['id']}"
        except Exception as error:
            return await pros.reply_text(cgr("err").format(em.gagal, error))
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb_url,
            data_ytp,
        ) = download_youtube(link, as_video=True)
    except Exception as error:
        return await pros.reply_text(cgr("err").format(em.gagal, error))
    thumbik = wget.download(thumb_url)
    await c.send_video(
        m.chat.id,
        video=file_name,
        thumb=thumbik,
        file_name=title,
        duration=duration,
        supports_streaming=True,
        caption=cgr("yutup").format(
            "Video",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            c.me.mention,
        ),
        progress=progress,
        progress_args=(
            pros,
            time(),
            cgr("proses").format(em.proses),
            f"{file_name}",
        ),
        reply_to_message_id=m.id,
    )
    await pros.delete()
    await m.delete()
    for files in (thumbik,file_name):
        try:
            if files and os.path.exists(files):
                os.remove(files)
        except:
            pass


@ky.ubot("stube", sudo=True)
async def _(c, m):
    em = Emojik()
    em.initialize()
    if len(m.command) < 2:
        return await m.reply(cgr("down_1").format(em.gagal, m.command))
    pros = await m.reply(cgr("proses").format(em.proses))
    query = m.text.split(None, 1)[1]
    if re.match(r"^https?://", query):
        link = query
    else:
        try:
            search = VideosSearch(query, limit=1).result()["result"][0]
            link = f"https://youtu.be/{search['id']}"
        except Exception as error:
            return await pros.edit(cgr("err").format(em.gagal, error))
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb_url,
            data_ytp,
        ) = await download_youtube(link, as_video=False)
    except Exception as error:
        return await pros.edit(cgr("err").format(em.gagal, error))
    thumbik = wget.download(thumb_url)
    await c.send_audio(
        m.chat.id,
        audio=file_name,
        thumb=thumbik,
        file_name=title,
        performer=channel,
        duration=duration,
        caption=cgr("yutup").format(
            "Audio",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            c.me.mention,
        ),
        progress=progress,
        progress_args=(
            pros,
            time(),
            cgr("proses").format(em.proses),
            f"{file_name}",
        ),
        reply_to_message_id=m.id,
    )
    await pros.delete()
    await m.delete()
    for files in (thumbik,file_name):
        try:
            if files and os.path.exists(files):
                os.remove(files)
        except:
            pass


def tiktok_id(url):
    match = re.search(r"/video/(\d+)", url)
    if match:
        return match.group(1)
    return None


async def download_tiktok(c, m, url, em):
    response = requests.get(url)
    video_id = tiktok_id(response.url)

    if not video_id:
        await m.reply(cgr("down_2").format(em.gagal, url))
        return

    video_response = requests.get(f"https://tikcdn.io/ssstik/{video_id}")

    if video_response.status_code == 200:
        video_path = f"Mix-Tiktok-Content.mp4"
        with open(video_path, "wb") as file:
            file.write(video_response.content)
        text = cgr("down_3").format(em.sukses, nlx.me.mention)
        await c.send_video(
            chat_id=m.chat.id, video=video_path, caption=text, reply_to_message_id=m.id
        )
        os.remove(video_path)
    else:
        await m.reply(cgr("down_4").format(em.gagal, video_response.status_code))


@ky.ubot("dtik", sudo=False)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    try:
        url = m.text.split(maxsplit=1)[1]
    except IndexError:
        await m.reply(cgr("down_5").format(em.gagal, m.command))
        return

    pros = await m.edit(cgr("proses").format(em.proses))
    await download_tiktok(c, m, url, em)
    await pros.delete()


"""
@ky.ubot("vtube", sudo=True)
async def _(c, m):
    em = Emojik()
    em.initialize()
    if len(m.command) < 2:
        return await m.reply(cgr("down_1").format(em.gagal, m.command))
    pros = await m.reply(cgr("proses").format(em.proses))
    try:
        search = VideosSearch(m.text.split(None, 1)[1], limit=1).result()["result"][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await pros.reply_text(cgr("err").format(em.gagal, error))
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=True)
    except Exception as error:
        return await pros.reply_text(cgr("err").format(em.gagal, error))
    thumbnail = wget.download(thumb)
    await c.send_video(
        m.chat.id,
        video=file_name,
        thumb=thumbnail,
        file_name=title,
        duration=duration,
        supports_streaming=True,
        caption=data_ytp.format(
            "VIDEO",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            c.me.mention,
        ),
        progress=progress,
        progress_args=(
            pros,
            time(),
            cgr("proses").format(em.proses),
            f"{search['id']}.mp4",
        ),
        reply_to_message_id=m.id,
    )
    await pros.delete()
    await m.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)


@ky.ubot("stube", sudo=True)
async def _(c, m):
    em = Emojik()
    em.initialize()
    if len(m.command) < 2:
        return await m.reply(cgr("down_1").format(em.gagal, m.command))
    pros = await m.reply(cgr("proses").format(em.proses))
    try:
        search = VideosSearch(m.text.split(None, 1)[1], limit=1).result()["result"][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await pros.edit(cgr("err").format(em.gagal, error))
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=False)
    except Exception as error:
        return await pros.edit(cgr("err").format(em.gagal, error))
    thumbnail = wget.download(thumb)
    await c.send_audio(
        m.chat.id,
        audio=file_name,
        thumb=thumbnail,
        file_name=title,
        performer=channel,
        duration=duration,
        caption=data_ytp.format(
            "AUDIO",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            c.me.mention,
        ),
        progress=progress,
        progress_args=(
            pros,
            time(),
            cgr("proses").format(em.proses),
            f"{search['id']}.mp3",
        ),
        reply_to_message_id=m.id,
    )
    await pros.delete()
    await m.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)
"""


def is_valid_twitter_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc.endswith("x.com") and "/status/" in parsed_url.path


def download_media_from_twitter(tweet_url):
    endpoint = "https://twitter-x-media-download.p.rapidapi.com/media"
    payload = {"url": tweet_url, "proxy": ""}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "twitter-x-media-download.p.rapidapi.com",
    }

    response = requests.post(endpoint, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "tweetResult" in data:
            return data["tweetResult"]
        else:
            return None
    else:
        return None


async def download_and_send_file(nlx, chat_id, url, content_type):
    em = Emojik()
    em.initialize()
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code == 200:
            text = cgr("down_3").format(em.sukses, nlx.me.mention)
            file_name = f"Mix-Twitter-Contet{content_type}.{url.split('.')[-1]}"
            with open(file_name, "wb") as f:
                f.write(response.content)
            if content_type == "photo":
                await nlx.send_photo(chat_id, photo=file_name, caption=text)
                return
            elif content_type == "video":
                await nlx.send_video(chat_id, video=file_name, caption=text)
                return
        else:
            err = cgr("menten").format(em.gagal)
            await nlx.send_mesaage(chat_id, text=err)
            return
    except Exception as e:
        await nlx.reply(cgr("err").format(em.gagal, e))
        return


@ky.ubot("twit|twitt", sudo=True)
async def twit(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.edit(cgr("proses").format(em.proses))
    if len(m.command) < 2:
        await pros.edit(cgr("down_6").format(em.gagal, m.command))
        return

    tweet_url = m.command[1]
    if not is_valid_twitter_url(tweet_url):
        await pros.edit(
            cgr("down_7").format(em.gagal, m.command),
            disable_web_page_preview=True,
        )
        return
    media_info = download_media_from_twitter(tweet_url)

    if media_info:
        media_type = (
            media_info.get("result", {})
            .get("legacy", {})
            .get("entities", {})
            .get("media", [{}])[0]
            .get("type")
        )
        if media_type == "photo":
            media_url = (
                media_info.get("result", {})
                .get("legacy", {})
                .get("entities", {})
                .get("media", [{}])[0]
                .get("media_url_https")
            )
            if media_url:
                caption = cgr("down_8").format(em.sukses, nlx.me.mention)
                await c.send_photo(chat_id=m.chat.id, photo=media_url, caption=caption)
                await pros.delete()
        elif media_type == "video":
            video_info = (
                media_info.get("result", {})
                .get("legacy", {})
                .get("entities", {})
                .get("media", [{}])[0]
                .get("video_info", {})
            )
            if video_info:
                variants = video_info.get("variants", [])
                video_url = None
                for variant in variants:
                    content_type = variant.get("content_type", "")
                    if "video/mp4" in content_type:
                        video_url = variant.get("url", "")
                        break
                if video_url:
                    caption = cgr("down_9").format(em.sukses, nlx.me.mention)
                    await c.send_video(
                        chat_id=m.chat.id, video=video_url, caption=caption
                    )
                    await pros.delete()
            else:
                await pros.edit(cgr("down_10").format(em.gagal))
    else:
        await pros.edit(cgr("down_11").formar(em.gagal))


@ky.ubot("insta", sudo=True)
async def insta_handler(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.edit(cgr("proses").format(em.proses))
    try:
        url = m.command[1]
        if url.startswith("https://www.instagram.com/p/") or url.startswith(
            "https://instagram.com/p/"
        ):
            querystring = {"url": url}
            headers = {
                "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
                "X-RapidAPI-Host": "instagram-api-special.p.rapidapi.com",
            }
            response = requests.get(
                "https://instagram-api-special.p.rapidapi.com/instagram/",
                headers=headers,
                params=querystring,
            )
            data = response.json()
            if data["status"]:
                result = data["result"][0]
                media_url = result["url"]
                thumb_url = result.get("thumb", None)
                if result["type"] == "image/jpeg":
                    await c.send_photo(
                        m.chat.id,
                        photo=media_url,
                        caption=cgr("down_12").format(em.sukses, nlx.me.mention),
                        reply_to_message_id=m.id,
                    )
                    await pros.delete()
                    return
                elif result["type"] == "video/mp4":
                    await c.send_video(
                        m.chat.id,
                        video=media_url,
                        thumb=thumb_url,
                        caption=cgr("down_13").format(em.sukses, nlx.me.mention),
                        reply_to_message_id=m.id,
                    )
                    await pros.delete()
                    return
                else:
                    await pros.edit(cgr("down_14").format(em.gagal))
                    return
            else:
                await pros.edit(
                    cgr("down_15").format(em.gagal, url), disable_web_page_preview=True
                )
                return
        else:
            await pros.edit(cgr("down_16").format(em.gagal))
            return
    except IndexError:
        await pros.edit(cgr("down_17").format(em.gagal, m.command))
        return
